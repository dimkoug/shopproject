from django.db import models
from core.models import Timestamped, Seo, UUSlug, Published
from django.utils import timezone
from products.models import Product
from profiles.models import Profile


class Order(Timestamped):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)



class OrderStatus(Timestamped):
    OPEN,SENT,CANCELLED = range(0,3)
    STATUS_CHOICES = (
        (OPEN , 'Open'),
        (SENT, 'Sent'),
        (CANCELLED, 'Cancelled')
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(default=OPEN, choices=STATUS_CHOICES)

    class Meta:
        default_related_name = 'orderstatus'
        verbose_name = 'order status'
        verbose_name_plural = 'orders status'


class OrderDetail(Timestamped):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
