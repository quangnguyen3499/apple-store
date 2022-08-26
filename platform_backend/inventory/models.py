from django.db import models
from django.utils import timezone

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

    def add_inventory_qty(self, qty):
        self.quantity += qty
        return self.quantity


class ProductStock(models.Model):
    product = models.OneToOneField(
        Product,
        related_name="stocks",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        unique=True,
    )
    total_stock_qty = models.IntegerField(default=0)
    available_stock_qty = models.IntegerField(default=0)

    def can_allocate(self, quantity: int) -> bool:
        remaining_stocks = self.available_stock_qty - quantity
        if remaining_stocks < 0:
            return False
        return True

    def add_total_qty(self, quantity):
        self.total_stock_qty += quantity
        self.available_stock_qty += quantity
        return (self.total_stock_qty, self.available_stock_qty)


class ProductImport(Timestampable):
    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, related_name="product_import"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_import"
    )
    quantity = models.IntegerField(default=0)
    batch = models.CharField(max_length=255)
    import_date = models.DateField()
    manufacturer = models.CharField(max_length=255, default="Apple")
