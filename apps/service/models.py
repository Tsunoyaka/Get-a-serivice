from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Service(models.Model):
    user_id = models.ForeignKey(User, related_name='user_service', on_delete=models.SET_NULL, null=True, default="")
    stack = models.ManyToManyField('base.Stack', related_name='stack', blank=True)
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

    type = models.CharField(choices=TYPE, max_length=255, verbose_name='Тип Цены', blank=True)


    def save(self,*args, **kwargs):
        if self.price == 0:
            self.type = 'For free'
        super().save(*args, **kwargs)


    def __str__(self) -> str:
        return str(self.user_id)
    
    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"