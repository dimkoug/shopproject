from rest_framework import serializers

from shop.models import (
    Category, Supplier, Brand, BrandSupplier, Feature,
    FeatureCategory, Attribute, Tag, Product, Shipment,
    ProductTag, ProductAttribute, ProductCategory,
    Media, Offer, OfferProduct, Order, OrderItem,
    ShoppingCart, Hero, HeroItem
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


class FeatureSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Feature
        fields = ['url', 'name', 'categories', 'order']


class AttributeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Attribute
        fields = ['url', 'name', 'feature', 'order']


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


class ShipmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Shipment
        fields = ['url', 'product', 'stock', 'shipment_date']


class MediaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Media
        fields = ['url', 'product', 'image', 'order']
