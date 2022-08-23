from django.urls import path
from . import api


app_name = "inventory"

urlpatterns = [
    path(
        "api/v1/inventory/list/",
        api.ProductInventoryListAPIView.as_view(),
        name="inventories_list",
    ),
    path(
        "api/v1/stock/creating/",
        api.CreatingStockAPIView.as_view(),
        name="stock-creating",
    ),
    path(
        "api/v1/stock/list/",
        api.StockListAPIView.as_view(),
        name="stock-list",
    ),
]
