from django.conf.urls import url
from django.urls import path
from .views import account_details, registration, log_in, log_out

urlpatterns = [
    path('', account_details, name="account_details"),
    path('registration/', registration, name="registration"),
    path('log-in/', log_in, name="log_in"),
    path('log-out/', log_out, name="log_out"),
]
