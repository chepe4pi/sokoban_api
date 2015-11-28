from rest_framework.filters import BaseFilterBackend
from django.db.models import Q


class IsPublicFilterBackend(BaseFilterBackend):
    """
    Filter that only allows users to see only public objects.
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(Q(public=True) | Q(owner=request.user))
