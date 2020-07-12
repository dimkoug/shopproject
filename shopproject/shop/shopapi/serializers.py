from rest_framework import serializers

from shop.models import (
    Category, Supplier, Brand, BrandSupplier, Specification,
    SpecificationCategory, Attribute, Tag, Product, ProductShipment,
    ProductStatistics, ProductTag, ProductAttribute, ProductCategory,
    ProductMedia, Offer, OfferDetail, Order, OrderStatus, OrderDetail,
    ShoppingCartItem, Hero, HeroItem
)


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['url', 'name', 'image', 'parent', 'order']


class SupplierSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Supplier
        fields = ['url', 'name', 'order']


class BrandSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Brand
        fields = ['url', 'name', 'image', 'suppliers', 'order']


class SpecificationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Specification
        fields = ['url', 'name', 'categories', 'order']


class AttributeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Attribute
        fields = ['url', 'name', 'specification', 'order']


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ['url', 'name', 'order']


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['url', 'name', 'image', 'description', 'brand', 'parent',
                  'price', 'featured', 'categories', 'tags', 'attributes',
                  'order']


class ProductShipmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductShipment
        fields = ['url', 'product', 'stock', 'shipment_date']


class ProductMediaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductMedia
        fields = ['url', 'product', 'image', 'order']
