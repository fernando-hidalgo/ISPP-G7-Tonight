# Generated by Django 4.0.3 on 2022-03-27 11:17

import datetime
import django.core.validators
from django.db import migrations, models
from django.utils.timezone import utc
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0008_alter_evento_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='tlf',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True),
        ),
        migrations.AlterField(
            model_name='evento',
            name='fecha',
            field=models.DateTimeField(validators=[django.core.validators.MinValueValidator(datetime.datetime(2022, 3, 28, 11, 17, 40, 452703, tzinfo=utc))], verbose_name='YYYY-MM-DD HH:mm'),
        ),
    ]