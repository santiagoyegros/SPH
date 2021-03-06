# Generated by Django 2.1.2 on 2019-07-25 13:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Operarios', '0099_auto_20190725_0954'),
    ]

    operations = [
       
        migrations.AddField(
            model_name='histasigfiscalpuntoservicio',
            name='puntoServicio',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Operarios.PuntoServicio'),
        ),
        migrations.AddField(
            model_name='histasigfiscalpuntoservicio',
            name='userFiscal',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='HistFiscalAsigFiscalPuntoServicio', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='histasigjefefiscal',
            name='userFiscal',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='histasigjefefiscal',
            name='userJefe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='HistJefeOpAsigJefeFiscal', to=settings.AUTH_USER_MODEL),
        ),
       
    ]
