import pytest
from django.core.exceptions import ObjectDoesNotExist
from platform_backend.users.selectors import get_user_by_id, get_user_by_email

@pytest.mark.django_db
def test_get_user_by_id(user_factory):
    with pytest.raises(ObjectDoesNotExist):
        user = user_factory()
        id = user.id
        get_user_by_id(id=id)

@pytest.mark.django_db
def test_get_user_by_email(user_factory):
    user = user_factory()
    email = user.email
    assert get_user_by_email(email=email).email == email
