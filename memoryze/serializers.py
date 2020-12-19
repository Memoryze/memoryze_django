from rest_framework import serializers
from .models import Audio, Playlist
from users.models import User

class AudioSerializer(serializers.HyperlinkedModelSerializer):
    tutor_id = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        source = 'user'
    )
    tutor = serializers.StringRelatedField(
        queryset = User.objects.all(),
        source = 'user'
    )
    class Meta:
        model = Audio
        fields = ('id', 'title', 'recording', 'tutor_id', 'tutor', 'likes' )

class PlaylistSerializer(serializers.HyperlinkedModelSerializer):
    owner_id = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        source = 'user'
    )
    owner = serializers.StringRelatedField(
        queryset = User.objects.all(),
        source = 'user'
    )
    class Meta:
        model = Audio
        fields = ('id', 'name', 'owner_id', 'owner', 'audio' )