# Generated by Django 2.1.2 on 2019-02-22 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Operarios', '0012_auto_20190221_1524'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='relevamientodet',
            options={'verbose_name_plural': 'Servicios Especificos'},
        ),
        migrations.RemoveField(
            model_name='relevamientocupohoras',
            name='cantHoras',
        ),
        migrations.AddField(
            model_name='relevamientocab',
            name='cantAprendices',
            field=models.IntegerField(blank=True, null=True, verbose_name='Cantidad de Aprendices'),
        ),
        migrations.AddField(
            model_name='relevamientocupohoras',
            name='cantCHoras',
            field=models.IntegerField(blank=True, db_column='cantHoras', null=True, verbose_name='Cantidad de Horas'),
        ),
    ]
