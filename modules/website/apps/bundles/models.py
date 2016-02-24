import re
import jsonfield

from django.db import models
from django.db.models import F
from django.contrib.auth.models import User

from django_extensions.db.fields import UUIDField
from django_extensions.db.models import TimeStampedModel

from website.apps.utils.settings import STATUS_INIT, STATUS_RUNNING
from website.apps.utils.files import file_size_format
from website.apps.api.exceptions import BandwidthOverload

from managers import BundleManager, ResourceManager

class Bundle(models.Model):
    uuid = UUIDField(primary_key=True)
    user = models.ForeignKey(User)
    title = models.CharField(max_length=255, db_index=True)
    domain = models.URLField(max_length=255, verify_exists=True, db_index=True, null=True, blank=True)

    objects = models.Manager()
    api = BundleManager()

    @property
    def domain_base(self):
        return re.sub('^https?:\/\/', '', self.domain).strip('/')

    class Meta:
        db_table = 'app_bundle'
        unique_together = ('user', 'domain')

    def api_save(self, user, force_insert=False, force_update=False, using=None):
        if user.get_profile().used_bundles >= user.get_profile().package.limit_bundles:
            raise BandwidthOverload()

        super(Bundle, self).save(force_insert, force_update, using)
        user.get_profile().used_bundles = F('used_bundles') + 1
        user.get_profile().save()

    def api_delete(self, user, using=None):
        super(Bundle, self).delete(using)
        user.get_profile().used_bundles = F('used_bundles') - 1
        user.get_profile().save()

class Resource(TimeStampedModel):
    uuid = UUIDField(primary_key=True)
    bundle = models.ForeignKey(Bundle, related_name='resources')
    status = models.SmallIntegerField(default=STATUS_INIT)

    compiler_warnings = jsonfield.JSONField(null=True, blank=True)
    compiler_errors = jsonfield.JSONField(null=True, blank=True)

    source = models.TextField()
    source_map = models.TextField()
    source_processed = models.TextField()

    objects = models.Manager()
    api = ResourceManager()

    @property
    def source_size(self):
        return file_size_format(len(self.source))

    @property
    def source_processed_size(self):
        return file_size_format(len(self.source_processed))

    @property
    def is_processed(self):
        return True if self.status > STATUS_RUNNING else False

    class Meta:
        db_table = 'app_resource'
