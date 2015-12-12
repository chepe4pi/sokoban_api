from sk_core.tests.factories import OwnableObjBaseFactory
import factory
from ..models import UserMapMembership
from sk_map.tests.factories import MapFactory


class GameFactory(OwnableObjBaseFactory):
    class Meta:
        model = UserMapMembership

    map = factory.SubFactory(MapFactory)
    steps = [{"x": 1, 'y': 2}, {"x": 3, 'y': 4}]
