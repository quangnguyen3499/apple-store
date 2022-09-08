from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from ..store.selectors.orders import get_order

from .models import Payment, Invoice
from .selectors import get_payment_detail, get_invoice_by_id
from ..common.api.mixins import APIErrorsMixin
from ..common.api.permissions import IsCustomer
from ..mystripe.services import create_stripe_charge, create_stripe_invoice
from .services import create_payment, create_invoice


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = "__all__"


class PaymentDetailView(APIErrorsMixin, APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def get(self, request, payment_id):
        payment = get_payment_detail(pk=payment_id)
        return Response(PaymentSerializer(payment).data)


class CreateOnlinePayment(APIErrorsMixin, APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    class CreatePaymentRequestSerializer(serializers.Serializer):
        amount = serializers.IntegerField()
        description = serializers.CharField()
        credit_card_id = serializers.CharField()

    def post(self, request, invoice_id):
        serializer = self.CreatePaymentRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cleaned_data = serializer.validated_data

        invoice = get_invoice_by_id(pk=invoice_id)
        create_payment(
            invoice=invoice,
            **cleaned_data,
        )
        create_stripe_charge(
            customer=request.user.customer.stripe_customer_id,
            amount=cleaned_data["amount"],
            description=cleaned_data["description"],
            currency=invoice.currency,
        )
        return Response("success", status=200)


class CreateInvoice(APIErrorsMixin, APIView):
    class InvoiceRequestSerializer(serializers.Serializer):
        order_id = serializers.CharField()
        currency = serializers.CharField()

    def post(self, request):
        serializer = self.InvoiceRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cleaned_data = serializer.validated_data

        order = get_order(pk=cleaned_data["order_id"])
        create_stripe_invoice(
            customer=request.user.customer.stripe_customer_id,
            description=cleaned_data["description"],
            currency=invoice.currency,
            order=order,
        )
        invoice = create_invoice(
            user=request.user,
            order=order,
            currency=cleaned_data["currency"],
        )
        return Response(InvoiceSerializer(invoice).data)
