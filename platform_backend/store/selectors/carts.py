from django.core.exceptions import ObjectDoesNotExist, ValidationError

from ..models.carts import Cart
from ...users.models import User

def get_cart(*, pk: str) -> Cart:
    try:
        cart = Cart.objects.get(pk=pk)
        cart = (
            Cart.objects.select_related("owner")
            .prefetch_related(
                "cart_item__product",
                "cart_item__product__image",
                "promos",
            )
            .order_by("id")
            .get(pk=pk)
        )
        print(vars(cart))
    except Cart.DoesNotExist:
        ObjectDoesNotExist("Cart does not exist")
    return cart

def get_user_cart(*, user: User) -> Cart:
    try:
        cart = (
            Cart.objects.select_related("owner")
            .prefetch_related(
                "cart_item__product",
                "cart_item__product__image",
                "promos",
            )
            .order_by("id")
            .get(owner=user)
        )
        return cart
    except Cart.DoesNotExist:
        ObjectDoesNotExist("Cart does not exist")
