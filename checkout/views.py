from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from .forms import CustomerDetailForm, PaymentForm
from products.models import Product
from .models import Coupon, Order, Order_Product_Intermediary
from django.http import JsonResponse
from products.views import shop
from users.forms import RegisterForm
from datetime import datetime
import stripe
import os
import math

DEFAULT_IMAGE_UUID = "0662e7f0-e44d-4f4b-8482-715f396f5fb0"
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

# This is a helper function which creates a new order


def order_creator(user, charge_id, cart_items):
    if user:
        try:
            new_order = Order(
                ordered_by=user,
                stripe_charge_token=charge_id,
                time_of_purchase=datetime.now(),
                payment_recieved=True
            )
            new_order.save()
            for i in cart_items:
                selected_product_id = i['product_number']
                selected_product = Product.objects.get(
                    pk=selected_product_id
                )
                new_order.product_ordered.add(
                    selected_product,
                    through_defaults={
                        'quantity': i['quantity']
                    }
                )
            new_order.save()
        except BaseException:
            return False
        else:
            return True

# This is a helper function which reduces the quantity of the purchased items


def quantity_reducer(cart_items):
    for i in cart_items:
        selected_product_id = i['product_number']
        selected_product = Product.objects.get(
            pk=selected_product_id
        )
        new_quantity = selected_product.quantity_in_stock - i['quantity']
        selected_product.quantity_in_stock = new_quantity
        selected_product.save()

# Create your views here.


def checkout(request):
    user_cart = request.session.get('user_cart')
    if user_cart is None or user_cart['cart_items'] == []:
        messages.error(
            request,
            "This cart does not exist."
        )
        return redirect(view_cart)
    else:
        if request.method == "GET":
            custom_detail_form = CustomerDetailForm()
            return render(
                request,
                "checkout.html",
                {
                    "user_cart": user_cart,
                    "custom_detail_form": custom_detail_form
                })
        else:
            req_username = request.POST.get('account_username')
            req_password1 = request.POST.get('account_password_1')
            req_password2 = request.POST.get('account_password_2')
            user_creation_data = {
                'username': req_username,
                'first_name': request.POST.get('first_name'),
                'last_name': request.POST.get('last_name'),
                'email': request.POST.get('email'),
                'password1': req_password1,
                'password2': req_password2,
                'profile_picture': DEFAULT_IMAGE_UUID,
                'seller': False
            }
            dirty_custom_detail_form = CustomerDetailForm(request.POST)
            if dirty_custom_detail_form.is_valid():
                dirty_custom_detail_form.save()
                if req_username:
                    try:
                        dirty_user_creation_form = RegisterForm(
                            user_creation_data
                        )
                    except Exception as e:
                        print(e)
                    else:
                        if dirty_user_creation_form.is_valid():
                            dirty_user_creation_form.save()
                        else:
                            messages.error(
                                request,
                                "We are unable to create your account!"
                            )
                return redirect(payment)
            else:
                if req_username or req_password1 or req_password2:
                    create_account_intention = True
                return render(
                    request,
                    "checkout.html",
                    {
                        "user_cart": user_cart,
                        "custom_detail_form": dirty_custom_detail_form,
                        "create_account_intention": create_account_intention,
                    })


