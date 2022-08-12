from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from platform_backend.users.models import Customer, User
from platform_backend.users.selectors import get_user_by_email, get_user_by_token
from platform_backend.users.services import (
    create_customer, 
    send_mail_active_service, 
    active_user,
    send_mail_reset_password_service,
    change_password
)

class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    status = serializers.CharField()

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'username', 'status']

class CustomerSerializer(serializers.ModelSerializer):
    address = serializers.CharField()
    city = serializers.CharField()
    province = serializers.CharField()
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = '__all__'

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
        send_mail_active_service(email=customer.user.email, content="Activation mail", token=token)

        data = CustomerSerializer(customer).data
        return Response(data, status=201)

class ResendActiveView(APIView):
    class ResendActiveRequestSerializer(serializers.Serializer):
        email = serializers.EmailField()

    def post(self, request):
        serializer = self.ResendActiveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cleaned_data = serializer.validated_data

        user = get_user_by_email(email=cleaned_data["email"])
        token = user.generate_token()
        send_mail_active_service(email=user.email, content="Activation mail", token=token)

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

class SendMailResetPasswordView(APIView):
    class SendMailResetPasswordRequestSerializer(serializers.Serializer):
        email = serializers.EmailField()

    def post(self, request):
        serializer = self.SendMailResetPasswordRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cleaned_data = serializer.validated_data

        user = get_user_by_email(email=cleaned_data["email"])
        token = user.generate_token()
        send_mail_reset_password_service(email=user.email, content="Reset password mail", token=token)

        return Response("success", status=200)

class ChangePasswordView(APIView):
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
