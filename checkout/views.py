from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomerDetailForm
from products.models import Product

# Create your views here.
def checkout(request):
    selected_order = None
    custom_detail_form = CustomerDetailForm()
    if request.method == "GET":
        return render(
            request,
            "checkout.html",
            {
                "selected_order":selected_order
            })
    else:
        dirty_custom_detail_form = CustomerDetailForm(request.POST)
        if dirty_custom_detail_form.is_valid():
            dirty_custom_detail_form.save(commit=False)
            return redirect(None)
        else:
            messages.error(
                request,
                "We are unable to accept your details."
                )
            
# Cart Class used by all of the cart view functions
class cart:
    def __init__(self):
        self.cart_items = []
    
    def add_item_to_cart(self,cart_item):
        cart_item['total_price'] = cart_item['price'] * cart_item['quantity']
        self.cart_items.append(cart_item)
        return True
    
    def edit_item_quantity(self,product_number,new_quantity):
        found = False
        for idx,item in enumerate(self.cart_items):
            if item['product_number'] == product_number:
                item['quantity'] = new_quantity
                found = True
                found_product_number = item['product_number']
                
        if found is False:
            return None
        else:
            return found_product_number
    
    def delete_item_quantity(self,product_number):
        found = False
        for idx,item in enumerate(self.cart_items):
            if item['product_number'] == product_number:
                found = True
                found_product_position = idx
                
        if found is False:
            return None
        else:
            self.cart_items.pop(found_product_position)
            return True
    
    
def view_cart(request):
    user_cart = request.session.get('user_cart', cart())
    print(user_cart)
    return render(
        request,
        "cart.html",
        {
            "user_cart":user_cart
        })
        
def add_to_cart(request,product_number,quantity):
    try:
        selected_product = Product.objects.get(pk=product_number)
    except Product.DoesNotExist:
        messages.error(
                request,
                "This product does not exist."
                )
    else:
        cart_item = {
                    "img_url":selected_product["product_picture"]["cdn_url"],
                    "product_number":product_number,
                    "price":selected_product["price"],
                    "quantity":quantity
                }
                
    user_cart = request.session.get('user_cart', cart())
    if user_cart.add_item_to_cart(cart_item):
        messages.success(
                request,
                "Item added to cart."
                )
    else:
        messages.error(
                request,
                "We are unable to add this item to your cart."
                )
    return redirect(view_cart)

def edit_cart(request,product_number,new_quantity):
    user_cart = request.session.get('user_cart')
    if user_cart:
        if user_cart.edit_item_quantity(product_number,new_quantity):
             messages.success(
                 request,
                 "Item quantity has been edited."
                 )
        else:
            messages.error(
                request,
                "We are unable to edit this item in your cart."
                )
    else:
        messages.error(
            request,
            "This cart does not exist."
            )
    
    return redirect(view_cart)
    
def delete_cart(request):
    request.session['user_cart'] = cart()
    messages.success(
        request,
        "Cart has been successfully cleared."
        )
    return redirect(view_cart)