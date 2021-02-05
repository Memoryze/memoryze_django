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
from .serializers import UserRegistrationSerializer, UserSerializer, MyTokenObtainPairSerializer, EmailVerificationSerializer
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse 
import jwt
from django.conf import settings
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
        user=User.objects.get(email=user_data['email'])

        token=RefreshToken.for_user(user).access_token

        current_site = get_current_site(request)
        relativeLink = reverse('verify-email')
        
        absurl = f'http://{current_site}{relativeLink}?token={str(token)}'
        email_body=f'Hi {user.name}, thanks for signing up to Memoryze, use the link below to verify your account \n {absurl}'
        data = {'email_body': email_body, 'email_subject': 'Verify Your Email', 'to_email': user.email}
        Util.send_email(data)
        
        return Response(user_data, status=status.HTTP_201_CREATED)

@permission_classes((AllowAny, ))
class VerifyEmail(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer
    def get(self):
        token = request.GET.get('token')
        try: 
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activated Expired'}, status=status.HTTP_400_BAD_REQUEST)
        # if the link has been tampered with and cant be decoded
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid Token, Request new one'}, status=status.HTTP_400_BAD_REQUEST)



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