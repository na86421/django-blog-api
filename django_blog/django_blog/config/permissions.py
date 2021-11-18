from django.contrib.auth import get_user_model

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.IsAuthenticated):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `user` attribute.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.__class__ == get_user_model():
            return bool(obj == request.user)

        # Instance must have an attribute named `user`.
        return bool(
            request.method in permissions.SAFE_METHODS
            or obj.user == request.user
        )
