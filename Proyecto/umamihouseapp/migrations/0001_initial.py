# Generated by Django 5.2 on 2025-05-20 18:05
# Generated by Django 5.2.1 on 2025-05-20 17:28

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mesa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('EstadoMesa', models.CharField(choices=[('RESERVADA', 'Reservada'), ('OCUPADA', 'Ocupada'), ('DISPONIBLE', 'Disponible')], default='DISPONIBLE', max_length=50)),
                ('fecha_creacion', models.DateTimeField(default=django.utils.timezone.now)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Plato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.TextField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=5)),
                ('imagen', models.CharField(max_length=2000)),
                ('tipo_plato', models.CharField(choices=[('ENTRANTE', 'Entrante'), ('SUSHI', 'Sushi'), ('PLATO_PRINCIPAL', 'Plato_principal'), ('POSTRE', 'Postre'), ('BEBIDA', 'Bebida')], default='ENTRANTE', max_length=50)),
                ('estado_plato', models.BooleanField(default=True)),
                ('fecha_creacion', models.DateTimeField(default=django.utils.timezone.now)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status')),
                ('nombre', models.CharField(blank=True, max_length=100, verbose_name='nombre')),
                ('apellido', models.CharField(blank=True, max_length=100, verbose_name='apellido')),
                ('telefono', models.CharField(blank=True, max_length=100, verbose_name='telefono')),
                ('fecha_nacimiento', models.DateField(null=True, verbose_name='fecha_nacimiento')),
                ('rol', models.CharField(choices=[('ADMIN', 'Administrador'), ('COCINERO', 'Cocinero'), ('CAMARERO', 'Camarero'), ('CLIENTE', 'Cliente')], default='CLIENTE', max_length=10)),
                ('fecha_creacion', models.DateTimeField(default=django.utils.timezone.now)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('alta_usuario', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=150)),
                ('fecha_nacimiento', models.DateField()),
                ('mail', models.EmailField(max_length=150)),
                ('imagen_url', models.CharField(max_length=1000)),
                ('fecha_creacion', models.DateTimeField(default=django.utils.timezone.now)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreCompleto', models.CharField(max_length=500)),
                ('fecha_nacimiento', models.DateField()),
                ('mail', models.EmailField(max_length=150)),
                ('imagen_url', models.CharField(max_length=1000)),
                ('rol', models.CharField(choices=[('ADMIN', 'Administrador'), ('COCINERO', 'Cocinero'), ('CAMARERO', 'Camarero'), ('CLIENTE', 'Cliente')], default='COCINERO', max_length=50)),
                ('fecha_creacion', models.DateTimeField(default=django.utils.timezone.now)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(blank=True, max_length=100)),
                ('fecha', models.DateTimeField()),
                ('estado', models.IntegerField(choices=[(1, 'Preparando'), (2, 'En proceso'), (3, 'Finalizado')], default=1)),
                ('fecha_creacion', models.DateTimeField(default=django.utils.timezone.now)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='pedidos', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PedidoLinea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('precio_unitario', models.DecimalField(decimal_places=2, max_digits=5)),
                ('precio_total', models.DecimalField(decimal_places=2, editable=False, max_digits=5)),
                ('fecha_creacion', models.DateTimeField(default=django.utils.timezone.now)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='umamihouseapp.pedido')),
                ('plato', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='umamihouseapp.plato')),
            ],
        ),
    ]
