from django.db import models
from django.contrib.auth.models import AbstractUser
from pyuploadcare.dj.models import ImageField
# Create your models here.


class UserAccount(AbstractUser):
    first_name = models.CharField(
        max_length=30,
        blank=False
    )
    last_name = models.CharField(
        max_length=30,
        blank=False
    )
    email = models.EmailField(
        blank=False
    )
    bio = models.TextField(
        blank=True
    )
    profile_picture = ImageField(
        blank=False
    )
    seller = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.username