from django.shortcuts import render,redirect

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
        