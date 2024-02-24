from django.db import models

# Create your models here.
from core.models import Timestamped,Ordered,Published


class Tag(Timestamped, Ordered, Published):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        default_related_name = 'tags'
        verbose_name = 'tag'
        verbose_name_plural = 'tags'
        ordering = ['order']

    def __str__(self):
        return f"{self.name}"