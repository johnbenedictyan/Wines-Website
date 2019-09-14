from django.db import models
from pyuploadcare.dj.models import ImageField
# Create your models here.


class Product(models.Model):
    FRANCE = "FR"
    ITALY = "IT"
    USA = "US"
    SPAIN = "ES"
    PORTUGUAL = "PT"
    ARGENTINA = "AR"
    AUSTRALIA = "AU"
    NEW_ZEALAND = "NZ"
    UNITED_KINGDOM = "UK"

    LIGHT_BODIED = "LB"
    MEDIUM_BODIED = "MB"
    FULL_BODIED = "FB"

    REGION_CHOICES = [
        (FRANCE, "France"),
        (ITALY, "Italy"),
        (USA, "USA"),
        (SPAIN, "Spain"),
        (PORTUGUAL, "Portugal"),
        (ARGENTINA, "Argentina"),
        (AUSTRALIA, "Australia"),
        (NEW_ZEALAND, "New Zealand"),
        (UNITED_KINGDOM, "United Kingdom")
    ]

    BODY_CHOICES = [
        (LIGHT_BODIED, "Light-Bodied"),
        (MEDIUM_BODIED, "Medium-Bodied"),
        (FULL_BODIED, "Full-Bodied")
    ]

    AROMA_CHOICES = [
        ("Fruits","Fruits"),
        ("Herbs","Herbs"),
        ("Flowers","Flowers"),
        ("Earth","Earth"),
        ("Grass","Grass"),
        ("Tobacco","Tobacco"),
        ("Butterscotch","Butterscotch"),
        ("Toast","Toast"),
        ("Vanilla","Vanilla"),
        ("Mocha","Mocha"),
        ("Chocolate","Chocolate")
    ]

    name = models.CharField(
        blank=False,
        max_length=255
    )
    description = models.TextField(
        blank=False
    )
    price = models.FloatField(
        blank=False,
        default=0.0
    )
    quantity_in_stock = models.IntegerField(
        blank=False,
        default=0
    )
    product_picture = ImageField(
        blank=False
    )
    region = models.CharField(
        blank=False,
        max_length=1,
        choices=REGION_CHOICES,
    )
    aroma = models.CharField(
        blank=False,
        max_length=1,
        choices=BODY_CHOICES,
    )
    body = models.CharField(
        blank=False,
        max_length=1,
        choices=AROMA_CHOICES,
    )

    def __str__(self):
        return self.name