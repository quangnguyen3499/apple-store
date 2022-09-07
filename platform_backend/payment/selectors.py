from .models.payment import Payment, Invoice
from django.core.exceptions import ObjectDoesNotExist

def get_payment_detail(*, pk: int) -> Payment:
    try:
        payment = Payment.objects.get(pk=pk)
    except Payment.DoesNotExist:
        raise ObjectDoesNotExist("Payment not found.")
    return payment

def get_invoice_by_id(*, pk: str) -> Invoice:
    try:
        invoice = Invoice.objects.get(pk=pk)
    except Invoice.DoesNotExist:
        raise ObjectDoesNotExist("Invoice not found.")
    return invoice
