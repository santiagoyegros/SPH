# Generated by Django 2.1.2 on 2019-04-11 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Operarios', '0032_auto_20190409_1517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relevamientocupohoras',
            name='cantCHoras',
            field=models.DecimalField(blank=True, db_column='cantHoras', decimal_places=2, max_digits=7, null=True, verbose_name='Cantidad de Horas'),
        ),
    ]