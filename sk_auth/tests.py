from rest_framework.test import APITestCase
from sk_core.factories import faker
from rest_framework import status
from django.contrib.auth import get_user_model


class AuthTestCase(APITestCase):

    User = get_user_model()
    username = faker.simple_profile()['username']
    email = faker.simple_profile()['mail']
    password = faker.password()

    def test_create_user(self):
        data = {
            'username': self.username,
            'email': self.email,
            'password': self.password
        }
        url = '/register/'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.User.objects.get(username=self.username).username, self.username)

    def test_login(self):
        data = {
            'username': self.username,
            'password': self.password
        }
        url = '/api-auth/login/'
        response = self.client.post(url, data, format='json')
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.User.objects.get(username=self.username).username, self.username)

# TODO Cases raise 400(invalid data), wrong pass