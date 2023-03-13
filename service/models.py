from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Stack(models.Model):
    title = models.CharField(max_length=100, unique=True,verbose_name='Стек')

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = "Стек"
        verbose_name_plural = "Стеки"


class Service(models.Model):
    user_id = models.ForeignKey(User, related_name='user_service', on_delete=models.SET_NULL, null=True, default="")
    stack = models.ManyToManyField(Stack, related_name='stack', blank=True)
    price = models.PositiveIntegerField(default=100, verbose_name='Цена')
    experience = models.CharField(max_length=255, verbose_name='Опыт')
    photo = models.ImageField(upload_to='media', null=True, blank=True, verbose_name='Изображение', default="")
    description = models.CharField(max_length=255, verbose_name='Описание')

    TYPE = [
        ('Cash', 'Наличные'),
        ('PVC', 'Через карту'),
        ('Negotiable', 'Договорно'),
        ('For free', 'Бесплатно'),
    ]

    type = models.CharField(choices=TYPE, max_length=255, verbose_name='Тип Цены')
        
    def __str__(self) -> str:
        return str(self.user_id)
    
    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    
class StackService(models.Model):
    stacks = models.CharField(max_length=100, verbose_name='Стек')
    service = models.ManyToManyField(Stack, blank=True, related_name='stack_service')

    class Meta:
        verbose_name = "Стек Услуги"
        verbose_name_plural = "Стеки Услуг"

    def __str__(self) -> str:
        return self.stacks
    
class UserStack(models.Model):
    stack = models.CharField(max_length=100, verbose_name='Стек')
    user = models.ManyToManyField(Stack, blank=True, related_name='user_stack')

    def __str__(self) -> str:
        return self.stack
    
    class Meta:
        verbose_name = "Юзер Стек"
        verbose_name_plural = "Юзер Стеки"






    
