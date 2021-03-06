# Generated by Django 2.1.2 on 2019-06-21 14:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Operarios', '0063_auto_20190610_1612'),
    ]

    operations = [
        migrations.CreateModel(
            name='RemplazosCab',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaInicio', models.DateField(null=True, verbose_name='Fecha Inicio Remplazo')),
                ('fechaFin', models.DateField(null=True, verbose_name='Fecha Inicio Remplazo')),
                ('FechaHoraRemplazo', models.DateTimeField(verbose_name='Fecha hora del Remplazo')),
                ('tipoRemplazo', models.CharField(max_length=10, verbose_name='Tipo de Remplazo')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RemplazosDet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(null=True, verbose_name='Fecha Inicio Remplazo')),
                ('Asignacion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Operarios.AsignacionDet')),
                ('remplazo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Operarios.Operario')),
            ],
        ),
    ]
