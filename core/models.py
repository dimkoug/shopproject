from django.db import models

# Create your models here.
class Timestamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Ordered(models.Model):
    order = models.PositiveIntegerField(default=0, db_index=True, blank=True)

    class Meta:
        abstract = True


class Published(models.Model):
    is_published = models.BooleanField(default=False)

    class Meta:
        abstract = True
