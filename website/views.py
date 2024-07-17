from django.shortcuts import render, redirect
from django.contrib import messages
from project4 import settings
from .forms import ContactForm, BlogCreatorFrom
from .models import Blog as blog
from products.models import Product
from django.contrib.auth.decorators import login_required

# Create your views here.


def main_page(request):
    best_sellers = Product.objects.order_by('views')[:3]
    return render(
        request,
        'index.html',
        {
            'best_sellers': best_sellers
        })


def about_us(request):
    return render(
        request,
        'about-us.html'
    )


def contact_us(request):
    if request.method == "GET":
        contact_form = ContactForm()
        return render(
            request,
            'contact.html',
            {
                'contact_form': contact_form
            })
    else:
        dirty_contact_form = ContactForm(request.POST)
        if dirty_contact_form.is_valid():
            dirty_contact_form.save()
            messages.success(
                request,
                "Thank you for contacting us."
            )
            return redirect(settings.HOME_URL)
        else:
            messages.error(
                request,
                "There was an error in the contact form."
            )
            return render(
                request,
                'contact.html',
                {
                    'contact_form': dirty_contact_form
                })


@login_required
def blog_creator(request):
    if request.method == "GET":
        blog_form = BlogCreatorFrom()
        blog_form.fields["writer"].initial = request.user.username
        return render(
            request,
            "blog-creator.html",
            {
                "blog_form": blog_form
            })
    else:
        dirty_blog_form = BlogCreatorFrom(request.POST)
        if dirty_blog_form.is_valid():
            dirty_blog_form.save()
            return redirect(bloghub)
        else:
            messages.error(
                request,
                "We were unable to create this blog."
            )
            return render(
                request,
                "blog-creator.html",
                {
                    "blog_form": dirty_blog_form
                })


def bloghub(request):
    all_blogs = blog.objects.all()
    return render(
        request,
        "bloghub.html",
        {
            "all_blogs": all_blogs
        })


def single_blog(request, blog_number):
    try:
        single_blog = blog.objects.get(pk=blog_number)
    except blog.DoesNotExist:
        messages.error(
            request,
            "This blog does not exist."
        )
        return redirect(bloghub)
    else:
        return render(
            request,
            "blog.html",
            {
                "blog": single_blog
            })


def csrf_failure(request, reason=""):
    messages.error(
        request,
        "This form has expired. Please try again."
    )
    return redirect("/")


def handler404(request, exception=None):
    return render(
        request,
        '404.html',
        status=404
    )
