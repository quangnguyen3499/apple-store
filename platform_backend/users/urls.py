from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenBlacklistView,
)

urlpatterns = [
    # user
    path(
        "reset_mail/",
        views.SendMailForgotPasswordView.as_view(),
        name="send-mail-forgot-password",
    ),
    path(
        "resend_active/",
        views.ResendActiveView.as_view(),
        name="resend-active-account",
    ),
    path(
        "active/",
        views.ActiveAccountView.as_view(),
        name="active-account",
    ),
    path(
        "change_password/",
        views.ChangeForgotPasswordView.as_view(),
        name="change-password",
    ),
    path(
        "new_password/",
        views.NewPasswordView.as_view(),
        name="new-password",
    ),
    path(
        "token/",
        views.MyTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "token/blacklist/",
        TokenBlacklistView.as_view(),
        name="token_blacklist",
    ),
    # customer
    path(
        "customers/",
        views.CreateCustomerAPIView.as_view(),
        name="create-customer",
    ),
    path(
        "customers/list/",
        views.ListCustomerView.as_view(),
        name="get-list-customer",
    ),
    path(
        "customers/<int:user_id>",
        views.GetAndUpdateAndDeleteCustomerView.as_view(),
        name="get-update-delete-customer",
    ),
    # admin
    path(
        "admins/",
        views.CreateAdminAPIView.as_view(),
        name="create-admin",
    ),
    path(
        "admins/list/",
        views.ListAdminView.as_view(),
        name="get-list-admin",
    ),
]
