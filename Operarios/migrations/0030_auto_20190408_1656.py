# Generated by Django 2.1.2 on 2019-04-08 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Operarios', '0029_auto_20190408_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planificacionesp',
            name='frecuencia',
            field=models.CharField(choices=[('DIA', 'Diario'), ('SEM', 'Semanal'), ('MEN', 'Mensual'), ('BIM', 'Bimestral'), ('TRI', 'Trimestral'), ('CUA', 'Cuatrimestral'), ('SEL', 'Semestral'), ('ANU', 'Anual')], default='MEN', max_length=3, verbose_name='Frecuencia'),
        ),
        migrations.AlterField(
            model_name='relevamientoesp',
            name='frecuencia',
            field=models.CharField(choices=[('DIA', 'Diario'), ('SEM', 'Semanal'), ('MEN', 'Mensual'), ('BIM', 'Bimestral'), ('TRI', 'Trimestral'), ('CUA', 'Cuatrimestral'), ('SEL', 'Semestral'), ('ANU', 'Anual')], default='MEN', max_length=3, verbose_name='Frecuencia'),
        ),
    ]
