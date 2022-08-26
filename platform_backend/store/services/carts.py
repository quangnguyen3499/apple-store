from typing import Optional
from django.db import transaction

from django.core.exceptions import ObjectDoesNotExist, ValidationError

from ..models.carts import Cart, CartItem
from ..models.store import Store
from ..selectors.store import get_store
from ..selectors.products import get_product_by_id, get_sellable_product_by_id
from ..selectors.carts import get_cart
from platform_backend.users.models import User


def create_cart(
    *,
    store: Store,
    owner: Optional[User] = None,
) -> Cart:
    return Cart.objects.create(store=store, owner=owner)


@transaction.atomic
def add_item_to_cart(
    *,
    product_id: int,
    quantity: int,
    store_id: str,
    user: User,
):
    store = get_store(store_id)
    product = get_sellable_product_by_id(pk=product_id)
    try:
        cart = Cart.objects.get(store=store, owner=user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(store=store, owner=user)

    try:
        item = CartItem.objects.get(cart=cart, product=product)
        item.quantity = quantity
        item.save()
    except CartItem.DoesNotExist:
        item = CartItem.objects.create(cart=cart, product=product, quantity=quantity)

    return get_cart(pk=cart.id)


@transaction.atomic
def delete_item_from_cart(
    *,
    product_id: int,
    store_id: str,
    user: User,
):
    store = get_store(store_id)
    product = get_product_by_id(pk=product_id)
    try:
        cart = Cart.objects.get(store=store, owner=user)
    except Cart.DoesNotExist:
        raise ObjectDoesNotExist("Cart does not exist")

    CartItem.objects.get(product=product, cart=cart).delete()

    return get_cart(pk=cart.id)
