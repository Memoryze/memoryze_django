from django.db import models
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from .models import User
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions, status, views, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, UserSerializer, MyTokenObtainPairSerializer, ResendCodeSerializer
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse 
import jwt
import requests
from django.conf import settings
from django.template import Context
from django.template.loader import render_to_string
# Create your views here.
@permission_classes((AllowAny, ))
class UserCreate(generics.GenericAPIView):
    # queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        if serializer.is_valid():
            serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])

        code = user.code
        html_content = render_to_string('users/sign_up_verification_code.html', {'user':user.name, 'code': code})

        data = {'email_subject': 'Email Verification Code', 'to_email': user.email, 'html_content':html_content}
        Util.send_email(data)
        
        return Response(user_data, status=status.HTTP_201_CREATED)
        
@permission_classes((AllowAny, ))
class ResendCode(generics.GenericAPIView):
    serializer_class = ResendCodeSerializer
    def post(self, request):
        data = {'user_id' : request.data['user_id'], 'code' : request.data['code']}
        user = User.objects.get(id=data['user_id'])
        user.code = data['code']
        user.save()        
        code = user.code

        html_content = render_to_string('users/new_code.html', {'user':user.name, 'code': code}) 
        email_data = {'email_subject': 'New Email Verification Code', 'to_email': user.email, 'html_content':html_content}
        Util.send_email(email_data)
        return Response(data, status=status.HTTP_200_OK)
        
class UserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
@permission_classes((AllowAny, ))
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    @receiver(models.signals.pre_delete, sender=User)
    def remove_file_from_s3(sender, instance, using, **kwargs):
       instance.profile_image.delete(save=False)

@permission_classes((AllowAny, ))
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
