from django.utils import timezone
from django.db import models

# Create your models here.
from mptt.models import MPTTModel, TreeForeignKey
from core.models import Timestamped, Seo, UUSlug, Published
from core.managers import StatusManager
from profiles.models import Profile


class Category(Timestamped, Seo, UUSlug, Published, MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    hero = models.ImageField(upload_to='category/heroes', null=True, blank=True)
    category_order=models.PositiveIntegerField(default=0, editable=False, db_index=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True,
                            blank=True, related_name='children')
    status = StatusManager()
    objects = models.Manager()

    slug_field = 'name'

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        default_related_name = 'categories'
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Brand(Timestamped, UUSlug,Published):
    name = models.CharField(max_length=50, unique=True)
    logo = models.ImageField(upload_to='brand/logos', null=True, blank=True)
    brand_order=models.PositiveIntegerField(default=0, editable=False, db_index=True)
    status = StatusManager()
    objects = models.Manager()

    slug_field = 'name'

    class Meta:
        default_related_name = 'brands'
        verbose_name = 'brand'
        verbose_name_plural = 'brands'

    def __str__(self):
        return self.name


class Specification(Timestamped, Published):
    name = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    specification_order=models.PositiveIntegerField(default=0, editable=False, db_index=True)
    status = StatusManager()
    objects = models.Manager()

    class Meta:
        default_related_name = 'specifications'
        verbose_name = 'specification'
        verbose_name_plural = 'specifications'

    def __str__(self):
        return self.name


class Attribute(Timestamped):
    specification = models.ForeignKey(Specification, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        default_related_name = 'attributes'
        verbose_name = 'attribute'
        verbose_name_plural = 'attributes'

    def __str__(self):
        return self.name


class Tag(Timestamped, Published):
    name = models.CharField(max_length=50, unique=True)
    tag_order=models.PositiveIntegerField(default=0, editable=False, db_index=True)
    status = StatusManager()
    objects = models.Manager()

    class Meta:
        default_related_name = 'tags'
        verbose_name = 'tag'
        verbose_name_plural = 'tags'

    def __str__(self):
        return self.name


class Product(Timestamped, Seo, UUSlug, Published, MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    hero = models.ImageField(upload_to='product/heroes', null=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    featured = models.BooleanField(default=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, through='ProductCategory')
    tags = models.ManyToManyField(Tag, through='ProductTag')
    attributes = models.ManyToManyField(Attribute, through='ProductAttribute')
    product_order=models.PositiveIntegerField(default=0, editable=False, db_index=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')
    status = StatusManager()
    objects = models.Manager()

    slug_field = 'name'

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        default_related_name = 'products'
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name


class ProductShipment(Timestamped, Published):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)
    shipment_date = models.DateTimeField(default=timezone.now)
    status = StatusManager()
    objects = models.Manager()

    class Meta:
        default_related_name = 'productshipment'
        verbose_name = 'product shipments'
        verbose_name_plural = 'product shipment'

    def __str__(self):
        return self.product.name


class ProductStatistics(Timestamped):
    journey = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    @classmethod
    def create(cls, journey,product):
        obj = cls(journey=journey, product=product)
        obj.save()
        return obj



class ProductMedia(Timestamped, Published):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    caption = models.CharField(max_length=50, blank=True)
    media_order=models.PositiveIntegerField(default=0, editable=False, db_index=True)
    image = models.ImageField(upload_to='productmedia/')
    status = StatusManager()
    objects = models.Manager()


    class Meta:
        default_related_name = 'productmedia'
        verbose_name = 'product media'
        verbose_name_plural = 'product media'

    def __str__(self):
        return self.product.name


class ProductTag(Timestamped, Published):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    status = StatusManager()
    objects = models.Manager()


    class Meta:
        default_related_name = 'producttags'
        verbose_name = 'product tag'
        verbose_name_plural = 'product tags'

    def __str__(self):
        return self.tag.name


class ProductCategory(Timestamped, Published):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = StatusManager()
    objects = models.Manager()


    class Meta:
        default_related_name = 'productcategories'
        verbose_name = 'product category'
        verbose_name_plural = 'product categories'

    def __str__(self):
        return self.category.name


class ProductAttribute(Timestamped, Published):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    status = StatusManager()
    objects = models.Manager()


    class Meta:
        default_related_name = 'productattributes'
        verbose_name = 'product attribute'
        verbose_name_plural = 'product attributes'

    def __str__(self):
        return self.attribute.name


class ShoppingCartItem(Timestamped):
    cartId = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def get_price(self):
        return self.product.price * self.quantity
