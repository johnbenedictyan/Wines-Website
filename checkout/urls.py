from django.conf.urls import url
from django.urls import path
from .views import view_cart,add_to_cart,edit_cart,checkout,delete_from_cart
urlpatterns = [
    path('cart/', view_cart, name="view_cart"),
    path('cart/add/<int:product_number>/<int:quantity>/', add_to_cart, name="add_to_cart"),
    path('cart/edit/<int:product_number>/<int:new_quantity>/', edit_cart, name="edit_cart"),
    path('cart/delete/<int:product_number>/', delete_from_cart, name="delete_from_cart"),
    path('checkout/', checkout, name="checkout"),
]
