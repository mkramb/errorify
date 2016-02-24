from django.db import models

class BundleManager(models.Manager):
    def get(self, uuid, user):
        return self.get_query_set().get(
            uuid=uuid,
            user=user
        )

    def all(self, user):
        return self.filter(
            user=user
        )

class ResourceManager(models.Manager):
    def get(self, uuid, user):
        return self.get_query_set().get(
            uuid=uuid,
            bundle__user=user
        )

    def all(self, user):
        return self.filter(
            bundle__user=user
        )

