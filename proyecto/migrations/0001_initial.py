import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import localflavor.es.models
import phonenumber_field.modelfields


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
                ('tlf', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True)),
                ('imagen', models.ImageField(blank=True, upload_to='media/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_c', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tlf', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True)),
                ('cif', localflavor.es.models.ESIdentityCardNumberField(max_length=9)),
                ('imagen', models.ImageField(blank=True, upload_to='media/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_eprs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(validators=[django.core.validators.MinValueValidator(datetime.datetime(2022, 4, 4, 17, 37, 20, 313382))], verbose_name='Fecha')),
                ('precioEntrada', models.PositiveIntegerField(verbose_name='Precio Entrada')),
                ('totalEntradas', models.PositiveIntegerField(verbose_name='Total Entradas')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('descripcion', models.TextField(max_length=500, verbose_name='Descripción')),
                ('ubicacion', models.CharField(max_length=100, verbose_name='Ubicación')),
                ('salt', models.CharField(max_length=100)),
                ('imagen', models.ImageField(blank=True, upload_to='media/', verbose_name='Imagen')),
                ('latitud', models.FloatField(verbose_name='Latitud')),
                ('longitud', models.FloatField(verbose_name='Longitud')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='empresa', to='proyecto.empresa')),
            ],
        ),
        migrations.CreateModel(
            name='Transaccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('V', 'Vender'), ('C', 'Comprar'), ('N', 'Neutralizar')], max_length=1)),
                ('fechaAudit', models.DateTimeField()),
                ('fechaLimite', models.DateTimeField()),
                ('done', models.BooleanField(default=False)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cliente_trans', to='proyecto.cliente')),
                ('evento', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='evento_trans', to='proyecto.evento')),
            ],
        ),
        migrations.CreateModel(
            name='Entrada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaCompra', models.DateTimeField()),
                ('fechaCaducidad', models.DateTimeField()),
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
