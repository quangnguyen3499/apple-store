from .models import User, Customer
from rest_framework.exceptions import NotFound
from django.db.models.query import QuerySet
import django_filters
from django.db.models import Q

def get_user_by_id(*, id: int) -> User:
    try:
        return User.objects.get(pk=id)
    except:
        raise NotFound("User does not exist")

def get_user_by_email(*, email: str) -> User:
    return User.objects.filter(email=email).first()

def get_user_by_token(*, token: str) -> User:
    try:
        return User.objects.get(token=token)
    except User.DoesNotExist:
        raise NotFound("Token not valid")

def customer_list(*, filters=None) -> QuerySet[User]:
    filters = filters or {}
    customers = User.objects.filter(type=User.Types.CUSTOMER).all()
    return CustomerFilter(filters, customers).qs

class CustomerFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(method="search_filter", label="first_name")
    last_name = django_filters.CharFilter(method="search_filter", label="last_name")
    username = django_filters.CharFilter(method="search_filter", label="username")

    class Meta:
        model = Customer
        fields = ("first_name", "last_name", "username")

    def search_filter(self, queryset, value):
        return queryset.filter(
            Q(first_name__icontains=value)
            | Q(last_name__icontains=value)
            | Q(username__icontains=value)
        )
