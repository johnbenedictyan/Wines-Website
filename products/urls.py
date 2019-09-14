from django.conf.urls import url
from django.urls import path
from .views import shop,individual_product,product_creator,product_update

urlpatterns = [
    path('', shop, name="shop"),
    path('product/<int:product_number>/', individual_product, name="individual_product"),
    path('product/update/<int:product_number>/', product_update, name="product_update"),
    path('product/create/', product_creator, name="product_creator")
]
