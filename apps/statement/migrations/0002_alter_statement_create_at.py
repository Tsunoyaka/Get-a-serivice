# Generated by Django 4.1.7 on 2023-03-13 16:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statement', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statement',
            name='create_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 3, 13, 22, 22, 42, 478959)),
        ),
    ]
