from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .factories import WallFactory, MapFactory, PointFactory

User = get_user_model()


class MapTestCase(APITestCase):

    # url = '/auth/login/'

    def setUp(self):
        self.map = MapFactory.build()
        self.point = PointFactory()
        print(self.map.x_size)
        print(self.point.x)
        # self.data = {
        #     'username': self.user.username,
        #     'password': self.user.password
        # }
        # self.user.set_password(self.user.password)
        # self.user.save()

    def test_create_map(self):
        pass
        # response = self.client.post(self.url, self.data)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(User.objects.get(username=self.user.username).username, self.user.username)