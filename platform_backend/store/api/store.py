from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from platform_backend.common.api.permissions import IsAdmin
from platform_backend.common.api.mixins import APIErrorsMixin
from platform_backend.store.models.store import Store
from platform_backend.store.services.store import create_store
from platform_backend.store.selectors.store import get_store_detai_list


class CreatingStoreAPIView(APIErrorsMixin, APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    class CreatingStoreRequestSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=255)
        address = serializers.CharField(max_length=255)
        province = serializers.CharField(max_length=255)

    class CreatingStoreResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Store
            fields = "__all__"

    def post(self, request):
        serializer = self.CreatingStoreRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        store = create_store(
            data["name"],
            data["address"],
            data["province"],
        )
        store_data = self.CreatingStoreResponseSerializer(store).data
        return Response(store_data)


class StoreDetailAPIView(APIErrorsMixin, APIView):
    class StoreDetailRequestSerializer(serializers.Serializer):
        store_id = serializers.CharField(allow_null=True, default=None)

    class StoreDetailResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Store
            fields = "__all__"

    def get(self, request):
        serializer = self.StoreDetailRequestSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        store = get_store_detai_list(data["store_id"])
        store_data = self.StoreDetailResponseSerializer(store, many=True).data
        return Response(store_data)
