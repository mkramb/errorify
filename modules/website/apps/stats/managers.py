from django.db import models

class StatsManager(models.Manager):
    def get(self, pk, user):
        return self.get_query_set().get(
            pk=pk, user=user
        )

    def all(self, user):
        return self.filter(
            user=user
        )