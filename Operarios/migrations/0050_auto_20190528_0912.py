# Generated by Django 2.1.2 on 2019-05-28 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Operarios', '0049_asignaciondetaux_totalhoras'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asignaciondetaux',
            name='fechaInicio',
            field=models.DateField(null=True, verbose_name='Fecha Inicio Operario Aux'),
        ),
    ]