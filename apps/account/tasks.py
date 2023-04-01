from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.conf import settings


def send_activation_code(email, activation_code):
    html_message = render_to_string(
        'account/code_mail.html',
        {'activation_code': activation_code}
    )
    send_mail(
        subject='MentorKG - Активационный код',
        message='',
        from_email=settings.EMAIL_HOST_USER,
        html_message=html_message,
        recipient_list=[email]
    )