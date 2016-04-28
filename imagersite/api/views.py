"""Establish views for API access."""
# from rest_framework import permissions, renderers, viewsets
# from rest_framework.decorators import api_view, detail_route
# from rest_framework.response import Response
# from rest_framework.reverse import reverse
# from django.contrib.auth.models import User

from .permissions import IsOwnerAndReadOnly
from api.serializers import PhotoSerializer
from imager_images.models import Photo
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class PhotoListView(ListAPIView):
    """View allowing API access to view lists of owner's photos."""

    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = (IsOwnerAndReadOnly,)
