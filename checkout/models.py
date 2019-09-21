from django.db import models
from products.models import Product as product
from project4.settings import AUTH_USER_MODEL
from django_countries.fields import CountryField
# Create your models here.

class Customer_Details(models.Model):
    country = CountryField(
        label="Country",
        blank=False
    )
    
    first_name = models.CharField(
        label="First Name",
        blank=False
    )
    
    last_name = models.CharField(
        label="Last Name",
        blank=False
    )
    
    address_1 = models.CharField(
        label="Address",
        blank=False
    )
        
    address_2 = models.CharField(
        blank=False
    )
        
    state_or_country = models.CharField(
        label="State / Country",
        blank=False
    )
    
    postal_code_or_zip = models.CharField(
        label="Postal Code / Zip",
        blank=False
    )
    
    email = models.CharField(
        label="Email Address",
        blank=False
    )
    
    phone = models.CharField(
        label="Phone Number",
        blank=False
    )

    account_password = models.CharField(
        label="Account Password",
        blank=True
    )

    alt_country = CountryField(
        label="Country",
        blank=True
    )
        
    alt_address_1 = models.CharField(
        label="Address",
        blank=True
    )
    alt_address_2 = models.CharField(
        blank=True
    )
    alt_state_or_country = models.CharField(
        label="State / Country",
        blank=True
    )
    alt_postal_code_or_zip = models.CharField(
        label="Postal Code / Zip",
        blank=True
    )

    coupon_code = models.CharField(
        label="Enter your coupon code if you have one",
        blank=True
    )

    order_notes = models.CharField(
        label="Order Notes",
        blank=True
    )
    
class Order(models.Model):
    ordered_by = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    stripe_token = models.CharField(
        max_length=1000,
        blank=False
    )
    date_of_purchase = models.DateTimeField(
        blank=False
    )
    payment_recieved = models.BooleanField(
        blank=False,
        default=False
    )
    product_ordered = models.ManyToManyField(
        product,
        related_name="orders"
    )

    def __str__(self):
        return "Order - " + str(self.id)