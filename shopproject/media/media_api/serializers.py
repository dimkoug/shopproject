from rest_framework import serializers

from media.models import Media


class MediaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Media
        fields = ['url', 'image', 'order', 'is_published']