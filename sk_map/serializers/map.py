from decimal import Decimal

from rest_framework import serializers

from sk_core.serializer import BaseModelSerializer
from ..models import Wall, Box, Point, Men, Map, MapLocation
from sk_game.models import UserMapMembership
from rest_framework.exceptions import ValidationError


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
    rating = serializers.SerializerMethodField()

    def validate_public(self, value):
        if value is False or UserMapMembership.objects.filter(owner=self.context['request'].user,
                                                              map=self.instance.id, done=True).count() > 0:
            return value
        else:
            raise ValidationError('First you have to took this map')

    def get_rating(self, instance):
        rating = instance.rating
        players_count = UserMapMembership.objects.filter(map=instance).exclude(rate=None).count()
        if rating and players_count:
            return round(Decimal(rating / players_count), 2)

    class Meta:
        model = Map
        fields = ('id', 'title', 'owner', 'public', 'rating')
        extra_kwargs = {'rating': {'read_only': True}}


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
