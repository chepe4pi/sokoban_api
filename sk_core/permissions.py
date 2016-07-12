from rest_framework import permissions

from sk_core.models import STATE_PUBLIC, STATE_INITIAL


class MapObjectPermission(permissions.BasePermission):
    message = 'Access to object not allowed.'

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS and (obj.state == STATE_PUBLIC) or
            obj.owner == request.user and\
            (request.method not in permissions.SAFE_METHODS and obj.state == STATE_INITIAL) or
            obj.owner == request.user and request.method in permissions.SAFE_METHODS
        )


class MapPermission(permissions.BasePermission):
    message = 'Access to map not allowed.'

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS and (obj.state == STATE_PUBLIC) or
            obj.owner == request.user
        )
