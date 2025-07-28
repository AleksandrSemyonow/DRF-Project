from django.core.management.base import BaseCommand
from users.models import User
from payment.models import Payment
from materials.models import Course, Lesson


class Command(BaseCommand):
    """Кастомная команда для создания платежей"""

    def handle(self, *args, **options):
        """Create user and payments"""

        # Create user
        params = dict(email='example@mail.com', password='qwerty')
        user, user_status = User.objects.get_or_create(**params)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        print('User created successfully.')

        # Create payments
        payment1 = {
            'user': user,
            'payment_data': '2022-01-01',
            'paid_course': Course.objects.get(pk=2),
            'paid_lesson': None,
            'payment_amount': 100,
            'payment_method': 'наличные'
        }
        payment2 = {
            'user': user,
            'payment_data': '2022-10-01',
            'paid_course': Course.objects.get(pk=2),
            'paid_lesson': Lesson.objects.get(pk=4),
            'payment_amount': 50,
            'payment_method': 'перевод'
        }
        payment3 = {
            'user': user,
            'payment_data': '2024-09-12',
            'paid_course': Course.objects.get(pk=2),
            'paid_lesson': Lesson.objects.get(pk=4),
            'payment_amount': 60,
            'payment_method': 'перевод'
        }
        [Payment.objects.create(**payment) for payment in (payment1, payment2, payment3)]
        print('Payment created successfully.')
