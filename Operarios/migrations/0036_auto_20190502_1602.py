# Generated by Django 2.1.2 on 2019-05-02 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Operarios', '0035_auto_20190502_1552'),
    ]

    operations = [
        migrations.AddField(
            model_name='planificacionesp',
            name='cantHoras',
            field=models.TimeField(blank=True, null=True, verbose_name='Cantidad de Horas'),
        ),
        migrations.AddField(
            model_name='planificacionope',
            name='corte',
            field=models.TimeField(blank=True, null=True, verbose_name='Corte'),
        ),
        migrations.AddField(
            model_name='planificacionope',
            name='total',
            field=models.TimeField(blank=True, null=True, verbose_name='Total'),
        ),
        migrations.AddField(
            model_name='relevamientocupohoras',
            name='cantCHoras',
            field=models.TimeField(blank=True, db_column='cantHoras', null=True, verbose_name='Cantidad de Horas'),
        ),
        migrations.AddField(
            model_name='relevamientoesp',
            name='cantHoras',
            field=models.TimeField(blank=True, null=True, verbose_name='Cantidad de Horas'),
        ),
    ]
