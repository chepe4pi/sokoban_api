from rest_framework.test import APITestCase
from ..serializers.users import BaseAuthSerializer
from .factories import UserFactory


class MapSerializerTestCase(APITestCase):

    def setUp(self):
        self.obj = UserFactory()
        self.data = BaseAuthSerializer(self.obj).data
        self.expected = {
            'username': self.obj.username,
            'email': self.obj.email,
        }

    def test_serializer(self):
        self.assertEqual(self.data, self.expected)
