from django.contrib import admin
from django.urls import path
from Baseapp import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/',views.signup, name='signup'),
    path('login/',views.login,name="login"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('products/create_product/', views.create_product, name='create_product'),
    path('products/get_products/', views.get_products, name='get_products'),
    path('products/get_products/<int:product_id>/', views.get_productById, name='get_productById'),
    path('products/delete/<int:id>/',views.delete_Product,name='delete_product'),
    path('products/update/<int:id>/',views.update_product,name='UpdateProduct'),
    path('Order/create/',views.create_order,name='createOrder'),
    path('Order/all/',views.getallOrders),
    path('Order/<str:order_id>/',views.update_order,name='update_Order'),
    path('order/delete/<str:order_id>/',views.deleteOrder,name='deleteOrder'),
    path('checkout/',views.chekout,name='checkout'),
    path('khalti/callback/',views.verify,name='verify')
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

