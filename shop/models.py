import os
import hashlib
import datetime
from django.utils import timezone
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.db.models.signals import post_delete, pre_delete
from django.dispatch.dispatcher import receiver
from django.utils.html import format_html, mark_safe
from profiles.models import Profile


from core.models import (
    Timestamped, Ordered, Published
)


class MediaFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if max_length and len(name) > max_length:
            raise(Exception("name's length is greater than max_length"))
        return name

    def _save(self, name, content):
        if self.exists(name):
            # if the file exists, do not call the superclasses _save method
            return name
        # if the file is new, DO call it
        return super(MediaFileSystemStorage, self)._save(name, content)


class ImageModel(models.Model):
    image = models.ImageField(upload_to='',
                              storage=MediaFileSystemStorage(), max_length=500, null=True, blank=True)
    md5sum = models.CharField(blank=True, max_length=255, null=True)

    class Meta:
        abstract = True

    def get_thumb(self):
        if self.image:
            return format_html("<img src='{}' width='100' height='auto'>",
                               self.image.url)
        return ''

    def save(self, *args, **kwargs):
        if not self.pk:  # file is new
            if self.image:
                md5 = hashlib.md5()
                for chunk in self.image.chunks():
                    md5.update(chunk)
                self.md5sum = md5.hexdigest()
        super().save(*args, **kwargs)


class Category(Timestamped, ImageModel, Ordered, Published):
    name = models.CharField(max_length=100, unique=True)
    children = models.ManyToManyField("self", through='ChildCategory',
                                      through_fields=('source', 'target'),
                                      symmetrical=False, blank=True)

    class Meta:
        default_related_name = 'categories'
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ['order']

    def __str__(self):
        return f"{self.name}"


class ChildCategory(Timestamped, Ordered, Published):
    source = models.ForeignKey(Category, on_delete=models.CASCADE,
                               related_name='source')
    target = models.ForeignKey(Category, on_delete=models.CASCADE,
                               related_name='target')

    class Meta:
        unique_together = (('source', 'target'),)
        ordering = ['order']
        indexes = [
            models.Index(fields=['source', 'target']),
        ]


class Tag(Timestamped, Ordered, Published):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        default_related_name = 'tags'
        verbose_name = 'tag'
        verbose_name_plural = 'tags'
        ordering = ['order']

    def __str__(self):
        return f"{self.name}"


class Supplier(Timestamped, Ordered, Published):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        default_related_name = 'suppliers'
        verbose_name = 'supplier'
        verbose_name_plural = 'suppliers'
        ordering = ['order']

    def __str__(self):
        return f"{self.name}"


class WareHouse(Timestamped, Ordered, Published):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        default_related_name = 'warehouses'
        verbose_name = 'warehouse'
        verbose_name_plural = 'warehouses'
        ordering = ['order']

    def __str__(self):
        return f"{self.name}"


class Brand(Timestamped, ImageModel, Ordered, Published):
    name = models.CharField(max_length=100, unique=True)
    url = models.URLField(blank=True, null=True)
    suppliers = models.ManyToManyField(Supplier, through='BrandSupplier')

    class Meta:
        default_related_name = 'brands'
        verbose_name = 'brand'
        verbose_name_plural = 'brands'
        ordering = ['order']

    def __str__(self):
        return f"{self.name}"


class BrandSupplier(Timestamped, Ordered, Published):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('brand', 'supplier'),)
        indexes = [
            models.Index(fields=['brand', 'supplier']),
        ]
        ordering = ['order']


class Feature(Timestamped, ImageModel, Ordered, Published):
    name = models.CharField(max_length=100, unique=True)
    url = models.URLField(blank=True, null=True)
    categories = models.ManyToManyField(Category, through='FeatureCategory')

    class Meta:
        default_related_name = 'features'
        verbose_name = 'feature'
        verbose_name_plural = 'features'
        ordering = ['order']

    def __str__(self):
        return f"{self.name}"


class FeatureCategory(Timestamped, Ordered, Published):
    feature = models.ForeignKey(
        Feature, on_delete=models.CASCADE, related_name='featurecategories')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    filter_display = models.BooleanField(null=True, blank=True)

    class Meta:
        unique_together = (('feature', 'category', 'filter_display'),)
        indexes = [
            models.Index(fields=['feature', 'category', 'filter_display']),
        ]
        ordering = ['order']


class Attribute(Timestamped, Ordered, Published):
    name = models.TextField()
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'attributes'
        verbose_name = 'attribute'
        verbose_name_plural = 'attributes'
        ordering = ['order']

    def __str__(self):
        return f"{self.name}"


class Product(Timestamped, ImageModel, Ordered, Published):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    parent = models.ForeignKey("self", on_delete=models.CASCADE,
                               null=True, blank=True, related_name='children')
    categories = models.ManyToManyField(Category, through='ProductCategory')
    attributes = models.ManyToManyField(Attribute, through='ProductAttribute')
    tags = models.ManyToManyField(Tag, through='ProductTag')
    relatedproducts = models.ManyToManyField("self", through='ProductRelated',
                                             through_fields=(
                                                 'source', 'target'),
                                             symmetrical=False, blank=True)
    name = models.CharField(max_length=100, unique=True)
    price_str = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(
        max_digits=18, decimal_places=2, null=True, blank=True)
    subtitle = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        default_related_name = 'products'
        verbose_name = 'product'
        verbose_name_plural = 'products'
        ordering = ['order']

    def __str__(self):
        return f"{self.name}"


