from django.conf.urls import url
from django.urls import path
from .views import cart,checkout
urlpatterns = [
    path('', cart, name="cart"),
    path('', checkout, name="checkout"),
]
