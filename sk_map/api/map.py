from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import ModelViewSet

from sk_core.permissions import IsOwnerOrReadOnlyIfPublic, ReadOnly
from sk_core.views import BaseModelViewSet
from ..models import Map, Wall, Box, Point, Men
from ..serializers.map import MapSerializer, MapDetailSerializer,\
    WallSerializer, BoxSerializer, PointSerializer, MenSerializer


class MapObjectsBaseViewSet(ModelViewSet):
    permission_classes = [IsOwnerOrReadOnlyIfPublic]
    filter_fields = ('aggrigator__owner', 'aggrigator__public')

    class Meta:
        abstract = True
    # TODO add filter class


class MapsViewSet(BaseModelViewSet):
    """
    A View for CRUD Map-object.
    """
    permission_classes = [IsOwnerOrReadOnlyIfPublic]
    queryset = Map.objects.all()
    serializer_class = MapSerializer
    filter_fields = ('owner', 'public')
    # TODO add filter class


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


class BoxViewSet(MapObjectsBaseViewSet):
    """
    A View for CRUD Box-objects.
    """
    serializer_class = BoxSerializer
    queryset = Box.objects.all()


class PointViewSet(MapObjectsBaseViewSet):
    """
    A View for CRUD Point-objects.
    """
    serializer_class = PointSerializer
    queryset = Point.objects.all()


class MenViewSet(MapObjectsBaseViewSet):
    """
    A View for CRUD Men-objects.
    """
    serializer_class = MenSerializer
    queryset = Men.objects.all()
