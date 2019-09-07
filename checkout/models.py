from django.db import models
from products.models import Product as product
from project4.settings import AUTH_USER_MODEL as AUTH_USER_MODEL
# Create your models here.


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
    product = models.ManyToManyField(
        product,
        related_name="order"
    )

    def __str__(self):
        return "Order - " + str(self.id)