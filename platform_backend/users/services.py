from django.db import transaction
from django.utils.crypto import get_random_string
from django.core.exceptions import ValidationError
from django.core.mail import send_mail

from .selectors import get_user_by_token
from .models import Customer, User
from allauth.utils import generate_unique_username

@transaction.atomic
def create_user(
    *,
    email: str,
    first_name: str,
    last_name: str,
    password: str,
    type: str,
) -> User:
    unique = get_random_string(
        length=10, allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    )
    username = generate_unique_username([email, first_name, last_name, unique])
    user = User(
        email=email,
        username=username,
        first_name=first_name,
        last_name=last_name,
        type=type
    )

    user.set_password(password)
    user.save()
    return user

@transaction.atomic
def create_customer(
    *,
    email: str,
    password: str,
    first_name: str,
    last_name: str,
    address: str,
    city: str,
    province: str,
) -> Customer:
    user = create_user(
        email=email,
        first_name=first_name,
        last_name=last_name,
        password=password,
        type=User.Types.CUSTOMER
    )

    customer = Customer.objects.create(
        user=user,
        address=address,
        city=city,
        province=province
    )

    return customer

def send_mail_active_service(*, email: str, content: str, token: str):
    subject = content
    body = "Click url to active user: " + token
    to = [email]
    send_mail(subject, body, token, to)

def active_user(*, token: str):
    user = get_user_by_token(token=token)
    if not user.validate_token():
        raise ValidationError("token expires, please resend")

    user.status = User.Status.ACTIVE
    user.token = ""
    user.save()

def send_mail_reset_password_service(*, email: str, content: str, token: str):
    subject = content
    body = "Click url to reset password: " + token
    to = [email]
    send_mail(subject, body, token, to)

def change_password(*, user: User, token: str, password1: str, password2: str):
    if password1 != password2:
        raise ValidationError("password1 & 2 not match")
    user.set_password(password1)
    user.save()
