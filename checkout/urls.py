from django.conf.urls import url
from django.urls import path
from .views import view_cart,checkout
urlpatterns = [
    path('', view_cart, name="view_cart"),
    path('', checkout, name="checkout"),
]
