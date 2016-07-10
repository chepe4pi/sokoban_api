from sk_auth.tests.factories import UserFactory
from rest_framework import status

from sk_core.models import STATE_PUBLIC


class AuthorizeForTestsMixin(object):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

    def test_deny_post_unauthorized(self):
        self.client.logout()
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BaseTestMixin(AuthorizeForTestsMixin):
    def setUp(self):
        super(BaseTestMixin, self).setUp()
        self.obj_url = self.url + str(self.obj.id) + '/'


class BasePermissionTestMixin(BaseTestMixin):
    def setUp(self):
        super(BasePermissionTestMixin, self).setUp()
        self.wrong_user = UserFactory(username='mr_wrong')


class TestCasePermissionPublicMixin(BasePermissionTestMixin):
    def test_allow_get_unauthorized_if_public(self):
        setattr(self.obj, 'state', STATE_PUBLIC)
        self.obj.save()
        self.client.logout()
        response = self.client.get(self.obj_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_allow_get_public_obj(self):
        self.client.force_authenticate(user=self.wrong_user)
        self.obj.public = STATE_PUBLIC
        self.obj.save()
        response = self.client.get(self.obj_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_deny_change_public_obj(self):
        self.client.force_authenticate(user=self.wrong_user)
        self.obj.public = STATE_PUBLIC
        self.obj.save()
        response = self.client.delete(self.obj_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.put(self.obj_url, self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestCasePermissionsMixin(BasePermissionTestMixin):
    def test_deny_get_some_obj(self):
        self.client.force_authenticate(user=self.wrong_user)
        response = self.client.get(self.obj_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_allow_get_own_obj(self):
        self.response = self.client.get(self.obj_url)
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_allow_remove_own_obj(self):
        response = self.client.delete(self.obj_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
