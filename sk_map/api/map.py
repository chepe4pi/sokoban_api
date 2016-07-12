from rest_framework.filters import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from sk_core.filters.backends import IsPublicFilterBackend
from sk_core.permissions import MapObjectPermission, MapPermission
from sk_core.views import BaseModelViewSet
from ..filters.filters import WallFilterSet, BoxFilterSet, PointFilterSet, MenFilterSet, MapFilterSet
from ..models import Map, Wall, Box, Point, Men
from ..serializers.map import MapSerializer, WallSerializer, BoxSerializer, PointSerializer, MenSerializer


class MapObjectsBaseViewSet(BaseModelViewSet):

    filter_backends = (DjangoFilterBackend, IsPublicFilterBackend)
    permission_classes = [MapObjectPermission, IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        """
        This method return a list of objects.
        It's a nice way to filter objects by Map for receive all necessary elements for creating a game level.
        """
        return super(MapObjectsBaseViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        This method return a object by id.
        It's allow to get any Map-object by id, but more usefull to get list of objects and filter by Map.
        """
        return super(MapObjectsBaseViewSet, self).retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        This method create a object on the Map.
        """
        return super(MapObjectsBaseViewSet, self).create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        This method delete object from the Map.
        """
        return super(MapObjectsBaseViewSet, self).destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        This method update object on the Map.
        It's can be usefull for drag-and-drop object on the Map without second creating.
        """
        return super(MapObjectsBaseViewSet, self).update(request, *args, **kwargs)

    class Meta:
        abstract = True


class MapViewSet(MapObjectsBaseViewSet):
    """
    Maps as a game levels.
    The Map objects is a game levels, which can create any authorized User and share with other players.
    """
    queryset = Map.objects.all()
    serializer_class = MapSerializer
    permission_classes = [MapPermission, IsAuthenticatedOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        """
        This method return info about single Map
        """
        return super(MapObjectsBaseViewSet, self).retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        This method delete a Map-object.
        """
        return super(MapObjectsBaseViewSet, self).destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        This method update info about a Map
        """
        return super(MapObjectsBaseViewSet, self).update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        This method partial update info about a Map.
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class MapListViewSet(MapViewSet):

    filter_class = MapFilterSet

    def list(self, request, *args, **kwargs):
        """
        This method return a list and info about available Maps
        """
        return super(MapObjectsBaseViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        This method create a Map-object.
        """
        return super(MapObjectsBaseViewSet, self).create(request, *args, **kwargs)


class WallViewSet(MapObjectsBaseViewSet):
    """
    Wall on the Map.
    The Box-objects will appear on the Map as element of gameplay.
    Wall objects can be created on the Map for limit moving of Man and produce more interesting levels.
    """
    serializer_class = WallSerializer
    queryset = Wall.objects.all()


class WallListViewSet(WallViewSet):
    filter_class = WallFilterSet


class BoxViewSet(MapObjectsBaseViewSet):
    """
    Box on the Map.
    The Box-objects will appear on the Map as element of gameplay.
    Player have to move Boxes and cover Points.
    """
    serializer_class = BoxSerializer
    queryset = Box.objects.all()
    filter_class = BoxFilterSet


class BoxListViewSet(BoxViewSet):
    filter_class = BoxFilterSet


class PointViewSet(MapObjectsBaseViewSet):
    """
    Point on the Map.
    The Point-objects will appear on the Map as element of gameplay.
    Player have to cover all Points by Boxes for complete the game level.
    """
    serializer_class = PointSerializer
    queryset = Point.objects.all()


class PointListViewSet(PointViewSet):
    filter_class = PointFilterSet


class MenViewSet(MapObjectsBaseViewSet):
    """
    Man on the Map.
    The Man-object will appear on the Map as element of gameplay.
    Player have to manipulate the Man for move Boxes and cover all Points.
    """
    serializer_class = MenSerializer
    queryset = Men.objects.all()


class MenListViewSet(MenViewSet):
    filter_class = MenFilterSet
