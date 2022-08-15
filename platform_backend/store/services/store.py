from django.core.exceptions import ObjectDoesNotExist, ValidationError

from platform_backend.store.models.store import Store


def create_store(
    name: str,
    address: str,
    province: str,
):
    try:
        store = Store.objects.get(name=name, address=address, province=province)
        if store:
            raise ValidationError("store is already created")
    except Store.DoesNotExist:
        store = Store.objects.create(name=name, address=address, province=province)
    return store
