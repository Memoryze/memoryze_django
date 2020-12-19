from rest_framework import serializers
from .models import User
from memoryze.serializers import AudioSerializer, PlaylistSerializer

class UserSerializer(serializers.HyperlinkedModelSerializer):
    audios = AudioSerializer(many=True, read_only=True)
    playlists = PlaylistSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('id', 'name','email', 'password', 'audios', 'playlists')
