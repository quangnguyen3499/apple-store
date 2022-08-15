from django.urls import path

from .api import carts, products, orders, store

app_name = "store"

stores_pattern = [
    path(
        "api/v1/store/creating/",
        store.CreatingStoreAPIView.as_view(),
        name="store-create",
    ),
    path(
        "api/v1/store/detail/",
        store.StoreDetailAPIView.as_view(),
        name="store-detail",
    ),
]

urlpatterns = stores_pattern
