from django.urls import path
from . import views
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

urlpatterns = [
    path('customers/', views.CreateCustomerAPIView.as_view(), name='create-user'),
]
