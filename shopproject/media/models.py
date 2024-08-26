from django.db import models

# Create your models here.

from core.models import Timestamped, Ordered,Published
from core.storage import OverwriteStorage


class Media(Timestamped, Ordered, Published):
    
    image = models.ImageField(upload_to='media/',
                              storage=OverwriteStorage(), max_length=500,null=True,blank=True)
    image_url = models.URLField(max_length=2048, null=True,blank=True)

    class Meta:
        default_related_name = 'media'
        verbose_name = 'media'
        verbose_name_plural = 'media'
        ordering = ['order']

    def __str__(self):
        return f"{self.image.name}"