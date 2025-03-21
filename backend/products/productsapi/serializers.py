from rest_framework import serializers

from products.models import *

from media.models import Media





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
    name = serializers.SerializerMethodField('get_name')
    class Meta:
        model = ChildCategory
        fields = ['id','name','target']

    def get_name(self, obj):
        return obj.target.name



class CategorySerializer(serializers.HyperlinkedModelSerializer):
    children = ChildCategorySerializer(source='sources', many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'url', 'children', 'name', 'image', 'order']


class FeatureSerializer(serializers.HyperlinkedModelSerializer):
    categories = FeatureCategorySerializer(source='featurecategories',many=True)
    class Meta:
        model = Feature
        fields = ['url', 'name', 'categories', 'order']




class MediaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Media
        fields = ['url', 'image', 'image_url', 'order']


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



