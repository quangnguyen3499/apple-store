from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from platform_backend.common.api.mixins import APIErrorsMixin
from platform_backend.common.api.pagination import (
    LimitOffsetPagination,
    get_paginated_response,
)
from platform_backend.common.api.permissions import IsCustomer
from platform_backend.rating.models import ProductRatings, Tag, Rating
from platform_backend.store.selectors.orders import get_order
from platform_backend.store.selectors.products import get_product
from .selectors import check_allow_create_rating, check_allow_edit_rating, tag_list
from .services import apply_product_rating, edit_product_rating
from platform_backend.store.services.products import update_average_rating
from django.core.exceptions import ValidationError


class TagSerializer(serializers.ModelSerializer):
    tag_type = serializers.CharField()
    name = serializers.CharField()

    class Meta:
        model = Tag
        fields = "__all__"


class TagListView(APIErrorsMixin, APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    class Pagination(LimitOffsetPagination):
        default_limit = 50
        max_limit = 100

    class FilterSerializer(serializers.Serializer):
        tag_type = serializers.CharField()

    def get(self, request):
        filters = self.FilterSerializer(data=request.query_params)
        filters.is_valid(raise_exception=True)
        tags = tag_list(filters=filters.validated_data)
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=TagSerializer,
            queryset=tags,
            request=request,
            view=self,
        )


class ApplyRatingItem(APIErrorsMixin, APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    class ApplyRatingItemRequestSerializer(serializers.Serializer):
        order_id = serializers.CharField()
        product_id = serializers.IntegerField()
        rating = serializers.IntegerField()
        comment = serializers.CharField()
        list_tag_id = serializers.ListField()

    class ApplyRatingItemResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = ProductRatings
            fields = "__all__"

    def post(self, request):
        serializer = self.ApplyRatingItemRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cleaned_data = serializer.validated_data

        order = get_order(pk=cleaned_data["order_id"])
        product = get_product(pk=cleaned_data["product_id"])
        rating = apply_product_rating(
            user=request.user,
            order=order,
            product=product,
            rating=cleaned_data["rating"],
            comment=cleaned_data["comment"],
        )
        update_average_rating(product_id=cleaned_data["product_id"])
        response = self.ApplyRatingItemResponseSerializer(rating).data
        return Response(response)


class ApplyRatingItem(APIErrorsMixin, APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    class ApplyRatingItemRequestSerializer(serializers.Serializer):
        order_id = serializers.CharField()
        product_id = serializers.IntegerField()
        rating = serializers.IntegerField()
        comment = serializers.CharField()
        list_tag_id = serializers.ListField()

    class ApplyRatingItemResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = ProductRatings
            fields = "__all__"

    def post(self, request):
        serializer = self.ApplyRatingItemRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cleaned_data = serializer.validated_data

        order = get_order(pk=cleaned_data["order_id"])
        product = get_product(pk=cleaned_data["product_id"])
        rating = apply_product_rating(
            user=request.user,
            order=order,
            product=product,
            rating=cleaned_data["rating"],
            comment=cleaned_data["comment"],
        )
        update_average_rating(product_id=cleaned_data["product_id"])
        response = self.ApplyRatingItemResponseSerializer(rating).data
        return Response(response)


class ApplyRatingItem(APIErrorsMixin, APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    class ApplyRatingItemRequestSerializer(serializers.Serializer):
        order_id = serializers.CharField()
        product_id = serializers.IntegerField()
        rating = serializers.IntegerField()
        comment = serializers.CharField()
        list_tag_id = serializers.ListField()

    class ApplyRatingItemResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Rating
            fields = "__all__"

    def post(self, request):
        serializer = self.ApplyRatingItemRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cleaned_data = serializer.validated_data

        order = get_order(pk=cleaned_data["order_id"])
        product = get_product(pk=cleaned_data["product_id"])
        if not check_allow_create_rating(
            order=order,
            product=product,
        ):
            raise ValidationError("Order is not allowed rating!")

        rating = apply_product_rating(
            user=request.user,
            order=order,
            product=product,
            rating=cleaned_data["rating"],
            comment=cleaned_data["comment"],
            list_tag_id=cleaned_data["list_tag_id"],
        )
        update_average_rating(product_id=cleaned_data["product_id"])
        response = self.ApplyRatingItemResponseSerializer(rating).data
        return Response(response)


class EditRatingItem(APIErrorsMixin, APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    class EditRatingItemRequestSerializer(serializers.Serializer):
        order_id = serializers.CharField()
        product_id = serializers.IntegerField()
        rating = serializers.IntegerField()
        comment = serializers.CharField()
        list_tag_id = serializers.ListField()

    class EditRatingItemResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Rating
            fields = "__all__"

    def put(self, request):
        serializer = self.EditRatingItemRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cleaned_data = serializer.validated_data

        order = get_order(pk=cleaned_data["order_id"])
        product = get_product(pk=cleaned_data["product_id"])
        if not check_allow_edit_rating(
            order=order,
            product=product,
        ):
            raise ValidationError("Order is not allowed rating!")

        rating = edit_product_rating(
            order=order,
            product=product,
            rating=cleaned_data["rating"],
            comment=cleaned_data["comment"],
            list_tag_id=cleaned_data["list_tag_id"],
        )
        update_average_rating(product_id=cleaned_data["product_id"])
        response = self.EditRatingItemResponseSerializer(rating).data
        return Response(response)
