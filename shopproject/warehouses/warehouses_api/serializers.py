from rest_framework import serializers


from warehouses.models import WareHouse


class WareHouseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WareHouse
        fields = ['name','is_published']