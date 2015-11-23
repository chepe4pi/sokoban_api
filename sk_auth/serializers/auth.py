from rest_framework import serializers


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        fields = ('username', 'password')

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass