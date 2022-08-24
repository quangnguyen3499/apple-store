from platform_backend.rating.models import ProductRatings, Tag
from django.db.models.query import QuerySet
from platform_backend.store.models.orders import Order
from platform_backend.store.models.products import Product


def tag_list(*, filters) -> QuerySet[Tag]:
    tags = Tag.objects.filter(**filters).all()
    return tags


def check_allow_edit_rating(*, order: Order, product: Product) -> bool:
    allow_rating = (
        ProductRatings.objects.select_related("rating")
        .filter(
            product=product,
            rating__order=order,
        )
        .first()
        .rating.allow_rating
    )

    return allow_rating & order.is_allowed_rating()


def check_allow_create_rating(*, order: Order, product: Product) -> bool:
    allow_rating = (
        ProductRatings.objects.select_related("rating")
        .filter(
            product=product,
            rating__order=order,
        )
        .exists()
    )

    return not allow_rating & order.is_allowed_rating()

def get_product_rating(*, order: Order, product: Product) -> ProductRatings:
    product_rating = ProductRatings.objects.filter(
        product=product,
        rating__order=order,
    ).first()
    return product_rating
