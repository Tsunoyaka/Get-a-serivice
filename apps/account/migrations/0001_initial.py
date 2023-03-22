# Generated by Django 4.1.7 on 2023-03-22 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(blank=True, max_length=50, verbose_name='Full_name')),
                ('email', models.EmailField(blank=True, max_length=255, unique=True, verbose_name='Email')),
                ('image', models.ImageField(blank=True, upload_to='user_images')),
                ('position', models.CharField(blank=True, max_length=100)),
                ('place_of_work', models.CharField(blank=True, max_length=255)),
                ('stacks', models.CharField(blank=True, max_length=255)),
                ('about_me', models.CharField(blank=True, max_length=255)),
                ('help_org', models.CharField(blank=True, max_length=255)),
                ('level_mentor', models.CharField(blank=True, max_length=255)),
                ('experience', models.CharField(blank=True, max_length=255)),
                ('speciality', models.CharField(blank=True, max_length=255)),
                ('skills', models.CharField(blank=True, max_length=255)),
                ('price', models.CharField(blank=True, choices=[('Negotiable', 'Договорно'), ('For free', 'Бесплатно'), ('1000 сом', '1000 RUB'), ('2000 сом', '2000 RUB'), ('3000 сом', '3000 RUB'), ('4000 сом', '4000 RUB'), ('5000 сом', '5000 RUB'), ('6000 сом', '6000 RUB'), ('7000 сом', '7000 RUB'), ('8000 сом', '8000 RUB'), ('9000 сом', '9000 RUB'), ('10000 сом', '10000 RUB')], max_length=255)),
                ('is_active', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('activation_code', models.CharField(blank=True, max_length=8)),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
    ]
