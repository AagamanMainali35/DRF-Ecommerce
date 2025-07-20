from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile as CustomUser , Product,Cart,Cart_item

admin.site.register(CustomUser)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Cart_item)