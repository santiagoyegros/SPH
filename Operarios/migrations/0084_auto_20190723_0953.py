# Generated by Django 2.1.2 on 2019-07-23 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Operarios', '0083_auto_20190704_1011'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalendarioCupo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anho', models.IntegerField(blank=True, null=True, verbose_name='Anho calendario')),
                ('mes', models.CharField(max_length=2, verbose_name='Mes del anho')),
                ('cantLunes', models.IntegerField(blank=True, null=True, verbose_name='Cant de lunes por mes')),
                ('cantMartes', models.IntegerField(blank=True, null=True, verbose_name='Cant de martes por mes')),
                ('cantMiercoles', models.IntegerField(blank=True, null=True, verbose_name='Cant de miercoles por mes')),
                ('cantJueves', models.IntegerField(blank=True, null=True, verbose_name='Cant de jueves por mes')),
                ('cantViernes', models.IntegerField(blank=True, null=True, verbose_name='Cant de viernes por mes')),
                ('cantSabado', models.IntegerField(blank=True, null=True, verbose_name='Cant de sabado por mes')),
                ('cantDomingo', models.IntegerField(blank=True, null=True, verbose_name='Cant de domingo por mes')),
            ],
        ),
        
    ]