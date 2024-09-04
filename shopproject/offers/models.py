from django.db import models

# Create your models here.
from core.models import Timestamped


class Offer(Timestamped):
    name = models.CharField(max_length=100)
    desc = models.TextField(null=True, blank=True)
    categories = models.ManyToManyField('shop.Category',related_name='categoryoffers')
    brands = models.ManyToManyField('brands.Brand',related_name='brandoffers')
    products = models.ManyToManyField('shop.Product', through='OfferProduct')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        default_related_name = 'offers'
        verbose_name = 'offer'
        verbose_name_plural = 'offers'

    def __str__(self):
        return self.name


class OfferProduct(Timestamped):
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    is_primary = models.BooleanField(default=False)
    is_complementary = models.BooleanField(default=False)
    discount_price = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True)


    class Meta:
        default_related_name = 'offerproducts'
        verbose_name = 'offer product'
        verbose_name_plural = 'offer products'
        unique_together = (
            ('product', 'offer', 'is_primary', 'is_complementary'),)
        indexes = [
            models.Index(fields=['product', 'offer',
                         'is_primary', 'is_complementary']),
        ]