# Generated by Django 2.1.2 on 2019-05-26 04:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Operarios', '0044_auto_20190525_1815'),
    ]

    operations = [
        
        migrations.AlterField(
            model_name='operario',
            name='numPasaporte',
            field=models.CharField(blank=True, max_length=10, verbose_name='Numero de Pasaporte'),
        ),
    ]
