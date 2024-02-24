from django.db import models

# Create your models here.
from core.models import Timestamped


class Order(Timestamped):
    order_registration = models.CharField(max_length=255)
    billing_address = models.ForeignKey(
        'addresses.Address', on_delete=models.CASCADE, related_name='billing_address')
    shipping_address = models.ForeignKey('addresses.Address', on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    comments = models.TextField(blank=True, null=True)

    class Meta:
        default_related_name = 'orders'
        verbose_name = 'order'
        verbose_name_plural = 'orders'

    def __str__(self):
        return f"{self.order_registration}"


class OrderItem(Timestamped):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True)
    discount_price = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True)

    class Meta:
        default_related_name = 'orderitems'
        verbose_name = 'order item'
        verbose_name_plural = 'order items'

    def __str__(self):
        return f"{self.order.order_registration}"