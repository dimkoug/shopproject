from rest_framework import serializers

from heroes.models import Hero, HeroItem

class HeroSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Hero
        fields = ['name',]

class HeroItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HeroItem
        fields = ['hero', 'product']