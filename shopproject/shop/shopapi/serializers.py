from rest_framework import serializers

from shop.models import (
    Category,ChildCategory, Feature,
    FeatureCategory, Attribute, Product,ProductTag,ProductRelated,
    Media,Logo,Stock, Shipment,ProductAttribute,
    Hero,HeroItem, Offer, OfferProduct, Order, OrderItem,
    ShoppingCart, Address,
)

from warehouses.warehouses_api.serializers import WareHouseSerializer



class FeatureCategorySerializer(serializers.HyperlinkedModelSerializer):
    feature = serializers.HyperlinkedRelatedField(
        view_name='feature-detail',
        read_only=True,
        lookup_field='pk'
    )
    category = serializers.HyperlinkedRelatedField(
        view_name='category-detail',
        read_only=True,
        lookup_field='pk'
    )
    class Meta:
        model = FeatureCategory
        fields = ['feature', 'category']


class ProductTagSerializer(serializers.HyperlinkedModelSerializer):
    product = serializers.HyperlinkedRelatedField(
        view_name='product-detail',
        read_only=True,
        lookup_field='pk'
    )
    tag = serializers.HyperlinkedRelatedField(
        view_name='tag-detail',
        read_only=True,
        lookup_field='pk'
    )
    class Meta:
        model = ProductTag
        fields = ['product', 'tag']


class ProductRelatedSerializer(serializers.HyperlinkedModelSerializer):
    target = serializers.HyperlinkedRelatedField(
        view_name='product-detail',
        read_only=True,
        lookup_field='pk'
    )
    class Meta:
        model = ProductRelated
        fields = ['target']


class ProductAttributeSerializer(serializers.HyperlinkedModelSerializer):
    product = serializers.HyperlinkedRelatedField(
        view_name='product-detail',
        read_only=True,
        lookup_field='pk'
    )
    attribute = serializers.HyperlinkedRelatedField(
        view_name='attribute-detail',
        read_only=True,
        lookup_field='pk'
    )
    class Meta:
        model = ProductTag
        fields = ['product', 'attribute']



class AddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Address
        fields = ['address_type', 'profile', 'first_name', 'last_name','mobile', 'street_name', 'postal_code',
                  'city','street_number', 'floor_number']

class AttributeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Attribute
        fields = ['url', 'name', 'feature', 'order']









class ChildCategorySerializer(serializers.HyperlinkedModelSerializer):
    target = serializers.HyperlinkedRelatedField(
        view_name='category-detail',
        read_only=True,
        lookup_field='pk'
    )
    class Meta:
        model = ChildCategory
        fields = ['target']



class CategorySerializer(serializers.HyperlinkedModelSerializer):
    children = ChildCategorySerializer(source='source', many=True)

    class Meta:
        model = Category
        fields = ['id', 'url', 'children', 'name', 'image', 'order']


class FeatureSerializer(serializers.HyperlinkedModelSerializer):
    categories = FeatureCategorySerializer(source='featurecategories',many=True)
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



class ProductSerializer(serializers.HyperlinkedModelSerializer):
    tags = ProductTagSerializer(source='producttags',many=True)
    attributes = ProductAttributeSerializer(source='productattributes',many=True)
    relatedproducts = ProductRelatedSerializer(many=True)



    class Meta:
        model = Product
        fields = ['url', 'name', 'image', 'description', 'brand','category', 'parent',
                  'price', 'tags', 'attributes',
                  'relatedproducts',
                  'order']


class ShipmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Shipment
        fields = ['url', 'product', 'stock', 'shipment_date']





class StockSerializer(serializers.HyperlinkedModelSerializer):
    product = ProductSerializer(many=False, read_only=True)
    warehouse = WareHouseSerializer(many=False, read_only=True)
    class Meta:
        model = Stock
        fields = ['warehouse','product', 'stock']


class OfferSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Offer
        fields = ['start_date', 'end_date']



