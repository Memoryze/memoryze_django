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
from .serializers import UserRegistrationSerializer, UserSerializer, MyTokenObtainPairSerializer, ResendCodeSerializer, MiddleManLoginSerializer, ForgotPasswordSerializer, VerifyUserSerializer
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse 
import jwt
import requests
import json
from django.conf import settings
from django.template import Context
from django.template.loader import render_to_string
import math, random
import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# Create your views here.
android = 'okhttp/3.12.1'
expo_ios_phone = 'Expo/2.18.4.1010552 CFNetwork/1209 Darwin/20.2.0'
expo_ios_simulator = 'Expo/2.17.4.101 CFNetwork/1220.1 Darwin/20.2.0'

def generate_code(possible_chars):
    code = '' 
    for i in range(6):
        index = math.floor(random.random() * len(possible_chars))
        code += possible_chars[index]
    return code

@permission_classes((AllowAny, ))
class UserCreate(generics.GenericAPIView):
    # queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    def post(self, request):
        user_agent = request.META['HTTP_USER_AGENT']

        if (user_agent == android) or (user_agent == expo_ios_phone) or (user_agent == expo_ios_simulator) or ('AppleWebKit/537.36' in user_agent): 
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
            else:
                try:
                    user = User.objects.get(name=request.data['name'])
                    return Response({'error': 'Username taken'}, status=status.HTTP_200_OK)
                except User.DoesNotExist:
                    return Response({'error': 'User with email already exists'}, status=status.HTTP_200_OK)       
        else:
            return Response({'error': "Access Denied, oops!"}, status=status.HTTP_423_LOCKED)


@permission_classes((AllowAny, ))
class ResendCodeView(generics.GenericAPIView):
    serializer_class = ResendCodeSerializer
    def post(self, request):
        user_agent = request.META['HTTP_USER_AGENT']

        if (user_agent == android) or (user_agent == expo_ios_phone) or (user_agent == expo_ios_simulator) or ('AppleWebKit/537.36' in user_agent):
            user = User.objects.get(email=request.data['email'])
            # generate the code
            code = generate_code('0123456789')

            user.code = code
            user.save()        
            data = {'email' : request.data['email'], 'code' : code}

            #create and send email html content
            html_content = render_to_string('users/new_code.html', {'user':user.name, 'code': user.code}) 
            email_data = {'email_subject': 'New Email Verification Code', 'to_email': user.email, 'html_content':html_content}
            Util.send_email(email_data)
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'error': "Access Denied, oops!"}, status=status.HTTP_400_BAD_REQUEST)

@permission_classes((AllowAny, ))
class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer
    def put(self, request):
        user_agent = request.META['HTTP_USER_AGENT']

        if (user_agent == android) or (user_agent == expo_ios_phone) or (user_agent == expo_ios_simulator) or ('AppleWebKit/537.36' in user_agent):
          
            # generate the code
            possible_chars = '1234567890abcdefghijkmnlopqrstuvwxyzABCDEFGHIJKMNLOPQRSTUVWXYZ'
            password = generate_code(possible_chars)
            try:
                user = User.objects.get(email=request.data['email'])
                user.set_password(password)
                user.save()
                data = {'email' : request.data['email']}

                #create and send email html content
                html_content = render_to_string('users/forgot_password.html', {'user': user.name, 'password': password}) 
                email_data = {'email_subject': 'New Issued Password', 'to_email': user.email, 'html_content':html_content}
                Util.send_email(email_data)
                return Response(data, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'error': 'We couldn\'t find any Memoryze user with that email'}, status=status.HTTP_200_OK)       

            #create new password with code
            
        else:
            return Response({'error': "Access Denied, oops!"}, status=status.HTTP_400_BAD_REQUEST)

@permission_classes((AllowAny, ))
class VerifyUserView(generics.GenericAPIView):
    serializer_class = VerifyUserSerializer
    def put(self, request):
        user_agent = request.META['HTTP_USER_AGENT']
        
        if (user_agent == android) or (user_agent == expo_ios_phone) or (user_agent == expo_ios_simulator) or ('AppleWebKit/537.36' in user_agent):
          
            user = User.objects.get(email=request.data['email'])
            user.is_verified = True
            user.save()
            data = {'successful': 'successful'}
            return Response(data, status=status.HTTP_200_OK)
            
        else:
            return Response({'error': "Access Denied, oops!"}, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((AllowAny, ))       
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

@permission_classes((AllowAny, ))
class MiddleManLoginView(generics.GenericAPIView):
    serializer_class = MiddleManLoginSerializer
    def post(self, request):
        user_agent = request.META['HTTP_USER_AGENT']

        android = 'okhttp/3.12.1'
        expo_ios_phone = 'Expo/2.18.4.1010552 CFNetwork/1209 Darwin/20.2.0'
        expo_ios_simulator = 'Expo/2.17.4.101 CFNetwork/1220.1 Darwin/20.2.0'

        domain = env('DEVELOPMENT_DOMAIN') if env('MODE') == 'dev' else env('PRODUCTION_DOMAIN')
        api_key = env('ACCESS_KEY')
        url = f'{domain}/users/token/{api_key}'
        if (user_agent == android) or (user_agent == expo_ios_phone) or (user_agent == expo_ios_simulator) or ('AppleWebKit/537.36' in user_agent):
            data = {'email': request.data['email'], 'password':request.data['password']}
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, data=json.dumps(data), headers=headers)
            return  Response(response.json(), status=status.HTTP_200_OK)
        else:
            return Response({'error': "Access Denied, oops!"}, status=status.HTTP_400_BAD_REQUEST)