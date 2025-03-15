from django.db import models
# Create your models here.

from core.models import Timestamped


class Basket(Timestamped):
    session = models.ForeignKey('sessions.Session',on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True)
    discount_price = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True)