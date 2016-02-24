from django.db import models
from django.contrib.auth.models import User

from website.apps.utils.settings import EVENTS, EVENT_ERROR
from managers import StatsManager

class StatsEvent(models.Model):
    user = models.ForeignKey(User)
    date = models.DateField(db_index=True)
    count = models.PositiveIntegerField()
    type = models.SmallIntegerField(default=EVENT_ERROR, choices=EVENTS)

    objects = models.Manager()
    api = StatsManager()

    class Meta:
        db_table = 'app_stats_event'
        unique_together = ('user', 'date')
