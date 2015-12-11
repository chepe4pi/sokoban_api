from rest_framework import status
from rest_framework.test import APITestCase
from sk_core.tests.tests import AuthorizeForTestsMixin
from ..models import UserMapMembership
from faker import Faker
from .factories import GameFactory
from sk_map.tests.factories import MapFactory

faker = Faker()


class GameTestCase(AuthorizeForTestsMixin, APITestCase):
    url = '/game/'
    fixtures = ['test_admin_user.json', 'test_map1.json']

    def setUp(self):
        super(GameTestCase, self).setUp()
        self.data = {
            'steps': [
                {"x": 6, 'y': 3}, {"x": 6, 'y': 2}, {"x": 5, 'y': 2}, {"x": 4, 'y': 2}, {"x": 4, 'y': 3},
                {"x": 4, 'y': 2}, {"x": 5, 'y': 2}, {"x": 6, 'y': 2}, {"x": 6, 'y': 3}, {"x": 6, 'y': 4},
                {"x": 5, 'y': 4}, {"x": 4, 'y': 4}, {"x": 3, 'y': 4}, {"x": 4, 'y': 4}, {"x": 5, 'y': 4},
                {"x": 6, 'y': 4}, {"x": 6, 'y': 3}, {"x": 6, 'y': 2}, {"x": 5, 'y': 2}, {"x": 4, 'y': 2},
                {"x": 4, 'y': 3}, {"x": 3, 'y': 3}
            ],
            'map': 6
        }

    def test_put_steps(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserMapMembership.objects.filter(owner=self.user.id, map=6, done=True).count(), 1)

    def test_try_jump(self):
        self.data['steps'][1] = {"x": 6, 'y': 4}
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_go_to_wall(self):
        self.data['steps'][2] = {"x": 6, 'y': 1}
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_born_at_other_place(self):
        self.data['steps'][0] = {"x": 2, 'y': 5}
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_forget_about_one_box(self):
        self.data['steps'][-1] = {"x": 4, 'y': 2}
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_set_rate(self):
        obj = MapFactory()
        self.url = self.url + str(obj.id) + '/'
        GameFactory(map=obj, owner=self.user, done=True)
        response = self.client.patch(self.url, {'rate': faker.random_int(min=1, max=4)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
