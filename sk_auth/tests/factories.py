import factory
from django.contrib.auth import get_user_model
from sk_core.factories import faker

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = faker.simple_profile()['username']
    email = faker.simple_profile()['mail']
    password = faker.password()
