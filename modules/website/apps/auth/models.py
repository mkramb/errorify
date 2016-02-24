from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.utils.timezone import get_default_timezone

class Package(models.Model):
    title = models.CharField(max_length=255)
    expire_days = models.SmallIntegerField(default=None, null=True, blank=True)

    limit_bundles = models.PositiveIntegerField(default=1)
    limit_events = models.PositiveIntegerField(default=100)
    limit_api = models.PositiveIntegerField(default=50)

    class Meta:
        db_table = 'app_package'

    def __unicode__(self):
        return self.title

def get_default_package():
    return Package.objects.get(id=1)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    is_expired = models.BooleanField(default=False)

    package = models.ForeignKey(Package, default=get_default_package)
    timezone = models.CharField(max_length=125, default=get_default_timezone())

    used_bundles = models.PositiveIntegerField(default=0)
    used_events  = models.PositiveIntegerField(default=0)
    used_api = models.PositiveIntegerField(default=0)

    class Meta:
        order_with_respect_to = 'user'
        verbose_name = _(u'User profile')
        db_table = 'auth_user_profile'

    def __unicode__(self):  
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
