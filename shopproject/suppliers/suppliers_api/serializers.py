from rest_framework import serializers

from suppliers.models import Supplier

class SupplierSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Supplier
        fields = ['url', 'name', 'order']