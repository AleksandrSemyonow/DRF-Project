from rest_framework.routers import SimpleRouter
from payment.views import PaymentApiView
from payment.apps import PaymentConfig
from django.urls import path


app_name = PaymentConfig.name

urlpatterns = [
    path("payments/", PaymentApiView.as_view(), name="payments_list"),
]
