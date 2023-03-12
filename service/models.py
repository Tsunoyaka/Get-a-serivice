from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Service(models.Model):
    user_id = models.ForeignKey(User, related_name='user_service', on_delete=models.SET_NULL, null=True, default="")
    stack = models.CharField(max_length=90, verbose_name='Стек')
    price = models.IntegerField(default=1000, verbose_name='Цена')
    experience = models.CharField(max_length=255, verbose_name='Опыт')
    photo = models.ImageField(upload_to='media', null=True, blank=True, verbose_name='Изображение', default="")
    description = models.CharField(max_length=255, verbose_name='Описание')

    TYPE = [
        ('Cash', 'Наличные'),
        ('PVC', 'Через карту'),
        ('Negotiable', 'Договорное'),
    ]

    type = models.CharField(choices=TYPE, max_length=255, default='cash', verbose_name='Тип')


    
    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    
