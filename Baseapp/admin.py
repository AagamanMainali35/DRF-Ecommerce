from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile as CustomUser

admin.site.register(CustomUser)