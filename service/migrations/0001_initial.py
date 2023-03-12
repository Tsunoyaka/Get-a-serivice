# Generated by Django 4.1.7 on 2023-03-12 14:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stack', models.CharField(max_length=90, verbose_name='Стек')),
                ('price', models.IntegerField(default=1000, verbose_name='Цена')),
                ('experience', models.CharField(max_length=255, verbose_name='Опыт')),
                ('photo', models.ImageField(blank=True, default='', null=True, upload_to='media', verbose_name='Изображение')),
                ('description', models.CharField(max_length=255, verbose_name='Описание')),
                ('type', models.CharField(choices=[('Cash', 'Наличные'), ('PVC', 'Через карту'), ('Negotiable', 'Договорное')], default='cash', max_length=255, verbose_name='Тип')),
                ('user_id', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_service', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Услуга',
                'verbose_name_plural': 'Услуги',
            },
        ),
    ]