def payment(request):
    if request.session.get('user_cart'):
        if request.method == "GET":
            payable_amount = request.session.get('user_cart')['cart_total']
            payment_form = PaymentForm(
                initial={
                    'payable_amount': payable_amount
                }
            )
            return render(
                request,
                "payment.html",
                {
                    'payment_form': payment_form
                })
        else:
            dirty_payment_form = PaymentForm(request.POST)
            if dirty_payment_form.is_valid():
                credit_card_number = dirty_payment_form.cleaned_data.get(
                    'credit_card_number'
                )
                expiry_month = dirty_payment_form.cleaned_data.get(
                    'expiry_month'
                )
                expiry_year = dirty_payment_form.cleaned_data.get(
                    'expiry_year'
                )
                cvc = dirty_payment_form.cleaned_data.get(
                    'cvc'
                )
                payable_amount = dirty_payment_form.cleaned_data.get(
                    'payable_amount'
                )

                card_token = stripe.Token.create(
                    card={
                        'number': credit_card_number,
                        'exp_month': int(expiry_month),
                        'exp_year': int(expiry_year),
                        'cvc': cvc,
                    },
                )

                payable_amount = int(math.ceil(float(payable_amount)))

                try:
                    charge = stripe.Charge.create(
                        amount=payable_amount,
                        currency="usd",
                        source=card_token['id'],
                        description="Example charge"
                    )
                except stripe.error.CardError as e:
                    error_code = e.error.code
                    if error_code == 'card_declined':
                        dirty_payment_form.add_error(
                            'credit_card_number',
                            forms.ValidationError(
                                ("Card Declined."),
                                code='card_declined'
                            )
                        )
                    elif error_code == 'expired_card':
                        dirty_payment_form.add_error(
                            'credit_card_number',
                            forms.ValidationError(
                                ("This card is expired."),
                                code='expired_card'
                            )
                        )
                    elif error_code == 'incorrect_cvc':
                        dirty_payment_form.add_error(
                            'cvc',
                            forms.ValidationError(
                                ("Incorrect CVC."),
                                code='incorrect_cvc'
                            )
                        )
                    elif error_code == 'invalid_cvc':
                        dirty_payment_form.add_error(
                            'cvc',
                            forms.ValidationError(
                                ("Invalid CVC."),
                                code='invalid_cvc'
                            )
                        )
                    elif error_code == 'incorrect_number':
                        dirty_payment_form.add_error(
                            'credit_card_number',
                            forms.ValidationError(
                                ("Incorrect Credit Card Number."),
                                code='incorrect_number'
                            )
                        )
                    elif error_code == 'invalid_number':
                        dirty_payment_form.add_error(
                            'credit_card_number',
                            forms.ValidationError(
                                ("Invalid Credit Card Number."),
                                code='invalid_number'
                            )
                        )
                    elif error_code == 'invalid_expiry_month':
                        dirty_payment_form.add_error(
                            'expiry_month',
                            forms.ValidationError(
                                ("Invalid Expiry Month."),
                                code='invalid_expiry_month'
                            )
                        )
                    elif error_code == 'invalid_expiry_year':
                        dirty_payment_form.add_error(
                            'expiry_year',
                            forms.ValidationError(
                                ("Invalid Expiry Year."),
                                code='invalid_expiry_year'
                            )
                        )

                    return render(
                        request,
                        "payment.html",
                        {
                            'payment_form': dirty_payment_form
                        })
                else:
                    charge_id = charge['id']
                    cart_items = request.session.get('user_cart')['cart_items']
                    user = request.user
                    order_creator(user, charge_id, cart_items)
                    quantity_reducer(cart_items)
                    del request.session['user_cart']
                    return redirect(shop)

            else:
                return render(
                    request,
                    "payment.html",
                    {
                        'payment_form': dirty_payment_form
                    })
    else:
        messages.error(
            request,
            "This cart does not exist."
        )
        return redirect(view_cart)


def coupon_check(request):
    coupon_code = request.GET.get('coupon_code', None)
    if coupon_code is None:
        data = {
            'discount': None,
            'status': 'Missing Coupon Input'
        }

    try:
        selected_coupon = Coupon.objects.get(coupon_code=coupon_code)
    except Coupon.DoesNotExist:

        data = {
            'discount': None,
            'status': 'Coupon Does Not Exist'
        }
        messages.error(
            request,
            "We are unable to accept your coupon code."
        )
    else:
        data = {
            'discount': int(selected_coupon.discount[:2]),
            'status': 'Coupon Applied'
        }
    finally:
        return JsonResponse(data)

# Cart Class used by all of the cart view functions


class cart:
    def __init__(self):
        self.cart_items = []
        self.cart_subtotal = 0
        self.coupon_applied = 'no-coupon'
        self.chargable_percentage = 1

    def add_item_to_cart(self, cart_item):
        cart_item['total_price'] = cart_item['price'] * cart_item['quantity']
        self.cart_items.append(cart_item)
        return True

    def edit_item_quantity(self, product_number, new_quantity):
        found = False
        for idx, item in enumerate(self.cart_items):
            if item['product_number'] == product_number:
                item['quantity'] = new_quantity
                item['total_price'] = item['price'] * item['quantity']
                found = True
                found_product_number = item['product_number']

        if found is False:
            return None
        else:
            return found_product_number

    def delete_item_from_cart(self, product_number):
        found = False
        for idx, item in enumerate(self.cart_items):
            if item['product_number'] == product_number:
                found = True
                found_product_position = idx

        if found is False:
            return None
        else:
            self.cart_items.pop(found_product_position)
            return True

    def calculate_cart_subtotal(self):
        cart_subtotal = 0
        for i in self.cart_items:
            cart_subtotal += i["total_price"]
        self.cart_subtotal = cart_subtotal

    def edit_cart_coupon_applied(self, coupon_applied, chargable_percentage):
        # This will check if the new coupon extracted from the form data is
        # different from the coupon code in the cart object.
        # If it is different then the changing of values will occur.
        if coupon_applied != self.coupon_applied:
            self.coupon_applied = coupon_applied
            self.chargable_percentage = chargable_percentage
            return True

    def calculate_cart_total(self):
        chargable_percentage = float(self.chargable_percentage)
        cart_subtotal = float(self.cart_subtotal)
        self.cart_total = chargable_percentage * cart_subtotal

    def export_data(self):
        self.calculate_cart_subtotal()
        self.calculate_cart_total()
        # This is the export variable that stores all of the relevant
        # information that the cart page would need.
        export_dict = {
            "cart_items": self.cart_items,
            "cart_subtotal": self.cart_subtotal,
            "cart_total": self.cart_total,
            "coupon_applied": self.coupon_applied,
            "chargable_percentage": self.chargable_percentage
        }
        return export_dict

    def import_data(self, cart_data):
        self.cart_items = cart_data["cart_items"]
        self.cart_subtotal = cart_data["cart_subtotal"]
        self.cart_total = cart_data["cart_total"]
        self.coupon_applied = cart_data["coupon_applied"]
        self.chargable_percentage = cart_data["chargable_percentage"]


