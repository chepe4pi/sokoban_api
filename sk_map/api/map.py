from django.utils.functional import cached_property
from sk_core.views import BaseModelViewSet
from ..permissions import IsOwnerOrReadOnlyIfPublic, ReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from ..models import Map, Wall, Box, Point, Men
from ..serializers.map import MapBaseSerializer, MapSerializer,\
    WallSerializer, BoxSerializer, PointSerializer, MenSerializer
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin
from django.shortcuts import get_object_or_404
from rest_framework.filters import DjangoObjectPermissionsFilter
from sk_core.permissions import CustomObjectPermissions


class MapObjectsBaseViewSet(ModelViewSet):
    permission_classes = [CustomObjectPermissions, IsOwnerOrReadOnlyIfPublic]
    filter_backends = [DjangoObjectPermissionsFilter] # TODO Enable filter
    filter_fields = ('aggrigator__owner', 'aggrigator__public')

    # def get_object(self):
    #     obj = get_object_or_404(self.get_queryset())
    #     self.check_object_permissions(self.request, obj)
    #     return obj

    class Meta:
        abstract = True
    # TODO add filter calss


class MapsViewSet(BaseModelViewSet):
    """
    A View for CRUD Map-object.
    """
    permission_classes = [IsOwnerOrReadOnlyIfPublic]
    queryset = Map.objects.all()
    serializer_class = MapBaseSerializer
    filter_fields = ('owner', 'public')
    # TODO add filter calss


class MapDetailViewSet(RetrieveModelMixin, GenericViewSet):
    """
    A View for get full description of Map.
    """
    queryset = Map.objects.all()
    serializer_class = MapSerializer
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
