# Generated by Django 2.1.2 on 2019-07-24 18:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Operarios', '0091_auto_20190724_1441'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistPlanificacionEsp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frecuencia', models.CharField(choices=[('DIA', 'Diario'), ('SEM', 'Semanal'), ('MEN', 'Mensual'), ('BIM', 'Bimestral'), ('TRI', 'Trimestral'), ('CUA', 'Cuatrimestral'), ('SEL', 'Semestral'), ('ANU', 'Anual')], default='MEN', max_length=3, verbose_name='Frecuencia')),
                ('cantHoras', models.CharField(blank=True, max_length=8, null=True, verbose_name='Cantidad de Horas')),
                ('fechaLimpProf', models.DateField(null=True, verbose_name='Fecha Inicio Limpieza Prof')),
                ('vfechaInicio', models.DateTimeField(null=True, verbose_name='Fecha Inicio Reg')),
                ('vfechaFin', models.DateTimeField(null=True, verbose_name='Fecha Fin Reg')),
                ('vregistro', models.IntegerField(blank=True, null=True, verbose_name='Valor de Salario')),
                ('especialista', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Operarios.Especializacion')),
                ('planificacionCab', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Operarios.PlanificacionCab')),
                ('tipo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Operarios.TipoServicio')),
                ('vactual', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Operarios.PlanificacionEsp')),
            ],
        )
    ]
