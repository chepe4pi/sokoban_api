from rest_framework.filters import BaseFilterBackend


class OwnerFilterBackend(BaseFilterBackend):
    """
    Base filter - allows users to see only own objects.
    """

    def filter_queryset(self, request, queryset, view):
        if request.user.is_authenticated():
            return queryset.filter(owner=request.user)
