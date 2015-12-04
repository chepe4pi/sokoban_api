from sk_core.serializer import BaseModelSerializer
from ..models import Wall, Box, Point, Men, Map


class MapObjectSerializer(BaseModelSerializer):
    class Meta:
        fields = ('id', 'x', 'y', 'map')


class WallSerializer(MapObjectSerializer):
    class Meta(MapObjectSerializer.Meta):
        model = Wall


class BoxSerializer(MapObjectSerializer):
    class Meta(MapObjectSerializer.Meta):
        model = Box


class PointSerializer(MapObjectSerializer):
    class Meta(MapObjectSerializer.Meta):
        model = Point


class MenSerializer(MapObjectSerializer):
    class Meta(MapObjectSerializer.Meta):
        model = Men


class MapSerializer(BaseModelSerializer):
    class Meta:
        model = Map
        fields = ('id', 'title', 'owner', 'public')
