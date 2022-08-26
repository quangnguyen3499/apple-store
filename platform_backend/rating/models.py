from django.db import models

from platform_backend.users.models import User
from platform_backend.store.models.orders import Order
from platform_backend.store.models.products import Product
from platform_backend.common.models.mixins import Timestampable


class Rating(Timestampable):
    class Types(models.TextChoices):
        PRODUCT = "PRODUCT"
        SERVICE = "SERVICE"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="ratings")
    rating_type = models.CharField(
        max_length=50, choices=Types.choices, null=True, blank=True
    )
    rating = models.SmallIntegerField()
    comment = models.TextField(null=True, blank=True)
    allow_rating = models.BooleanField(default=True)


class ProductRatings(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_ratings"
    )
    rating = models.ForeignKey(
        Rating, on_delete=models.CASCADE, related_name="product_ratings"
    )


class AdminRatings(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="admin_ratings"
    )
    rating = models.ForeignKey(
        Rating, on_delete=models.CASCADE, related_name="admin_ratings"
    )


class Tag(models.Model):
    class Types(models.TextChoices):
        PRODUCT = "PRODUCT"
        LOGISTIC = "LOGISTIC"

    name = models.CharField(max_length=100)
    tag_type = models.CharField(
        max_length=50, choices=Types.choices, null=True, blank=True
    )


class RatingTags(models.Model):
    rating = models.ForeignKey(
        Rating, on_delete=models.CASCADE, related_name="rating_tags"
    )
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="rating_tags")
