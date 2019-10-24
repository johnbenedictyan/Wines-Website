from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProductForm
from .models import Product

# Create your views here.
def shop(request):
    all_products = None
    return render(
        request,
        "shop.html",
        {
            "all_products":all_products
        })

def wine_collection(request):
    best_sellers = None
    return render (
        request,
        "wine-collection.html",
        {
            "best_sellers":best_sellers
        })
        
def individual_product(request):
    single_product = None
    return render(
        request,
        "shop-single.html",
        {
            "single_product":single_product
        })

@login_required
def inventory(request):
    current_user = request.user
    all_products = Product.objects.filter(seller_id=current_user.id)
    number_of_products_found = all_products.count()
    print(all_products)
    return render(
        request,
        "inventory.html",
        {
            "all_products":all_products,
            "number_of_products_found":number_of_products_found
        })

@login_required
def product_update(request):
    selected_product = None
    if request.method == "GET":
        product_form = ProductForm(instance=selected_product)
        return render(
            request,
            "product-form.html",
            {
                "product_form":product_form
            })
    else:
        dirty_product_form = ProductForm(
            request.POST,
            instance=selected_product
            )
        if dirty_product_form.is_valid():
            dirty_product_form.save()
            return redirect("Inventory")
        else:
            messages.error(
                request,
                "We were unable to update the details of thie product."
                )
            return render(
                request,
                "product-form.html",
                {
                    "product_form":dirty_product_form
                })
                

def product_creator(request):
    if request.method == "GET":
        product_form = ProductForm()
        # This line sets the initial value of the seller id to the current
        # user's id
        product_form.fields["seller_id"].initial = request.user.id
        return render(
            request,
            "product-form.html",
            {
                "product_form":product_form
            })
    else:
        dirty_product_form = ProductForm(request.POST)
        if dirty_product_form.is_valid():
            dirty_product_form.save()
            return redirect(inventory)
        else:
            messages.error(
                request,
                "We were unable to create a listing for this product."
                )
            return render(
                request,
                "product-form.html",
                {
                    "product_form":dirty_product_form
                })
            
def delete_product(request):
    selected_product = None
    return redirect()