from rest_framework import serializers

from brands.models import *



class BrandSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Brand
        fields = ['url', 'name', 'image', 'order']