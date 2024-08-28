from rest_framework import serializers


from warehouses.models import Warehouse


class WarehouseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['name','is_published']