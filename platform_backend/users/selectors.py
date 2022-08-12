from .models import User
from rest_framework.exceptions import NotFound

def get_user_by_email(*, email: str) -> User:
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        raise NotFound("User does not exist.")

def get_user_by_token(*, token: str) -> User:
    try:
        return User.objects.get(token=token)
    except User.DoesNotExist:
        raise NotFound("Token not valid")
