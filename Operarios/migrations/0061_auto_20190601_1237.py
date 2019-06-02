# Generated by Django 2.1.2 on 2019-06-01 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Operarios', '0060_auto_20190530_2108'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='operariosasignaciondet',
            options={'verbose_name': 'Operario disponible', 'verbose_name_plural': 'Operarios disponibles'},
        ),
        migrations.AlterField(
            model_name='operario',
            name='latitud',
            field=models.CharField(blank=True, max_length=20, verbose_name='Latitud'),
        ),
        migrations.AlterField(
            model_name='operario',
            name='longitud',
            field=models.CharField(blank=True, max_length=20, verbose_name='Longitud'),
        ),
    ]