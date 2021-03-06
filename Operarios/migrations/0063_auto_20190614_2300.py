# Generated by Django 2.1.2 on 2019-06-15 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Operarios', '0062_auto_20190610_1516'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='operariosasignaciondet',
            name='id_opeario',
        ),
        migrations.AddField(
            model_name='operariosasignaciondet',
            name='id_operario',
            field=models.IntegerField(db_column='id_opeario', default=None, verbose_name=' '),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='asignaciondet',
            name='fechaFin',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha Fin Operario'),
        ),
        migrations.AlterField(
            model_name='operariosasignaciondet',
            name='antiguedad',
            field=models.IntegerField(db_column='antiguedad', verbose_name='Antiguedad'),
        ),
        migrations.AlterField(
            model_name='operariosasignaciondet',
            name='ids_puntoServicio',
            field=models.CharField(db_column='ids_puntoServicio', max_length=100, verbose_name=' '),
        ),
        migrations.AlterField(
            model_name='operariosasignaciondet',
            name='nombres',
            field=models.CharField(db_column='nombres', max_length=200, verbose_name='Nombres'),
        ),
        migrations.AlterField(
            model_name='operariosasignaciondet',
            name='nombres_puntoServicio',
            field=models.CharField(db_column='nombres_puntoServicio', max_length=200, verbose_name='Nombres Puntos de Servicio'),
        ),
        migrations.AlterField(
            model_name='operariosasignaciondet',
            name='nroLegajo',
            field=models.CharField(db_column='nroLegajo', max_length=6, verbose_name='Numero de legajo'),
        ),
        migrations.AlterField(
            model_name='operariosasignaciondet',
            name='perfil',
            field=models.CharField(db_column='perfil', max_length=400, verbose_name='Perfil'),
        ),
        migrations.AlterField(
            model_name='operariosasignaciondet',
            name='totalHoras',
            field=models.FloatField(db_column='totalHoras', verbose_name='Total Horas'),
        ),
    ]
