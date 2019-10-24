from django.db import models
from pyuploadcare.dj.models import ImageField
# Create your models here.


class Product(models.Model):
    FRANCE = "FR"
    ITALY = "IT"
    USA = "US"
    SPAIN = "ES"
    PORTUGAL = "PT"
    ARGENTINA = "AR"
    AUSTRALIA = "AU"
    NEW_ZEALAND = "NZ"
    UNITED_KINGDOM = "UK"

    LIGHT_BODIED = "LB"
    MEDIUM_BODIED = "MB"
    FULL_BODIED = "FB"
    
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
        
    ANY = "NP"
    
    REGION_CHOICES = [
        (ANY, "Any"),
        (FRANCE, "France"),
        (ITALY, "Italy"),
        (USA, "USA"),
        (SPAIN, "Spain"),
        (PORTUGAL, "Portugal"),
        (ARGENTINA, "Argentina"),
        (AUSTRALIA, "Australia"),
        (NEW_ZEALAND, "New Zealand"),
        (UNITED_KINGDOM, "United Kingdom")
    ]

    BODY_CHOICES = [
        (ANY, "Any"),
        (LIGHT_BODIED, "Light-Bodied"),
        (MEDIUM_BODIED, "Medium-Bodied"),
        (FULL_BODIED, "Full-Bodied")
    ]

    NODE_CHOICES = [
        (ANY, "Any"),
        (FRUITS,"Fruits"),
        (HERBS,"Herbs"),
        (FLOWERS,"Flowers"),
        (EARTH,"Earth"),
        (GRASS,"Grass"),
        (TOBACCO,"Tobacco"),
        (BUTTERSCOTCH,"Butterscotch"),
        (TOAST,"Toast"),
        (VANILLA,"Vanilla"),
        (MOCHA,"Mocha"),
        (CHOCOLATE,"Chocolate")
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

    def __str__(self):
        return self.name