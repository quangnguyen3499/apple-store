from .models.payment import Payment
from django.core.exceptions import ObjectDoesNotExist

def get_payment_detail(*, pk: int) -> Payment:
    try:
        payment = Payment.objects.get(pk=pk)
    except Payment.DoesNotExist:
        raise ObjectDoesNotExist("Payment not found.")
    return payment
