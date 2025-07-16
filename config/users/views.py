from django.shortcuts import render
from rest_framework import generics
from .serializers import UserSignupSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
# Create your views here.

class UserSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer
    permission_classes = [AllowAny]