from platform_backend.users.models import User
from platform_backend.store.selectors.orders import order_list
from platform_backend.store.models.orders import Order
from django.db.models.query import Q, F
from .models import Promo
from django.db.models import Count
from django.utils import timezone


def get_available_user_promos(
    *,
    user: User,
    order_amount,
):
    orders_count = (
        order_list()
        .filter(
            ~Q(status=Order.OrderStatus.CANCELED),
            user=user,
        )
        .count()
    )
    promos = (
        Promo.objects.annotate(
            total_claims=Count("user_claims", filter=Q(user_claims__user=user))
        )
        .filter(
            Q(expires_at__gt=timezone.now()) | Q(expires_at__isnull=True),
            active=True,
        )
        .filter(
            Q(minimum_order_amount=0)
            | Q(minimum_order_amount__gt=0) & Q(minimum_order_amount__lte=order_amount)
        )
        .filter(
            Q(min_order_count=0)
            | Q(min_order_count__gt=0) & Q(min_order_count__lte=orders_count)
        )
        .filter(
            Q(max_order_count=0)
            | Q(max_order_count__gt=0) & Q(max_order_count__gt=orders_count)
        )
        .filter(
            Q(max_claims=0) | Q(max_claims__gt=0) & Q(total_claims__lte=F("max_claims"))
        )
        .order_by("-discount_amount")
    )
    return promos
