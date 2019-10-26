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
        self.cart_total = 0
    
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
    
    def delete_item_from_cart(self,product_number):
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
    
    def calculate_cart_total(self):
        cart_total = 0
        for i in self.cart_items:
            cart_total+=i["total_price"]
        self.cart_total = cart_total
        
    def export_data(self):
        self.calculate_cart_total()
        # This is the export variable that stores all of the relevant
        # information that the cart page would need.
        export_dict = {
            "cart_items":self.cart_items,
            "cart_total":self.cart_total
        }
        return export_dict
        
    def import_data(self,cart_data):
        self.cart_items = cart_data["cart_items"]
        self.cart_total = cart_data["cart_total"]
        

def view_cart(request):
    user_cart = request.session.get('user_cart', cart().export_data())
    return render(
        request,
        "cart.html",
        {
            "user_cart":user_cart
        })
        
def add_to_cart(request,product_number,quantity):
    # This checks to see if there is cart data stored in the session.
    # It first creates a new cart object.
    # If there is, the user cart will be formed using the import data function
    # of the cart.
    
    user_cart = cart()
    
    if request.session.get('user_cart'):
        user_cart.import_data(
            request.session.get('user_cart')
            )
    
    # This checks the selected product exists within the product table inside
    # of the database.
    # If it does, then an auxiliary cart item will be created to be consumed
    # by the add_items_to_cart function of the cart object.
    # If the product does not exist, an error will be raised.
    try:
        selected_product = Product.objects.get(pk=product_number)
    except Product.DoesNotExist:
        messages.error(
                request,
                "This product does not exist."
                )
    else:
        img_url = selected_product.product_picture.cdn_url
        product_name = selected_product.name
        price = selected_product.price
        
        # The temporary cart_item variable stores all of the information which
        # will be displayed in the cart page.
        
        cart_item = {
                    "img_url":img_url,
                    "product_number":product_number,
                    "product_name":product_name,
                    "price":price,
                    "quantity":quantity
                }
    
    if user_cart.add_item_to_cart(cart_item):
        messages.success(
                request,
                "Item added to cart."
                )
        request.session['user_cart']=user_cart.export_data()
    else:
        messages.error(
                request,
                "We are unable to add this item to your cart."
                )
    return redirect(view_cart)

def edit_cart(request,product_number,new_quantity):
    # This is an identical check to the one above inside of the add items
    # to cart function
    
    if request.session.get('user_cart'):
        cart_data = request.session.get('user_cart')
        user_cart = cart()
        user_cart.import_data(cart_data)
        
        if user_cart.edit_item_quantity(product_number,new_quantity):
             messages.success(
                 request,
                 "Item quantity has been edited."
                 )
             request.session['user_cart']=user_cart.export_data()
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
    
def delete_from_cart(request,product_number):
    if request.session.get('user_cart'):
        cart_data = request.session.get('user_cart')
        user_cart = cart()
        user_cart.import_data(cart_data)
        
        if user_cart.delete_item_from_cart(product_number):
            messages.success(
                 request,
                 "Item has been successfully deleted."
                 )
            request.session['user_cart']=user_cart.export_data()
        else:
            messages.error(
                request,
                "We are unable to delete this item from your cart."
                )
    else:
        messages.error(
            request,
            "This cart does not exist."
            )
    return redirect(view_cart)