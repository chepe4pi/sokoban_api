from django_filters import FilterSet, CharFilter, BooleanFilter
from sk_map.models import Wall, Box, Point, Men, Map


class MapBaseFilterSet(FilterSet):
    owner = CharFilter(name='aggrigator__owner__username')
    public = BooleanFilter(name='aggrigator__public')

    class Meta:
        abstract = True
        fields = ['owner', 'public']


class MapFilterSet(MapBaseFilterSet):
    owner = CharFilter(name='owner__username')
    public = BooleanFilter(name='public')

    class Meta(MapBaseFilterSet.Meta):
        model = Map


class WallFilterSet(MapBaseFilterSet):
    class Meta(MapBaseFilterSet.Meta):
        model = Wall


class BoxFilterSet(MapBaseFilterSet):
    class Meta(MapBaseFilterSet.Meta):
        model = Box


class PointFilterSet(MapBaseFilterSet):
    class Meta(MapBaseFilterSet.Meta):
        model = Point


class MenFilterSet(MapBaseFilterSet):
    class Meta(MapBaseFilterSet.Meta):
        model = Men
