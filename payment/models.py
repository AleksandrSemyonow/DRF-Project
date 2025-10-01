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
        blank=True,
        null=True,
        verbose_name="Пользователь",
        related_name="payment",
    )

    payment_data = models.DateField(
        blank=True,
        null=True,
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

    payment_amount = models.PositiveIntegerField(
        verbose_name="Сумма платежа"
    )

    payment_method = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        choices=PAYMENT_CHOICE,
        verbose_name="Способ оплаты"
    )

    payment_url = models.URLField(
        max_length=400,
        blank=True,
        null=True,
        verbose_name="Ссылка на оплату"
    )

    payment_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Идентификатор платежа"
    )

    def __str__(self):
        return f"{self.user} оплатил {self.payment_data}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
