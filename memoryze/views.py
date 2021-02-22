from django.db import models
from django.dispatch import receiver
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from .models import Audio, Playlist, Activity
from .serializers import AudioSerializer, PlaylistSerializer, ActivitySerializer

# Create your views here.
@permission_classes((AllowAny, ))
class AudioView(generics.ListCreateAPIView):
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer

@permission_classes((AllowAny, ))
class AudioDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer
    @receiver(models.signals.pre_delete, sender=Audio)
    def remove_file_from_s3(sender, instance, using, **kwargs):
       instance.recording.delete(save=False)
       instance.image.delete(save=False)

@permission_classes((AllowAny, ))
class PlaylistView(generics.ListCreateAPIView):
     queryset = Playlist.objects.all()
     serializer_class = PlaylistSerializer
     
@permission_classes((AllowAny, ))
class PlaylistDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

@permission_classes((AllowAny, ))
class ActivityView(generics.ListCreateAPIView):
     queryset = Activity.objects.all()
     serializer_class = ActivitySerializer
     
@permission_classes((AllowAny, ))
class ActivityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer 