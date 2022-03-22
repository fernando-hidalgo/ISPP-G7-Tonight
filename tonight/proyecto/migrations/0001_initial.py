# Generated by Django 4.0.3 on 2022-03-17 18:47

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
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saldo', models.PositiveIntegerField()),
                ('tlf', models.PositiveIntegerField()),
                ('imagen', models.ImageField(blank=True, upload_to='')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_c', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tlf', models.PositiveIntegerField()),
                ('imagen', models.ImageField(blank=True, upload_to='')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_eprs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fech', models.DateTimeField()),
                ('totalEntradas', models.PositiveIntegerField()),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('ubicacion', models.CharField(max_length=100)),
                ('salt', models.CharField(max_length=100)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='empresa', to='proyecto.empresa')),
            ],
        ),
        migrations.CreateModel(
            name='Entrada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechCompra', models.DateTimeField()),
                ('fechCaducidad', models.DateTimeField()),
                ('estado', models.CharField(choices=[('E', 'En venta'), ('A', 'Adquirida'), ('V', 'Vendida'), ('U', 'Usada'), ('C', 'Caducada')], max_length=1)),
                ('hash', models.CharField(blank=True, max_length=100)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cliente', to='proyecto.cliente')),
                ('evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evento', to='proyecto.evento')),
            ],
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyecto.empresa')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_epld', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]