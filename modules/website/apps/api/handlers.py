from urlparse import urlparse

from piston.utils import rc
from piston.handler import BaseHandler

from django.db import IntegrityError
from piston.utils import validate
from django.core.exceptions import ObjectDoesNotExist

from website.apps.events.models import Event
from website.apps.bundles.models import Bundle, Resource
from website.apps.bundles.forms import BundleForm
from website.apps.tasks import ResourceCompile
from website.apps.tasks import EventProcess
from website.apps.utils.settings import STATUS_RUNNING, STATUS_PROCESSED
from website.apps.utils.files import is_text_file

from decorators import api_throttle

class BundleHandler(BaseHandler):
    allowed_methods = ('GET','POST','DELETE',)
    model = Bundle

    fields = (
        'uuid', 'title',
        ('resources', ('uuid', 'status', 'created'),),
    )

    @api_throttle()
    def read(self, request):
        if not self.has_model():
            return rc.NOT_IMPLEMENTED

        try:
            if request.GET.has_key('uuid'):
                return self.model.api.get(
                    request.GET.get('uuid'),
                    request.user
                )

            return self.model.api.all(request.user)
        except ObjectDoesNotExist:
            return rc.NOT_FOUND

    @api_throttle()
    @validate(BundleForm)
    def create(self, request, *args, **kwargs):
        if not self.has_model():
            return rc.NOT_IMPLEMENTED

        attrs = self.flatten_dict(request.data)
        attrs['user'] = request.user

        if self.model.api.filter(**attrs).exists():
            return rc.DUPLICATE_ENTRY

        try:
            obj = self.model(**attrs)
            obj.api_save(request.user)

            return obj
        except self.model.MultipleObjectsReturned:
            return rc.DUPLICATE_ENTRY

    @api_throttle()
    def delete(self, request):
        if not self.has_model():
            return rc.NOT_IMPLEMENTED

        try:
            if request.GET.has_key('uuid'):
                bundle = self.model.api.get(
                    request.GET.get('uuid'),
                    request.user
                )

                if bundle:
                    bundle.api_delete(request.user)
                    return rc.DELETED

            return rc.FORBIDDEN
        except self.model.MultipleObjectsReturned:
            return rc.DUPLICATE_ENTRY
        except self.model.DoesNotExist:
            return rc.NOT_HERE

class ResourceHandler(BaseHandler):
    allowed_methods = ('GET', 'POST','DELETE',)
    model = Resource

    fields = (
        'uuid', 'status', 'compiler_warnings', 'compiler_errors',
        'source', 'source_processed', ('events', ('uuid', 'status', 'created'),),
    )

    @api_throttle()
    def read(self, request):
        if not self.has_model():
            return rc.NOT_IMPLEMENTED

        try:
            if request.GET.has_key('uuid'):
                return self.model.api.get(
                    request.GET.get('uuid'),
                    request.user
                )

            return self.model.api.all(
                request.user
            )
        except ObjectDoesNotExist:
            return rc.NOT_FOUND

    @api_throttle()
    def create(self, request):
        if not self.has_model():
            return rc.NOT_IMPLEMENTED

        bundle = request.GET.get('bundle')
        source = request.FILES.get('source')
        resource = None

        if not bundle or not source:
            return rc.BAD_REQUEST

        if not is_text_file(source):
            return rc.BAD_REQUEST

        # have to reset file pointer (because of is_text_file)
        source.seek(0)

        try:
            resource = self.model(bundle=Bundle.api.get(bundle, request.user))
            resource.source = source.read()
            resource.status = STATUS_RUNNING
            resource.save()

            ResourceCompile.delay(resource)
        except IntegrityError:
            return rc.NOT_HERE
        except:
            return rc.BAD_REQUEST

        return resource

    @api_throttle()
    def delete(self, request):
        if not self.has_model():
            return rc.NOT_IMPLEMENTED

        try:
            if request.GET.has_key('uuid'):
                resource = self.model.api.get(
                    request.GET.get('uuid'),
                    request.user
                )

                if resource:
                    resource.delete()
                    return rc.DELETED

            return rc.FORBIDDEN
        except self.model.MultipleObjectsReturned:
            return rc.DUPLICATE_ENTRY
        except self.model.DoesNotExist:
            return rc.NOT_HERE

class EventHandler(BaseHandler):
    allowed_methods = ('GET')
    model = Event
    
    fields = (
        'uuid', 'status', 'last_time', 'first_time', 'payload', 'source_position', 'error_name', 'error_message',
        'client_ip', 'client_url', 'client_browser', 'client_language', 'client_platform',
        'client_user_agent', 'client_cookie_enabled',
    )

    @api_throttle()
    def read(self, request):
        if not self.has_model():
            return rc.NOT_IMPLEMENTED

        try:
            events = self.model.api.all(request.user)

            if request.GET.has_key('bundle'):
                return events.filter(resource__bundle = request.GET.get('bundle'))
            
            if request.GET.has_key('resource'):
                return events.filter(resource = request.GET.get('resource'))

            return events
        except ObjectDoesNotExist:
            return rc.NOT_FOUND

class LogHandler(BaseHandler):
    allowed_methods = ('GET')

    def read(self, request):
        resource_id = request.GET.get('resourceId')
        resource = None
        
        payload = request.GET.get('payload')
        response = rc.CREATED

        if not payload:
            response = rc.BAD_REQUEST

        referer = urlparse(request.META.get('HTTP_REFERER', '')).netloc

        try:
            if resource_id:
                resource = Resource.objects.select_related().get(uuid=resource_id)
                
                if resource.bundle.domain:
                    if resource.status != STATUS_PROCESSED or not len(referer):
                        return rc.BAD_REQUEST
    
                    if not resource.bundle.domain_base.startswith(referer):
                        return rc.FORBIDDEN
            else:
                bundles = Bundle.api.all(request.user)
                domain_exists = False
                
                for bundle in bundles:
                    if bundle.domain_base.startswith(referer):
                        domain_exists = True
                        
                if not domain_exists:
                    return rc.BAD_REQUEST

            EventProcess.delay(
                request.user, resource,
                payload, request.META.get('HTTP_USER_AGENT', ''),
            )
        except IntegrityError:
            return rc.NOT_FOUND
        except ObjectDoesNotExist:
            return rc.NOT_FOUND

        if resource and resource.bundle.domain:
            if resource.status != STATUS_PROCESSED or not len(referer):
                return None

            if not resource.bundle.domain_base.startswith(referer):
                return None

        response['Content-Type'] = 'application/javascript'
        response.content = ''

        return response
