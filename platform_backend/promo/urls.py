from django.urls import path
from . import views


urlpatterns = [
    path(
        "api/v1/promos/",
        views.GetAvailableUserPromoAPIView.as_view(),
        name="get-available-user-promo",
    ),
]
