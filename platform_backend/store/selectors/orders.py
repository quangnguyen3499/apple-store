from platform_backend.store.models.orders import Order
from django.db.models.query import QuerySet, Q
import django_filters
from django.core.exceptions import ObjectDoesNotExist


def order_list(*, filters=None) -> QuerySet[Order]:
    filters = filters or {}
    orders = Order.objects.all()
    return OrderFilter(filters, orders).qs


class OrderFilter(django_filters.FilterSet):
    delivery_method = django_filters.CharFilter(field_name="delivery_method")
    payment_method = django_filters.CharFilter(field_name="payment_method")
    payment_status = django_filters.CharFilter(field_name="payment_status")
    status = django_filters.CharFilter(field_name="status")
    user = django_filters.NumberFilter(field_name="user")
    search = django_filters.CharFilter(method="search_filter", label="search")
    sort = django_filters.OrderingFilter(
        fields=(
            ("created_at", "created_at"),
            ("total_amount", "total_amount"),
            ("user__first_name", "user__first_name"),
            ("user__last_name", "user__last_name"),
        )
    )

    class Meta:
        model = Order
        fields = ("id", "status", "payment_status", "payment_method", "delivery_method")

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(user__first_name__icontains=value) | Q(user__last_name__icontains=value)
        )


def get_order(*, pk: str) -> Order:
    try:
        return Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        raise ObjectDoesNotExist("Order not found.")
