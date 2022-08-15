import django_filters
from django.db.models.query import QuerySet
from django.core.exceptions import ObjectDoesNotExist, ValidationError


from platform_backend.store.models.store import Store


def get_store_detai_list(store_id: str):
    if store_id is None:
        store = Store.objects.all()
    else:
        try:
            store = Store.objects.filter(id=store_id)
        except Store.DoesNotExist:
            raise ValidationError("Store does not exist")
    return store
