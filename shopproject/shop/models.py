from django.db import models
from django.utils.html import format_html, mark_safe
from profiles.models import Profile
from django.db.models import Q

from core.models import (
    Timestamped, Ordered, Published
)
from core.storage import OverwriteStorage

from .managers import ActiveProductManager
from django.urls import reverse


class Category(Timestamped, Ordered, Published):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=255, null=True,blank=True)
    image = models.ImageField(upload_to='categories/',
                              storage=OverwriteStorage(), max_length=500, null=True, blank=True)
    children = models.ManyToManyField("self", through='ChildCategory',
                                      through_fields=('source', 'target'),
                                      symmetrical=False, blank=True,related_name='source')

    class Meta:
        default_related_name = 'categories'
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ['order']

    def __str__(self):
        return f"{self.name}"

    def has_products(self):
        """Check if this category or any of its descendants have products."""
        # Check if the current category has products
        if self.products.filter(price__gt=0).exists():
            return True
        
        # Check if any of the child categories have products
        return any(child.has_products() for child in self.children.all())


class ChildCategory(Timestamped, Ordered):
    source = models.ForeignKey(Category, on_delete=models.CASCADE,
                                      related_name='sources', db_index=True)
    target = models.ForeignKey(Category, on_delete=models.CASCADE,
                               related_name='targets', db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['source', 'target'], name="childcategory")
        ]
        ordering = ['order']
        indexes = [
            models.Index(fields=['source', 'target']),
        ]



class Feature(Timestamped, Ordered, Published):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='features/',
                              storage=OverwriteStorage(), max_length=500, null=True, blank=True)
    url = models.URLField(blank=True, null=True)
    categories = models.ManyToManyField(Category, through='FeatureCategory')

    class Meta:
        default_related_name = 'features'
        verbose_name = 'feature'
        verbose_name_plural = 'features'
        ordering = ['order']

    def __str__(self):
        return f"{self.name}"


class FeatureCategory(Timestamped,Ordered):
    feature = models.ForeignKey(
        Feature, on_delete=models.CASCADE, related_name='featurecategories')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    filter_display = models.BooleanField(default=False,db_index=True)

    class Meta:
        ordering = ['order']
        default_related_name = 'featurecategories'
        unique_together = (('feature', 'category', 'filter_display'),)
        constraints = [
            models.UniqueConstraint(fields=['feature', 'category', 'filter_display'], name="feature_category")
        ]
        indexes = [
            models.Index(fields=['feature', 'category', 'filter_display']),
        ]



class Attribute(Timestamped, Ordered, Published):
    value = models.TextField()
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    hash = models.CharField(max_length=128, null=True,blank=True)

    class Meta:
        default_related_name = 'attributes'
        verbose_name = 'attribute'
        verbose_name_plural = 'attributes'
        ordering = ['order']

    def __str__(self):
        return f"{self.value}"


class Product(Timestamped,  Ordered, Published):
    brand = models.ForeignKey('brands.Brand', on_delete=models.CASCADE)
    parent = models.ForeignKey("self", on_delete=models.CASCADE,
                               null=True, blank=True, related_name='children')
    image = models.ImageField(upload_to='products/',
                              storage=OverwriteStorage(), max_length=500, null=True, blank=True)
    image_url = models.URLField(max_length=2048, null=True,blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    attributes = models.ManyToManyField(Attribute, through='ProductAttribute')
    tags = models.ManyToManyField('tags.Tag', through='ProductTag')
    relatedproducts = models.ManyToManyField("self", through='ProductRelated',
                                             through_fields=(
                                                 'source', 'target'),
                                             symmetrical=False, blank=True)
    name = models.CharField(max_length=255)
    pdf_guide = models.FileField(upload_to='files/',
                                 storage=OverwriteStorage(), max_length=500, null=True, blank=True)
    cepdf = models.FileField(upload_to='files/',
                                 storage=OverwriteStorage(), max_length=500, null=True, blank=True)
    pdf_url = models.URLField(max_length=2048, null=True,blank=True)
    cepdf_url = models.URLField(max_length=2048, null=True,blank=True)
    video_url = models.URLField(max_length=2048, null=True,blank=True)
    code = models.CharField(max_length=255, null=True,blank=True)
    price_str = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(
        max_digits=18, decimal_places=2, null=True, blank=True)
    subtitle = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    objects = models.Manager()
    active_products = ActiveProductManager()

    class Meta:
        default_related_name = 'products'
        verbose_name = 'product'
        verbose_name_plural = 'products'
        ordering = ['-pk']
        indexes = (
            models.Index(
                fields=('price','is_published'),
                name="%(app_label)s_%(class)s_p_product_idx",
                condition=(Q(price__gt=0)&Q(is_published=True))
            ),
        )

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('shop:catalog-product-detail', args=[self.pk])


class ProductTag(Timestamped):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    tag = models.ForeignKey('tags.Tag', on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'producttags'
        constraints = [
            models.UniqueConstraint(fields=['product', 'tag'], name="product_tag")
        ]
        indexes = [
            models.Index(fields=['product', 'tag']),
        ]



class ProductRelated(Timestamped):
    source = models.ForeignKey(Product, on_delete=models.CASCADE,
                               related_name='source')
    target = models.ForeignKey(Product, on_delete=models.CASCADE,
                               related_name='target')

    class Meta:
        default_related_name = 'productsrelated'
        constraints = [
            models.UniqueConstraint(fields=['source', 'target'], name="related_ptr")
        ]
        indexes = [
            models.Index(fields=['source', 'target']),
        ]



class ProductMedia(Timestamped):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    media = models.ForeignKey('media.Media', on_delete=models.CASCADE)


    class Meta:
        default_related_name = 'productmedia'
        verbose_name = 'product media'
        verbose_name_plural = 'product media'
        constraints = [
            models.UniqueConstraint(fields=['product', 'media'], name="productmedia")
        ]
        indexes = [
            models.Index(fields=['product', 'media']),
            models.Index(fields=['product']),
        ]

    def __str__(self):
        return f"{self.product.image.name}"


class ProductLogo(Timestamped):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    logo = models.ForeignKey('logos.Logo', on_delete=models.CASCADE)


    class Meta:
        default_related_name = 'productlogos'
        verbose_name = 'product logo'
        verbose_name_plural = 'product logos'
        constraints = [
            models.UniqueConstraint(fields=['product', 'logo'], name="productlogos")
        ]
        indexes = [
            models.Index(fields=['product', 'logo']),
            models.Index(fields=['product']),
        ]

    def __str__(self):
        return f"{self.logo.image.name}"


class ProductAttribute(Timestamped, Ordered):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'productattributes'
        verbose_name = 'product attribute'
        verbose_name_plural = 'product attributes'
        constraints = [
            models.UniqueConstraint(fields=['attribute', 'product'], name="attribute_product")
        ]
        indexes = [
            models.Index(fields=['product', 'attribute']),
        ]
        ordering = ['order']

    def __str__(self):
        return f"{self.attribute.name}"







