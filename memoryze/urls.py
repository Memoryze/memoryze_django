from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
import os
import environ
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
api_key = env('ACCESS_KEY')

urlpatterns = [
    path('recordings', views.AudioView.as_view(), name='audio_list'),
    path(f'recordings/<int:pk>', views.AudioDetail.as_view(), name='audio_detail'),
    path('playlists/', views.PlaylistView.as_view(), name='playlist_list'),
    path(f'playlists/<int:pk>', views.PlaylistDetail.as_view(), name='playlist_detail'),
    path('activities/', views.ActivityView.as_view(), name='activity_list'),
    path(f'activities/<int:pk>', views.ActivityDetail.as_view(), name='activity_detail'),
]