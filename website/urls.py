from django.conf.urls import url
from django.urls import path
from .views import main_page,about_us,contact_us

urlpatterns = [
    path('/', main_page),
    path('/about-us/', about_us),
    path('/contact-us/', contact_us),
]
