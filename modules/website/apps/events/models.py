import jsonfield

from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django_extensions.db.fields import UUIDField

from website.apps.utils.settings import STATUS_INIT, STATUS
from website.apps.api.exceptions import BandwidthOverload
from website.apps.bundles.models import Resource

from website.apps.utils.settings import EVENT_ERROR, EVENTS
from managers import EventManager

class Event(models.Model):
    uuid = UUIDField(primary_key=True)
    user = models.ForeignKey(User)
    resource = models.ForeignKey(Resource, null=True, blank=True)
    type = models.SmallIntegerField(default=EVENT_ERROR, choices=EVENTS)

    status = models.SmallIntegerField(default=STATUS_INIT)
    reviewed = models.BooleanField(default=False, db_index=True)

    first_time = models.DateTimeField(db_index=True)
    last_time = models.DateTimeField(db_index=True)
    count = models.PositiveIntegerField(default=1)

    payload = jsonfield.JSONField()

    client_position = jsonfield.JSONField(null=True, blank=True)
    source_position = jsonfield.JSONField(null=True, blank=True)

    error_name = models.CharField(max_length=128, db_index=True)
    error_message = models.CharField(max_length=128, db_index=True)

    client_url = models.CharField(max_length=128, db_index=True)
    client_browser = models.CharField(max_length=128, db_index=True)
    client_browser_version = models.CharField(max_length=128, db_index=True)
    client_language = models.CharField(max_length=128)
    client_platform = models.CharField(max_length=128)
    client_user_agent = models.CharField(max_length=512, db_index=True)
    client_cookie_enabled = models.BooleanField(default=False)

    objects = models.Manager()
    api = EventManager()

    @property
    def status_title(self):
        return STATUS[self.status][1]

    @property
    def client_browser_name(self):
        if not hasattr(self, '_client_browser_name'):
            self._client_browser_name = '_'.join(self.client_browser.split(' '))

        try:
            browser = self._client_browser_name.lower()
            if browser in ['chrome', 'firefox', 'safari', 'opera', 'microsoft_internet_explorer']:
                return browser
        except:
            pass

        return None

    class Meta:
        db_table = 'app_event'

    def api_save(self, user, force_insert=False, force_update=False, using=None):
        if user.get_profile().used_events >= user.get_profile().package.limit_events:
            raise BandwidthOverload()

        super(Event, self).save(force_insert, force_update, using)
        user.get_profile().used_events = F('used_events') + 1
        user.get_profile().save()
