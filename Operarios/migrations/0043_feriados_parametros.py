# Generated by Django 2.1.2 on 2019-05-24 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Operarios', '0042_asignacionesprocesadas'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feriados',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anho', models.IntegerField(blank=True, null=True, verbose_name='Año')),
                ('fecha', models.DateField(null=True, verbose_name='Fecha Inicio Cobertura')),
                ('descripcion', models.CharField(max_length=200, verbose_name='Parametro')),
            ],
            options={
                'verbose_name': 'Parametro de Sistema',
                'verbose_name_plural': 'Parametros de Sistema',
            },
        ),
        migrations.CreateModel(
            name='Parametros',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=30, verbose_name='Tipo de Parametro')),
                ('parametro', models.CharField(max_length=50, verbose_name='Parametro')),
                ('valor', models.CharField(max_length=150, verbose_name='Parametro')),
            ],
            options={
                'verbose_name': 'Parametro de Sistema',
                'verbose_name_plural': 'Parametros de Sistema',
            },
        ),
    ]
