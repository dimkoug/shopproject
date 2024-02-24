from django.db import models

# Create your models here.
from core.models import Timestamped


class WareHouse(Timestamped):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        default_related_name = 'warehouses'
        verbose_name = 'warehouse'
        verbose_name_plural = 'warehouses'

    def __str__(self):
        return f"{self.name}"