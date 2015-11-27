from django.contrib.auth.models import User
from rest_framework import serializers


class BaseAuthSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(allow_null=True) # TODO choice one of options

    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}


class RegisterSerializer(BaseAuthSerializer):

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'], email=validated_data['email'],\
                                        password=validated_data['password'])
        return user
