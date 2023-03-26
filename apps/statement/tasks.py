from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import Statement

def send_response(email: str, mentor: str, response: bool):
    if response is True:
        send_mail(
            subject='Вашу заявку приняли!',
            message=f'Вашу заявку принял ментор - {mentor}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email]
        )
    else:
        send_mail(
            subject='Вам было отказано',
            message=f'Ваша заявка откланена ментором - {mentor}',
            from_email=settings.EMAIL_HOST_USER,
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