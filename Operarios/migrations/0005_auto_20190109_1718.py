# Generated by Django 2.1.2 on 2019-01-09 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Operarios', '0004_relevamientocab_cantidadhrtotal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relevamientocab',
            name='cantidadHrTotal',
            field=models.CharField(blank=True, max_length=8, null=True, verbose_name='Cantidad de Horas total por Semana'),
        ),
    ]
