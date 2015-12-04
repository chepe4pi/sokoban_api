import factory
from faker import Faker
from sk_auth.tests.factories import UserFactory
from ..models import Map, Wall, Box, Point, Men

faker = Faker()


class AccesableObjBaseFactory(factory.django.DjangoModelFactory):
    class Meta:
        abstract = True

    owner = factory.SubFactory(UserFactory)
    public = False


class MapFactory(AccesableObjBaseFactory):
    class Meta:
        model = Map

    title = faker.word()


class MapObjFactory(AccesableObjBaseFactory):
    class Meta:
        abstract = True

    map = factory.SubFactory(MapFactory)
    x = factory.LazyAttribute(lambda obj: faker.random_int(min=0, max=99))
    y = factory.LazyAttribute(lambda obj: faker.random_int(min=0, max=99))


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
