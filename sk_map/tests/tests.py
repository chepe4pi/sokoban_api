from rest_framework import status
from rest_framework.test import APITestCase
from sk_core.tests import TestCasePermissions, AuthorizeForTests
from .factories import WallFactory, MapFactory, PointFactory, MenFactory, BoxFactory
from ..models import Map, Wall, Box, Point, Men
from faker import Faker

faker = Faker()


class MapCreateTestCase(AuthorizeForTests, APITestCase):
    url = '/maps/'

    def setUp(self):
        super(MapCreateTestCase, self).setUp()
        self.obj = MapFactory.build()
        self.data = {
            'title': self.obj.title,
        }
        self.expected = {
            'title': self.obj.title,
            'public': self.obj.public,
            'owner': self.user.username
        }

    def test_create_map(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Map.objects.get(owner=self.user.id, id=response.data['id']).title, self.obj.title)
        self.expected['id'] = int(response.data['id'])
        self.assertEqual(response.data, self.expected)

    def test_wrong_map(self):
        self.data['title'] = ''
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class MapTestCase(TestCasePermissions, APITestCase):
    url = '/maps/'

    def setUp(self):
        self.obj = MapFactory()
        super(MapTestCase, self).setUp()
        self.data = {
            'id': self.obj.id,
            'title': self.obj.title,
            'public': self.obj.public,
            'owner': self.user.username
        }

    def test_allow_get_own_obj(self):
        super(MapTestCase, self).test_allow_get_own_obj()
        self.assertEqual(self.response.data, self.data)

    def test_allow_put_own_obj(self):
        self.data['title'] = faker.word()
        response = self.client.put(self.obj_url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.data)


class MapObjCreateTestCase(object):
    class Meta:
        abstract = True

    def setUp(self):
        super(MapObjCreateTestCase, self).setUp()
        self.map = MapFactory()
        self.data = {
            'x': self.obj.x,
            'y': self.obj.y,
            'map': self.map.id
        }
        
    def test_create_obj(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.data['id'] = response.data['id']
        self.assertEqual(response.data, self.data)

    def test_deny_create_same(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wrong_x(self):
        self.data['x'] = ''
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.data['x'] = 'a'
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wrong_y(self):
        self.data['y'] = ''
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.data['x'] = 'b'
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class MapObjTestCase(object):
    class Meta:
        abstract = True

    def setUp(self):
        super(MapObjTestCase, self).setUp()
        self.data = {
            'id': self.obj.id,
            'x': self.obj.x,
            'y': self.obj.y,
            'map': self.obj.map.id
        }

    def test_allow_get_own_obj(self):
        super(MapObjTestCase, self).test_allow_get_own_obj()
        self.assertEqual(self.response.data, self.data)

    def test_allow_put_own_obj(self):
        self.data['x'] = faker.random_int(min=0, max=99)
        self.data['y'] = faker.random_int(min=0, max=99)
        response = self.client.put(self.obj_url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.data)


class WallCreateTestCase(MapObjCreateTestCase, AuthorizeForTests, APITestCase):
    url = '/wall/'

    def setUp(self):
        self.obj = WallFactory.build()
        super(WallCreateTestCase, self).setUp()

    def test_create_obj(self):
        super(WallCreateTestCase, self).test_create_obj()
        self.assertEqual(Wall.objects.filter(x=self.obj.x, y=self.obj.y, map=self.map).count(), 1)


class WallTestCase(MapObjTestCase, TestCasePermissions, APITestCase):
    url = '/wall/'

    def setUp(self):
        self.obj = WallFactory()
        super(WallTestCase, self).setUp()


class BoxCreateTestCase(MapObjCreateTestCase, AuthorizeForTests, APITestCase):
    url = '/box/'

    def setUp(self):
        self.obj = BoxFactory.build()
        super(BoxCreateTestCase, self).setUp()

    def test_create_obj(self):
        super(BoxCreateTestCase, self).test_create_obj()
        self.assertEqual(Box.objects.filter(x=self.obj.x, y=self.obj.y, map=self.map).count(), 1)


class BoxTestCase(MapObjTestCase, TestCasePermissions, APITestCase):
    url = '/box/'

    def setUp(self):
        self.obj = BoxFactory()
        super(BoxTestCase, self).setUp()


class PointCreateTestCase(MapObjCreateTestCase, AuthorizeForTests, APITestCase):
    url = '/point/'

    def setUp(self):
        self.obj = PointFactory.build()
        super(PointCreateTestCase, self).setUp()

    def test_create_obj(self):
        super(PointCreateTestCase, self).test_create_obj()
        self.assertEqual(Point.objects.filter(x=self.obj.x, y=self.obj.y, map=self.map).count(), 1)


class PointTestCase(MapObjTestCase, TestCasePermissions, APITestCase):
    url = '/point/'

    def setUp(self):
        self.obj = PointFactory()
        super(PointTestCase, self).setUp()


class MenCreateTestCase(MapObjCreateTestCase, AuthorizeForTests, APITestCase):
    url = '/men/'

    def setUp(self):
        self.obj = MenFactory.build()
        super(MenCreateTestCase, self).setUp()

    def test_create_obj(self):
        super(MenCreateTestCase, self).test_create_obj()
        self.assertEqual(Men.objects.filter(x=self.obj.x, y=self.obj.y, map=self.map).count(), 1)

    def test_uniq_on_map(self):
        super(MenCreateTestCase, self).test_create_obj()
        self.data['x'] = self.data['x'] + 1
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class MenTestCase(MapObjTestCase, TestCasePermissions, APITestCase):
    url = '/men/'

    def setUp(self):
        self.obj = MenFactory()
        super(MenTestCase, self).setUp()


# TODO create  bath