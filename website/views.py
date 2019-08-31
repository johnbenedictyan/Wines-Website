from django.shortcuts import render,redirect
from django.contrib import messages

# Create your views here.
def main_page(request):
    return render(request,
                    'index.html',
                    {
                        
                    }
        )

def contact_us(request):
    if request.method=="GET":
        return render(request,
                        'contact.html',
                        {
                            
                        }
        )
    else:
        return render(request,
                        'contact.html',
                        {
                            
                        }
        )
        
def csrf_failure(request, reason=""):
    messages.error(
                request,
                "This form has expired. Please try again."
            )
    return redirect("/")