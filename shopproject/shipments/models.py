from django.db import models

# Create your models here.

from core.models import Timestamped


class Shipment(Timestamped):
    warehouse = models.ForeignKey('warehouses.WareHouse', on_delete=models.CASCADE)
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)
    date = models.DateTimeField()

    class Meta:
        default_related_name = 'shipments'
        verbose_name = 'shipment'
        verbose_name_plural = 'shipments'


    def __str__(self):
        return f"{str(self.stock)}"