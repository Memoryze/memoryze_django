from django.db import models
from users.models import User
from django.contrib.postgres.fields import ArrayField

# Create your models here.
# class Category(models.Model):
#     category = models.CharField(max_length=30)

class Playlist(models.Model):
    name = models.CharField(max_length=250)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists', related_query_name='playlist')
    descriptive_image = models.ImageField(blank=True, null=True, upload_to="images/%Y/%m/%D/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.name}'

class Audio(models.Model):
    title = models.CharField(max_length=250)
    recording = models.FileField(blank=True, null=True, upload_to='recordings/%Y/%m/%D/')
    likes = models.IntegerField(default=0)
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audios', related_query_name='audio')
    course = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='audios', related_query_name='audio', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = ArrayField(models.CharField(max_length=30), default=list)
    image = models.ImageField(blank=True, null=True, upload_to="images/%Y/%m/%D/")

    def __str__(self):
        return f'{self.title}'


class Activity(models.Model):
    played_recordings = ArrayField(models.JSONField(null=True), default=list)
    # the array is to take objects that are in this format:
    # {
    #     data: {recording object}
    #     last_played: <current time>,
    #     times_played: <incremented each time the recording was played>
    # }
    recently_played = ArrayField(models.JSONField(null=True), default=list) #recording object

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities', related_query_name='activity')