from django.db import models

class EventManager(models.Manager):
    def get(self, uuid, user):
        return self.get_query_set().get(
            uuid=uuid,
            user=user
        )

    def all(self, user):
        return self.filter(
            user=user
        )
