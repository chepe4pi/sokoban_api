from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
