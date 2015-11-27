from django_filters import FilterSet, MethodFilter
from .models import Wall, Box, Point, Men, Map


class MapBaseFilterSet(FilterSet):
    owner = MethodFilter(action='filter_public')

    class Meta:
        abstract = True
        fields = ['owner']

    def filter_public(self, queryset, value):
        return queryset.filter(aggrigator__owner__username=value, aggrigator__public=True)


class MapFilterSet(MapBaseFilterSet):
    class Meta(MapBaseFilterSet.Meta):
        model = Map
    def filter_public(self, queryset, value):
        return queryset.filter(owner__username=value, public=True)


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
