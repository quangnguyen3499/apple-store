from enum import unique
from django.db import models

from platform_backend.common.models.mixins import Timestampable
from platform_backend.store.models.products import Product


class Stock(Timestampable):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    province = models.CharField(max_length=255)

    class Meta:
        unique_together = ("name", "address", "province")


class Inventory(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="inventory"
    )
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="inventory")
    quantity = models.IntegerField(default=0)

    class Meta:
        unique_together = ("product", "stock")
