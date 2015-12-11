from rest_framework import status
from rest_framework.test import APITestCase
from faker import Faker
from sk_map.tests.factories import MapFactory
from django.utils.http import urlencode
import random


faker = Faker()


class SkinTestCase(APITestCase):
    url = '/skins/'
    fixtures = ['test_admin_user.json', 'base_skins.json']
    choices = ['box', 'point', 'wall', 'men', 'background']

    def setUp(self):
        super(SkinTestCase, self).setUp()
        self.skin_id = faker.random_int(min=1, max=4)
        self.obj = MapFactory(skin_id=self.skin_id)

    def test_get_any_skin(self):
        response = self.client.get(self.url + str(faker.random_int(min=1, max=4)) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_skin_by_filter(self):
        response = self.client.get(self.url + '?' + urlencode({'map': self.obj.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_second = self.client.get(self.url + str(self.skin_id) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(response_second.data, response.data)

    # def test_get_any_image_from_skin(self):
    #     response = self.client.get(self.url + str(faker.random_int(min=1, max=4)) + '/')
    #     self.url = response.data[random.choice(self.choices)]
    #     print(self.url)
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
