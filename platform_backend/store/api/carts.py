import structlog

from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from platform_backend.common.utils import inline_serializer
from platform_backend.common.api.permissions import IsAdmin, IsCustomer
from platform_backend.common.api.mixins import APIErrorsMixin
from platform_backend.common.api.pagination import (
    LimitOffsetPagination,
    get_paginated_response,
)

from ..models.carts import Cart
from ..services.carts import add_item_to_cart, delete_item_from_cart
from ..selectors.carts import get_cart


logger = structlog.get_logger(__name__)


class CartLineItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    product = inline_serializer(
        fields={
            "id": serializers.CharField(),
            "name": serializers.CharField(),
            "image": inline_serializer(
                many=True,
                fields={
                    "url": serializers.CharField(),
                    "default": serializers.BooleanField(),
                },
            ),
            "srp_price": serializers.DecimalField(max_digits=19, decimal_places=4),
            "unit_of_measurement": serializers.CharField(),
            "stocks": inline_serializer(
                fields={
                    "available_stock_qty": serializers.IntegerField(),
                }
            ),
        },
    )
    quantity = serializers.IntegerField()
    has_enough_stock = serializers.BooleanField()
    subtotal = serializers.DecimalField(max_digits=19, decimal_places=4)


class CartSerializer(serializers.Serializer):
    cart_item = serializers.SerializerMethodField()
    promo = inline_serializer(
        many=True,
        fields={
            "promo": inline_serializer(
                fields={
                    "id": serializers.IntegerField(),
                    "code": serializers.CharField(),
                    "description": serializers.CharField(),
                    "discount_amount": serializers.DecimalField(
                        max_digits=19, decimal_places=4
                    ),
                }
            )
        },
    )
    total_items_amount = serializers.DecimalField(max_digits=19, decimal_places=4)

    class Meta:
        model = Cart
        fields = (
            "id",
            "owner",
            "store",
            "cart_item",
            "promo",
            "is_checked_out",
            "total_items_amount",
        )

    def get_cart_item(self, obj):
        return CartLineItemSerializer(obj.cart_item, many=True).data


class CartAddItemAPIView(APIErrorsMixin, APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    class CartAddItemRequestSerializer(serializers.Serializer):
        product_id = serializers.IntegerField()
        quantity = serializers.IntegerField()
        store_id = serializers.CharField()

    class CartDeleteItemRequestSerializer(serializers.Serializer):
        product_id = serializers.IntegerField()
        store_id = serializers.CharField()

    def post(self, request):
        serializer = self.CartAddItemRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        item = add_item_to_cart(
            product_id=data["product_id"],
            quantity=data["quantity"],
            store_id=data["store_id"],
            user=request.user,
        )
        item_data = CartSerializer(item).data
        return Response(item_data)

    def delete(self, request):
        serializer = self.CartDeleteItemRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        cart = delete_item_from_cart(
            product_id=data["product_id"],
            store_id=data["store_id"],
            user=request.user,
        )
        cart_data = CartSerializer(cart).data
        return Response(cart_data)


class CartDetailAPIView(APIErrorsMixin, APIView):
    def get(self, request, pk):
        cart = get_cart(pk=pk)
        cart_data = CartSerializer(cart).data
        return Response(cart_data)
