from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers.auth import UserLoginSerializer
from ..serializers.user import UserSerializer
from ..models import AuthToken


User = get_user_model()


class LoginAPIView(GenericAPIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = authenticate(username=serializer.data.get('username'), password=serializer.data.get('password'))

            if user:
                token = AuthToken(user=user)
                token.save()

                return Response(
                    UserSerializer(instance=user).data,
                    headers={
                        'X-Auth-Token': token.token
                    }
                )

            else:
                return Response(
                    {'errors': {'non_field_errors': 'User not found'}},
                    status=status.HTTP_401_UNAUTHORIZED
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

login_api_view = LoginAPIView.as_view()


class LogoutAPIView(APIView):
    def delete(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
        except AuthToken.DoesNotExist:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)

logout_api_view = LogoutAPIView.as_view()
