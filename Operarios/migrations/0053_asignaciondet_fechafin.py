# Generated by Django 2.1.2 on 2019-05-30 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Operarios', '0052_merge_20190530_1501'),
    ]

    operations = [
        migrations.AddField(
            model_name='asignaciondet',
            name='fechaFin',
            field=models.DateField(null=True, verbose_name='Fecha Inicio Operario'),
        ),
    ]
