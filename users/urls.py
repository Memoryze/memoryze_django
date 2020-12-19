from django.urls import path
from .views import UserCreate, UserView, UserDetail
import os
import environ
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
api_key = env('ACCESS_KEY')

urlpatterns = [
    path('create_user/', UserCreate.as_view()),
    path(f'users/{api_key}', UserView.as_view()),
    path(f'users/<int:pk>/{api_key}', UserDetail.as_view()) ]