import pytz

from datetime import timedelta

from celery.task import Task
from celery.registry import tasks

from django.contrib.auth.models import User
from django.core.cache import cache
from django.utils import timezone

from website.apps.stats.models import StatsEvent
from website.apps.events.models import Event

class StatsEventAggregate(Task):
    def run(self):
        logger = StatsEventAggregate.get_logger()

        for user in User.objects.all():
            try:
                timezone.activate(pytz.timezone(user.get_profile().timezone))
                events = Event.api.all(user).filter(last_time__gte = timezone.now() - timedelta(days=1))

                StatsEvent(
                    user=user,
                    date=timezone.now(),
                    count=events.count()
                ).save()
            except Exception, ex:
                logger.error(ex.message)
                continue

        cache.clear()
        return True

tasks.register(StatsEventAggregate)
