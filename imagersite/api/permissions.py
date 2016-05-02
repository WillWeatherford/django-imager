"""Establish permissions for Imagersite API."""
from rest_framework import permissions


class IsOwnerAndReadOnly(permissions.BasePermission):
    """Custom permission to only allow owners of an object to view it."""

    def has_object_permission(self, request, view, obj):
        """Only allow GET, and only allow object's user to GET."""
        return all([obj.owner == request.user,
                    request.method in permissions.SAFE_METHODS])
