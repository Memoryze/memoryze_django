from rest_framework import serializers
from .models import Audio, Playlist, Activity
from users.models import User

class AudioSerializer(serializers.HyperlinkedModelSerializer):
    tutor_id = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        source = 'tutor'
    )
    class Meta:
        model = Audio
        fields = ('id', 'title', 'recording', 'tutor_id', 'likes','image', 'categories' )

class PlaylistSerializer(serializers.HyperlinkedModelSerializer):
    owner_id = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        source = 'owner',
    )
    class Meta:
        model = Playlist
        fields = ('id', 'name', 'owner_id', 'audios' )

class ActivitySerializer(serializers.HyperlinkedModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        source = 'user',
    )
    class Meta:
        model = Activity
        fields = ('id', 'played_recordings', 'recently_played', 'user_id' )