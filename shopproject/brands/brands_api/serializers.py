from rest_framework import serializers

from brands.models import Brand, BrandSupplier


class BrandSupplierSerializer(serializers.HyperlinkedModelSerializer):
    brand = serializers.HyperlinkedRelatedField(
        view_name='brand-detail',
        read_only=True,
        lookup_field='pk'
    )
    supplier = serializers.HyperlinkedRelatedField(
        view_name='supplier-detail',
        read_only=True,
        lookup_field='pk'
    )
    class Meta:
        model = BrandSupplier
        fields = ['brand', 'supplier']


class BrandSerializer(serializers.HyperlinkedModelSerializer):
    suppliers = BrandSupplierSerializer(many=True, read_only=True)
    class Meta:
        model = Brand
        fields = ['url', 'name', 'image', 'suppliers', 'order']