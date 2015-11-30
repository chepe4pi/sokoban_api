from rest_framework import permissions


class IsOwnerOrReadOnlyIfPublic(permissions.BasePermission):
    message = 'Access to object not allowed.'

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS and obj.public and request.user.is_authenticated() or
            obj.owner == request.user
        )


class ReadOnly(permissions.BasePermission):
    message = 'Read only View.'

    def has_object_permission(self, request, view, obj):

        return (
            request.method in permissions.SAFE_METHODS and obj.public and request.user.is_authenticated() or
            request.method in permissions.SAFE_METHODS and obj.owner == request.user
        )
