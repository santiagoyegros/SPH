# Generated by Django 2.1.2 on 2019-06-16 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Operarios', '0068_dialibre'),
    ]

    operations = [
        migrations.CreateModel(
            name='OperariosAsignacionDet',
            fields=[
                ('id_operario', models.IntegerField(db_column='id_opeario', primary_key=True, serialize=False, verbose_name=' ')),
                ('nombres', models.CharField(db_column='nombres', max_length=200, verbose_name='Nombres')),
                ('nroLegajo', models.CharField(db_column='nroLegajo', max_length=6, verbose_name='Numero de legajo')),
                ('nombres_puntoServicio', models.CharField(db_column='nombres_puntoServicio', max_length=200, verbose_name='Nombres Puntos de Servicio')),
                ('ids_puntoServicio', models.CharField(db_column='ids_puntoServicio', max_length=100, verbose_name=' ')),
                ('totalHoras', models.FloatField(db_column='totalHoras', verbose_name='Total Horas')),
                ('perfil', models.CharField(db_column='perfil', max_length=400, verbose_name='Perfil')),
                ('antiguedad', models.IntegerField(db_column='antiguedad', verbose_name='Antiguedad')),
            ],
            options={
                'verbose_name': 'Operario disponible',
                'verbose_name_plural': 'Operarios disponibles',
            },
        ),
    ]
