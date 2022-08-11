from .models import User
from django.core.exceptions import ObjectDoesNotExist

def get_user_by_email(*, email: str) -> User:
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        raise ObjectDoesNotExist("User does not exist.")
