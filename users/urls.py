from django.urls import path
from .views import UserView, UserDetail, UserCreate, MyTokenObtainPairView, ResendCodeView, MiddleManLoginView, ForgotPasswordView, VerifyUserView
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
    path(f'create_user', UserCreate.as_view()),
    path(f'users', UserView.as_view()),
    path(f'users/<int:pk>', UserDetail.as_view()),
    path(f'token', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(f'token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path(f'resend_code', ResendCodeView.as_view(), name='resend_code'),
    path('login_middle_man', MiddleManLoginView.as_view(), name='login_middle_man'),
    path('forgot_password', ForgotPasswordView.as_view(), name='forgot_password'),
    path('verify_user', VerifyUserView.as_view(), name='verify_user'),
    ]