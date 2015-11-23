from rest_framework import serializers
from ..models import Wall, Box, Point, Men, Map


class MapObjectSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'x', 'y')


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


class MapBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = ('id', 'title', 'owner')


class MapSerializer(MapBaseSerializer):
    wall_set = WallSerializer(many=True)
    box_set = BoxSerializer(many=True)
    point_set = PointSerializer(many=True)
    men = MenSerializer()

    class Meta(MapBaseSerializer.Meta):
        fields = ('id', 'title', 'owner', 'wall_set', 'box_set', 'point_set', 'men')
