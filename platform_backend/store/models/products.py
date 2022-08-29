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
    floor_price = models.DecimalField(max_digits=19, decimal_places=4)
    price = models.DecimalField(max_digits=19, decimal_places=4)
    promo_price = models.DecimalField(max_digits=19, decimal_places=4, default=0)
    sale_percent = models.IntegerField(default=0)
    sellable = models.BooleanField(default=False)
    items_sold = models.IntegerField(default=0)
    on_sale = models.BooleanField(default=False)
    avg_rating = models.FloatField(default=0)

    @property
    def is_saleable(self):
        return self.sellable

    @property
    def is_onsale(self):
        return self.on_sale

    @property
    def srp_price(self):
        if not self.is_onsale:
            srp_price = self.price
        if self.is_onsale and self.promo_price > 0 and self.sale_percent == 0:
            srp_price = self.promo_price
        if self.is_onsale and self.sale_percent > 0 and self.promo_price == 0:
            srp_price = self.price - (self.price * self.sale_percent / 100)
        if self.is_onsale and self.sale_percent > 0 and self.promo_price > 0:
            srp_price = min(
                self.price - (self.price * self.sale_percent / 100), self.promo_price
            )
        return srp_price


class ProductImage(Timestampable):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="image")
    upload = models.ImageField(upload_to=get_image_path)
    default = models.BooleanField(default=False)
    image = models.ImageField()

    @property
    def url(self):
        if self.upload:
            return self.upload.url
