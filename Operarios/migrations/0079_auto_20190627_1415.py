# Generated by Django 2.1.2 on 2019-06-27 18:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Operarios', '0078_auto_20190627_1412'),
    ]

    operations = [
        
        migrations.AlterField(
            model_name='alertaresp',
            name='motivo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Operarios.Motivos'),
        ),
    ]
