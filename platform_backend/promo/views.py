from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from platform_backend.common.api.mixins import APIErrorsMixin
from platform_backend.common.api.permissions import IsCustomer

from .selectors import get_available_user_promos


class GetAvailableUserPromoAPIView(APIErrorsMixin, APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    class GetAvailableUserPromoRequestSerializer(serializers.Serializer):
        order_amount = serializers.FloatField()

    def get(self, request):
        serializer = self.GetAvailableUserPromoRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        promos = get_available_user_promos(
            user=request.user,
            **serializer.validated_data,
        )
        return Response(promos)
