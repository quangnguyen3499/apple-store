from typing import Optional
from django.db import transaction

from django.core.exceptions import ObjectDoesNotExist, ValidationError

from ..models.orders import DeliveryAddress, Order
from ..models.carts import Cart, CartItem
from ..models.store import Store

from ..selectors.store import get_store
from ..selectors.products import get_product_by_id, get_sellable_product_by_id
from ..selectors.carts import get_cart

from ...users.models import User

from ...promo.services import apply_cart_promo

from ..services.orders import create_order


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


@transaction.atomic
def checkout_cart(
    *,
    user: User,
    cart: Cart,
    delivery_address: DeliveryAddress,
    delivery_method: Order.DeliveryMethod,
    payment_method: Order.PaymentMethod.choices,
    order_status: Order.OrderStatus.choices,
) -> Cart:
    if cart.cart_item.count() == 0:
        raise ValidationError("Cart has no items.")
    if cart.is_checked_out:
        raise ValidationError("Cart has been checked out.")

    order = create_order(
        user=user,
        cart=cart,
        delivery_method=delivery_method,
        payment_method=payment_method,
        order_status=order_status,
    )
    if delivery_address and delivery_method == "DELIVERY":
        delivery_address = DeliveryAddress.objects.create(
            order=order,
            user=user,
            address=delivery_address["address"],
            city=delivery_address["city"],
            province=delivery_address["province"],
        )

    return order


@transaction.atomic
def apply_cart_discount(
    *,
    cart: Cart,
    discount_type: Cart.DiscountTypes,
    code: str,
) -> Cart:
    if discount_type == Cart.DiscountTypes.VOUCHER:
        pass
        # TODO
    elif discount_type == Cart.DiscountTypes.PROMO:
        apply_cart_promo(cart=cart, code=code)
        # delete all vouchers
    return cart
