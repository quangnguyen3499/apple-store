from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from platform_backend.store.selectors.orders import get_order

from .models.payment import Payment
from .selectors import get_payment_detail, get_invoice_by_id
from ..common.api.mixins import APIErrorsMixin
from ..common.api.permissions import IsCustomer
from ..mystripe.services import create_stripe_charge
from .services import create_payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
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
        currency = serializers.CharField()
        credit_card_id = serializers.CharField()

    def post(self, request, invoice_id):
        serializer = self.CreatePaymentRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cleaned_data = serializer.validated_data

        # TODO: apply invoice
        invoice = get_invoice_by_id(pk=invoice_id)
        create_payment(
            invoice=invoice,
            **cleaned_data,
        )
        create_stripe_charge(
            customer=request.user.customer.stripe_customer_id,
            amount=cleaned_data["amount"],
            description=cleaned_data["description"],
            currency=cleaned_data["currency"],
        )
        return Response("success", status=204)
