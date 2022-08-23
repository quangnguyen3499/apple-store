from django.core.exceptions import ObjectDoesNotExist, ValidationError

from ..models.products import Product, Categories
from ..selectors.store import get_store
from ..selectors.products import get_category


def create_categories(name: str) -> Categories:
    try:
        Categories.objects.get(name=name)
        raise ValidationError("Category is already exist")
    except Categories.DoesNotExist:
        category = Categories.objects.create(name=name)
        return category


def update_categories(category_id: int, name: str) -> Categories:
    try:
        category = Categories.objects.get(id=category_id)
        category.name = name
        category.save()
        return category
    except Categories.DoesNotExist:
        raise ValidationError("category does not exist")


def create_product(
    store_id: str,
    category_id: int,
    name: str,
    unit_of_measurement: str,
    price: float,
    promo_price: float,
    sale_percent: int,
) -> Product:
    store = get_store(store_id=store_id)
    category = get_category(category_id=category_id)

    product, _ = Product.objects.update_or_create(
        store=store,
        category=category,
        name=name,
        unit_of_measurement=unit_of_measurement,
        default_price=price,
        promo_price=promo_price,
        sale_percent=sale_percent,
    )

    return product
