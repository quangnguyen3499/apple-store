from django.core.exceptions import ObjectDoesNotExist, ValidationError
import django_filters

from .models import Inventory, Stock


def get_stock(stock_id: int) -> Stock:
    try:
        stock = Stock.objects.get(id=stock_id)
    except Stock.DoesNotExist:
        raise ObjectDoesNotExist("Stock does not exist")


def get_stock_list() -> Stock:
    stocks = Stock.objects.all()
    return stocks


class InventoryFilter(django_filters.FilterSet):
    category = django_filters.NumberFilter(method="category_filter", label="category")
    product = django_filters.NumberFilter(lookup_expr="exact")
    search = django_filters.CharFilter(method="search_filter", label="search")

    class Meta:
        models = Inventory
        fields = ["product", "stock"]

    def search_filter(self, request, search, value):
        inventories_search = (
            Inventory.objects.select_related("product", "stock")
            .filter(product__name__icontains=value)
            .order_by("-quantity")
        )
        return inventories_search

    def category_filter(self, request, category, value):
        category_search = (
            Inventory.objects.select_related("product", "stock")
            .filter(product__category=value)
            .order_by("-quantity")
        )
        return category_search


def get_stock_of_product(*, filters={}):
    inventories = (
        Inventory.objects.select_related("product")
        .select_related("stock")
        .all()
        .order_by("-quantity")
    )

    return InventoryFilter(filters, inventories).qs
