# Generated by Django 5.2.1 on 2025-05-23 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('umamihouseapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='empleado',
            name='user',
        ),
        migrations.RemoveField(
            model_name='mesa',
            name='fecha_creacion',
        ),
        migrations.RemoveField(
            model_name='mesa',
            name='fecha_modificacion',
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='fecha_creacion',
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='fecha_modificacion',
        ),
        migrations.RemoveField(
            model_name='pedidolinea',
            name='fecha_creacion',
        ),
        migrations.RemoveField(
            model_name='pedidolinea',
            name='fecha_modificacion',
        ),
        migrations.RemoveField(
            model_name='plato',
            name='fecha_creacion',
        ),
        migrations.RemoveField(
            model_name='plato',
            name='fecha_modificacion',
        ),
        migrations.RemoveField(
            model_name='user',
            name='fecha_creacion',
        ),
        migrations.RemoveField(
            model_name='user',
            name='fecha_modificacion',
        ),
        migrations.AlterField(
            model_name='pedidolinea',
            name='cantidad',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='pedidolinea',
            name='precio_total',
            field=models.DecimalField(decimal_places=2, default=0.0, editable=False, max_digits=5),
        ),
        migrations.AlterField(
            model_name='pedidolinea',
            name='precio_unitario',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='plato',
            name='tipo_plato',
            field=models.CharField(choices=[('ENTRANTE', 'Entrante'), ('SUSHI', 'Sushi'), ('PLATO_PRINCIPAL', 'Plato_principal'), ('POSTRE', 'Postre'), ('BEBIDA', 'Bebida')], default='PLATO_PRINCIPAL', max_length=50),
        ),
        migrations.DeleteModel(
            name='Cliente',
        ),
        migrations.DeleteModel(
            name='Empleado',
        ),
    ]
