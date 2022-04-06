# Generated by Django 4.0.3 on 2022-04-03 10:11

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evento',
            name='fecha',
            field=models.DateTimeField(validators=[django.core.validators.MinValueValidator(datetime.datetime(2022, 4, 4, 10, 11, 13, 911558))], verbose_name='Fecha'),
        ),
    ]
