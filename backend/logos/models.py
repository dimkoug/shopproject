from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

from core.models import Timestamped, Ordered,Published
from core.storage import OverwriteStorage

User = get_user_model()

class Logo(Timestamped, Ordered, Published):
    
    image = models.ImageField(upload_to='logos/',
                              storage=OverwriteStorage(), max_length=500,null=True,blank=True)
    url = models.URLField(max_length=2048, null=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'logos'
        verbose_name = 'logo'
        verbose_name_plural = 'logos'
        ordering = ['order']

    def __str__(self):
        return f"{self.image.name}"