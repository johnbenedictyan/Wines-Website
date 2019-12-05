from django.db import models

# Create your models here.
class Contact(models.Model):
    first_name = models.CharField(
        blank=False,
        max_length=30
    )
    last_name = models.CharField(
        blank=False,
        max_length=30
    )
    phone_number = models.IntegerField(
        blank=False,
    )
    email_address = models.EmailField(
        blank=False,
    )
    message = models.TextField(
        blank=False
    )