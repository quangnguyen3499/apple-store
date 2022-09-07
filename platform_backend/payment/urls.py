from django.urls import path
from . import views

payment_patterns = [
    path(
        "api/v1/payments/<int:payment_id>/",
        views.PaymentDetailView.as_view(),
        name="get-payment-detail",
    ),
    path(
        "api/v1/payments/invoices/<str:invoice_id>/online/",
        views.CreateOnlinePayment.as_view(),
        name="create-online-payment",
    ),
]

invoice_patterns = [
    # path(
    #     "api/v1/invoices/",
    #     views.CreateInvoiceView.as_view(),
    #     name="create-invoice",
    # ),
]

urlpatterns = payment_patterns + invoice_patterns
