"""Serializers to convert models into JSON."""

from rest_framework import serializers
from imager_images.models import Photo, Album


class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for the Photo model."""

    owner = serializers.ReadOnlyField(source='owner.username')
    img_file = serializers.FileField(use_url=True)

    class Meta:
        """Meta for PhotoSerializer."""

        model = Photo
        fields = ['owner', 'img_file', 'title', 'description',
                  'published']


class AlbumSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for the Album model."""

    owner = serializers.ReadOnlyField(source='owner.username')
    # cover = serializers.HyperlinkedRelatedField(
    #     view_name='photo-list',
    #     lookup_field='albums',
    #     queryset='photos',
    # )
    # photos = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     view_name='album-photo-list',
    #     lookup_field='albums',
    #     queryset='photos',
    # )

    class Meta:
        """Meta for AlbumSerializer."""

        model = Album
        fields = ['owner',
                  # 'cover',
                  # 'photos',
                  'title', 'description',
                  'published']
