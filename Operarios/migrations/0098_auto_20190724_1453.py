# Generated by Django 2.1.2 on 2019-07-24 18:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Operarios', '0097_auto_20190724_1452'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistRelevamientoMensualeros',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mensuCantidad', models.IntegerField(blank=True, null=True, verbose_name='Cantidad de Mensualeros')),
                ('sueldo', models.IntegerField(blank=True, null=True, verbose_name='Sueldo')),
                ('vfechaInicio', models.DateTimeField(null=True, verbose_name='Fecha Inicio Reg')),
                ('vfechaFin', models.DateTimeField(null=True, verbose_name='Fecha Fin Reg')),
                ('vregistro', models.IntegerField(blank=True, null=True, verbose_name='Valor de Salario')),
                ('relevamientoCab', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Operarios.RelevamientoCab')),
                ('vactual', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Operarios.RelevamientoMensualeros')),
            ],
        )
    ]