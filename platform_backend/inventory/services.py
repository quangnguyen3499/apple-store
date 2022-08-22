from django.core.exceptions import ValidationError, ObjectDoesNotExist

from .models import Stock
from .selectors import get_stock


def creat_stock(name: str, address: str, province: str) -> Stock:
    try:
        Stock.objects.get(name=name, address=address, province=province)
        raise ValidationError("Stock already exists")
    except Stock.DoesNotExist:
        stock = Stock.objects.create(name=name, address=address, province=province)
        return stock
