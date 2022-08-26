from django.core.exceptions import ObjectDoesNotExist, ValidationError
import django_filters
from django.db.models.expressions import (
    Q,
    F,
    Case,
    When,
)

from .models import Inventory, Stock, ProductImport


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


class ProductImportFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(lookup_expr="exact")
    batch = django_filters.CharFilter(lookup_expr="iexact")
    product_id = django_filters.NumberFilter(
        method="product_id_filter", label="product_id"
    )
    search = django_filters.CharFilter(method="search_filter", label="search")

    class Meta:
        model = ProductImport
        fields = ["id", "batch"]

    def product_id_filter(self, request, id, value):
        product_search = (
            ProductImport.objects.select_related("product")
            .filter(product__id=value)
            .order_by("import_date")
        )
        return product_search

    def search_filter(self, request, search, value):
        stock_search = ProductImport.objects.select_related("product").filter(
            Q(product__name__icontains=value) | Q(batch__icontains=value)
        )
        return stock_search


def get_product_import(*, filters={}):
    product_import = ProductImport.objects.select_related("product", "stock").all()
    return ProductImportFilter(filters, product_import).qs
