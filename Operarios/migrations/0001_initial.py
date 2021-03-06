# Generated by Django 2.1.2 on 2018-12-10 18:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ciudad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NombreCiudad', models.CharField(max_length=70, verbose_name='Ciudad')),
            ],
            options={
                'verbose_name_plural': 'Ciudades',
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Cliente', models.CharField(max_length=100)),
                ('CodigoCliente', models.CharField(max_length=15, verbose_name='Codigo Cliente')),
                ('Direccion', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Especializacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('especializacion', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Especializaciones',
            },
        ),
        migrations.CreateModel(
            name='GrupoEmpresarial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GrupoEmpresarial', models.CharField(max_length=100, verbose_name='Grupo Empresarial')),
                ('CodigoGrupo', models.CharField(max_length=15, verbose_name='Codigo Grupo')),
            ],
            options={
                'verbose_name_plural': 'Grupos Empresariales',
            },
        ),
        migrations.CreateModel(
            name='Nacionalidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Pais', models.CharField(max_length=70)),
            ],
            options={
                'verbose_name_plural': 'Nacionalidades',
            },
        ),
        migrations.CreateModel(
            name='Operario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nombre', models.CharField(max_length=70)),
                ('Direccion', models.CharField(max_length=100)),
                ('Barrios', models.CharField(max_length=70)),
                ('NroLegajo', models.CharField(blank=True, max_length=6, verbose_name='Numero de Legajo')),
                ('Telefono', models.CharField(max_length=15)),
                ('Email', models.CharField(blank=True, max_length=30)),
                ('FechaNacimiento', models.DateField(verbose_name='Fecha Nacimiento')),
                ('LugarNacimiento', models.CharField(max_length=30, verbose_name='Lugar de Nacimiento')),
                ('NumCedula', models.CharField(max_length=30, verbose_name='N° Cedula')),
                ('NumPasaporte', models.CharField(max_length=10, verbose_name='Numero de Pasaporte')),
                ('Banco', models.CharField(blank=True, max_length=30)),
                ('CtaBanco', models.CharField(blank=True, max_length=20)),
                ('Clase', models.CharField(blank=True, max_length=10)),
                ('NombreContacto', models.CharField(blank=True, max_length=70)),
                ('Profesion', models.CharField(blank=True, max_length=20)),
                ('FechaInicio', models.DateField(verbose_name='Fecha Inicio')),
                ('FechaFin', models.DateField(verbose_name='Fecha Fin')),
                ('Ciudad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Operarios.Ciudad')),
                ('Especialidad', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Operarios.Especializacion')),
                ('Nacionalidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Operarios.Nacionalidad')),
            ],
        ),
        migrations.CreateModel(
            name='PuntoServicio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CodPuntoServicio', models.CharField(max_length=50, verbose_name='Punto de Servicio')),
                ('NombrePServicio', models.CharField(max_length=100, verbose_name='Nombre de Punto de Servicio')),
                ('DireccionContrato', models.CharField(max_length=150, verbose_name='Direccion del Punto de Servicio')),
                ('Barrios', models.CharField(max_length=70, verbose_name='Barrio')),
                ('Contacto', models.CharField(max_length=100, verbose_name='Nombre del Contacto')),
                ('MailContacto', models.CharField(blank=True, max_length=70, verbose_name='E-Mail Contacto')),
                ('TelefonoContacto', models.CharField(max_length=100, verbose_name='Telefono del Contacto')),
                ('Coordenadas', models.CharField(max_length=100, verbose_name='Coordenadas')),
                ('Ciudad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Operarios.Ciudad')),
                ('Cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Operarios.Cliente')),
            ],
            options={
                'verbose_name_plural': 'Puntos de Servicio',
            },
        ),
        migrations.CreateModel(
            name='RelevamientoCab',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True, verbose_name='Fecha Relevamiento')),
                ('cantidad', models.IntegerField(blank=True, null=True, verbose_name='Cantidad de Operarios')),
                ('puntoServicio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Operarios.PuntoServicio')),
            ],
        ),
        migrations.CreateModel(
            name='RelevamientoDet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orden', models.IntegerField(blank=True, null=True, verbose_name='Orden')),
                ('lunEnt', models.TimeField(blank=True, null=True, verbose_name='Lunes entradas')),
                ('lunSal', models.TimeField(blank=True, null=True, verbose_name='Lunes salida')),
                ('marEnt', models.TimeField(blank=True, null=True, verbose_name='Martes entrada')),
                ('marSal', models.TimeField(blank=True, null=True, verbose_name='Martes salida')),
                ('mieEnt', models.TimeField(blank=True, null=True, verbose_name='Miercoles entrada')),
                ('mieSal', models.TimeField(blank=True, null=True, verbose_name='Miercoles salida')),
                ('jueEnt', models.TimeField(blank=True, null=True, verbose_name='Jueves entrada')),
                ('jueSal', models.TimeField(blank=True, null=True, verbose_name='Jueves salida')),
                ('vieEnt', models.TimeField(blank=True, null=True, verbose_name='Viernes entrada')),
                ('vieSal', models.TimeField(blank=True, null=True, verbose_name='Viernes salida')),
                ('sabEnt', models.TimeField(blank=True, null=True, verbose_name='Sabado entrada')),
                ('sabSal', models.TimeField(blank=True, null=True, verbose_name='Sabado salida')),
                ('domEnt', models.TimeField(blank=True, null=True, verbose_name='Domingo entrada')),
                ('domSal', models.TimeField(blank=True, null=True, verbose_name='Domingo salida')),
                ('relevamientoCab', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Operarios.RelevamientoCab')),
            ],
        ),
        migrations.CreateModel(
            name='RelevamientoEsp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frecuencia', models.CharField(choices=[('DIA', 'Diario'), ('SEM', 'Semanal'), ('MEN', 'Mensual'), ('BIM', 'Bimestral'), ('TRI', 'Trimestral'), ('SEM', 'Semestral'), ('ANU', 'Anual')], default='MEN', max_length=3, verbose_name='Frecuencia')),
                ('dia', models.CharField(choices=[('LUN', 'Lunes'), ('MAR', 'Martes'), ('MIE', 'Miercoles'), ('JUE', 'Jueves'), ('VIE', 'Viernes'), ('SAB', 'Sabado'), ('DOM', 'Domingo')], max_length=3, verbose_name='Dia')),
                ('cantHoras', models.IntegerField(blank=True, null=True, verbose_name='Cantidad de Horas')),
                ('relevamientoCab', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Operarios.RelevamientoCab')),
            ],
        ),
        migrations.CreateModel(
            name='TipoServicio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipoServicio', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Tipos de Servicio',
            },
        ),
        migrations.AddField(
            model_name='relevamientoesp',
            name='tipo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Operarios.TipoServicio'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='GrupoEmpresarial',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Operarios.GrupoEmpresarial'),
        ),
    ]