class ProductCategory(Timestamped, Ordered, Published):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'productcategories'
        unique_together = (('product', 'category'),)
        indexes = [
            models.Index(fields=['product', 'category']),
        ]
        ordering = ['order']


class ProductTag(Timestamped, Ordered, Published):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'producttags'
        unique_together = (('product', 'tag'),)
        indexes = [
            models.Index(fields=['product', 'tag']),
        ]
        ordering = ['order']


class ProductRelated(Timestamped, Ordered, Published):
    source = models.ForeignKey(Product, on_delete=models.CASCADE,
                               related_name='source')
    target = models.ForeignKey(Product, on_delete=models.CASCADE,
                               related_name='target')

    class Meta:
        default_related_name = 'relatedproducts'
        unique_together = (('source', 'target'),)
        indexes = [
            models.Index(fields=['source', 'target']),
        ]
        ordering = ['order']


class Media(Timestamped, ImageModel, Ordered, Published):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'media'
        verbose_name = 'media'
        verbose_name_plural = 'media'
        ordering = ['order']

    def __str__(self):
        return f"{self.image.name}"


class Logo(Timestamped, ImageModel, Ordered, Published):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'logos'
        verbose_name = 'logo'
        verbose_name_plural = 'logos'
        ordering = ['order']

    def __str__(self):
        return f"{self.image.name}"


class Stock(Timestamped, Ordered, Published):
    warehouse = models.ForeignKey(WareHouse, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        default_related_name = 'stocks'
        verbose_name = 'stock'
        verbose_name_plural = 'stocks'
        unique_together = (('warehouse', 'product'),)
        indexes = [
            models.Index(fields=['warehouse', 'product']),
        ]
        ordering = ['order']

    def __str__(self):
        return f"{str(self.stock)}"


class Shipment(Timestamped, Ordered, Published):
    warehouse = models.ForeignKey(WareHouse, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)
    date = models.DateTimeField()

    class Meta:
        default_related_name = 'shipments'
        verbose_name = 'shipment'
        verbose_name_plural = 'shipments'
        ordering = ['order']

    def __str__(self):
        return f"{str(self.stock)}"


class ProductAttribute(Timestamped, Ordered, Published):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'productattributes'
        verbose_name = 'product attribute'
        verbose_name_plural = 'product attributes'
        indexes = [
            models.Index(fields=['product', 'attribute']),
        ]
        ordering = ['order']

    def __str__(self):
        return f"{self.attribute.name}"


class Hero(Timestamped, Ordered, Published):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        default_related_name = 'heroes'
        verbose_name = 'hero'
        verbose_name_plural = 'heroes'
        ordering = ['order']

    def __str__(self):
        return f"{self.name}"


class HeroItem(Timestamped, Ordered, Published):
    hero = models.ForeignKey(Hero, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'heroitems'
        verbose_name = 'hero item'
        verbose_name_plural = 'heroitems'
        unique_together = (('hero', 'product'),)
        indexes = [
            models.Index(fields=['hero', 'product']),
        ]
        ordering = ['order']

    def __str__(self):
        return f"{self.hero.name}"


class Offer(Timestamped):
    name = models.CharField(max_length=100)
    products = models.ManyToManyField(Product, through='OfferProduct')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        default_related_name = 'offers'
        verbose_name = 'offer'
        verbose_name_plural = 'offers'

    def __str__(self):
        return self.name


class OfferProduct(Timestamped, Published):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    is_primary = models.BooleanField(default=False)
    is_complementary = models.BooleanField(default=False)
    discount_price = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True)
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        default_related_name = 'offerproducts'
        verbose_name = 'offer product'
        verbose_name_plural = 'offer products'
        ordering = ['order']
        unique_together = (
            ('product', 'offer', 'is_primary', 'is_complementary'),)
        indexes = [
            models.Index(fields=['product', 'offer',
                         'is_primary', 'is_complementary']),
        ]


class ShoppingCart(Timestamped):
    shopping_cart_id = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True)
    discount_price = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True)


class Address(Timestamped):
    SHIPPING_ADDRESS, BILLING_ADDRESS = range(0, 2)
    ADDRESS_CHOICES = (
        (SHIPPING_ADDRESS, 'Shipping Address'),
        (BILLING_ADDRESS, 'Billing Address')
    )
    address_type = models.PositiveIntegerField(choices=ADDRESS_CHOICES)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,
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


class Order(Timestamped):
    order_registration = models.CharField(max_length=255)
    billing_address = models.ForeignKey(
        Address, on_delete=models.CASCADE, related_name='billing_address')
    shipping_address = models.ForeignKey(Address, on_delete=models.CASCADE)
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
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
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
