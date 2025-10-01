from django.shortcuts import render
from rest_framework import generics
from payment.serializers import PaymentSerializer
from payment.models import Payment
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from payment.services import create_stripe_price, create_stripe_session, convert_rub_to_dollars
from rest_framework.permissions import AllowAny


class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["paid_course", "paid_lesson", "payment_method"]
    ordering_fields = ["payment_data",]


class PaymentCreateView(generics.CreateAPIView):
    """
    Класс для создания нового платежа
    """
    serializer_class = PaymentSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        amount_in_dollars = convert_rub_to_dollars(payment.payment_amount)
        price = create_stripe_price(amount_in_dollars)
        payment_id, payment_url = create_stripe_session(price)
        payment.payment_id = payment_id
        payment.payment_url = payment_url
        payment.save()


class PaymentDetailView(generics.RetrieveAPIView):
    """
    Класс для просмотра подробной информации по платежу
    """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all


class PaymentUpdateView(generics.UpdateAPIView):
    """
    Класс для обновления данных по платежу
    """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all


class PaymentDestroyView(generics.DestroyAPIView):
    """
    Класс для удаления платежа
    """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all
