from rest_framework import serializers

from shop.models import (
    Category,ChildCategory,Tag, Supplier,WareHouse, Brand, BrandSupplier, Feature,
    FeatureCategory, Attribute, Product, ProductCategory,ProductTag,ProductRelated,
    Media,Logo,Stock, Shipment,ProductAttribute,
    Hero,HeroItem, Offer, OfferProduct, Order, OrderItem,
    ShoppingCart, Address,
)

class AddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Address
        fields = ['address_type', 'profile', 'first_name', 'last_name','mobile', 'street_name', 'postal_code',
                  'city','street_number', 'floor_number']

class AttributeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Attribute
        fields = ['url', 'name', 'feature', 'order']

class BrandSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Brand
        fields = ['url', 'name', 'image', 'suppliers', 'order']


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['url', 'name', 'image', 'parent', 'order']


class FeatureSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Feature
        fields = ['url', 'name', 'categories', 'order']

class HeroSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Hero
        fields = ['name',]

class HeroItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HeroItem
        fields = ['hero', 'product']


class LogoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Logo
        fields = ['url', 'product', 'image', 'order', 'is_published']


class MediaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Media
        fields = ['url', 'product', 'image', 'order']


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ['order_registration', 'billing_address', 'shipping_address', 'total', 'comments']


class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'quantity', 'price']


class SupplierSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Supplier
        fields = ['url', 'name', 'order']











class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ['url', 'name', 'order']


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['url', 'name', 'image', 'description', 'brand', 'parent',
                  'price', 'categories', 'tags', 'attributes',
                  'order']


class ShipmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Shipment
        fields = ['url', 'product', 'stock', 'shipment_date']








class StockSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Stock
        fields = ['warehouse','product', 'stock']





class OfferSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Offer
        fields = ['start_date', 'end_date']


class WareHouseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WareHouse
        fields = ['name','is_published']
