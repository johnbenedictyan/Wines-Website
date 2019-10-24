from django.db import models
from pyuploadcare.dj.models import ImageField
import datetime
# Create your models here.

#Useful Utility Functions for year field
def year_choices():
        return [(r,r) for r in range(1984, datetime.date.today().year)]

def current_year():
    return datetime.date.today().year
        
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

    def __str__(self):
        return self.name