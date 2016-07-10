import factory

from sk_auth.tests.factories import UserFactory
from sk_core.models import STATE_INITIAL


class OwnableObjBaseFactory(factory.django.DjangoModelFactory):
    class Meta:
        abstract = True

    owner = factory.SubFactory(UserFactory)


class AccesableObjBaseFactory(OwnableObjBaseFactory):
    class Meta:
        abstract = True

    state = STATE_INITIAL
