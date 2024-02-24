from django.db import models

# Create your models here.

from core.models import Timestamped,Ordered,Published
from core.storage import OverwriteStorage


class Brand(Timestamped, Ordered, Published):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='brands/',
                              storage=OverwriteStorage(), max_length=500, null=True, blank=True)
    url = models.URLField(blank=True, null=True)
    suppliers = models.ManyToManyField('suppliers.Supplier', through='BrandSupplier')

    class Meta:
        default_related_name = 'brands'
        verbose_name = 'brand'
        verbose_name_plural = 'brands'
        ordering = ['order']

    def __str__(self):
        return f"{self.name}"


class BrandSupplier(Timestamped):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    supplier = models.ForeignKey('suppliers.Supplier', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['brand', 'supplier'], name="brands_supplier")
        ]
        indexes = [
            models.Index(fields=['brand', 'supplier']),
        ]