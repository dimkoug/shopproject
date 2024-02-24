from rest_framework import serializers

from addresses.models import Address


class AddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Address
        fields = ['address_type', 'profile', 'first_name', 'last_name','mobile', 'street_name', 'postal_code',
                  'city','street_number', 'floor_number']