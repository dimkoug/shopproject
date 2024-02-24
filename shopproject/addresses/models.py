from django.db import models

# Create your models here.
from core.models import Timestamped


class Address(Timestamped):
    SHIPPING_ADDRESS, BILLING_ADDRESS = range(0, 2)
    ADDRESS_CHOICES = (
        (SHIPPING_ADDRESS, 'Shipping Address'),
        (BILLING_ADDRESS, 'Billing Address')
    )
    address_type = models.PositiveIntegerField(choices=ADDRESS_CHOICES)
    profile = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE,
                                null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    street_name = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street_number = models.PositiveIntegerField()
    floor_number = models.PositiveIntegerField()

    class Meta:
        default_related_name = 'addresses'
        verbose_name = 'address'
        verbose_name_plural = 'addresses'

    def __str__(self):
        return f"{self.first_name},{self.last_name}"