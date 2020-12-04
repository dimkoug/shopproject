from django.db import models
from core.models import Timestamped, Seo, UUSlug, Published
from django.utils import timezone
from products.models import Product


class Offer(Timestamped, Published):
    name = models.CharField(max_length=50, unique=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    offer_order=models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        default_related_name = 'offers'
        verbose_name = 'offer'
        verbose_name_plural = 'offers'

    def __str__(self):
        return self.name


class OfferDetail(Timestamped):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        default_related_name = 'offerdetails'
        verbose_name = 'offer details'
        verbose_name_plural = 'offer detail'

    def __str__(self):
        return f"offer for product{self.product.title}"
