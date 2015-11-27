from django.contrib.auth.models import User
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny
from ..serializers.users import RegisterSerializer


class RegisterView(CreateModelMixin, GenericViewSet):
    """
    A View for registration Users.
    """
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()

