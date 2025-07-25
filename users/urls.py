from rest_framework.routers import SimpleRouter
from users.views import PaymentApiView
from users.apps import UsersConfig
from django.urls import path

app_name = UsersConfig.name

urlpatterns = [
    path("payment/", PaymentApiView.as_view(), name="payments_list"),
]

