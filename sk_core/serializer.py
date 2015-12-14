from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username',
                                      help_text='username of owner of this object')
