from decimal import Decimal

from rest_framework import serializers

from sk_core.models import STATE_PUBLIC, STATE_PRIVATE, STATE_INITIAL
from sk_core.serializer import BaseModelSerializer
from ..models import Wall, Box, Point, Men, Map
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
    rating = serializers.SerializerMethodField()

    def get_rating(self, instance):
        rating = instance.rating
        players_count = UserMapMembership.objects.filter(map=instance).exclude(rate=None).count()
        if rating and players_count:
            return round(Decimal(rating / players_count), 2)

    def validate_state(self, value):
        if value == STATE_PUBLIC:
            if self.instance.state == STATE_PRIVATE:
                return value
            else:
                raise ValidationError(_('First you have to took this map'))
        elif value == STATE_INITIAL:
            UserMapMembership.objects.filter(map=self.instance, owner=self.instance.owner).update(done=False)
            return value
        return value

    class Meta:
        model = Map
        fields = ('id', 'title', 'owner', 'rating', 'state')
        extra_kwargs = {'rating': {'read_only': True},
                        'owner': {'read_only': True}}


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
