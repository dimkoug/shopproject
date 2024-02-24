from django.db import models

# Create your models here.

from core.models import Timestamped, Ordered,Published
from core.storage import OverwriteStorage


class Logo(Timestamped, Ordered, Published):
    image = models.ImageField(upload_to='logos/',
                              storage=OverwriteStorage(), max_length=500)

    class Meta:
        default_related_name = 'logos'
        verbose_name = 'logo'
        verbose_name_plural = 'logos'
        ordering = ['order']

    def __str__(self):
        return f"{self.image.name}"