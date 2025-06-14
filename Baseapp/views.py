from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from .utility import generate_profile_id, checkpass , check_field
from django.urls import reverse
from django.db.transaction import atomic
from django.db.models import Q
import re
@api_view(['POST'])
def signup(requests):
    email = requests.data.get('email')
    password = requests.data.get('password')
    first_name = requests.data.get('first_name')
    last_name = requests.data.get('last_name')
    gender = requests.data.get('gender')
    missing_fields = ['email', 'password', 'first_name', 'last_name']
    result=check_field(requests, *missing_fields)
    if result is not None:
        return result
    if checkpass(password) is not None:
        return Response({"error": checkpass(password),"status_code": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(Q(email=email) | Q(username=email)).exists():
        return Response({"error": "Email or Username already exists."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        profile_id=generate_profile_id()
        user_model=User.objects.create(email=email, username=email, first_name=first_name, last_name=last_name)
        user_model.set_password(password)
        user_model.save()
        Profile.objects.create(user=user_model,profile_id=profile_id,gender=gender)
        login_url= f'http://127.0.0.1:8000{reverse("signin")}'
        return Response({"message": f"Signup completed for {email}","login_url": login_url})
def signin():
    pass
