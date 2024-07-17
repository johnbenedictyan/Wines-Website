from django.db import models
from users.models import UserAccount as user
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


class Blog(models.Model):
    headline = models.CharField(
        blank=False,
        max_length=100
    )
    body = models.TextField(
        blank=False
    )
    writer = models.CharField(
        blank=False,
        max_length=50
    )
