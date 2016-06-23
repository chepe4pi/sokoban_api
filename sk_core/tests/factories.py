import factory

from sk_auth.tests.factories import UserFactory


class OwnableObjBaseFactory(factory.django.DjangoModelFactory):
    class Meta:
        abstract = True

    owner = factory.SubFactory(UserFactory)


class AccesableObjBaseFactory(OwnableObjBaseFactory):
    class Meta:
        abstract = True

    public = False
