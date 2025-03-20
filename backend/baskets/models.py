from django.db import models
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from core.models import Timestamped


class Basket(Timestamped):
    session_key = models.CharField(max_length=255)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    discount_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['session_key']),
        ]


