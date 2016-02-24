from django.db import models
from django.contrib.auth.models import User

class Feedback(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    email = models.EmailField(null=True, blank=True, db_index=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'app_feedback'

    def __unicode__(self):
        return self.message
