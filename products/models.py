from django.db import models
from pyuploadcare.dj.models import ImageField
import datetime
# Create your models here.

# Useful Utility Functions for year field


def year_choices():
    return [(r, r) for r in range(1984, datetime.date.today().year)]


def current_year():
    return datetime.date.today().year


class Product(models.Model):
    FR = "FRANCE"
    IT = "ITALY"
    US = "USA"
    ES = "SPAIN"
    PT = "PORTUGAL"
    AR = "ARGENTINA"
    AU = "AUSTRALIA"
    NZ = "NEW ZEALAND"
    UK = "UNITED KINGDOM"

    LB = "Light"
    MB = "Medium"
    FB = "Full"

    FRUITS = "Fruits"
    HERBS = "Herbs"
    FLOWERS = "Flowers"
    EARTH = "Earth"
    GRASS = "Grass"
    TOBACCO = "Tobacco"
    BUTTERSCOTCH = "Butterscotch"
    TOAST = "Toast"
    VANILLA = "Vanilla"
    MOCHA = "Mocha"
    CHOCOLATE = "Chocolate"

    REGION_CHOICES = [
        (FR, "France"),
        (IT, "Italy"),
        (US, "USA"),
        (ES, "Spain"),
        (PT, "Portugal"),
        (AR, "Argentina"),
        (AU, "Australia"),
        (NZ, "New Zealand"),
        (UK, "United Kingdom")
    ]

    BODY_CHOICES = [
        (LB, "Light-Bodied"),
        (MB, "Medium-Bodied"),
        (FB, "Full-Bodied")
    ]

    NODE_CHOICES = [
        (FRUITS, "Fruits"),
        (HERBS, "Herbs"),
        (FLOWERS, "Flowers"),
        (EARTH, "Earth"),
        (GRASS, "Grass"),
        (TOBACCO, "Tobacco"),
        (BUTTERSCOTCH, "Butterscotch"),
        (TOAST, "Toast"),
        (VANILLA, "Vanilla"),
        (MOCHA, "Mocha"),
        (CHOCOLATE, "Chocolate")
    ]

    name = models.CharField(
        blank=False,
        max_length=255
    )
    year = models.IntegerField(
        blank=False,
        choices=year_choices(),
        default=current_year()
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
        max_length=25,
        choices=REGION_CHOICES,
    )
    nodes = models.CharField(
        blank=False,
        max_length=25,
        choices=NODE_CHOICES,
    )
    body = models.CharField(
        blank=False,
        max_length=25,
        choices=BODY_CHOICES,
    )
    seller_id = models.IntegerField(
        blank=False,
        default=1
    )
    views = models.IntegerField(
        blank=False,
        default=0
    )

    def __str__(self):
        return self.name
