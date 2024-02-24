from rest_framework import serializers

from stocks.models import Stock

from shop.shopapi.serializers import ProductSerializer
from warehouses.warehouses_api.serializers import WareHouseSerializer


class StockSerializer(serializers.HyperlinkedModelSerializer):
    product = ProductSerializer(many=False, read_only=True)
    warehouse = WareHouseSerializer(many=False, read_only=True)
    class Meta:
        model = Stock
        fields = ['warehouse','product', 'stock']