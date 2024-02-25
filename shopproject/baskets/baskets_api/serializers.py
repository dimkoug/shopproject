from rest_framework import serializers

from baskets.models import Basket


class BasketSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Basket
        fields = ['url', 'product','quantity', 'price']