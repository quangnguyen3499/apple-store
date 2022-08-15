from django.db import models
from common.models.fields import PriceField
from users.models import User
from store.models.orders import Order

class Promo(models.Model):
    code = models.CharField(max_length=255, null=True, blank=True, unique=True)
    description = models.CharField(max_length=255, default="")
    discount_amount = PriceField()
    minimum_order_amount = models.IntegerField()
    max_claims = models.IntegerField(default=0)
    min_order_count = models.IntegerField(default=0)
    max_order_count = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    special = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class UserPromoClaim(models.Model):
    user = models.ForeignKey(User, related_name="promo_user", on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name="order", on_delete=models.SET_NULL)
    promo = models.ForeignKey(Promo, related_name="promo", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
