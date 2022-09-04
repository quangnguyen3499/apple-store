from django.urls import path
from . import views

urlpatterns = [
    path(
        "api/v1/payments/<int:payment_id>/",
        views.PaymentDetailView.as_view(),
        name="get-payment-detail",
    ),
    path(
        "api/v1/payments/checkout/invoices/<int:invoice_id>/",
        views.CreatePayment.as_view(),
        name="create-payment",
    ),
]
