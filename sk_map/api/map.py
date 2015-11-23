from django.utils.functional import cached_property
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, DjangoModelPermissionsOrAnonReadOnly
from ..models import Map
from ..serializers.map import MapSerializer, MapBaseSerializer


class MapBaseAPIView(object):
    permission_classes = [AllowAny]
    queryset = Map.objects.all()

    class Meta:
        abstract = True


class MapCreateApiView(MapBaseAPIView, CreateAPIView):
    """
    A View for create Map objects
    """

    serializer_class = MapBaseSerializer

map_create_api_view = MapCreateApiView.as_view()


class MapApiView(MapBaseAPIView, RetrieveUpdateDestroyAPIView):
    """
    A View for read-update-delete Map objects.
    """

    serializer_class = MapSerializer

map_api_view = MapApiView.as_view()


class MapsListView(MapBaseAPIView, ListAPIView):
    """
    A View for viewing list of Map object.
    """

    serializer_class = MapBaseSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

maps_list_api_view = MapsListView.as_view()
