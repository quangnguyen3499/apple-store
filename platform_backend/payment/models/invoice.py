from platform_backend.common.models.mixins import Timestampable
from ...users.models import User
from ...store.models.orders import Order
from django.db import models
import uuid


class Invoice(Timestampable):
    class InvoiceStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        DRAFT = "DRAFT", "Draft"
        PAID = "PAID", "Paid"
        PARTIALLY_PAID = "PARTIALLY_PAID", "Partially Paid"

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="invoices")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="invoices", null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice_number = models.CharField(max_length=255, default="", blank=True)
    invoice_date = models.DateField(null=True, blank=True)
    invoice_due_date = models.DateField(null=True, blank=True)
    total_order = models.DecimalField(max_digits=19, decimal_places=4, default=0)
    total_charges = models.DecimalField(max_digits=19, decimal_places=4, default=0)
    total_due = models.DecimalField(max_digits=19, decimal_places=4, default=0)
    status = models.CharField(
        max_length=255, default=InvoiceStatus.DRAFT, choices=InvoiceStatus.choices
    )
