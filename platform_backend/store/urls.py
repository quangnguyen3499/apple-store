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

products_pattern = [
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
carts_pattern = [
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
    path(
        "api/v1/cart/checkout/",
        carts.CartCheckoutAPIView.as_view(),
        name="cart-checkout",
    ),
    path(
        "api/v1/cart/apply-promo/",
        carts.CartApplyDiscountAPIView.as_view(),
        name="cart-apply-promo",
    ),
]
orders_pattern = [
    # path(
    #     "api/v1/orders/cancel/",
    #     orders.OrderCancelAPIView.as_view(),
    #     name="order-cancel",
    # ),
]
urlpatterns = stores_pattern + products_pattern + carts_pattern + orders_pattern
