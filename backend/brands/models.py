from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

from core.models import Timestamped,Ordered,Published
from core.storage import OverwriteStorage


User = get_user_model()

class Brand(Timestamped, Ordered, Published):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='brands/',
                              storage=OverwriteStorage(), max_length=500, null=True, blank=True)
    url = models.URLField(blank=True, null=True)


    class Meta:
        default_related_name = 'brands'
        verbose_name = 'brand'
        verbose_name_plural = 'brands'
        ordering = ['order']
        indexes = [
            models.Index(fields=['user', 'name']),
            models.Index(fields=['name']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='%(app_label)s_%(class)s_unique_name')
        ]

    def __str__(self):
        return f"{self.name}"


