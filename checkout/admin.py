from django.contrib import admin
from .models import Order, Coupon, Customer_Detail, Order_Product_Intermediary
# Register your models here.
admin.site.register(Order)
admin.site.register(Coupon)
admin.site.register(Customer_Detail)
admin.site.register(Order_Product_Intermediary)
