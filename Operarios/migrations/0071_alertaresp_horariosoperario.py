# Generated by Django 2.1.2 on 2019-06-21 16:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Operarios', '0070_operariosasignaciondet_ids_perfil'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlertaResp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accion', models.CharField(max_length=30, verbose_name='Accion')),
                ('hora', models.TimeField(blank=True, null=True, verbose_name='Hora Aproximada')),
                ('motivo', models.CharField(max_length=1000, verbose_name='Motivo')),
                ('fechaRetorno', models.DateField(blank=True, verbose_name='Fecha de Retorno')),
                ('comentarios', models.CharField(max_length=1000, verbose_name='Comentarios')),
                ('escalado', models.BooleanField(default=False, verbose_name='Escalado')),
                ('id_alerta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Operarios.Alertas')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HorariosOperario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diaEntrada', models.CharField(max_length=30, verbose_name='Dia Entrada')),
                ('horaEntrada', models.TimeField(blank=True, verbose_name='Hora Entrada')),
                ('diaSalida', models.CharField(max_length=30, verbose_name='Dia Salida')),
                ('horaSalida', models.TimeField(blank=True, verbose_name='Hora Salida')),
            ],
            options={
                'verbose_name': 'Horarios Operario',
                'verbose_name_plural': 'Horarios Operario',
            },
        ),
    ]
