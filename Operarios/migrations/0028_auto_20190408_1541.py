# Generated by Django 2.1.2 on 2019-04-08 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Operarios', '0027_auto_20190402_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relevamientoesp',
            name='frecuencia',
            field=models.CharField(choices=[('DIA', 'Diario'), ('SEM', 'Semanal'), ('MEN', 'Mensual'), ('BIM', 'Bimestral'), ('TRI', 'Trimestral'), ('SEL', 'Semestral'), ('ANU', 'Anual')], default='MEN', max_length=3, verbose_name='Frecuencia'),
        ),
    ]
