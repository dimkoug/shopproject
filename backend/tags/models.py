from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
from core.models import Timestamped,Ordered,Published

User = get_user_model()

class Tag(Timestamped, Ordered, Published):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'tags'
        verbose_name = 'tag'
        verbose_name_plural = 'tags'
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