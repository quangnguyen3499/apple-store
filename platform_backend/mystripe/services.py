from unicodedata import numeric
from ..users.models import Customer
import stripe


def create_stripe_customer(
    *,
    customer: Customer,
) -> str:
    user = customer.user
    stripe_customer = stripe.Customer.create(
        address={
            "city": customer.city,
            "state": customer.province,
            "line1": customer.address,
        },
        description="Test Customer",
        email=user.email,
        name=user.first_name + user.last_name,
    )

    return stripe_customer.id

def create_stripe_charge(
    *,
    amount: int,
    currency: str,
    customer: str,
    description: str,
):
    stripe.Charge.create(
        amount=amount,
        currency=currency,
        customer=customer,
        description=description,
    )