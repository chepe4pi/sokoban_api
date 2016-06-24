from decimal import Decimal

from rest_framework.test import APITestCase

from sk_auth.tests.factories import UserFactory
from sk_game.tests.factories import UserMapMembershipFactory
from ..serializers.map import MapSerializer, BoxSerializer, WallSerializer, PointSerializer, MenSerializer
from .factories import MapFactory, BoxFactory, WallFactory, PointFactory, MenFactory


class MapTestCase(APITestCase):

    fixtures = ['test_admin_user.json', 'base_skins.json']

    def setUp(self):
        self.obj = MapFactory()
        self.expected = {
            'id': self.obj.id,
            'title': self.obj.title,
            'owner': self.obj.owner.username,
            'public': self.obj.public,
            'rating': None
        }

    def test_serializer(self):
        self.data = MapSerializer(self.obj).data
        self.assertEqual(self.data, self.expected)

    def test_with_rating(self):
        self.obj.public = True
        self.obj.rating = 11
        other_man = UserFactory(username='other_man')
        other_man2 = UserFactory(username='other_man2')
        UserMapMembershipFactory(map=self.obj, owner=self.obj.owner, done=True, rate=3)
        UserMapMembershipFactory(map=self.obj, owner=other_man, done=True, rate=4)
        UserMapMembershipFactory(map=self.obj, owner=other_man2, done=True, rate=4)
        self.data = MapSerializer(self.obj).data
        self.expected['rating'] = Decimal('3.67')
        self.expected['public'] = True
        self.assertEqual(self.data, self.expected)


class MapObjSerializerTestCaseMixin(object):

    def setUp(self):
        self.expected = {
            'id': self.obj.id,
            'x': self.obj.x,
            'y': self.obj.y,
            'map': self.obj.map.id,
        }

    def test_serializer(self):
        self.assertEqual(self.data, self.expected)


class WallTestCase(MapObjSerializerTestCaseMixin, APITestCase):

    def setUp(self):
        self.obj = WallFactory()
        super(WallTestCase, self).setUp()
        self.data = WallSerializer(self.obj).data


class PointTestCase(MapObjSerializerTestCaseMixin, APITestCase):

    def setUp(self):
        self.obj = PointFactory()
        super(PointTestCase, self).setUp()
        self.data = PointSerializer(self.obj).data


class BoxTestCase(MapObjSerializerTestCaseMixin, APITestCase):

    def setUp(self):
        self.obj = BoxFactory()
        super(BoxTestCase, self).setUp()
        self.data = BoxSerializer(self.obj).data


class MenTestCase(MapObjSerializerTestCaseMixin, APITestCase):

    def setUp(self):
        self.obj = MenFactory()
        super(MenTestCase, self).setUp()
        self.data = MenSerializer(self.obj).data
