from rest_framework.test import APITestCase
from ..serializers.map import MapSerializer, BoxSerializer, WallSerializer, PointSerializer, MenSerializer
from .factories import MapFactory, BoxFactory, WallFactory, PointFactory, MenFactory


class MapTestCase(APITestCase):

    fixtures = ['test_admin_user.json', 'base_skins.json']

    def setUp(self):
        self.obj = MapFactory()
        self.data = MapSerializer(self.obj).data
        self.expected = {
            'id': self.obj.id,
            'title': self.obj.title,
            'owner': self.obj.owner.username,
            'public': self.obj.public
        }

    def test_serializer(self):
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
