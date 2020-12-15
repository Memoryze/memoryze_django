from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from users.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    audios = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('id', 'name','email', 'password', 'audios')