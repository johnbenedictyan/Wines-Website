from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomerDetailForm

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
            
def view_cart(request):
    class cart:
        def __init__(self):
            self.cart_items = []
        
        def add_item_to_cart(self,cart_item):
            cart_item.total_price = cart_item.price * cart_item.quantity
            self.cart_items.append(cart_item)
        
        def edit_item_quantity(self,product_number,new_quantity):
            found = False
            for idx,item in enumerate(self.cart_items):
                if item.product_number == product_number:
                    item.quantity = new_quantity
                    found = True
                    found_product_number = item.product_number
                    
            if found is False:
                return None
            else:
                return found_product_number
        
        def delete_item_quantity(self,product_number):
            found = False
            for idx,item in enumerate(self.cart_items):
                if item.product_number == product_number:
                    found = True
                    found_product_position = idx
                    
            if found is False:
                return None
            else:
                self.cart_items.pop(found_product_position)
                return True
    
    user_cart = request.session.get('user_cart', cart())
    print(user_cart)
    return render(
        request,
        "cart.html",
        {
            "user_cart":user_cart
        })
        
def add_to_cart(request,product_number):
    return None

def change_cart(request,product_number,new_number):
    return None
    