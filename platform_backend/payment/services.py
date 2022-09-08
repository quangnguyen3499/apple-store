from .models import Payment, Invoice, OnlinePayment
from django.db import transaction
from ..store.models.orders import Order
from ..users.models import User


@transaction.atomic
def create_payment(
    *,
    description: str,
    invoice: Invoice,
    credit_card_id: str,
    amount: int,
) -> Payment:
    payment = Payment.objects.create(
        payment_method=Payment.PaymentMethod.CARD,
        notes=description,
        currency=invoice.currency,
        invoice=invoice,
        status=Payment.Status.PAID,
    )

    create_online_payment(
        amount=amount,
        payment=payment,
        credit_card_id=credit_card_id,
    )

    update_invoice(is_cod=False, invoice=invoice, payment=payment)
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


@transaction.atomic
def create_invoice(
    *,
    user: User,
    order: Order,
    currency: str,
) -> Invoice:
    invoice = Invoice.objects.create(
        total_due=order.cart.total_amount,
        total_remain=order.cart.total_amount,
        order=order,
        user=user,
        currency=currency,
    )
    return invoice

@transaction.atomic
def update_invoice(
    *,
    payment: Payment,
    invoice: Invoice,
    is_cod: bool,
) -> Invoice:
    if is_cod:
        invoice.total_charges = invoice.total_due
    else:
        invoice.total_charges += payment.online_payment.first().amount

    invoice.save()
    return invoice
