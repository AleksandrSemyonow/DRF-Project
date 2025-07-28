from django.db import models
from users.models import User
from materials.models import Course, Lesson


class Payment(models.Model):

    PAYMENT_CHOICE = [
        ("cash", "наличные"),
        ("transfer", "перевод на счет"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="payment",
    )

    payment_data = models.DateField(
        verbose_name="Дата оплаты",
    )

    paid_course = models.ForeignKey(
        Course,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Оплаченный курс",
        related_name="courses",
    )

    paid_lesson = models.ForeignKey(
        Lesson,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Оплаченный урок",
        related_name="lessons"
    )

    payment_amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Сумма платежа"
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICE,
        verbose_name="Способ оплаты"
    )

    def __str__(self):
        return f"{self.user} оплатил {self.payment_data}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
