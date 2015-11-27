from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from ..filters import WallFilterSet, BoxFilterSet, PointFilterSet, MenFilterSet, MapFilterSet
from sk_core.permissions import IsOwnerOrReadOnlyIfPublic, ReadOnly
from sk_core.views import BaseModelViewSet
from ..models import Map, Wall, Box, Point, Men
from ..serializers.map import MapSerializer, MapDetailSerializer,\
    WallSerializer, BoxSerializer, PointSerializer, MenSerializer


class MapObjectsBaseViewSet(ModelViewSet):
    permission_classes = [IsOwnerOrReadOnlyIfPublic]
# TODO List only through filter
    class Meta:
        abstract = True


class MapsViewSet(BaseModelViewSet):
    """
    A View for CRUD Map-object.
    """
    permission_classes = [IsOwnerOrReadOnlyIfPublic]
    queryset = Map.objects.all()
    serializer_class = MapSerializer
    filter_class = MapFilterSet
# TODO List only through filter


class MapDetailViewSet(RetrieveModelMixin, GenericViewSet):
    """
    A View for get full description of Map.
    """
    queryset = Map.objects.all()
    serializer_class = MapDetailSerializer
    permission_classes = [ReadOnly]  # TODO AggrigatorReadOnly


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