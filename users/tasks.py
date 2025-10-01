from celery import shared_task
import datetime
from django.utils import timezone

from users.models import User


@shared_task
def check_user_activity():
    """
    Проверяем активность пользователя, если больше 30 дней, деактивируем
    """
    users = User.objects.filter(is_active=True, last_login__isnul=False)
    date_now = timezone.now()
    deactivate_time = datetime.timedelta(days=30)
    for user in users:
        if date_now - user.last_login > deactivate_time:
            user.is_active = False
            user.save()
