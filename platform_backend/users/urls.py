from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenBlacklistView,
)

user_patterns = [
    path(
        "api/v1/users/reset_mail/",
        views.SendMailForgotPasswordView.as_view(),
        name="send-mail-forgot-password",
    ),
    path(
        "api/v1/users/resend_active/",
        views.ResendActiveView.as_view(),
        name="resend-active-account",
    ),
    path(
        "api/v1/users/active/",
        views.ActiveAccountView.as_view(),
        name="active-account",
    ),
    path(
        "api/v1/users/change_password/",
        views.ChangeForgotPasswordView.as_view(),
        name="change-password",
    ),
    path(
        "api/v1/users/new_password/",
        views.NewPasswordView.as_view(),
        name="new-password",
    ),
    path(
        "api/v1/users/token/",
        views.MyTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/v1/users/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "api/v1/users/token/blacklist/",
        TokenBlacklistView.as_view(),
        name="token_blacklist",
    ),
    path(
        "api/v1/users/invoice/monthly/",
        views.SendInvoiceMonthlyView.as_view(),
        name="send_invoice_monthly",
    ),
]

customer_patterns = [
    path(
        "api/v1/users/customers/",
        views.CreateCustomerAPIView.as_view(),
        name="create-customer",
    ),
    path(
        "api/v1/users/customers/list/",
        views.ListCustomerView.as_view(),
        name="get-list-customer",
    ),
    path(
        "api/v1/users/customers/<int:user_id>",
        views.GetAndUpdateAndDeleteCustomerView.as_view(),
        name="get-update-delete-customer",
    ),
]

admin_patterns = [
    path(
        "api/v1/users/admins/",
        views.CreateAdminAPIView.as_view(),
        name="create-admin",
    ),
    path(
        "api/v1/users/admins/list/",
        views.ListAdminView.as_view(),
        name="get-list-admin",
    ),
]

urlpatterns = user_patterns + customer_patterns + admin_patterns
