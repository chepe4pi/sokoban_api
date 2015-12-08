from rest_framework.test import APITestCase
from rest_framework import status
from .factories import UserFactory
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginTestCase(APITestCase):

    url = '/auth/login/'

    def setUp(self):
        self.user = UserFactory()
        self.data = {
            'username': self.user.username,
            'password': self.user.password
        }
        self.expected = {
            'username': self.user.username,
            'email': self.user.email,
        }
        self.user.set_password(self.user.password)
        self.user.save()

    def test_login(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.expected)
        self.assertEqual(User.objects.get(username=self.user.username).username, self.user.username)

    def test_wrong_password(self):
        self.data['password'] = 'sW3%j34G3'
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.data['password'] = ''
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wrong_username(self):
        self.data['username'] = self.user.email
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.data['username'] = ''
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class RegTestCase(APITestCase):

    url = '/auth/register/'

    def setUp(self):
        self.user = UserFactory.build()
        self.data = {
            'username': self.user.username,
            'email': self.user.email,
            'password': self.user.password
        }
        self.expected = {
            'username': self.user.username,
            'email': self.user.email,
        }

    def test_create_user(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, self.expected)
        self.assertEqual(User.objects.get(username=self.user.username).username, self.user.username)

    def test_not_valid_password(self):
        self.data['password'] = '1$aF'
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.data['password'] = '1213123'
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.data['password'] = 'password'
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.data['password'] = ''
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_valid_email(self):
        self.data['email'] = self.user.username
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.data['email'] = ''
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_valid_username(self):
        self.data['username'] = '%$%Fjfk'
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.data['username'] = ''
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
