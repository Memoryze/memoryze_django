from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from .models import Audio, Playlist
from .serializers import AudioSerializer, PlaylistSerializer
# Create your views here.

class AudioView(generics.ListCreateAPIView):
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer\
        
class AudioDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer

class PlaylistView(generics.ListCreateAPIView):
     queryset = Playlist.objects.all()
     serializer_class = PlaylistSerializer
     
class PlaylistDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer 