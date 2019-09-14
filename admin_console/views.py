from django.shortcuts import render
from products.models import Product
from checkout.models import Order

# Create your views here.
def admin_console(request):
    all_products_in_stock = None
    all_orders = None
    return render(
        request,
        "admin-console.html",
        {
            "all_products_in_stock":all_products_in_stock,
            "all_orders":all_orders
        })
