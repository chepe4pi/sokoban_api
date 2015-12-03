import factory
from sk_core.factories import faker
from sk_auth.tests.factories import UserFactory
from ..models import Map, Wall, Box, Point, Men


class AccesableObjBaseFactory(factory.django.DjangoModelFactory):
    class Meta:
        abstract = True

    owner = factory.SubFactory(UserFactory)
    public = True


class MapFactory(AccesableObjBaseFactory):
    class Meta:
        model = Map

    title = faker.word()
    x_size = faker.random_int(min=0, max=99)
    y_size = faker.random_int(min=0, max=99)


class MapObjFactory(AccesableObjBaseFactory):
    class Meta:
        abstract = True

    map = factory.SubFactory(MapFactory)
    x = factory.LazyAttribute(lambda obj: faker.random_int(min=0, max=obj.map.x_size))
    y = factory.LazyAttribute(lambda obj: faker.random_int(min=0, max=obj.map.y_size))


class WallFactory(MapObjFactory):
    class Meta:
        model = Wall


class BoxFactory(MapObjFactory):
    class Meta:
        model = Box


class PointFactory(MapObjFactory):
    class Meta:
        model = Point


class MenFactory(MapObjFactory):
    class Meta:
        model = Men
