from django.db import models
from users.models import User

# Create your models here.

class Audio(models.Model):
    title = models.CharField(max_length=150)
    recording = models.FileField(blank=True, null=True, upload_to='recordings/%Y/%m/%D/')
    likes = models.IntegerField(default=0)
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audios', related_query_name='audio')
class Playlist(models.Model):
    name = models.CharField(max_length)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists', related_query_name='playlist')
    audio = ArrayField(
            models.CharField(blank=True),
        ),
