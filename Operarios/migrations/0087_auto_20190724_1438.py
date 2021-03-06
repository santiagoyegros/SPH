# Generated by Django 2.1.2 on 2019-07-24 18:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Operarios', '0086_auto_20190724_1417'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistAsigFiscalPuntoServicio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vfechaInicio', models.DateTimeField(null=True, verbose_name='Fecha Inicio Reg')),
                ('vfechaFin', models.DateTimeField(null=True, verbose_name='Fecha Fin Reg')),
                ('vregistro', models.IntegerField(blank=True, null=True, verbose_name='Valor de Salario')),
                ('puntoServicio', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='HistpuntoServicioAsigFiscalPuntoServicio', to='Operarios.PuntoServicio')),
                ('userFiscal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='HistFiscalAsigFiscalPuntoServicio', to=settings.AUTH_USER_MODEL)),
                ('vactual', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Operarios.AsigFiscalPuntoServicio')),
            ],
        )
    ]
