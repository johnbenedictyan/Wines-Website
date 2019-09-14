from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import DetailForm

# Create your views here.
def checkout(request):
    selected_order = None
    custom_detail_form = DetailForm()
    if request.method == "GET":
        return render(
            request,
            "checkout.html",
            {
                "selected_order":selected_order
            })
    else:
        dirty_custom_detail_form = DetailForm(request.POST)
        if dirty_custom_detail_form.is_valid():
            dirty_custom_detail_form.save(commit=False)
            return redirect(None)
        else:
            messages.error(
                request,
                "We are unable to accept your details."
                )
            
def cart(request):
    selected_cart = None
    return render(
        request,
        "cart.html",
        {
            "selected_cart":selected_cart
        })