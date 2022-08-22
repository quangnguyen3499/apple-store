from re import M
from django.db import models

from platform_backend.common.models.mixins import Timestampable
from .store import Store


def get_image_path(instance, filename):
    return f"products/{instance.product}/{filename}"


class Categories(models.Model):
    name = models.CharField(max_length=255)


class Product(Timestampable):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="product")
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        Categories, on_delete=models.CASCADE, related_name="product"
    )
    unit_of_measurement = models.CharField(max_length=50)
    default_price = models.DecimalField(max_digits=19, decimal_places=4, default=0)
    price = models.DecimalField(max_digits=19, decimal_places=4, default=0)
    promo_price = models.DecimalField(max_digits=19, decimal_places=4, default=0)
    sale_percent = models.IntegerField(default=0)
    sellable = models.BooleanField(default=False)
    items_sold = models.IntegerField(default=0)


class ProductImage(Timestampable):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="image")
    upload = models.ImageField(upload_to=get_image_path)
    default = models.BooleanField(default=False)

    @property
    def url(self):
        if self.upload:
            return self.upload.url
