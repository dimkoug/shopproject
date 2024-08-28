from rest_framework import serializers

from stocks.models import Stock

from shop.shopapi.serializers import ProductSerializer
from warehouses.warehouses_api.serializers import WarehouseSerializer


class StockSerializer(serializers.HyperlinkedModelSerializer):
    product = ProductSerializer(many=False, read_only=True)
    warehouse = WarehouseSerializer(many=False, read_only=True)
    class Meta:
        model = Stock
        fields = ['warehouse','product', 'stock']