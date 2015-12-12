from django_filters import FilterSet, NumberFilter
from ..models import Skins


class SkinFilterSet(FilterSet):
    map = NumberFilter(name='map__id')

    class Meta:
        fields = ['map']
        model = Skins
