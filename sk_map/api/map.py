from ..filters.filters import WallFilterSet, BoxFilterSet, PointFilterSet, MenFilterSet, MapFilterSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from sk_core.permissions import IsOwnerOrReadOnlyIfPublic
from sk_core.views import BaseModelViewSet, PartialUpdateMixin
from ..models import Map, Wall, Box, Point, Men
from ..serializers.map import MapSerializer, WallSerializer, BoxSerializer, PointSerializer, MenSerializer
from ..filters.backends import IsPublicFilterBackend
from rest_framework.filters import DjangoFilterBackend


class MapObjectsBaseViewSet(BaseModelViewSet):
    """
    A Base ViewSet for Maps and MapObjects
    """
    filter_backends = (DjangoFilterBackend, IsPublicFilterBackend)
    permission_classes = [IsOwnerOrReadOnlyIfPublic, IsAuthenticatedOrReadOnly]

    class Meta:
        abstract = True


class MapsViewSet(MapObjectsBaseViewSet, PartialUpdateMixin):
    """
    A View for CRUD Map-object.
    """
    queryset = Map.objects.all()
    serializer_class = MapSerializer
    filter_class = MapFilterSet


class WallViewSet(MapObjectsBaseViewSet):
    """
    A View for CRUD Wall-objects.
    """
    serializer_class = WallSerializer
    queryset = Wall.objects.all()
    filter_class = WallFilterSet


class BoxViewSet(MapObjectsBaseViewSet):
    """
    A View for CRUD Box-objects.
    """
    serializer_class = BoxSerializer
    queryset = Box.objects.all()
    filter_class = BoxFilterSet


class PointViewSet(MapObjectsBaseViewSet):
    """
    A View for CRUD Point-objects.
    """
    serializer_class = PointSerializer
    queryset = Point.objects.all()
    filter_class = PointFilterSet


class MenViewSet(MapObjectsBaseViewSet):
    """
    A View for CRUD Men-objects.
    """
    serializer_class = MenSerializer
    queryset = Men.objects.all()
    filter_class = MenFilterSet
