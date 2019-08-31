from django.conf.urls import url
from django.urls import path
from .views import account_details,registration,log_in,log_out

urlpatterns = [
    path('/', account_details),
    path('/registration/', registration),
    path('/log-in/', log_in),
    path('/log-out/', log_out),
]
