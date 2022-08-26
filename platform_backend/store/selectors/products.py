from django.core.exceptions import ObjectDoesNotExist, ValidationError
import django_filters

from ..models.products import Product, Categories
from django.db.models.expressions import (
    F,
    Case,
    When,
)
from django.db.models.query import Q


def get_product(*, pk: int) -> Product:
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        raise ObjectDoesNotExist("Product not found.")
    return product


def get_product_by_id(pk: int) -> Product:
    try:
        product = Product.objects.get(id=pk)
        return product
    except Product.DoesNotExist:
        raise ObjectDoesNotExist("Product does not exist")


def get_sellable_product_by_id(pk: int) -> Product:
    try:
        product = Product.objects.filter(sellable=True).get(id=pk)
        return product
    except Product.DoesNotExist:
        raise ObjectDoesNotExist("Product is not sellable")


def get_category(category_id: int) -> Categories:
    try:
        category = Categories.objects.get(id=category_id)
        return category
    except Categories.DoesNotExist:
        raise ObjectDoesNotExist("category does not exist")


class CategoryFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(lookup_expr="exact")
    name = django_filters.CharFilter(method="search_filter", label="name")

    class Meta:
        fields = ["id", "name"]

    def search_filter(self, queryset, name, value):
        search_category = Categories.objects.filter(name__icontains=value)
        return search_category


def get_list_of_all_category(*, filters={}):
    categories = Categories.objects.all()
    return CategoryFilter(filters, categories).qs


class ProductFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(lookup_expr="exact")
    name = django_filters.CharFilter(lookup_expr="exact")
    category = django_filters.NumberFilter(lookup_expr="exact")
    search = django_filters.CharFilter(method="search_filter", label="search")

    class Meta:
        models = Product
        fields = {"id": ["exact"]}

    def search_filter(self, queryset, name, value):
        search_products = Product.objects.filter(
            Q(name__icontains=value) | Q(category__name__icontains=value)
        ).filter(sellable=True)
        return search_products


def get_list_of_all_product(*, filters=None) -> Product:
    filters = filters or {}
    products = (
        Product.objects.select_related("category")
        .annotate(
            product_srp_price=Case(
                When(promo_price__gt=0, then=F("promo_price")),
                default=F("price"),
            )
        )
        .filter(sellable=True)
        .order_by("category")
    )
    if "min_price" in filters:
        products = products.filter(product_srp_price__gte=filters["min_price"])
    if "max_price" in filters:
        products = products.filter(product_srp_price__lte=filters["max_price"])
    return ProductFilter(filters, products).qs
