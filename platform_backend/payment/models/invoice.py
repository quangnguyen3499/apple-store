from platform_backend.common.models.mixins import Timestampable
from ...users.models import User
from ...store.models.orders import Order
from django.db import models
import uuid


class Invoice(Timestampable):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"
        PARTIALLY_PAID = "PARTIALLY_PAID", "Partially Paid"

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="invoices")
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="invoices", null=True
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice_number = models.CharField(max_length=255, default="", blank=True)
    invoice_date = models.DateField(null=True, blank=True)
    invoice_due_date = models.DateField(null=True, blank=True)
    total_charges = models.IntegerField(default=0)
    total_due = models.IntegerField(default=0)
    total_remain = models.IntegerField(default=0)
    status = models.CharField(
        max_length=255, default=Status.PENDING, choices=Status.choices
    )
    currency = models.CharField(max_length=255, null=True, blank=True)
    invoice_url = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.total_remain = self.total_due - self.total_charges
        if self.total_remain == 0:
            self.status = Invoice.Status.PAID
        elif self.total_remain == self.total_due:
            self.status = Invoice.Status.PENDING
        elif self.total_remain > 0:
            self.status = Invoice.Status.PARTIALLY_PAID
        super(Invoice, self).save(*args, **kwargs)
