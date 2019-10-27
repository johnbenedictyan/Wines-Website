from django.contrib import admin
from .models import Order,Coupon,Customer_Details
# Register your models here.
admin.site.register(Order)
admin.site.register(Coupon)
admin.site.register(Customer_Details)