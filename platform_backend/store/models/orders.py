import uuid
from django.db import models

from platform_backend.common.models.mixins import Timestampable
from platform_backend.users.models import User
from .carts import Cart


class Order(Timestampable):
    class DeliveryMethod(models.TextChoices):
        DELIVERY = ("DELIVERY",)
        PICKUP = ("PICKUP",)

    class PaymentMethod(models.TextChoices):
        COD = "COD", "cash on delivery"
        CARD = "CARD", "Card"

    class OrderStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        FOR_APPROVAL = "FOR_APPROVAL", "For approval"
        FOR_PROCESSING = "FOR_PROCESSING", "For processing"
        PROCESSING = "PROCESSING", "Processing"
        FOR_DISPATCH = "FOR_DISPATCH", "For Dispatch"
        DISPATCHED = "DISPATCHED", "Dispatched"
        ENROUTE = "ENROUTE", "Enroute"
        ARRIVED = "ARRIVED", "Arrived"
        RECEIVED = "RECEIVED", "Received"
        REPORTED = "REPORTED", "Reported"
        PACKED = "PACKED", "Packed"
        CANCELED = "CANCELED", "Canceled"
        REJECTED = "REJECTED", "Rejected"
        COMPLETED = "COMPLETED", "Completed"
        DELIVERY_FAILED = "DELIVERY_FAILED", "Delivery Failed"
        RETURNED = "RETURNED", "Returned"

    class PaymentStatus(models.TextChoices):
        TO_COLLECT = "TO_COLLECT", "To collect"
        UNPAID = "UNPAID", "Unpaid"
        PROCESSING = "PROCESSING", "Processing"
        PAID = "PAID", "Paid"
        REFUNDED = "REFUNDED", "Refunded"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="order")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    delivery_method = models.CharField(
        max_length=50,
        choices=DeliveryMethod.choices,
        null=True,
        blank=True,
        db_index=True,
    )
    payment_method = models.CharField(
        max_length=50,
        choices=PaymentMethod.choices,
        default=PaymentStatus.TO_COLLECT,
        db_index=True,
    )
    payment_status = models.CharField(
        max_length=50,
        choices=PaymentStatus.choices,
        default=PaymentStatus.TO_COLLECT,
        db_index=True,
    )
    status = models.CharField(
        max_length=50,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
        db_index=True,
    )
