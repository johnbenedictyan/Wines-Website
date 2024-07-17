from django.conf.urls import url
from django.urls import path
from .views import shop, individual_product, product_creator, product_update, delete_product, inventory, wine_collection

urlpatterns = [
    path(
        '',
        shop,
        name="shop"),
    path(
        'collection/',
        wine_collection,
        name="wine_collection"),
    path(
        'products/<int:product_number>/',
        individual_product,
        name="individual_product"),
    path(
        'products/update/<int:product_number>/',
        product_update,
        name="product_update"),
    path(
        'products/create/',
        product_creator,
        name="product_creator"),
    path(
        'products/delete/<int:product_number>/',
        delete_product,
        name="delete_product"),
    path(
        'products/inventory/',
        inventory,
        name="inventory"),
]
