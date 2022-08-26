from platform_backend.rating.selectors import get_product_rating
from .models import ProductRatings, Rating, RatingTags
from platform_backend.users.models import User
from django.db.models import F
from platform_backend.store.models.products import Product
from platform_backend.store.models.orders import Order
from typing import List


def create_rating_tags(
    *,
    rating_id: int,
    tag_id: int,
) -> RatingTags:
    rating_tag = RatingTags.objects.create(
        rating_id=rating_id,
        tag_id=tag_id,
    )
    return rating_tag


def delete_rating_tags(
    *,
    rating_id: int,
):
    RatingTags.objects.filter(rating_id=rating_id).delete()


def create_rating(
    *,
    user: User,
    order: Order,
    rating_type: str,
    rating: int,
    comment: str,
) -> Rating:
    rating = Rating.objects.create(
        user=user,
        order=order,
        rating_type=rating_type,
        rating=rating,
        comment=comment,
    )
    return rating


def apply_product_rating(
    *,
    user: User,
    order: Order,
    product: Product,
    rating: int,
    comment: str,
    list_tag_id: List[int],
) -> Rating:
    rating = create_rating(
        user=user,
        order=order,
        rating_type=Rating.Types.PRODUCT,
        comment=comment,
        rating=rating,
    )
    product_rating = ProductRatings.objects.create(
        product=product,
        rating=rating,
    )
    for tag_id in list_tag_id:
        create_rating_tags(
            rating_id=rating.id,
            tag_id=tag_id,
        )
    return rating


# edit once
def edit_product_rating(
    *,
    order: Order,
    product: Product,
    rating: int,
    comment: str,
    list_tag_id: List[int],
) -> Rating:
    rating_record = get_product_rating(
        order=order,
        product=product,
    ).rating
    rating_record.rating = rating
    rating_record.comment = comment
    rating_record.allow_rating = False
    rating_record.save()

    delete_rating_tags(rating_id=rating_record.id)
    for tag_id in list_tag_id:
        create_rating_tags(
            rating_id=rating_record.id,
            tag_id=tag_id,
        )
    return rating_record
