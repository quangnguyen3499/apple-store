from platform_backend.payment.models.payment import OnlinePayment
from .models import Payment, Invoice
from django.db import transaction


@transaction.atomic
def create_payment(
    *,
    amount: int,
    description: str,
    currency: str,
    invoice: Invoice,
    credit_card_id: str,
) -> Payment:
    payment = Payment.objects.create(
        payment_method=Payment.PaymentMethod.CARD,
        notes=description,
        currency=currency,
        invoice=invoice,
        # invoice_url=...,
    )
    if amount < invoice.total_charges:
        payment.status = Payment.Status.PAID
        payment.save()
    create_online_payment(
        amount=amount,
        payment=payment,
        credit_card_id=credit_card_id,
    )

    return payment


@transaction.atomic
def create_online_payment(
    *,
    amount: int,
    payment: Payment,
    credit_card_id: str,
) -> OnlinePayment:
    online_payment = OnlinePayment.objects.create(
        amount=amount,
        payment=payment,
        credit_card_id=credit_card_id,
    )
    return online_payment
