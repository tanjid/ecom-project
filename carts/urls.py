from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('remove_cart/<int:cartitem_id>/', views.remove_qty, name='remove_qty'),
    path('add_cart_qty/<int:cartitem_id>/', views.add_cart_qty, name='add_cart_qty'),
    path('remove_cart_qty/<int:cartitem_id>/', views.remove_cart_qty, name='remove_cart_qty'),
]
