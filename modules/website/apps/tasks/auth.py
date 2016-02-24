from datetime import timedelta

from celery.task import Task
from celery.registry import tasks

from django.contrib.auth.models import User
from django.utils import timezone

from website.apps.utils.mail import send_multipart_mail
from website.apps.auth.models import UserProfile

class AuthPasswordReset(Task):
    def run(self, template_name, email_context, subject, recipient):
        logger = AuthPasswordReset.get_logger()

        try:
            send_multipart_mail(
                template_name, 
                email_context, 
                subject,
                recipient
            )
        except Exception, ex:
            logger.error(ex.message)
            return False

        return True

#class AuthPackageExpire(Task):
#    def run(self):
#        logger = AuthPackageExpire.get_logger()
#
#        for user in User.objects.select_related().all():
#            try:
#                user_profile = user.get_profile()
#                user_package = user_profile.package
#
#                if not user_package.expire_days:
#                    continue
#
#                if user.date_joined <= (timezone.now() - timedelta(days=user_package.expire_days)):
#                    user_profile.is_expired = True
#                    user_profile.save()
#            except Exception, ex:
#                logger.error(ex.message)
#                continue
#
#        return True

class AuthResetEvents(Task):
    def run(self):
        logger = AuthResetEvents.get_logger()

        try:
            UserProfile.objects.all().update(used_events=0)
        except Exception, ex:
            logger.error(ex.message)
            return False

        return True

class AuthResetApi(Task):
    def run(self):
        logger = AuthResetApi.get_logger()

        try:
            UserProfile.objects.all().update(used_api=0)
        except Exception, ex:
            logger.error(ex.message)
            return False

        return True

tasks.register(AuthPasswordReset)
#tasks.register(AuthPackageExpire)
tasks.register(AuthResetEvents)
tasks.register(AuthResetApi)
