from django.test.testcases import TestCase

from sk_core.models import STATE_DELETED, STATE_PRIVATE
from sk_map.tests.factories import MapFactory


class MapFsmTestCase(TestCase):
    def test_deny_change_deleted(self):
        self.map_obj = MapFactory(state=STATE_DELETED)
        self.map_obj.state = STATE_PRIVATE
        self.map_obj.save()

    def test_change_to_deleted(self):
        self.map_obj = MapFactory(state=STATE_PRIVATE)
        self.map_obj.state = STATE_DELETED
        self.map_obj.save()
