# Generated by Django 2.1.2 on 2018-12-27 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Operarios', '0002_auto_20181227_1209'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlanificacionCab',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True, verbose_name='Fecha Planificación')),
                ('cantidad', models.IntegerField(blank=True, null=True, verbose_name='Cantidad de Operarios')),
                ('cantHoras', models.IntegerField(blank=True, null=True, verbose_name='Cantidad de Horas Normales')),
                ('cantHorasNoc', models.IntegerField(blank=True, null=True, verbose_name='Cantidad de Horas Nocturnas')),
                ('cantHorasEsp', models.IntegerField(blank=True, null=True, verbose_name='Cantidad de Horas Especiales')),
                ('puntoServicio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Operarios.PuntoServicio')),
            ],
            options={
                'verbose_name_plural': 'Planificación',
            },
        ),
        migrations.CreateModel(
            name='PlanificacionDet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orden', models.IntegerField(blank=True, null=True, verbose_name='Orden')),
                ('lunEnt', models.TimeField(blank=True, null=True, verbose_name='Lunes entradas')),
                ('lunSal', models.TimeField(blank=True, null=True, verbose_name='Lunes salida')),
                ('marEnt', models.TimeField(blank=True, null=True, verbose_name='Martes entrada')),
                ('marSal', models.TimeField(blank=True, null=True, verbose_name='Martes salida')),
                ('mieEnt', models.TimeField(blank=True, null=True, verbose_name='Miercoles entrada')),
                ('mieSal', models.TimeField(blank=True, null=True, verbose_name='Miercoles salida')),
                ('jueEnt', models.TimeField(blank=True, null=True, verbose_name='Jueves entrada')),
                ('jueSal', models.TimeField(blank=True, null=True, verbose_name='Jueves salida')),
                ('vieEnt', models.TimeField(blank=True, null=True, verbose_name='Viernes entrada')),
                ('vieSal', models.TimeField(blank=True, null=True, verbose_name='Viernes salida')),
                ('sabEnt', models.TimeField(blank=True, null=True, verbose_name='Sabado entrada')),
                ('sabSal', models.TimeField(blank=True, null=True, verbose_name='Sabado salida')),
                ('domEnt', models.TimeField(blank=True, null=True, verbose_name='Domingo entrada')),
                ('domSal', models.TimeField(blank=True, null=True, verbose_name='Domingo salida')),
                ('especialista', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Operarios.Especializacion')),
                ('planificacionCab', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Operarios.PlanificacionCab')),
            ],
            options={
                'verbose_name_plural': 'Planificaciones de Operarios',
            },
        ),
        migrations.CreateModel(
            name='PlanificacionEsp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frecuencia', models.CharField(choices=[('DIA', 'Diario'), ('SEM', 'Semanal'), ('MEN', 'Mensual'), ('BIM', 'Bimestral'), ('TRI', 'Trimestral'), ('SEM', 'Semestral'), ('ANU', 'Anual')], default='MEN', max_length=3, verbose_name='Frecuencia')),
                ('dia', models.CharField(choices=[('LUN', 'Lunes'), ('MAR', 'Martes'), ('MIE', 'Miercoles'), ('JUE', 'Jueves'), ('VIE', 'Viernes'), ('SAB', 'Sabado'), ('DOM', 'Domingo')], max_length=3, verbose_name='Dia')),
                ('cantHoras', models.IntegerField(blank=True, null=True, verbose_name='Cantidad de Horas')),
                ('especialista', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Operarios.Especializacion')),
                ('planificacionCab', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Operarios.PlanificacionCab')),
                ('tipo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Operarios.TipoServicio')),
            ],
        ),
    ]
