from django.urls import path
from . import views

urlpatterns = [
    path(
        "api/v1/ratings/tags/",
        views.TagListView.as_view(),
        name="get-list-tags",
    ),
    path(
        "api/v1/ratings/rate_product/",
        views.ApplyRatingItem.as_view(),
        name="apply-rating-product",
    ),
    path(
        "api/v1/ratings/edit_rating/",
        views.EditRatingItem.as_view(),
        name="edit-rating-product",
    ),
]
