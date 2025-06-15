from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile as CustomUser , Product

admin.site.register(CustomUser)
admin.site.register(Product)