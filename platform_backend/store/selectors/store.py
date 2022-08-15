import django_filters
from django.db.models.query import QuerySet

from platform_backend.store.models.store import Store


def get_store_detai_list(store_id: str) -> Store:
    if store_id is None:
        store = Store.objects.all()
    else:
        store = Store.objects.get(id=store_id)
    return store
