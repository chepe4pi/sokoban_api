from rest_framework import permissions


class IsOwnerOrReadOnlyIfPublic(permissions.BasePermission):
    message = 'Access to object not allowed.'

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS and obj.is_public() or
            obj.get_owner() == request.user
        )


class ReadOnly(permissions.BasePermission):
    message = 'Read only View.'

    def has_object_permission(self, request, view, obj):

        return (
            request.method in permissions.SAFE_METHODS and obj.is_public() or
            request.method in permissions.SAFE_METHODS and obj.get_owner() == request.user
        )
