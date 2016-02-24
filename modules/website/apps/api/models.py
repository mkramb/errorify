from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.contrib.auth.models import User
from django.utils.timezone import now

from django_extensions.db.fields import UUIDField

class Api(models.Model):
    key = UUIDField()
    user = models.OneToOneField(User)
    status = models.BooleanField(default=False)
    last_access = models.DateTimeField(null=True, blank=True, editable=False)
    last_ip = models.CharField(max_length=32, blank=True, null=True, default=None)

    class Meta:
        db_table = 'app_api'

    def touch(self, ip):
        self.last_ip = ip
        self.last_access = now()
        self.save()

@receiver(post_save, sender=User)
def create_user_api(sender, instance, created, **kwargs):
    if created:
        Api.objects.get_or_create(
          user=instance,
          status=True
      )
