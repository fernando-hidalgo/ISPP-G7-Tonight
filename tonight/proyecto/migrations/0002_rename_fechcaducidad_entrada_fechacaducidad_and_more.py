# Generated by Django 4.0.3 on 2022-03-17 18:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entrada',
            old_name='fechCaducidad',
            new_name='fechaCaducidad',
        ),
        migrations.RenameField(
            model_name='entrada',
            old_name='fechCompra',
            new_name='fechaCompra',
        ),
        migrations.RenameField(
            model_name='evento',
            old_name='fech',
            new_name='fecha',
        ),
    ]
