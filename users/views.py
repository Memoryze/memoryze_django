from django.http import HttpResponseRedirect
from .models import User
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import UserRegistrationSerializer, UserSerializer

# Create your views here.
@permission_classes((AllowAny, ))
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
@permission_classes((AllowAny, ))
class UserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
@permission_classes((AllowAny, ))
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer