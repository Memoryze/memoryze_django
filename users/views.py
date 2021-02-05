from django.db import models
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from .models import User
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import UserRegistrationSerializer, UserSerializer, MyTokenObtainPairSerializer

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
        
        return Response(user_data, status=status.HTTP_201_CREATED)
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