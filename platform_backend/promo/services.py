from django.core.exceptions import ValidationError

from ..promo.models import UserPromoClaim, Promo
from ..store.models.carts import Cart, CartPromo
from ..store.models.orders import Order
from ..users.models import User
from django.db import transaction
from .selectors import get_available_user_promos


@transaction.atomic
def apply_cart_promo(
    *,
    cart: Cart,
    code: str,
) -> Cart:
    if cart.is_checked_out:
        raise ValidationError("Cart already checked out")

    available_promos = None
    total_amount = cart.total_items_amount
    get_available_user_promos(
        order_amount=total_amount,
        code=code,
    )
    if not available_promos:
        raise ValidationError("Promo not valid")

    promo = available_promos.first()
    if not promo:
        raise ValidationError("Promo not valid")

    CartPromo.objects.update_or_create(cart=cart, default={"promo": promo})
    return cart


def claim_user_promo(
    *,
    user: User,
    promo: Promo,
    order: Order,
) -> UserPromoClaim:
    claim = UserPromoClaim.objects.create(
        user=user,
        order=order,
        promo=promo,
    )
    return claim
