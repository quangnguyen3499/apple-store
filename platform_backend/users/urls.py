from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)

urlpatterns = [
    # user
    path('reset_mail/', views.SendMailResetPasswordView.as_view(), name="send-mail-reset-password"),
    path('resend_active/', views.ResendActiveView.as_view(), name="resend-active-account"),
    path('active/', views.ActiveAccountView.as_view(), name='active-account'),
    path('change_password/', views.ChangePasswordView.as_view(), name="change-password"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),

    # customer
    path('customers/', views.CreateCustomerAPIView.as_view(), name='create-customer'),
    # path('list', views.ListCustomerView.as_view(), name='get-list-customer'),
    # path('<int:user_id>', views.GetAndUpdateAndDeleteCustomerView.as_view(), name='get-update-delete-customer'),
    
    # admin
]
