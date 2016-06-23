from sk_core.serializer import BaseModelSerializer
from ..models import Wall, Box, Point, Men, Map, MapLocation
from sk_game.models import UserMapMembership
from rest_framework.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


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
    def validate_public(self, value):
        if value is False or UserMapMembership.objects.filter(owner=self.context['request'].user,
                                                              map=self.instance.id, done=True).count() > 0:
            return value
        else:
            raise ValidationError(_('First you have to took this map'))

    class Meta:
        model = Map
        fields = ('id', 'title', 'owner', 'public')


class LocationSerializer(BaseModelSerializer):
    class Meta:
        model = Wall  # TODO this is cheat
        fields = ('x', 'y')


class MapDetailSerializer(BaseModelSerializer):
    wall_set = LocationSerializer(many=True, read_only=True)
    box_set = LocationSerializer(many=True, read_only=True)
    point_set = LocationSerializer(many=True, read_only=True)
    men = LocationSerializer(read_only=True)

    class Meta(MapSerializer.Meta):
        model = Map
        fields = ('wall_set', 'box_set', 'point_set', 'men')
