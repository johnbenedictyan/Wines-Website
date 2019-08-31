from django.shortcuts import render,redirect
from django.contrib import messages
from project4 import settings
from .forms import ContactForm

# Create your views here.
def main_page(request):
    return render(request,
                    'index.html',
                    {
                        
                    }
        )

def about_us(request):
    return render(request,
                    'about-us.html',
                    {
                        
                    }
        )

def contact_us(request):
    if request.method=="GET":
        contact_form = ContactForm()
        return render(request,
                        'contact.html',
                        {
                            'contact_form':contact_form
                        }
        )
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
            return render(request,
                  'contact.html',
                  {
                      'contact_form':dirty_contact_form
                  })
            
        
        
def csrf_failure(request, reason=""):
    messages.error(
                request,
                "This form has expired. Please try again."
            )
    return redirect("/")