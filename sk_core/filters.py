from rest_framework.filters import BaseFilterBackend


# TODO Remove class if unused
class OwnerFilterBackend(BaseFilterBackend):
    """
    Base filter - allows users to see only own objects.
    """

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(owner=request.user)


class AggrigatorOwnerFilterBackend(BaseFilterBackend):
    """
    Base filter - allows users to see only own objects.
    """

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(aggrigator__owner=request.user)
