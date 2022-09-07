import structlog
import stripe
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from platform_backend.common.utils import inline_serializer
from platform_backend.common.api.permissions import IsAdmin, IsCustomer
from platform_backend.common.api.mixins import APIErrorsMixin
from platform_backend.store.selectors.products import get_product_by_id

from ..models.carts import Cart
from ..models.orders import Order
from ..services.carts import add_item_to_cart, delete_item_from_cart, checkout_cart, apply_cart_discount
from ..selectors.carts import get_cart, get_user_cart

from django.conf import settings
from django.db import transaction

logger = structlog.get_logger(__name__)

# config stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


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
    promos = inline_serializer(
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


class CartDeliveryAddressSerializer(serializers.Serializer):
    address = serializers.CharField()
    city = serializers.CharField()
    province = serializers.CharField()


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


class CreateCheckoutSessionView(APIView):
    def post(self, request, product_id):
        product = get_product_by_id(pk=product_id)
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price": product.stripe_price_id,
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url=YOUR_DOMAIN + "/success/",
            cancel_url=YOUR_DOMAIN + "/cancel/",
        )
        return Response(checkout_session.url)


class CartCheckoutAPIView(APIErrorsMixin, APIView):
    class CartCheckoutRequestSerializer(serializers.Serializer):
        delivery_method = serializers.ChoiceField(choices=Order.DeliveryMethod.choices)
        delivery_address = CartDeliveryAddressSerializer(
            required=False, allow_null=True, default=None
        )
        payment_method = serializers.ChoiceField(choices=Order.PaymentMethod.choices)
        order_status = serializers.ChoiceField(choices=Order.OrderStatus.choices)

    def post(self, request):
        serializer = self.CartCheckoutRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            data = serializer.validated_data
            delivery_address = data["delivery_address"] if data["delivery_address"] else None
            order = checkout_cart(
                cart=get_user_cart(user=request.user),
                user=request.user,
                delivery_address=delivery_address,
                delivery_method=data["delivery_method"],
                payment_method=data["payment_method"],
                order_status=data["order_status"]
            )
        return Response({"order_id": order.id})

class CartApplyDiscountAPIView(APIErrorsMixin, APIView):
    class CartApplyDiscountRequestSerializer(serializers.Serializer):
        discount_type = serializers.ChoiceField(choices=Cart.DiscountTypes)
        code = serializers.CharField()

    def post(self, request):
        serializer = self.CartApplyDiscountRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        apply_cart_discount(cart=request.user.cart, **serializer.validated_data)

        return Response({"success": True})
