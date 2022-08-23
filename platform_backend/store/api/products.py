from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from platform_backend.common.utils import inline_serializer
from platform_backend.common.api.permissions import IsAdmin
from platform_backend.common.api.mixins import APIErrorsMixin
from platform_backend.common.api.pagination import (
    LimitOffsetPagination,
    get_paginated_response,
)
from ..models.products import Product, Categories
from ..services.products import (
    create_categories,
    update_categories,
    create_product,
)
from ..selectors.products import get_list_of_all_product, get_list_of_all_category


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CreatingCategoryAPIView(APIErrorsMixin, APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    class CreatingCategoryRequestSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=255)

    class CreatingCategoryResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Categories
            fields = "__all__"

    def post(self, request):
        serializer = self.CreatingCategoryRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        category = create_categories(name=data["name"])
        category_data = self.CreatingCategoryResponseSerializer(category).data
        return Response(category_data)


class UpdatingCategoryAPIView(APIErrorsMixin, APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    class UpdatingCategoryRequestSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=255)

    class UpdatingCategoryResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Categories
            fields = "__all__"

    def post(self, request, category_id):
        serializer = self.UpdatingCategoryRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category = update_categories(
            category_id=category_id,
            name=serializer.validated_data["name"],
        )
        category_data = self.UpdatingCategoryResponseSerializer(category).data
        return Response(category_data)


class CategoriesListAPIView(APIErrorsMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 50
        max_limit = 100

    class CategoriesListFilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        name = serializers.CharField(required=False)

    class CategoriesListResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Categories
            fields = "__all__"

    def get(self, request):
        filters = self.CategoriesListFilterSerializer(data=request.query_params)
        filters.is_valid(raise_exception=True)
        categories = get_list_of_all_category(filters=filters.validated_data)
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.CategoriesListResponseSerializer,
            queryset=categories,
            request=request,
            view=self,
        )


class CreatingProductAPIView(APIErrorsMixin, APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    class CreatingProductRequestSerializer(serializers.Serializer):
        store_id = serializers.CharField(max_length=255)
        category_id = serializers.CharField(max_length=255)
        name = serializers.CharField(max_length=255)
        unit_of_measurement = serializers.CharField(max_length=50)
        price = serializers.DecimalField(max_digits=19, decimal_places=4)
        promo_price = serializers.DecimalField(
            max_digits=19, decimal_places=4, required=False
        )
        sale_percent = serializers.IntegerField(required=False)
        image = serializers.ImageField(required=False)

    def post(self, request):
        serializer = self.CreatingProductRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = create_product(**serializer.validated_data)
        product_data = ProductSerializer(product).data
        return Response(product_data)


class ProductListAPIView(APIErrorsMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 50
        max_limit = 100

    class ProductListFilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        category = serializers.CharField(required=False)
        name = serializers.CharField(required=False)
        search = serializers.CharField(required=False)
        min_price = serializers.IntegerField(required=False)
        max_price = serializers.IntegerField(required=False)

    def get(self, request):
        filters = self.ProductListFilterSerializer(data=request.query_params)
        filters.is_valid(raise_exception=True)
        products = get_list_of_all_product(filters=filters.validated_data)
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=ProductSerializer,
            queryset=products,
            request=request,
            view=self,
        )
