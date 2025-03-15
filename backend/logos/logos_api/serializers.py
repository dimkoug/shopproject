from rest_framework import serializers

from logos.models import Logo


class LogoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Logo
        fields = ['url', 'image', 'order', 'is_published']