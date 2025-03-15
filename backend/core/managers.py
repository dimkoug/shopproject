from django.db import models

class StatusQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)

    def drafts(self):
        return self.filter(is_published=False)

class StatusManager(models.Manager):
    def get_queryset(self):
        return StatusQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def drafts(self):
        return self.get_queryset().drafts()
