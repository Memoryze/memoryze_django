from django.db import models
from users.models import User
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Audio(models.Model):
    title = models.CharField(max_length=250)
    recording = models.FileField(blank=True, null=True, upload_to='recordings/%Y/%m/%D/')
    likes = models.IntegerField(default=0)
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audios', related_query_name='audio')

    def __str__(self):
        return f'{self.title}'
class Playlist(models.Model):
    name = models.CharField(max_length=250)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists', related_query_name='playlist')
    audio = ArrayField(
            models.CharField(blank=True),
        ),
    def __str__(self):
        return f'{self.name}'
