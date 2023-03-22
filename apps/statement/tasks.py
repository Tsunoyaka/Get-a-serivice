from django.core.mail import send_mail
from django.conf import settings
from config.celery import app
from django.conf import settings


@app.task
def send_response(email: str, message: str, response: bool):
    if response is True:
        send_mail(
            subject='Вашу заявку приняли!',
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email]
        )
    else:
        send_mail(
            subject='Вам было отказано',
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email]
            ) 

@app.task    
def send_statement(email: str, name: str):
    send_mail(
        subject='Вам отправили заявку!',
        message=f'Вам пришла заявка от {name}.',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
        )