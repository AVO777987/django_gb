from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings


def send_verify_mail(user):
    verify_link = reverse('authapp:verify', args=[user.email, user.activate_key])
    full_link = f'{settings.BASE_URL}{verify_link}'

    message = f'Ваша ссылка активации {full_link}'

    return send_mail(
        'Активация аккаунта',
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False
    )