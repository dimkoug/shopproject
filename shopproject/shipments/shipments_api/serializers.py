from rest_framework import serializers


from shipments.models import Shipment


class ShipmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Shipment
        fields = ['url', 'product', 'stock', 'shipment_date']