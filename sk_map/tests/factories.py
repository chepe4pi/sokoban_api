import factory
from sk_core.factories import faker
from ..models import Map, Wall, Box, Point, Men


# class MapBaseFactory(factory.django.DjangoModelFactory):


class MapFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Map

    username = faker.simple_profile()['username']
    email = faker.simple_profile()['mail']
    password = faker.password()


# class MapObjFactory(MapFactory)