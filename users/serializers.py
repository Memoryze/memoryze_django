from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.settings import api_settings
from memoryze.serializers import AudioSerializer, PlaylistSerializer

class UserSerializer(serializers.HyperlinkedModelSerializer):
    audios = AudioSerializer(many=True, read_only=True)
    playlists = PlaylistSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'name','email', 'password', 'audios', 'playlists','profile_image', 'is_learner', 'is_tutor', 'created_at', 'updated_at')
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    audios = AudioSerializer(many=True, read_only=True)
    playlists = PlaylistSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'name','email', 'password', 'audios', 'playlists', 'is_learner', 'is_tutor', 'created_at', 'updated_at')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance