from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from platform_backend.common.api.mixins import APIErrorsMixin
from platform_backend.common.api.pagination import (
    LimitOffsetPagination,
    get_paginated_response,
)
from platform_backend.common.api.permissions import IsAdmin, IsCustomer

from platform_backend.users.models import Customer, User, Admin
from platform_backend.users.selectors import (
    get_user_by_email,
    get_user_by_token,
    user_list,
    get_user_by_id,
)
from platform_backend.users.services import (
    create_customer,
    send_mail_active_service,
    active_user,
    send_mail_reset_password_service,
    change_password,
    update_customer,
    delete_user,
    create_admin,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import threading


class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    status = serializers.CharField()

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "username", "status"]


class CustomerSerializer(serializers.ModelSerializer):
    address = serializers.CharField()
    city = serializers.CharField()
    province = serializers.CharField()
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = "__all__"


class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Admin
        fields = "__all__"


class CreateCustomerAPIView(APIView):
    class CreateCustomerRequestSerializer(serializers.Serializer):
        email = serializers.EmailField(max_length=254)
        first_name = serializers.CharField(max_length=150)
        last_name = serializers.CharField(max_length=150)
        password = serializers.CharField(max_length=128)
        address = serializers.CharField(max_length=254)
        city = serializers.CharField(max_length=254)
        province = serializers.CharField(max_length=254)

    def post(self, request):
        serializer = self.CreateCustomerRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cleaned_data = serializer.validated_data

        user_check = get_user_by_email(email=cleaned_data["email"])
        if user_check:
            raise ValidationError("duplicate email")

        customer = create_customer(**cleaned_data)
        token = customer.user.generate_token()
        t = threading.Thread(
            target=send_mail_active_service(
                email=customer.user.email, content="Activation mail", token=token
            ),
            args=(3,),
        )
        t.setDaemon(True)
        t.start()
        t.join()

        data = CustomerSerializer(customer).data
        return Response(data, status=201)


class ResendActiveView(APIView):
    class ResendActiveRequestSerializer(serializers.Serializer):
        email = serializers.EmailField()

    def post(self, request):
        serializer = self.ResendActiveRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cleaned_data = serializer.validated_data

        user = get_user_by_email(email=cleaned_data["email"])
        token = user.generate_token()
        send_mail_active_service(
            email=user.email, content="Activation mail", token=token
        )

        return Response("success", status=200)


class ActiveAccountView(APIView):
    class ActiveAccountRequestSerializer(serializers.Serializer):
        token = serializers.CharField()

    def post(self, request):
        serializer = self.ActiveAccountRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cleaned_data = serializer.validated_data

        active_user(token=cleaned_data["token"])
        return Response("active success", status=200)


class SendMailForgotPasswordView(APIView):
    class SendMailResetPasswordRequestSerializer(serializers.Serializer):
        email = serializers.EmailField()

    def post(self, request):
        serializer = self.SendMailResetPasswordRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cleaned_data = serializer.validated_data

        user = get_user_by_email(email=cleaned_data["email"])
        token = user.generate_token()
        send_mail_reset_password_service(
            email=user.email, content="Forgot password mail", token=token
        )

        return Response("success", status=200)


class NewPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    class NewPasswordRequestSerializer(serializers.Serializer):
        password1 = serializers.CharField()
        password2 = serializers.CharField()

    def post(self, request):
        serializer = self.NewPasswordRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cleaned_data = serializer.validated_data

        change_password(user=request.user, **cleaned_data)
        return Response({"message": "Success"})


class ChangeForgotPasswordView(APIView):
    class ChangePasswordRequestSerializer(serializers.Serializer):
        token = serializers.CharField()
        password1 = serializers.CharField()
        password2 = serializers.CharField()

    def post(self, request):
        serializer = self.ChangePasswordRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cleaned_data = serializer.validated_data

        user = get_user_by_token(token=cleaned_data["token"])
        change_password(user=user, **cleaned_data)
        return Response({"message": "Success"})


class ListCustomerView(APIErrorsMixin, APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    class Pagination(LimitOffsetPagination):
        default_limit = 50
        max_limit = 100

    class FilterSerializer(serializers.Serializer):
        first_name = serializers.CharField(default="", required=False, allow_blank=True)
        last_name = serializers.CharField(default="", required=False, allow_blank=True)
        username = serializers.CharField(default="", required=False, allow_blank=True)

    def get(self, request):
        filters = self.FilterSerializer(data=request.query_params)
        filters.is_valid(raise_exception=True)
        customers = user_list(filters=filters.validated_data, type=User.Types.CUSTOMER)
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=UserSerializer,
            queryset=customers,
            request=request,
            view=self,
        )


class GetAndUpdateAndDeleteCustomerView(APIErrorsMixin, APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    class UpdateRequestSerializer(serializers.Serializer):
        first_name = serializers.CharField(default="", required=False, allow_blank=True)
        last_name = serializers.CharField(default="", required=False, allow_blank=True)
        username = serializers.CharField(default="", required=False, allow_blank=True)
        address = serializers.CharField(default="", required=False, allow_blank=True)
        city = serializers.CharField(default="", required=False, allow_blank=True)
        province = serializers.CharField(default="", required=False, allow_blank=True)

    def get(self, request):
        user = get_user_by_id(id=request.user.id)
        data = UserSerializer(user).data
        return Response(data, status=200)

    def put(self, request):
        user = get_user_by_id(id=request.user.id)
        serializer = self.UpdateRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = update_customer(user=user, **serializer.validated_data)
        data = UserSerializer(user).data
        return Response(data, status=200)

    def delete(self, request):
        user = get_user_by_id(id=request.user.id)
        delete_user(user=user)
        return Response("success", status=204)


class CreateAdminAPIView(APIView):
    class CreateAdminRequestSerializer(serializers.Serializer):
        email = serializers.EmailField(max_length=254)
        first_name = serializers.CharField(max_length=150)
        last_name = serializers.CharField(max_length=150)
        password = serializers.CharField(max_length=128)

    def post(self, request):
        serializer = self.CreateAdminRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cleaned_data = serializer.validated_data

        user_check = get_user_by_email(email=cleaned_data["email"])
        if user_check:
            raise ValidationError("duplicate email")

        admin = create_admin(**cleaned_data)
        token = admin.user.generate_token()
        t = threading.Thread(
            target=send_mail_active_service(
                email=admin.user.email, content="Activation mail", token=token
            ),
            args=(3,),
        )
        t.setDaemon(True)
        t.start()
        t.join()
        data = AdminSerializer(admin).data
        return Response(data, status=201)


class ListAdminView(APIErrorsMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 50
        max_limit = 100

    class FilterSerializer(serializers.Serializer):
        first_name = serializers.CharField(default="", required=False, allow_blank=True)
        last_name = serializers.CharField(default="", required=False, allow_blank=True)
        username = serializers.CharField(default="", required=False, allow_blank=True)

    def get(self, request):
        filters = self.FilterSerializer(data=request.query_params)
        filters.is_valid(raise_exception=True)
        customers = user_list(filters=filters.validated_data, type=User.Types.ADMIN)
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=UserSerializer,
            queryset=customers,
            request=request,
            view=self,
        )


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        if user.status == user.Status.DEACTIVATED:
            raise ValidationError("User is deactivated")
        token = super().get_token(user)
        breakpoint()
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
