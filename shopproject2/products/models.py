from django.db import models

# Create your models here.
from mptt.models import MPTTModel, TreeForeignKey
from core.models import Timestamped, Seo, UUSlug, Published
from profiles.models import Profile


class Category(Timestamped, Seo, UUSlug, Published, MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True,
                            blank=True, related_name='children')

    slug_field = 'name'

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        default_related_name = 'categories'
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Feature(Timestamped, Published):
    name = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'features'
        verbose_name = 'feature'
        verbose_name_plural = 'features'

    def __str__(self):
        return self.name


class Attribute(Timestamped):
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        default_related_name = 'attributes'
        verbose_name = 'attribute'
        verbose_name_plural = 'attributes'

    def __str__(self):
        return self.name


class Tag(Timestamped, Published):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        default_related_name = 'tags'
        verbose_name = 'tag'
        verbose_name_plural = 'tags'

    def __str__(self):
        return self.name


class Product(Timestamped, Seo, UUSlug, Published, MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, through='ProductTag')
    attributes = models.ManyToManyField(Attribute, through='ProductAttribute')
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')

    slug_field = 'name'

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        default_related_name = 'products'
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name


class ProductTag(Timestamped, Published):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


    class Meta:
        default_related_name = 'producttags'
        verbose_name = 'product tag'
        verbose_name_plural = 'product tags'

    def __str__(self):
        return self.tag.name


class ProductAttribute(Timestamped, Published):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)


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



class Order(Timestamped):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)


class OrderDetail(Timestamped):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
