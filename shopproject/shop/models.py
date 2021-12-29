from django.utils import timezone
from django.db import models

from profiles.models import Profile


from core.models import (
    Timestamped, Ordered, Published
)


class Category(Timestamped, Ordered, Published):
    name = models.CharField(max_length=100, unique=True)
    url = models.URLField(blank=True, null=True)
    children = models.ManyToManyField("self", through='ChildCategory',
                                      symmetrical=False, blank=True)
    image = models.ImageField(upload_to="category/heroes/",
                              null=True, blank=True)

    class Meta:
        default_related_name = 'categories'
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return f"{self.name}"


class ChildCategory(Timestamped, Ordered, Published):
    source = models.ForeignKey(Category, on_delete=models.CASCADE,
                               related_name='source')
    target = models.ForeignKey(Category, on_delete=models.CASCADE,
                               related_name='target')

    class Meta:
        unique_together = (('source', 'target'),)
        indexes = [
            models.Index(fields=['source', 'target']),
        ]


class Tag(Timestamped, Ordered, Published):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        default_related_name = 'tags'
        verbose_name = 'tag'
        verbose_name_plural = 'tags'

    def __str__(self):
        return f"{self.name}"


class Supplier(Timestamped, Ordered, Published):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        default_related_name = 'suppliers'
        verbose_name = 'supplier'
        verbose_name_plural = 'suppliers'

    def __str__(self):
        return f"{self.name}"


class WareHouse(Timestamped, Ordered, Published):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        default_related_name = 'warehouses'
        verbose_name = 'ware house'
        verbose_name_plural = 'ware houses'

    def __str__(self):
        return f"{self.name}"


class Brand(Timestamped, Ordered, Published):
    name = models.CharField(max_length=100, unique=True)
    url = models.URLField(blank=True, null=True)
    suppliers = models.ManyToManyField(Supplier, through='BrandSupplier')
    image = models.ImageField(upload_to="brand/logos/",
                              null=True, blank=True)

    class Meta:
        default_related_name = 'brands'
        verbose_name = 'brand'
        verbose_name_plural = 'brands'

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


class Feature(Timestamped, Ordered, Published):
    name = models.CharField(max_length=100, unique=True)
    url = models.URLField(blank=True, null=True)
    categories = models.ManyToManyField(Category, through='FeatureCategory')
    image = models.ImageField(upload_to="feature/logos/",
                              null=True, blank=True)

    class Meta:
        default_related_name = 'features'
        verbose_name = 'feature'
        verbose_name_plural = 'features'

    def __str__(self):
        return f"{self.name}"


class FeatureCategory(Timestamped, Ordered, Published):
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('feature', 'category'),)
        indexes = [
            models.Index(fields=['feature', 'category']),
        ]


class Attribute(Timestamped, Ordered, Published):
    name = models.TextField()
    features = models.ManyToManyField(Feature, through='AttributeFeature')

    class Meta:
        default_related_name = 'attributes'
        verbose_name = 'attribute'
        verbose_name_plural = 'attributes'

    def __str__(self):
        return f"{self.name}"


class AttributeFeature(Timestamped, Ordered, Published):
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        default_related_name = 'attributefeatures'
        verbose_name = 'attribute feature'
        verbose_name_plural = 'attribute features'
        ordering = ['order']
        unique_together = (('attribute', 'feature'),)
        indexes = [
            models.Index(fields=['attribute', 'feature']),
        ]


class Product(Timestamped, Ordered, Published):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    parent = models.ForeignKey("self", on_delete=models.CASCADE,
                               null=True, blank=True, related_name='children')
    categories = models.ManyToManyField(Category, through='ProductCategory')
    tags = models.ManyToManyField(Tag, through='ProductTag')
    relatedproducts = models.ManyToManyField("self", through='ProductRelated',
                                             symmetrical=False, blank=True)
    image = models.ImageField(upload_to="product/logos/",
                              null=True, blank=True)
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=18, decimal_places=2)
    subtitle = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        default_related_name = 'products'
        verbose_name = 'product'
        verbose_name_plural = 'products'

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


class ProductTag(Timestamped, Ordered, Published):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'producttags'
        unique_together = (('product', 'tag'),)
        indexes = [
            models.Index(fields=['product', 'tag']),
        ]


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


class Media(Timestamped, Ordered, Published):
    image = models.ImageField(upload_to="product/media/")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'media'
        verbose_name = 'media'
        verbose_name_plural = 'media'

    def __str__(self):
        return f"{self.image.name}"


class Logo(Timestamped, Ordered, Published):
    image = models.ImageField(upload_to="product/logo/")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'logos'
        verbose_name = 'logo'
        verbose_name_plural = 'logos'

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

    def __str__(self):
        return f"{self.attribute.name}"


class Hero(Timestamped, Ordered, Published):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        default_related_name = 'heroes'
        verbose_name = 'hero'
        verbose_name_plural = 'heroes'

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
    discount_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        default_related_name = 'offerproducts'
        verbose_name = 'offer product'
        verbose_name_plural = 'offer products'
        ordering = ['order']
        unique_together = (('product', 'offer', 'is_primary', 'is_complementary'),)
        indexes = [
            models.Index(fields=['product', 'offer', 'is_primary', 'is_complementary']),
        ]


class ShoppingCart(Timestamped):
    shopping_cart_id = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    discount_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)


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
    billing_address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='billing_address')
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
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    discount_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    class Meta:
        default_related_name = 'orderitems'
        verbose_name = 'order item'
        verbose_name_plural = 'order items'

    def __str__(self):
        return f"{self.order.order_registration}"