def view_cart(request):
    user_cart = request.session.get('user_cart', cart().export_data())
    return render(
        request,
        "cart.html",
        {
            "user_cart": user_cart
        })


def add_to_cart(request, product_number, quantity):
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
        if quantity <= selected_product.quantity_in_stock:
            cart_item = {
                "img_url": img_url,
                "product_number": product_number,
                "product_name": product_name,
                "price": price,
                "quantity": quantity
            }

            if user_cart.add_item_to_cart(cart_item):
                messages.success(
                    request,
                    "Item added to cart."
                )
                request.session['user_cart'] = user_cart.export_data()
            else:
                messages.error(
                    request,
                    "We are unable to add this item to your cart."
                )
        else:
            messages.error(
                request,
                "The quantity in stock for this item is too low."
            )
    return redirect(view_cart)


def edit_cart(request):
    # This packages the product number and item quantity from their individual
    # lists into an array of dictionaries which can then be ingested by the
    # edit item quantity function of the cart object.
    product_number = request.POST.getlist("product-number")
    item_quantity = request.POST.getlist("item-quantity")

    edit_cart_data = []
    for c, v in enumerate(product_number):
        # This checks if the request quantity of wine exceeds the quantity
        # in stock.
        try:
            selected_product = Product.objects.get(pk=v)
        except Product.DoesNotExist:
            pass
        else:
            if selected_product.quantity_in_stock > int(item_quantity[c]):
                cart_item = {
                    'product_number': v,
                    'item_quantity': item_quantity[c]
                }
                edit_cart_data.append(cart_item)
            else:
                selected_product_name = selected_product.name
                messages.error(
                    request,
                    "Quantity selected for '{}' is too high".format(
                        selected_product_name
                    )
                )

    # This section is responsible for gathering the information needed to
    # update the cart total and coupon applied.
    chargable_percentage = request.POST.get('chargable-percentage')
    coupon_applied = request.POST.get('coupon-applied')
    # This is an identical check to the one above inside of the add items
    # to cart function

    if request.session.get('user_cart'):
        cart_data = request.session.get('user_cart')
        user_cart = cart()
        user_cart.import_data(cart_data)
        editing_counter = 0
        for i in edit_cart_data:
            if user_cart.edit_item_quantity(
                int(i["product_number"]),
                int(i["item_quantity"])
            ):
                editing_counter += 1
        if editing_counter == len(edit_cart_data):
            messages.success(
                request,
                "Item quantities has been edited."
            )
            request.session['user_cart'] = user_cart.export_data()
        else:
            messages.error(
                request,
                "There has been an error in editing cart quantities."
            )
        if user_cart.edit_cart_coupon_applied(
            coupon_applied,
            chargable_percentage
        ):
            messages.success(
                request,
                "Coupon has been successfully applied."
            )
            request.session['user_cart'] = user_cart.export_data()
    else:
        messages.error(
            request,
            "This cart does not exist."
        )
    return redirect(view_cart)


def delete_from_cart(request, product_number):
    if request.session.get('user_cart'):
        cart_data = request.session.get('user_cart')
        user_cart = cart()
        user_cart.import_data(cart_data)

        if user_cart.delete_item_from_cart(product_number):
            messages.success(
                request,
                "Item has been successfully deleted."
            )
            request.session['user_cart'] = user_cart.export_data()
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


def clear_cart(request):
    request.session['user_cart'] = cart().export_data()
    return redirect(view_cart)


@login_required
def orders(request):
    orders = Order.objects.all().filter(ordered_by=request.user)
    return render(
        request,
        "orders.html",
        {
            "orders": orders,
        })
