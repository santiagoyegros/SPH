# Generated by Django 2.1.2 on 2019-04-02 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Operarios', '0025_auto_20190328_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operario',
            name='FechaFin',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha Fin'),
        ),
    ]
