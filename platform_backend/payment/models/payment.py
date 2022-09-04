from platform_backend.common.models.mixins import Timestampable
from django.db import models
from .invoice import Invoice
from django.utils import timezone

class Payment(Timestampable):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"
        REFUNDED = "REFUNDED", "Refunded"
        EXPIRED = "EXPIRED", "Expired"
        CANCELLED = "CANCELLED", "Cancelled"

    class PaymentMethod(models.TextChoices):
        COD = "COD", "cash on delivery"
        CARD = "CARD", "Card"

    invoice = models.ForeignKey(
        Invoice, related_name="payments", on_delete=models.CASCADE
    )
    payment_method = models.CharField(
        max_length=50,
        choices=PaymentMethod.choices,
    )
    invoice_url = models.CharField(max_length=255, null=True, blank=True)
    amount = models.DecimalField(max_digits=19, decimal_places=4, default=0)
    status = models.CharField(
        max_length=16, choices=Status.choices, default=Status.PENDING
    )
    notes = models.TextField(default="", blank=True)
    paid_at = models.DateTimeField(null=True, blank=True, db_index=True)
    refunded_at = models.DateTimeField(null=True, blank=True, db_index=True)

    @property
    def total_due(self):
        return self.amount


class OnlinePayment(Timestampable):
    class Status(models.TextChoices):
        PENDING = "PENDING", "PENDING"
        SUCCESS = "SUCCESS", "SUCCESS"
        FAILED = "FAILED", "FAILED"

    class CardType(models.TextChoices):
        VISA = "VISA", "visa"
        MASTERCARD = "MASTERCARD", "mastercard"
        AMERICANEXPRESS = "AMERICAN EXPRESS", "american express"
        DISCOVER = "DISCOVER", "discover"

    payment = models.ForeignKey(
        Payment, on_delete=models.CASCADE, related_name="online_payment"
    )
    amount = models.DecimalField(max_digits=19, decimal_places=4)
    status = models.CharField(
        max_length=16, choices=Status.choices, default=Status.PENDING, db_index=True
    )
    card_number = models.CharField(max_length=20, default="")
    card_expired_at = models.DateField(default=timezone.now)
    card_brand = models.CharField(max_length=20, default="")
    card_type = models.CharField(
        max_length=255,
        choices=CardType.choices,
        default=""
    )
    last_4_digits = models.CharField(max_length=4, null=True, blank=True)


class CODPayment(Timestampable):
    class Status(models.TextChoices):
        PENDING = "PENDING", "PENDING"
        SUCCESS = "SUCCESS", "SUCCESS"
        FAILED = "FAILED", "FAILED"

    payment = models.ForeignKey(
        Payment, on_delete=models.CASCADE, related_name="cod_payment"
    )
    address = models.CharField(max_length=254, null=True, blank=True)
    city = models.CharField(max_length=254, null=True, blank=True)
    province = models.CharField(max_length=254, null=True, blank=True)
    shipping_cost = models.IntegerField(default=0)
    amount = models.DecimalField(max_digits=19, decimal_places=4)
    status = models.CharField(
        max_length=16, choices=Status.choices, default=Status.PENDING, db_index=True
    )
