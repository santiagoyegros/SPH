# Generated by Django 2.1.2 on 2019-05-31 00:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Operarios', '0055_auto_20190530_2011'),
    ]

    operations = [
        migrations.AddField(
            model_name='operario',
            name='latitud',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='operario',
            name='longitud',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='operario',
            name='lugarNacimiento',
            field=models.ForeignKey(default='NULL', on_delete=django.db.models.deletion.CASCADE, related_name='operario_requests_created', to='Operarios.Ciudad'),
        ),
    ]
