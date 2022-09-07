from django.db import models
from platform_backend.common.models.fields import PriceField
from platform_backend.users.models import User
from platform_backend.store.models.orders import Order

class Promo(models.Model):
    code = models.CharField(max_length=255, null=True, blank=True, unique=True)
    description = models.CharField(max_length=255, default="")
    discount_amount = PriceField()
    minimum_order_amount = models.IntegerField()
    max_claims = models.IntegerField(default=0)
    min_order_count = models.IntegerField(default=0)
    max_order_count = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

class UserPromoClaim(models.Model):
    user = models.ForeignKey(User, related_name="user_claims", on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name="+", null=True, on_delete=models.CASCADE)
    promo = models.ForeignKey(Promo, related_name="user_claims", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
