# Generated by Django 2.1.2 on 2019-05-31 00:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Operarios', '0056_auto_20190530_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operario',
            name='lugarNacimiento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operario_requests_created', to='Operarios.Ciudad'),
        ),
    ]