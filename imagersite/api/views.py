"""Establish views for API access."""
# from rest_framework import permissions, renderers, viewsets
# from rest_framework.decorators import api_view, detail_route
# from rest_framework.response import Response
# from rest_framework.reverse import reverse
# from django.contrib.auth.models import User

from .permissions import IsOwnerAndReadOnly
from api.serializers import PhotoSerializer, AlbumSerializer
from imager_images.models import Photo, Album
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated


class PhotoListView(ListAPIView):
    """View allowing API access to view lists of owner's photos."""

    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = (
        IsAuthenticated,
        IsOwnerAndReadOnly,
    )

    def list(self, request, *args, **kwargs):
        """Filter list to only those belonging to the logged in user."""
        self.queryset = self.queryset.filter(owner=request.user)
        return super(PhotoListView, self).list(request, *args, **kwargs)


class AlbumListView(ListAPIView):
    """View allowing API access to view lists of owner's albums."""

    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = (
        IsAuthenticated,
        IsOwnerAndReadOnly,
    )

    def list(self, request, *args, **kwargs):
        """Filter list to only those belonging to the logged in user."""
        self.queryset = self.queryset.filter(owner=request.user)
        return super(AlbumListView, self).list(request, *args, **kwargs)


# class AlbumPhotoListView(PhotoListView):
#     """View allows API access to view list of owner's photos with an album."""

#     def list(self, request, *args, **kwargs):
#         """Filter list to only those belonging to the logged in user."""
#         # import pdb;pdb.set_trace()
#         self.queryset = None
#         return super(AlbumPhotoListView, self).list(request, *args, **kwargs)
