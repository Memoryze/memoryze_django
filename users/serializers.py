from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
from rest_framework_simplejwt.settings import api_settings
from memoryze.serializers import AudioSerializer, PlaylistSerializer, ActivitySerializer

class UserSerializer(serializers.HyperlinkedModelSerializer):
    audios = AudioSerializer(many=True, read_only=True)
    playlists = PlaylistSerializer(many=True, read_only=True)
    activities = ActivitySerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'name','email', 'password', 'audios', 'playlists','profile_image', 'bio', 'code','is_verified','is_learner', 'is_tutor', 'created_at', 'updated_at', 'activities')
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    audios = AudioSerializer(many=True, read_only=True)
    playlists = PlaylistSerializer(many=True, read_only=True)
    activities = ActivitySerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('id', 'name','email', 'password', 'audios', 'playlists','profile_image', 'bio','code', 'is_verified','is_learner', 'is_tutor', 'created_at', 'updated_at','activities')

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
        data.update({'id': self.user.id})
        # and everything else you want to send in the response
        return data
class ResendCodeSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    class Meta:
        model = User
        fields = ['user_id']