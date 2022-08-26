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

products_parttern = [
    path(
        "api/v1/product/category/creating",
        products.CreatingCategoryAPIView.as_view(),
        name="category-create",
    ),
    path(
        "api/v1/product/category/<int:category_id>/updating",
        products.UpdatingCategoryAPIView.as_view(),
        name="category-update",
    ),
    path(
        "api/v1/product/category/list",
        products.CategoriesListAPIView.as_view(),
        name="category-list",
    ),
    path(
        "api/v1/product/creating/",
        products.CreatingProductAPIView.as_view(),
        name="product_create",
    ),
    path(
        "api/v1/product/list/",
        products.ProductListAPIView.as_view(),
        name="product_list",
    ),
]
carts_parttern = [
    path(
        "api/v1/cart/item/update",
        carts.CartAddItemAPIView.as_view(),
        name="cart-update",
    ),
    path(
        "api/v1/cart/<str:pk>/detail/",
        carts.CartDetailAPIView.as_view(),
        name="cart-detail",
    ),
]
orders_parttern = []
urlpatterns = stores_pattern + products_parttern + carts_parttern + orders_parttern
