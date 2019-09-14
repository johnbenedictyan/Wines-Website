from django.conf.urls import url
from django.urls import path
from .views import shop,individual_product

urlpatterns = [
    path('', shop, name="shop"),
    path('product/<int:product_number>/', individual_product, name="shop")
]
