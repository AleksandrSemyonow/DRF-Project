from django.db import models
from django.contrib.auth.models import AbstractUser
from materials.models import Course, Lesson


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True,
        verbose_name="Почта",
        help_text="Укажите почту"
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Укажите телефон",
    )

    citi = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Укажите город",
    )

    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите ваше фото",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


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
