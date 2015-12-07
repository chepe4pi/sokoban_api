from sk_core.serializer import BaseModelSerializer
from ..models import Wall, Box, Point, Men, Map


class MapObjectSerializerMixin(BaseModelSerializer):
    class Meta:
        fields = ('id', 'x', 'y', 'map')


class WallSerializer(MapObjectSerializerMixin):
    class Meta(MapObjectSerializerMixin.Meta):
        model = Wall


class BoxSerializer(MapObjectSerializerMixin):
    class Meta(MapObjectSerializerMixin.Meta):
        model = Box


class PointSerializer(MapObjectSerializerMixin):
    class Meta(MapObjectSerializerMixin.Meta):
        model = Point


class MenSerializer(MapObjectSerializerMixin):
    class Meta(MapObjectSerializerMixin.Meta):
        model = Men


class MapSerializer(BaseModelSerializer):
    class Meta:
        model = Map
        fields = ('id', 'title', 'owner', 'public')
