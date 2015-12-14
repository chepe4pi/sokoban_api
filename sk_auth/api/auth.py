from django.contrib.auth.models import User
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny
from ..serializers.users import RegisterSerializer, LoginSerializer, BaseAuthSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, logout


class AuthAPIView(GenericAPIView):
    """
    A view for login logout user
    """

    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            login(request, user)
            return Response(BaseAuthSerializer(instance=user).data)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        logout(request)
        return Response(data={}, status=status.HTTP_204_NO_CONTENT)


class RegisterView(CreateModelMixin, GenericViewSet):
    """
    A View for registration Users.
    """
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()
