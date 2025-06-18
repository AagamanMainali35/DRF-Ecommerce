from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile as CustomUser , Product,Order,Order_item

admin.site.register(CustomUser)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Order_item)