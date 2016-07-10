from rest_framework.filters import BaseFilterBackend
from django.db.models import Q

from sk_core.models import STATE_PUBLIC


class IsPublicFilterBackend(BaseFilterBackend):
    """
    Filter that only allows users to see only public objects.
    """
    def filter_queryset(self, request, queryset, view):
        if request.user.is_authenticated():
            return queryset.filter(Q(state=STATE_PUBLIC) | Q(owner=request.user))
        else:
            return queryset.filter(state=STATE_PUBLIC)


class IsOwnerFilterBackend(BaseFilterBackend):
    """
    Filter that only allows users to see only own objects.
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(owner=request.user)
