# Generated by Django 2.1.2 on 2019-06-15 03:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Operarios', '0064_delete_operariosasignaciondet'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asignaciondetaux',
            name='asignacionCab',
        ),
        migrations.RemoveField(
            model_name='asignaciondetaux',
            name='operario',
        ),
        migrations.DeleteModel(
            name='AsignacionDetAux',
        ),
    ]
