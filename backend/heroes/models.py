from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

from core.models import Timestamped,Ordered,Published

User = get_user_model()

class Hero(Timestamped, Ordered, Published):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'heroes'
        verbose_name = 'hero'
        verbose_name_plural = 'heroes'
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


class HeroItem(Timestamped):
    hero = models.ForeignKey(Hero, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    order = models.PositiveBigIntegerField(default=0,db_index=True)

    class Meta:
        ordering = ['order']
        default_related_name = 'heroitems'
        verbose_name = 'hero item'
        verbose_name_plural = 'heroitems'
        unique_together = (('hero', 'product'),)
        indexes = [
            models.Index(fields=['hero', 'product']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['hero', 'product'], name='%(app_label)s_%(class)s_unique_name')
        ]


    def __str__(self):
        return f"{self.hero.name}"