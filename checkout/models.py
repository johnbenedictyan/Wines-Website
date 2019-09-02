from django.db import models
from products.models import product as product 
# Create your models here.
class order():
    ordered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name='orders')
    stripe_token = models.CharField(max_length=1000, blank=False)
    date_of_purchase = models.DateTimeField(blank=False)
    payment_recieved = models.BooleanField(blank=False,default=False)
    product = models.ManyToManyField(product, related_name="order")
    
    def __str__(self):
        return "Order - " + str(self.id)
    
