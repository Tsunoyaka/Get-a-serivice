from django.shortcuts import HttpResponse
from telebot import TeleBot
from telebot.types import (
    Message, 
    InlineKeyboardMarkup, 
    InlineKeyboardButton, 
    Update
    )
from django.views.decorators.csrf import csrf_exempt
from apps.statement.models import Statement
import json
import requests
from django.conf import settings


bot = TeleBot(settings.TELEBOT_TOKEN)


@csrf_exempt
def index(request):
    bot.set_webhook('https://cf8f-185-117-149-123.eu.ngrok.io')
    if request.method == "POST":
        update = Update.de_json(request.body.decode('utf-8'))
        bot.process_new_updates([update])

    return HttpResponse('<h1>Что бы перейти к свагеру напишите после домена сайтa /swagger/</h1>' 
                        '<h2>Пример: http://127.0.0.1:8000/swagger/</h2>')


@bot.message_handler(commands=['start'])
def start(message: Message):
    chat_id = message.chat.id
    user = message.from_user.id
    bot.send_message(chat_id=chat_id, text='Привет, дорогой ментор.\n'
                    f'Пожалуйста введите следующее значения в свой профиль на нашем сайте: *{user}*',
                    parse_mode='Markdown')
    

def mentor_response(instance: Statement):
    accepted = json.dumps({'accepted': instance.accepted_code})
    denied = json.dumps({'denied': instance.denied_code})
    keyboard = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton('Принять', callback_data=accepted)
    btn2 = InlineKeyboardButton('Отклонить', callback_data=denied)
    keyboard.add(btn1, btn2)
    chat_id = instance.mentor_service.telegram
    message = f"""Вам пришла новая заявка (◕‿◕✿)\n
*Имя*
_{instance.name}_\n
*Email*
_{instance.email}_\n
*Telegram*
_@{instance.telegram}_\n
*O чём хотите поговорить?*
_{instance.description}_\n
*Как вы оцениваете свой уровень?*
_{instance.my_level}_"""
    bot.send_message(chat_id=chat_id, text=message, 
                     parse_mode='Markdown', reply_markup=keyboard)


def response_statement(response, type_):
    if type_ == 'accepted':
        requests.get(url=f'http://127.0.0.1:8000/statement/accepted-email/{response}/')
    else:
        requests.get(url=f'http://127.0.0.1:8000/statement/denied-email/{response}/')


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    for key, values in json.loads(call.data).items():
        if key == 'accepted':
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, 
                                          message_id=call.message.message_id, 
                                          reply_markup=None)
            bot.send_message(chat_id=call.message.chat.id, text='*Вы приняли заявление!*\n'
                            'Если хотите поменять свой ответ зайдите в свой профиль на сайте (◕‿◕✿)',
                            parse_mode='Markdown')
            response_statement(response=values, type_=key)
        else:
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, 
                                          message_id=call.message.message_id, 
                                          reply_markup=None)
            bot.send_message(chat_id=call.message.chat.id, text='*Вы отклонили заявление!*\n'
                            'Если хотите поменять свой ответ зайдите в свой профиль на сайте (◕‿◕✿)',
                            parse_mode='Markdown')
            response_statement(response=values, type_=key)
    