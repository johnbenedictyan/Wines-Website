from django.shortcuts import render

# Create your views here.
def shop(request):
    all_products = None
    return render(
        request,
        "shop.html",
        {
            "all_products":all_products
        })
        
def individual_product(request):
    single_product = None
    return render(
        request,
        "shop-single.html",
        {
            "single_product":single_product
        })