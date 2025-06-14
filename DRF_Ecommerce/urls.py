from django.contrib import admin
from django.urls import path
from Baseapp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.signin, name='signin'),
    path('signup/',views.signup, name='signup'),
]
