import uuid

from django.db import models

from platform_backend.common.models.mixins import Timestampable
from platform_backend.users.models import User
from .store import Store
from .products import Product


class Cart(Timestampable):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart")
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="cart")
    is_checked_out = models.BooleanField(default=False)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_item")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="cart_item"
    )
    quantity = models.IntegerField(default=0)
