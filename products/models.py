from django.db import models

# Create your models here.
class product():
    name = models.CharField(blank=False,max_length = 255)
    description = models.TextField(blank=False)
    price = models.FloatField(blank=False,default=0.0)
    quantity_in_stock = models.IntegerField(blank=False,default=0)
    
    def __str__(self):
        return self.name    
    