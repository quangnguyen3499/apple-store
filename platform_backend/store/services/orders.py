from platform_backend.promo.services import claim_user_promo
from ..models.orders import DeliveryAddress, Order
from ..models.carts import Cart
from ...users.models import User


def create_order(
    *,
    user: User = None,
    cart: Cart,
    delivery_method: Order.DeliveryMethod,
    payment_method: Order.PaymentMethod.choices,
    order_status: Order.OrderStatus.choices,
) -> Order:
    order = Order.objects.create(
        user=user,
        cart=cart,
        delivery_method=delivery_method,
        status=order_status,
        payment_method=payment_method,
    )

    if payment_method == "CARD":
        order.payment_status = Order.PaymentStatus.PAID
    order.save()

    # update Cart status
    cart.is_checked_out = True
    cart.save()

    # create UserPromoClaim
    for cart_promo in cart.promos.all():
        promo = cart_promo.promo
        claim_user_promo(
            user=user,
            promo=promo,
            order=order,
        )
    # noti new Order
    # TODO
    return order
