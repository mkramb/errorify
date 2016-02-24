import json

from datetime import timedelta

from celery.task import Task
from celery.registry import tasks

from django.utils.timezone import now
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol

from website.apps.events.models import Event
from website.apps.stats.models import StatsEvent
from website.apps.thrift.service import ClousureService
from website.apps.utils.settings import STATUS_PROCESSED, STATUS_FAILED

import httpagentparser
import pytz

class EventProcess(Task):
    def run(self, user, resource, payload, useragent):
        logger = EventProcess.get_logger()
        event, transport = None, None

        try:
            event = self.event_check(user, resource, payload, useragent)

            if not event:
                return True

            transport = TSocket.TSocket(settings.THRIFT_SERVER, settings.THRIFT_PORT)
            transport = TTransport.TFramedTransport(transport)
            protocol = TBinaryProtocol.TBinaryProtocol(transport)
            client = ClousureService.Client(protocol)

            transport.open()
            stacktrace = event.payload['stacktrace']

            result = client.getSourcePosition(
                event.resource.source_map,
                stacktrace['stack'][0]['line'], 
                stacktrace['stack'][0]['column']
            )

            event.source_position = [result.line, result.column]
            event.status = STATUS_PROCESSED
            event.save()
        except Exception, ex:
            logger.error(ex.message)

            if event:
                event.status = STATUS_FAILED
                event.save()

            return False
        finally:
            if transport:
                transport.close()

        return True
    
    def event_check(self, user, resource, payload, useragent):
        data = json.loads(payload)
        agentparser = httpagentparser.detect(useragent)

        event = None
        has_stacktrace = True if data.has_key('stacktrace') and data['stacktrace'] else None

        try:
            event = Event.api.all(user).filter(
                resource=resource,
                client_user_agent=useragent,
                client_position =  data['position'],
                error_name=data['stacktrace']['name'] if has_stacktrace else None,
                error_message=data['stacktrace']['message'] if has_stacktrace else None
            )[0]
        except:
            pass

        if not event:
            event = Event(
                user=user,
                resource=resource,
                first_time=now(),
                last_time=now()
            )

            event.client_browser = agentparser['browser']['name']
            event.client_browser_version = agentparser['browser']['version']
            event.client_user_agent = useragent
            event.payload = data

            if agentparser.has_key('os'):
                event.client_platform = agentparser['os']['name']

            event.client_url = data['client']['url']
            event.client_cookie_enabled = data['client']['cookieEnabled']

            if data['client'].has_key('language'):
                event.client_language = data['client']['language']

            if data.has_key('position'):
                event.client_position = data['position']

            if has_stacktrace:
                event.error_name = data['stacktrace']['name']
                event.error_message = data['stacktrace']['message']
        else:
            event.last_time = now()
            event.reviewed = False
            event.count += 1

        has_stack = False

        if has_stacktrace:
            stack = data['stacktrace']['stack']
            has_stack = len(stack) and stack[0].has_key('column')

        if not has_stack:
            event.status = STATUS_PROCESSED

        event.api_save(user)
        return event if has_stack else None

class EventsClearData(Task):
    def run(self):
        logger = EventsClearData.get_logger()

        for user in User.objects.all():
            try:
                timezone.activate(
                    pytz.timezone(user.get_profile().timezone)
                )

                Event.api.all(user)\
                    .filter(last_time__gte = timezone.now() - timedelta(months=settings.APP_EVENTS_CLEAR_MONTHS))\
                    .delete()

                StatsEvent.api.all(user)\
                    .filter(date__gte = timezone.now() - timedelta(months=settings.APP_STATS_CLEAR_MONTHS))\
                    .delete()
            except Exception, ex:
                logger.error(ex.message)
                continue

        return True

tasks.register(EventProcess)
tasks.register(EventsClearData)
