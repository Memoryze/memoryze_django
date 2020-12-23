from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
from rest_framework_simplejwt.settings import api_settings
from memoryze.serializers import AudioSerializer, PlaylistSerializer, ActivitySerializer

class UserSerializer(serializers.HyperlinkedModelSerializer):
    audios = AudioSerializer(many=True, read_only=True)
    playlists = PlaylistSerializer(many=True, read_only=True)
    activity = ActivitySerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'name','email', 'password', 'audios', 'playlists','profile_image', 'is_learner', 'is_tutor', 'activity', 'created_at', 'updated_at')
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

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)
        # Custom data you want to include
        data.update({'name': self.user.name})
        data.update({'id': self.user.id})
        data.update({'audios': self.user.audios})
        data.update({'playlists': self.user.playlists})
        data.update({'is_learner': self.user.is_learner})
        data.update({'is_tutor': self.user.is_tutor})
        data.update({'created_at': self.user.created_at})
        # and everything else you want to send in the response
        return data