from django.db import models

# Create your models here.

from core.models import Timestamped


class Stock(Timestamped):
    warehouse = models.ForeignKey('warehouses.WareHouse', on_delete=models.CASCADE)
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        default_related_name = 'stocks'
        verbose_name = 'stock'
        verbose_name_plural = 'stocks'
        constraints = [
            models.UniqueConstraint(fields=['warehouse', 'product'], name="%(app_label)s_%(class)s_warehouse_product")
        ]
        indexes = [
            models.Index(fields=['warehouse', 'product']),
        ]


    def __str__(self):
        return f"{str(self.stock)}"