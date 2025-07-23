from django.shortcuts import render
from rest_framework.generics import ListAPIView
from users.serializers import PaymentSerializer
from users.models import Payment
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.filters import OrderingFilter


class PaymentApiView(ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["paid_course", "paid_lesson", "payment_method"]
    ordering_fields = ["payment_data",]
