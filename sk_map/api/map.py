from django.utils.functional import cached_property
from sk_core.views import BaseModelViewSet
from sk_core.filters import OwnerFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from ..models import Map
from ..serializers.map import MapSerializer, MapBaseSerializer


class MapsViewSet(BaseModelViewSet):
    """
    A View for viewing list of Map object.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Map.objects.all()
    serializer_class = MapBaseSerializer
    filter_backends = (OwnerFilterBackend,)
