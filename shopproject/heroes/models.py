from django.db import models

# Create your models here.

from core.models import Timestamped,Ordered,Published


class Hero(Timestamped, Ordered, Published):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        default_related_name = 'heroes'
        verbose_name = 'hero'
        verbose_name_plural = 'heroes'
        ordering = ['order']

    def __str__(self):
        return f"{self.name}"


class HeroItem(Timestamped):
    hero = models.ForeignKey(Hero, on_delete=models.CASCADE)
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'heroitems'
        verbose_name = 'hero item'
        verbose_name_plural = 'heroitems'
        unique_together = (('hero', 'product'),)
        indexes = [
            models.Index(fields=['hero', 'product']),
        ]


    def __str__(self):
        return f"{self.hero.name}"