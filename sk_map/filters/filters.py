from django_filters import FilterSet, CharFilter, BooleanFilter, NumberFilter
from sk_map.models import Wall, Box, Point, Men, Map


class MapFilterSet(FilterSet):
    owner = CharFilter(name='owner__username')
    public = BooleanFilter(name='public')

    class Meta:
        fields = ['owner', 'public']
        model = Map


class MapObjFilterSetMixin(FilterSet):
    map = NumberFilter(name='map__id')

    class Meta:
        fields = ['map']


class WallFilterSet(MapObjFilterSetMixin):
    class Meta(MapObjFilterSetMixin.Meta):
        model = Wall


class BoxFilterSet(MapObjFilterSetMixin):
    class Meta(MapObjFilterSetMixin.Meta):
        model = Box


class PointFilterSet(MapObjFilterSetMixin):
    class Meta(MapObjFilterSetMixin.Meta):
        model = Point


class MenFilterSet(MapObjFilterSetMixin):
    class Meta(MapObjFilterSetMixin.Meta):
        model = Men
