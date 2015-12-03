from django_filters import FilterSet, CharFilter, BooleanFilter
from sk_map.models import Wall, Box, Point, Men, Map


class MapFilterSet(FilterSet):
    owner = CharFilter(name='owner__username')
    public = BooleanFilter(name='public')

    class Meta:
        fields = ['owner', 'public']
        model = Map


class WallFilterSet(MapFilterSet):
    class Meta(MapFilterSet.Meta):
        model = Wall


class BoxFilterSet(MapFilterSet):
    class Meta(MapFilterSet.Meta):
        model = Box


class PointFilterSet(MapFilterSet):
    class Meta(MapFilterSet.Meta):
        model = Point


class MenFilterSet(MapFilterSet):
    class Meta(MapFilterSet.Meta):
        model = Men
