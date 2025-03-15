from rest_framework import serializers

from offers.models import Offer, OfferProduct


class OfferSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Offer
        fields = ['start_date', 'end_date']