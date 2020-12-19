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
    path('recordings/', views.AudioView.as_view(), name='audio_list'),
    path(f'recordings/<int:pk>/{api_key}', views.AudioDetail.as_view(), name='audio_detail'),
    path('playlists/', views.PlaylistView.as_view(), name='playlist_list'),
    path(f'playlists/<int:pk>/{api_key}', views.PlaylistDetail.as_view(), name='playlist_detail'),
]