# Generated by Django 2.1.2 on 2019-07-31 18:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Operarios', '0102_auto_20190731_1435'),
    ]

    operations = [
       
        migrations.AddField(
            model_name='planificacioncab',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
