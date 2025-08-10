from rest_framework.routers import SimpleRouter
from payment.views import PaymentListView, PaymentCreateView, PaymentDetailView, PaymentUpdateView, PaymentDestroyView
from payment.apps import PaymentConfig
from django.urls import path


app_name = PaymentConfig.name

urlpatterns = [
    path('payment/', PaymentListView.as_view(), name='payments_list'),
    path('payment/create/', PaymentCreateView.as_view(), name='payments_create'),
    path('payment/detail/<int:pk>/', PaymentDetailView.as_view(), name='payments_detail'),
    path('payment/update/<int:pk>/', PaymentUpdateView.as_view(), name='payments_update'),
    path('payment/delete/<int:pk>/', PaymentDestroyView.as_view(), name='payments_delete'),
]
