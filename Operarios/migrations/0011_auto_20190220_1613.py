# Generated by Django 2.1.2 on 2019-02-20 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Operarios', '0010_auto_20190220_1534'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tiposervicio',
            options={'verbose_name': 'Tipo de Limpieza Profunda', 'verbose_name_plural': 'Tipos de Limpiezas Profundas'},
        ),
        migrations.AddField(
            model_name='relevamientocab',
            name='comentario',
            field=models.CharField(blank=True, max_length=550, null=True, verbose_name='Comentarios del servicio aprobado'),
        ),
    ]
