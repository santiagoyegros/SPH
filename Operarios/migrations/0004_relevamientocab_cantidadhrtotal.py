# Generated by Django 2.1.2 on 2019-01-09 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Operarios', '0003_planificacioncab_planificaciondet_planificacionesp'),
    ]

    operations = [
        migrations.AddField(
            model_name='relevamientocab',
            name='cantidadHrTotal',
            field=models.IntegerField(blank=True, null=True, verbose_name='Cantidad de Horas total'),
        ),
    ]
