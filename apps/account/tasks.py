from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.conf import settings


def send_activation_code(email, activation_code):
    send_mail(
        subject='Активируйте ваш аккаунт!',
        message=f"Ваш активационный код: {activation_code}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False
    )