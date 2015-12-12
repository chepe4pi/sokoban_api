from rest_framework import status
from django.utils.http import urlencode
from rest_framework.test import APITestCase
from sk_core.tests.tests import TestCasePermissionsMixin, AuthorizeForTestsMixin, TestCasePermissionPublicMixin
from ..serializers.map import MenSerializer, PointSerializer, BoxSerializer, WallSerializer, MapSerializer
from .factories import WallFactory, MapFactory, PointFactory, MenFactory, BoxFactory
from sk_game.tests.factories import GameFactory
from ..models import Map, Wall, Box, Point, Men
from faker import Faker
from mock_django import mock_signal_receiver
from django.db.models.signals import post_save

faker = Faker()


class MapCreateTestCase(AuthorizeForTestsMixin, APITestCase):
    url = '/maps/'

    def setUp(self):
        super(MapCreateTestCase, self).setUp()
        self.obj = MapFactory.build()
        self.data = {
            'title': self.obj.title,
        }
        self.expected = MapSerializer(self.obj).data

    def test_create_map(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Map.objects.get(owner=self.user.id, id=response.data['id']).title, self.obj.title)
        self.expected['id'] = int(response.data['id'])
        self.assertEqual(response.data, self.expected)

    def test_create_wrong_map(self):
        self.data['title'] = ''
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class MapTestCase(TestCasePermissionsMixin, APITestCase):
    url = '/maps/'

    def setUp(self):
        self.obj = MapFactory()
        super(MapTestCase, self).setUp()
        self.data = MapSerializer(self.obj).data

    def test_allow_get_own_obj(self):
        super(MapTestCase, self).test_allow_get_own_obj()
        self.assertEqual(self.response.data, self.data)

    def test_allow_change_public(self):
        GameFactory(map=self.obj, owner=self.user, done=True)
        states = True, False
        for state in states:
            data = {'public': state}
            response = self.client.patch(self.obj_url, data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(data['public'], response.data['public'])

    def test_deny_change_public_if_no_done(self):
        self.data = {'public': True}
        response = self.client.put(self.obj_url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_allow_patch(self):
        title = faker.word()
        part = {'title': title}
        self.data['title'] = title
        response = self.client.patch(self.obj_url, part)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.data)

    def test_deny_put_owner(self):
        part = {'owner': self.wrong_user.username}
        self.data['owner'] = self.wrong_user.username
        response = self.client.patch(self.obj_url, part)
        self.assertEqual(response.data['owner'], self.user.username) # TODO response code

    def test_filter(self):
        self.filter_url = self.url + '?' + urlencode({'owner': self.user.username})
        response = self.client.get(self.filter_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.data, response.data)

    def test_allow_get_unauthorized_if_public(self):
        setattr(self.obj, 'public', True)
        self.obj.save()
        self.client.logout()
        response = self.client.get(self.obj_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MapObjCreateTestCaseMixin(object):
    class Meta:
        abstract = True

    def setUp(self):
        super(MapObjCreateTestCaseMixin, self).setUp()
        self.map = MapFactory()
        self.obj.map = self.map

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

    def test_create_wrong_x(self):
        self.data['x'] = ''
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.data['x'] = 'a'
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_wrong_y(self):
        self.data['y'] = ''
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.data['x'] = 'b'
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class MapObjFilterTestCaseMixin(object):
    class Meta:
        abstract = True

    def setUp(self):
        super(MapObjFilterTestCaseMixin, self).setUp()
        self.filter_url = self.url + '?' + urlencode({'map': self.obj.map.id})

    def test_filter(self):
        self.expected = self.data.copy()
        self.data['x'] = faker.random_int(min=0, max=99)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(self.filter_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.expected, [dict(resp_obj) for resp_obj in response.data])

    def test_limit_offset_filter(self):
        filter_url = self.url + '?' + urlencode({'map': self.obj.map.id, 'limit': 1, 'offset': 0})
        response = self.client.get(filter_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.data, response.data['results'])
        filter_url = self.url + '?' + urlencode({'map': self.obj.map.id, 'limit': 1, 'offset': 1})
        response = self.client.get(filter_url)
        self.assertNotIn(self.data, response.data['results'])


class MapObjTestCaseMixin(object):
    class Meta:
        abstract = True

    def setUp(self):
        super(MapObjTestCaseMixin, self).setUp()
        self.parent_url = '/maps/' + str(self.obj.map.id) + '/'

    def test_allow_get_own_obj(self):
        super(MapObjTestCaseMixin, self).test_allow_get_own_obj()
        self.assertEqual(self.response.data, self.data)

    def test_allow_put_own_obj(self):
        self.data['x'] = faker.random_int(min=0, max=99)
        self.data['y'] = faker.random_int(min=0, max=99)
        response = self.client.put(self.obj_url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data, self.data)

    def test_put_wrong_data(self):
        self.data['x'] = ''
        response = self.client.put(self.obj_url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_deny_partial_put(self):
        self.part = {'x': faker.random_int(min=0, max=99)}
        response = self.client.put(self.obj_url, self.part)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signal_change_public(self):
        GameFactory(map=self.obj.map, owner=self.user, done=True)
        public = True
        with mock_signal_receiver(post_save) as receiver:
            response = self.client.patch(self.parent_url, {'public': public})
            self.assertNotEqual(receiver.call_count, 0)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.force_authenticate(user=self.wrong_user)
        response = self.client.get(self.obj_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(self.parent_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_deny_change_public_directly(self):
        GameFactory(map=self.obj.map, owner=self.user, done=True)
        self.data = {'public': True}
        response = self.client.put(self.obj_url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class WallCreateTestCase(MapObjCreateTestCaseMixin, AuthorizeForTestsMixin, APITestCase):
    url = '/wall/'

    def setUp(self):
        self.obj = WallFactory.build()
        super(WallCreateTestCase, self).setUp()
        self.data = WallSerializer(self.obj).data

    def test_create_obj(self):
        super(WallCreateTestCase, self).test_create_obj()
        self.assertEqual(Wall.objects.filter(x=self.obj.x, y=self.obj.y, map=self.map).count(), 1)


class WallTestCase(MapObjFilterTestCaseMixin, MapObjTestCaseMixin, TestCasePermissionPublicMixin,\
                   TestCasePermissionsMixin, APITestCase):
    url = '/wall/'

    def setUp(self):
        self.obj = WallFactory()
        self.data = WallSerializer(self.obj).data
        super(WallTestCase, self).setUp()


class BoxCreateTestCase(MapObjCreateTestCaseMixin, AuthorizeForTestsMixin, APITestCase):
    url = '/box/'

    def setUp(self):
        self.obj = BoxFactory.build()
        super(BoxCreateTestCase, self).setUp()
        self.data = BoxSerializer(self.obj).data

    def test_create_obj(self):
        super(BoxCreateTestCase, self).test_create_obj()
        self.assertEqual(Box.objects.filter(x=self.obj.x, y=self.obj.y, map=self.map).count(), 1)


class BoxTestCase(MapObjFilterTestCaseMixin, MapObjTestCaseMixin,\
                  TestCasePermissionPublicMixin, TestCasePermissionsMixin, APITestCase):
    url = '/box/'

    def setUp(self):
        self.obj = BoxFactory()
        self.data = BoxSerializer(self.obj).data
        super(BoxTestCase, self).setUp()


class PointCreateTestCase(MapObjCreateTestCaseMixin, AuthorizeForTestsMixin, APITestCase):
    url = '/point/'

    def setUp(self):
        self.obj = PointFactory.build()
        super(PointCreateTestCase, self).setUp()
        self.data = PointSerializer(self.obj).data

    def test_create_obj(self):
        super(PointCreateTestCase, self).test_create_obj()
        self.assertEqual(Point.objects.filter(x=self.obj.x, y=self.obj.y, map=self.map).count(), 1)


class PointTestCase(MapObjFilterTestCaseMixin, MapObjTestCaseMixin, TestCasePermissionPublicMixin,\
                    TestCasePermissionsMixin, APITestCase):
    url = '/point/'

    def setUp(self):
        self.obj = PointFactory()
        self.data = PointSerializer(self.obj).data
        super(PointTestCase, self).setUp()


class MenCreateTestCase(MapObjCreateTestCaseMixin, AuthorizeForTestsMixin, APITestCase):
    url = '/men/'

    def setUp(self):
        self.obj = MenFactory.build()
        super(MenCreateTestCase, self).setUp()
        self.data = MenSerializer(self.obj).data

    def test_create_obj(self):
        super(MenCreateTestCase, self).test_create_obj()
        self.assertEqual(Men.objects.filter(x=self.obj.x, y=self.obj.y, map=self.map).count(), 1)

    def test_uniq_on_map(self):
        super(MenCreateTestCase, self).test_create_obj()
        self.data['x'] = faker.random_int(min=0, max=99)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class MenTestCase(MapObjFilterTestCaseMixin, MapObjTestCaseMixin, TestCasePermissionPublicMixin,\
                  TestCasePermissionsMixin, APITestCase):
    url = '/men/'

    def setUp(self):
        self.obj = MenFactory()
        self.data = MenSerializer(self.obj).data
        super(MenTestCase, self).setUp()

    def test_filter(self):
        response = self.client.get(self.filter_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.data, [dict(resp_obj) for resp_obj in response.data])
