from django.utils import timezone
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


class Offer(Timestamped, Published):
    name = models.CharField(max_length=50, unique=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)

    class Meta:
        default_related_name = 'offers'
        verbose_name = 'offer'
        verbose_name_plural = 'offers'

    def __str__(self):
        return self.name


class OfferDetail(Timestamped):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)


    class Meta:
        default_related_name = 'offerdetails'
        verbose_name = 'offer details'
        verbose_name_plural = 'offer detail'

    def __str__(self):
        return f"offer for product{self.product.title}"




class Brand(Timestamped, Published):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        default_related_name = 'brands'
        verbose_name = 'brand'
        verbose_name_plural = 'brands'

    def __str__(self):
        return self.name


class Specification(Timestamped, Published):
    name = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

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

    class Meta:
        default_related_name = 'tags'
        verbose_name = 'tag'
        verbose_name_plural = 'tags'

    def __str__(self):
        return self.name


class Product(Timestamped, Seo, UUSlug, Published, MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    featured = models.BooleanField(default=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, through='ProductCategory')
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


class ProductCategory(Timestamped, Published):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


    class Meta:
        default_related_name = 'productcategories'
        verbose_name = 'product category'
        verbose_name_plural = 'product categories'

    def __str__(self):
        return self.category.name


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
