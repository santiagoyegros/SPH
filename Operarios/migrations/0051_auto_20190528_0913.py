# Generated by Django 2.1.2 on 2019-05-28 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Operarios', '0050_auto_20190528_0912'),
    ]
    

    operations = [
        migrations.AlterField(
            model_name='asignaciondetaux',
            name='totalHoras',
            field=models.CharField(max_length=8, null=True, verbose_name='Total de horas necesarias tabla aux'),
        ),
    ]
