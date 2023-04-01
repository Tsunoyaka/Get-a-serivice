from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import Statement


def send_response(instance: Statement, response: bool):
    email = instance.email
    mentor = instance.mentor_service.username
    datetime = instance.create_at
    if response is True:
        html_message = render_to_string(
            'statement/accepted.html', 
            {'Fullname': mentor,
             'DateTime': datetime,
            })
        send_mail(
            subject='MentorKG - Вашу заявку приняли!',
            message='',
            from_email=settings.EMAIL_HOST_USER,
            html_message=html_message,
            recipient_list=[email]
        )
    else:
        html_message = render_to_string(
            'statement/denied.html', 
            {'Fullname': mentor,
             'DateTime': datetime,
            })
        send_mail(
            subject='MentorKG - Вашу заявку отклонили!',
            message='',
            from_email=settings.EMAIL_HOST_USER,
            html_message=html_message,
            recipient_list=[email]
        )
    


def send_respons_mentor(instance: Statement):
    email = instance.mentor_service.email
    accepted_code = instance.accepted_code
    denied_code = instance.denied_code
    accepted_link = f'http://127.0.0.1:8000/statement/accepted-email/{accepted_code}/'
    denied_link = f'http://127.0.0.1:8000/statement/denied-email/{denied_code}/'
    html_message = render_to_string(
        'statement/code_mail.html', 
        {'accepted_link': accepted_link, 
         'denied_link': denied_link,
         'name': instance.name,
         'email': instance.email,
         'telegram': instance.telegram,
         'description': instance.description,
         'my_level': instance.my_level}
        )
    send_mail(
        'Вам пришла заявка!',
        '',
        settings.EMAIL_HOST_USER,
        [email],
        html_message=html_message,
        fail_silently=False
    )