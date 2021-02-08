from django.urls import path
from .views import UserView, UserDetail, UserCreate, MyTokenObtainPairView, ResendCode
from rest_framework_simplejwt.views import TokenRefreshView
# help from https://medium.com/django-rest/django-rest-framework-jwt-authentication-94bee36f2af8
import os
import environ
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
api_key = env('ACCESS_KEY')

urlpatterns = [
    path(f'create_user/', UserCreate.as_view()),
    path(f'users/{api_key}', UserView.as_view()),
    path(f'users/<int:pk>/{api_key}', UserDetail.as_view()),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('resend_code/', ResendCode.as_view(), name='resend_code'),
    ]