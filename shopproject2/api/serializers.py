from rest_framework import  serializers

from users.models import User

from products.models import (Category, Tag, Specification, Attribute,
                             Product,ProductTag, ProductShipment,
                             Supplier, BrandSupplier, ProductAttribute,
                             ProductCategory, Brand, ProductMedia)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'email', 'is_staff']


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['url', 'name', 'image', 'parent', 'category_order']


class SupplierSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Supplier
        fields = ['url', 'name', 'supplier_order']


class BrandSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Brand
        fields = ['url', 'name', 'image', 'suppliers', 'brand_order']


class SpecificationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Specification
        fields = ['url', 'name', 'category', 'specification_order']


class AttributeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Attribute
        fields = ['url', 'name', 'specification', 'attribute_order']


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ['url', 'name', 'tag_order']


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['url', 'name','image', 'description', 'brand', 'parent',
                  'price', 'featured','categories', 'tags','attributes',
                  'product_order']


class ProductShipmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductShipment
        fields = ['url', 'product','stock', 'shipment_date']


class ProductMediaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductMedia
        fields = ['url', 'product','image', 'media_order']
