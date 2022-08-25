from enum import unique
import uuid

from django.db import models

from platform_backend.common.models.mixins import Timestampable
from platform_backend.users.models import User
from .store import Store
from .products import Product

# from platform_backend.promo.models import Promo


class Cart(Timestampable):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="cart",
    )
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name="cart",
    )
    is_checked_out = models.BooleanField(default=False)

    class DiscountTypes(models.TextChoices):
        PROMO = "PROMO", "Promo"
        VOUCHER = "VOUCHER", "Voucher"

    class Meta:
        unique_together = ("owner", "store")

    @property
    def total_items_amount(self):
        total = 0
        for item in self.cart_item.all():
            total += item.subtotal
        return total


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_item")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="cart_item"
    )
    quantity = models.IntegerField(default=0)

    class Meta:
        unique_together = ("cart", "product")

    @property
    def has_enough_stock(self):
        if hasattr(self.product, "stocks"):
            return self.product.stocks.can_allocate(self.quantity)

    @property
    def subtotal(self):
        return self.product.srp_price * self.quantity


class CartPromo(Timestampable):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="promos")
    promo = models.ForeignKey("promo.Promo", on_delete=models.CASCADE, related_name="+")

    @property
    def discount_amount(self):
        return self.promo.discount_amount
