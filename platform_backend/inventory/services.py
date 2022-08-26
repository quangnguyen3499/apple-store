import datetime

from django.db import transaction
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from .models import Stock, ProductImport, Inventory, ProductStock
from .selectors import get_stock
from platform_backend.store.selectors.products import get_product_by_id


def creat_stock(name: str, address: str, province: str) -> Stock:
    try:
        Stock.objects.get(name=name, address=address, province=province)
        raise ValidationError("Stock already exists")
    except Stock.DoesNotExist:
        stock = Stock.objects.create(name=name, address=address, province=province)
        return stock


@transaction.atomic
def import_product_to_stock(
    stock_id: int,
    product_id: int,
    quantity: int,
    batch: str,
    import_date: datetime,
    manufacturer: str,
):
    stock = get_stock(stock_id=stock_id)
    product = get_product_by_id(pk=product_id)
    product_import = ProductImport.objects.create(
        stock=stock,
        product=product,
        quantity=quantity,
        batch=batch,
        import_date=import_date,
        manufacturer=manufacturer,
    )
    try:
        inventory = Inventory.objects.get(product=product, stock=stock)
        inventory.add_inventory_qty(qty=quantity)
        inventory.save()
    except Inventory.DoesNotExist:
        Inventory.objects.create(
            product=product,
            quantity=quantity,
            stock=stock,
        )

    try:
        product_stock = ProductStock.objects.get(product=product)
        product_stock.add_total_qty(quantity)
        product_stock.save()
    except ProductStock.DoesNotExist:
        product_stock = ProductStock.objects.create(
            product=product,
            total_stock_qty=quantity,
            available_stock_qty=quantity,
        )

    return product_import
