from django.conf.urls import url
from django.urls import path
from .views import admin_console

urlpatterns = [
    path('', admin_console, name="admin_console"),
]
