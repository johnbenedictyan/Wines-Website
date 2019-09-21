from django.db import models
from products.models import Product as product
from project4.settings import AUTH_USER_MODEL
from django_countries.fields import CountryField
# Create your models here.

class Customer_Details(models.Model):
    country = CountryField(
        verbose_name="Country",
        blank_label="Select Country",
        blank=False
    )
    
    first_name = models.CharField(
        verbose_name="First Name",
        blank=False
    )
    
    last_name = models.CharField(
        verbose_name="Last Name",
        blank=False
    )
    
    address_1 = models.CharField(
        verbose_name="Address",
        blank=False
    )
        
    address_2 = models.CharField(
        blank=False
    )
        
    state_or_country = models.CharField(
        verbose_name="State / Country",
        blank=False
    )
    
    postal_code_or_zip = models.CharField(
        verbose_name="Postal Code / Zip",
        blank=False
    )
    
    email = models.CharField(
        verbose_name="Email Address",
        blank=False
    )
    
    phone = models.CharField(
        verbose_name="Phone Number",
        blank=False
    )

    account_password = models.CharField(
        verbose_name="Account Password",
        blank=True
    )

    alt_country = CountryField(
        verbose_name="Country",
        blank=True
    )
        
    alt_address_1 = models.CharField(
        verbose_name="Address",
        blank=True
    )
    alt_address_2 = models.CharField(
        blank=True
    )
    alt_state_or_country = models.CharField(
        verbose_name="State / Country",
        blank=True
    )
    alt_postal_code_or_zip = models.CharField(
        verbose_name="Postal Code / Zip",
        blank=True
    )

    coupon_code = models.CharField(
        verbose_name="Enter your coupon code if you have one",
        blank=True
    )

    order_notes = models.CharField(
        verbose_name="Order Notes",
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