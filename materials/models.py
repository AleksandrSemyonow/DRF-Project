from django.db import models


class Course(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Название",
        help_text="Введите название курса",
    )

    preview = models.ImageField(
        upload_to="materials/preview",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Загрузите фото",
    )

    description = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        verbose_name="Описание курса",
        help_text="Введите описание курса",
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Название",
        help_text="Введите описание урока"
    )

    description = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        verbose_name="Описание",
        help_text="Введите описание урока"
    )

    course = models.ForeignKey(
        Course,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        help_text="Укажите курс"
    )

    preview = models.ImageField(
        upload_to="materials/lesson_preview",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Загрузите фото"
    )

    video_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="Видеоурок"
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
