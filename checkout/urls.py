from django.conf.urls import url
from django.urls import path
from .views import view_cart,add_to_cart,edit_cart,checkout,delete_from_cart,clear_cart,coupon_check
urlpatterns = [
    path('cart/', view_cart, name="view_cart"),
    path('cart/add/<int:product_number>/<int:quantity>/', add_to_cart, name="add_to_cart"),
    path('cart/edit/', edit_cart, name="edit_cart"),
    path('cart/delete/<int:product_number>/', delete_from_cart, name="delete_from_cart"),
    path('cart/clear/', clear_cart, name="clear_cart"),
    path('checkout/', checkout, name="checkout"),
    path('coupon/', coupon_check, name="coupon_check"),
]
