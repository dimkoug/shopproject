from django.db import models

# Create your models here.

from core.models import Timestamped,Ordered, Published


class Supplier(Timestamped, Ordered, Published):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        default_related_name = 'suppliers'
        verbose_name = 'supplier'
        verbose_name_plural = 'suppliers'
        ordering = ['order']

    def __str__(self):
        return f"{self.name}"