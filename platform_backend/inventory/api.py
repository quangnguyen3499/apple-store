from this import s
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from platform_backend.common.utils import inline_serializer
from platform_backend.common.api.permissions import IsAdmin
from platform_backend.common.api.mixins import APIErrorsMixin
from platform_backend.common.utils import inline_serializer
from platform_backend.common.api.pagination import (
    LimitOffsetPagination,
    get_paginated_response,
)


from .models import Inventory, Stock, ProductImport
from .selectors import (
    get_stock_of_product,
    get_stock_list,
    get_product_import,
)
from .services import creat_stock, import_product_to_stock


class ProductInventoryListAPIView(APIErrorsMixin, APIView):
    # permission_classes = [IsAuthenticated, IsAdmin]

    class Pagination(LimitOffsetPagination):
        default_limit = 50
        max_limit = 100

    class ProductInventoryListRequestSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        category = serializers.IntegerField(required=False)
        product = serializers.IntegerField(required=False)
        search = serializers.CharField(required=False)

    class ProductInventoryListResponseSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        product = inline_serializer(
            fields={
                "id": serializers.IntegerField(),
                "name": serializers.CharField(),
                "category": inline_serializer(
                    fields={
                        "name": serializers.CharField(),
                    }
                ),
                "unit_of_measurement": serializers.CharField(),
                "floor_price": serializers.DecimalField(
                    max_digits=19,
                    decimal_places=4,
                ),
                "price": serializers.DecimalField(
                    max_digits=19,
                    decimal_places=4,
                ),
                "promo_price": serializers.DecimalField(
                    max_digits=19,
                    decimal_places=4,
                ),
                "sale_percent": serializers.IntegerField(),
                "image": inline_serializer(
                    many=True,
                    fields={
                        "url": serializers.CharField(),
                        "default": serializers.BooleanField(),
                    },
                ),
                "sellable": serializers.BooleanField(),
                "items_sold": serializers.IntegerField(),
                "on_sale": serializers.BooleanField(),
            }
        )
        stock = inline_serializer(
            fields={"name": serializers.CharField()},
        )
        quantity = serializers.IntegerField()

        class Meta:
            model = Inventory
            fields = (
                "id",
                "product",
                "stock",
                "quantity",
            )

    def get(self, request):
        filters = self.ProductInventoryListRequestSerializer(data=request.query_params)
        filters.is_valid(raise_exception=True)
        inventories = get_stock_of_product(filters=filters.validated_data)
        print(inventories)
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.ProductInventoryListResponseSerializer,
            queryset=inventories,
            request=request,
            view=self,
        )


class CreatingStockAPIView(APIErrorsMixin, APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    class CreatingStockRequestSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=255)
        address = serializers.CharField(max_length=255)
        province = serializers.CharField(max_length=255)

    class CreatingStockResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Stock
            fields = "__all__"

    def post(self, request):
        serializer = self.CreatingStockRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        stock = creat_stock(
            name=data["name"],
            address=data["address"],
            province=data["province"],
        )
        stock_data = self.CreatingStockResponseSerializer(stock).data
        return Response(stock_data)


class StockListAPIView(APIErrorsMixin, APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    class StockListResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Stock
            fields = "__all__"

    def get(self, request):
        stock = get_stock_list()
        stock_data = self.StockListResponseSerializer(stock, many=True).data
        return Response(stock_data)


class ImportingProductAPIView(APIErrorsMixin, APIView):
    # permission_classes = [IsAuthenticated, IsAdmin]

    class ImportingProductRequestSerializer(serializers.Serializer):
        stock_id = serializers.IntegerField()
        product_id = serializers.IntegerField()
        quantity = serializers.IntegerField()
        batch = serializers.CharField()
        import_date = serializers.DateField()
        manufacturer = serializers.CharField()

    class ImportingProductResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = ProductImport
            fields = "__all__"

    def post(self, request):
        serializer = self.ImportingProductRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        product_import = import_product_to_stock(
            stock_id=data["stock_id"],
            product_id=data["product_id"],
            quantity=data["quantity"],
            batch=data["batch"],
            import_date=data["import_date"],
            manufacturer=data["manufacturer"],
        )
        product_import_data = self.ImportingProductResponseSerializer(
            product_import
        ).data
        return Response(product_import_data)


class ProductImportDetailAPIView(APIErrorsMixin, APIView):
    # permission_classes = [IsAuthenticated, IsAdmin]

    class Pagination(LimitOffsetPagination):
        default_limit = 50
        max_limit = 100

    class ProductImportDetailFilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        batch = serializers.CharField(required=False)
        product_id = serializers.IntegerField(required=False)
        search = serializers.CharField(required=False)

    class ProductImportDetailResponseSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        stock = inline_serializer(
            fields={
                "id": serializers.IntegerField(),
                "name": serializers.CharField(),
            }
        )
        product = inline_serializer(
            fields={
                "id": serializers.IntegerField(),
                "name": serializers.CharField(),
            }
        )
        quantity = serializers.IntegerField()
        batch = serializers.CharField()
        import_date = serializers.DateField()
        manufacturer = serializers.CharField()

    def get(self, request):
        filters = self.ProductImportDetailFilterSerializer(data=request.query_params)
        filters.is_valid(raise_exception=True)
        data = get_product_import(filters=filters.validated_data)
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.ProductImportDetailResponseSerializer,
            queryset=data,
            request=request,
            view=self,
        )
