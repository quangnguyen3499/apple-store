from django.db import models

from platform_backend.common.models.mixins import Timestampable
from .store import Store


class Catergories(models.Model):
    name = models.CharField(max_length=255)


class Product(Timestampable):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="product")
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        Catergories, on_delete=models.CASCADE, related_name="product"
    )
    unit_of_measurement = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=19, decimal_places=4, default=0)
    promo_price = models.DecimalField(max_digits=19, decimal_places=4, default=0)
    sale_percent = models.IntegerField(default=0)
    image = models.ImageField()
