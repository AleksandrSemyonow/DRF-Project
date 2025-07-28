from django.shortcuts import render
from rest_framework.generics import ListAPIView
from payment.serializers import PaymentSerializer
from payment.models import Payment
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class PaymentApiView(ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["paid_course", "paid_lesson", "payment_method"]
    ordering_fields = ["payment_data",]
