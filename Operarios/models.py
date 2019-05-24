import logging
from django.utils.translation import gettext as _
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator

class Ciudad(models.Model):
    NombreCiudad = models.CharField("Ciudad", max_length=70)

    def __str__(self):
        return self.NombreCiudad

    class Meta:
        verbose_name_plural = "Ciudades"

class Nacionalidad(models.Model):
    Pais = models.CharField(max_length=70)

    def __str__(self):
        return self.Pais

    class Meta:
        verbose_name_plural = "Nacionalidades"

class Especializacion(models.Model):
    especializacion = models.CharField(max_length=200)

    def __str__(self):
        return self.especializacion

    class Meta:
        verbose_name_plural = "Especializaciones"

class Operario(models.Model):
    Nombre = models.CharField(max_length=70, blank=False)
    Apellido=models.CharField(max_length=70, blank=False, default="")
    Direccion = models.CharField(max_length=100, blank=False)
    Ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE, blank=False)
    Barrios = models.CharField(max_length=70, blank=False)
    NroLegajo = models.CharField('Numero de Legajo', max_length=6, blank=True)
    Telefono = models.BigIntegerField(blank=False, validators=[MaxValueValidator(9999999999)])
    Email = models.CharField(max_length=30, blank=True)
    FechaNacimiento = models.DateField('Fecha Nacimiento', blank=False)
    LugarNacimiento = models.CharField('Lugar de Nacimiento', max_length=30)
    NumCedula = models.CharField('N° Cedula', max_length=30, blank=False)
    NumPasaporte = models.CharField('Numero de Pasaporte', max_length=10)
    Banco = models.CharField(max_length=30, blank=False)
    CtaBanco = models.CharField(max_length=20, blank=False)
    NombreContacto = models.CharField(max_length=70, blank=True)
    TelefonoContacto=models.BigIntegerField('Telefono Contacto', blank=False, null=True, validators=[MaxValueValidator(9999999999)])
    Nacionalidad = models.ForeignKey(Nacionalidad, on_delete=models.CASCADE)
    FechaInicio = models.DateField('Fecha Inicio', blank=False)
    FechaFin = models.DateField('Fecha Fin', blank=True, null=True)
    latitud=models.FloatField(blank=False, null=True, default=None)
    longitud=models.FloatField(blank=False, null=True, default=None)
    escolaridad= models.CharField('Escolaridad', max_length=70, blank=True)


    def __str__(self):
        return self.NumCedula + ' - ' +  self.Nombre  

class GrupoEmpresarial(models.Model):
    GrupoEmpresarial = models.CharField('Grupo Empresarial', max_length=100)
    CodigoGrupo = models.CharField('Codigo Grupo', max_length=15)

    def __str__(self):
        return self.GrupoEmpresarial

    class Meta:
        verbose_name_plural = "Grupos Empresariales"

class Cliente(models.Model):
    Cliente = models.CharField(max_length=100)
    CodigoCliente = models.CharField('Codigo Cliente', max_length=15)
    Direccion = models.CharField(max_length=150)
    GrupoEmpresarial = models.ForeignKey(GrupoEmpresarial, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.Cliente

class TipoServicio(models.Model):
    tipoServicio = models.CharField(max_length=200)

    def __str__(self):
        return self.tipoServicio

    class Meta:
        verbose_name = _("Tipo de Limpieza Profunda")
        verbose_name_plural = _("Tipos de Limpiezas Profundas")

class PuntoServicio(models.Model):
    Cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    CodPuntoServicio = models.CharField('Punto de Servicio', max_length=50)
    NombrePServicio = models.CharField('Nombre de Punto de Servicio', max_length=100)
    DireccionContrato = models.CharField('Direccion del Punto de Servicio', max_length=150)
    Ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)
    Barrios = models.CharField('Barrio', max_length=70)
    Contacto = models.CharField('Nombre del Contacto', max_length=100)
    MailContacto = models.CharField('E-Mail Contacto', max_length=70, blank=True)
    TelefonoContacto = models.CharField('Telefono del Contacto', max_length=100)
    Coordenadas = models.CharField('Coordenadas', max_length=100)
    NumeroMarcador = models.CharField('Numero Marcador', max_length=15, blank=True, null=True)

    def __str__(self):
        return self.CodPuntoServicio

    class Meta:
        verbose_name_plural = "Puntos de Servicio"

class TipoHorario(models.Model):
    tipoHorario = models.CharField('Tipo de Horario', max_length=50)
    horaInicio = models.TimeField('Horario Inicio', blank=True, null=True)
    horaFin = models.TimeField('Horario Fin', blank=True, null=True)

    class Meta:
        verbose_name = _("Tipo de Horario")
        verbose_name_plural = _("Tipos de Horarios")

    def __str__(self):
        return self.tipoHorario

class TipoSalario(models.Model):
    tipoSalario = models.CharField('Tipo de Salario', max_length=50)
    descripcion = models.CharField('Descripcion', max_length=200, blank=True, null=True)
    valor = models.IntegerField('Valor de Salario', blank=True, null=True)

    class Meta:
        verbose_name = _("Tipo de Salario")
        verbose_name_plural = _("Tipos de Salarios")

    def __str__(self):
        return self.tipoSalario

class TipoServicioParticular(models.Model):
    tipoServicioParticular = models.CharField('Tipo de Salario', max_length=100)
    

    class Meta:
        verbose_name = _("Tipo de Servicio Particular")
        verbose_name_plural = _("Tipos de Servicios Particulares")

    def __str__(self):
        return self.tipoServicioParticular


class RelevamientoCab(models.Model):
    puntoServicio = models.ForeignKey(PuntoServicio, blank=True, null=True, on_delete=models.SET_NULL)
    fecha = models.DateTimeField('Fecha Relevamiento', auto_now_add=True)
    cantidad = models.IntegerField('Cantidad de Operarios', blank=True, null=True)
    cantAprendices =  models.IntegerField('Cantidad de Aprendices', blank=True, null=True)
    cantidadHrTotal = models.CharField('Cantidad de Horas total por Semana', max_length=8, blank=True, null=True)
    cantidadHrEsp = models.CharField('Cantidad de Horas Especiales por Semana', max_length=8, blank=True, null=True)
    fechaInicio = models.DateField('Fecha Inicio Cobertura', null=True)
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    tipoSalario = models.ForeignKey(TipoSalario, blank=True, null=True, on_delete=models.CASCADE)
    comentario = models.CharField('Comentarios del servicio aprobado', max_length=550, blank=True, null=True)
    
    def __str__(self):
        return self.puntoServicio.NombrePServicio

    class Meta:
        verbose_name = _("Servicio Aprobado")
        verbose_name_plural = "Servicios Aprobados"

class RelevamientoDet(models.Model):
    relevamientoCab =  models.ForeignKey(RelevamientoCab, blank=True, null=True, on_delete=models.SET_NULL)
    orden = models.IntegerField('Orden', blank=True, null=True)
    lunEnt = models.TimeField('Lunes entradas', blank=True, null=True)
    lunSal = models.TimeField('Lunes salida', blank=True, null=True)
    marEnt = models.TimeField('Martes entrada', blank=True, null=True)
    marSal = models.TimeField('Martes salida', blank=True, null=True)
    mieEnt = models.TimeField('Miercoles entrada', blank=True, null=True)
    mieSal = models.TimeField('Miercoles salida', blank=True, null=True)
    jueEnt = models.TimeField('Jueves entrada', blank=True, null=True)
    jueSal = models.TimeField('Jueves salida', blank=True, null=True)
    vieEnt = models.TimeField('Viernes entrada', blank=True, null=True)
    vieSal = models.TimeField('Viernes salida', blank=True, null=True)
    sabEnt = models.TimeField('Sabado entrada', blank=True, null=True)
    sabSal = models.TimeField('Sabado salida', blank=True, null=True)
    domEnt = models.TimeField('Domingo entrada', blank=True, null=True)
    domSal = models.TimeField('Domingo salida', blank=True, null=True)
    tipoServPart = models.ForeignKey(TipoServicioParticular, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Servicios Especificos"

class RelevamientoEsp(models.Model):
    
    DIARIO = 'DIA'
    SEMANAL = 'SEM'
    MENSUAL = 'MEN'
    BIMESTRAL = 'BIM'
    TRIMESTRAL = 'TRI'
    CUATRIMESTRAL = 'CUA'
    SEMESTRAL = 'SEL'
    ANUAL = 'ANU'

    FRECUENCIA = (
        (DIARIO, 'Diario'),
        (SEMANAL, 'Semanal'),
        (MENSUAL, 'Mensual'),
        (BIMESTRAL, 'Bimestral'),
        (TRIMESTRAL, 'Trimestral'),
        (CUATRIMESTRAL, 'Cuatrimestral'),
        (SEMESTRAL, 'Semestral'),
        (ANUAL, 'Anual'),
    )

    DIA = (
        ('LUN', 'Lunes'),
        ('MAR', 'Martes'),
        ('MIE', 'Miercoles'),
        ('JUE', 'Jueves'),
        ('VIE', 'Viernes'),
        ('SAB', 'Sabado'),
        ('DOM', 'Domingo'),
    )

    relevamientoCab =  models.ForeignKey(RelevamientoCab, blank=True, null=True, on_delete=models.CASCADE)
    tipo = models.ForeignKey(TipoServicio, blank=True, null=True, on_delete=models.CASCADE)
    frecuencia = models.CharField('Frecuencia', max_length = 3, choices = FRECUENCIA, default = MENSUAL, )
    #dia = models.CharField('Dia', max_length = 3, choices = DIA)
    #cantHoras = models.IntegerField('Cantidad de Horas', blank=True, null=True)
    cantHoras = models.CharField('Cantidad de Horas', max_length = 8, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Cupo de Horas Limpieza Profunda"

class RelevamientoCupoHoras(models.Model):
    SEMANAL = 'SEM'
    DOMINGO = 'DOM'
    FERIADO = 'FER'

    CUPO_FRECUENCIA = (
        (SEMANAL, 'Semanal'),
        (DOMINGO, 'Domingo'),
        (FERIADO, 'Feriado'),
    )
    
    relevamientoCab =  models.ForeignKey(RelevamientoCab, blank=True, null=True, on_delete=models.CASCADE)
    cantCHoras = models.CharField('Cantidad de Horas', max_length = 8, blank=True, null=True, db_column='cantHoras')
    #cantCHoras = models.DecimalField('Cantidad de Horas', max_digits=7, decimal_places=1, db_column='cantHoras', blank=True, null=True)
    frecuencia = models.CharField('Frecuencia', max_length = 3, choices = CUPO_FRECUENCIA, default = SEMANAL, )
    tipoHora = models.ForeignKey(TipoHorario, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Cupo de Horas")
        verbose_name_plural = _("Cupos de Horas")

class RelevamientoMensualeros(models.Model):
    relevamientoCab =  models.ForeignKey(RelevamientoCab, blank=True, null=True, on_delete=models.CASCADE)
    mensuCantidad = models.IntegerField('Cantidad de Mensualeros', blank=True, null=True)
    sueldo = models.IntegerField('Sueldo', blank=True, null=True)
    
    class Meta:
        verbose_name = _("Mensualeros")
        verbose_name_plural = _("Mensualeros")


class PlanificacionCab(models.Model):
    puntoServicio = models.ForeignKey(PuntoServicio, blank=True, null=True, on_delete=models.SET_NULL)
    fecha = models.DateTimeField('Fecha Planificación', auto_now_add=True)
    cantidad = models.IntegerField('Cantidad de Operarios', blank=True, null=True)
    cantHoras = models.CharField('Cantidad de Horas Normales', max_length=8, blank=True, null=True)
    cantHorasNoc = models.CharField('Cantidad de Horas Nocturnas', max_length=8, blank=True, null=True)
    cantHorasEsp = models.CharField('Cantidad de Horas Especiales', max_length=8, blank=True, null=True)
    
    def __str__(self):
        return self.puntoServicio.NombrePServicio

    class Meta:
        verbose_name_plural = "Planificación"

class PlanificacionOpe(models.Model):
    planificacionCab =  models.ForeignKey(PlanificacionCab, blank=True, null=True, on_delete=models.SET_NULL)
    especialista = models.ForeignKey(Especializacion, blank=True, null=True, on_delete=models.SET_NULL)
    cantidad = models.IntegerField('Cantidad', blank=True, null=True)
    lun = models.BooleanField('Lunes', default=False)
    mar = models.BooleanField('Martes', default=False)
    mie = models.BooleanField('Miercoles', default=False)
    jue = models.BooleanField('Jueves', default=False)
    vie = models.BooleanField('Viernes', default=False)
    sab = models.BooleanField('Sabado', default=False)
    dom = models.BooleanField('Domingo', default=False)
    fer = models.BooleanField('Feriado', default=False)
    ent = models.TimeField('Hora Inicio', blank=True, null=True)
    sal = models.TimeField('Hora Fin', blank=True, null=True)
    #corte = models.DecimalField('corte', max_digits=4, decimal_places=2, null=True, blank=True,)
    corte = models.CharField('Corte', max_length=8, blank=True, null=True)
    #total = models.DecimalField('total', max_digits=7, decimal_places=2, blank=True, null=True)
    total = models.CharField('Total', max_length=8, blank=True, null=True)

    class Meta:
        verbose_name = _("Planificacion de Horas Operarios")
        verbose_name_plural = _("Planificaciones de Horas de Operarios")

class PlanificacionEsp(models.Model):
    
    DIARIO = 'DIA'
    SEMANAL = 'SEM'
    MENSUAL = 'MEN'
    BIMESTRAL = 'BIM'
    TRIMESTRAL = 'TRI'
    CUATRIMESTRAL = 'CUA'
    SEMESTRAL = 'SEL'
    ANUAL = 'ANU'

    FRECUENCIA = (
        (DIARIO, 'Diario'),
        (SEMANAL, 'Semanal'),
        (MENSUAL, 'Mensual'),
        (BIMESTRAL, 'Bimestral'),
        (TRIMESTRAL, 'Trimestral'),
        (CUATRIMESTRAL, 'Cuatrimestral'),
        (SEMESTRAL, 'Semestral'),
        (ANUAL, 'Anual'),
    )

    DIA = (
        ('LUN', 'Lunes'),
        ('MAR', 'Martes'),
        ('MIE', 'Miercoles'),
        ('JUE', 'Jueves'),
        ('VIE', 'Viernes'),
        ('SAB', 'Sabado'),
        ('DOM', 'Domingo'),
    )

    planificacionCab =  models.ForeignKey(PlanificacionCab, blank=True, null=True, on_delete=models.CASCADE)
    especialista = models.ForeignKey(Especializacion, blank=True, null=True, on_delete=models.SET_NULL)
    tipo = models.ForeignKey(TipoServicio, blank=True, null=True, on_delete=models.CASCADE)
    frecuencia = models.CharField('Frecuencia', max_length = 3, choices = FRECUENCIA, default = MENSUAL, )
    #dia = models.CharField('Dia', max_length = 3, choices = DIA)
    cantHoras = models.CharField('Cantidad de Horas', max_length = 8, blank=True, null=True)
    #cantHoras = models.IntegerField('Cantidad de Horas', blank=True, null=True)
    fechaLimpProf = models.DateField('Fecha Inicio Limpieza Prof', null=True)

class Cargo(models.Model):
    cargo = models.CharField(max_length=100)

    def __str__(self):
        return self.cargo

    class Meta:
        verbose_name_plural = "Cargo"

class CargoAsignado(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cargo =  models.ForeignKey(Cargo, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name_plural = "Cargo Asignado"


@receiver(post_save, sender=User)
def create_user_cargoasignado(sender, instance, created, **kwargs):
    '''
    Aqui se define que se va realizar con el cargoasignado en el momento que se cree un usuario nuevo
    '''
    #if created:
    #    CargoAsignado.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_cargoasignado(sender, instance, **kwargs):
    logging.getLogger("error_logger").error('Se ingreso a save_user_cargoasignado')
    #instance.CargoAsignado.save()


class AsigJefeFiscal(models.Model):
    userJefe = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='JefeOpAsigJefeFiscal')
    userFiscal = models.OneToOneField(User, on_delete=models.CASCADE, related_name='FiscalAsigJefeFiscal')
    

    class Meta:
        verbose_name = _("Asignacion Jefe-Fiscal")
        verbose_name_plural = _("Asignaciones Jefe-Fiscales")

    def __str__(self):
        return self.userJefe.first_name

class AsigFiscalPuntoServicio(models.Model):
    userFiscal = models.ForeignKey(User, on_delete=models.CASCADE, related_name='FiscalAsigFiscalPuntoServicio')
    puntoServicio = models.OneToOneField(PuntoServicio, on_delete=models.CASCADE, related_name='puntoServicioAsigFiscalPuntoServicio')

    class Meta:
        verbose_name = _("Asignacion Fiscal-PuntoServicio")
        verbose_name_plural = _("Asignaciones Fiscales-PuntoServicio")

    def __str__(self):
        return self.userFiscal.first_name

class HisAsigJefeFiscal(models.Model):
    userJefe = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='JefeOp_HisAsigJefeFiscal')
    userFiscal = models.OneToOneField(User, on_delete=models.CASCADE, related_name='Fiscal_HisAsigJefeFiscal')
    fecha_inicio = models.DateField('Fecha de Inicio')
    fecha_fin = models.DateField('Fecha Final', blank=True, null=True)
    

    class Meta:
        verbose_name = _("Historico Asignacion Jefe-Fiscal")
        verbose_name_plural = _("Historico Asignaciones Jefe-Fiscales")

    def __str__(self):
        return self.userJefe.first_name

class HisAsigFiscalPuntoServicio(models.Model):
    userFiscal = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Fiscal_HisAsigFiscalPuntoServicio')
    puntoServicio = models.OneToOneField(PuntoServicio, on_delete=models.CASCADE, related_name='puntoServicio_HisAsigFiscalPuntoServicio')
    fecha_inicio = models.DateField('Fecha de Inicio')
    fecha_fin = models.DateField('Fecha Final', blank=True, null=True)

    class Meta:
        verbose_name = _("Historico Asignacion Fiscal-PuntoServicio")
        verbose_name_plural = _("Historico Asignaciones Fiscales-PuntoServicio")

    def __str__(self):
        return self.userFiscal.first_name


class AsignacionCab(models.Model):
    puntoServicio = models.ForeignKey(PuntoServicio, blank=True, null=True, on_delete=models.CASCADE)
    fechaUltimaMod = models.DateTimeField('Fecha Relevamiento', auto_now_add=True)
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    totalasignado = models.CharField('Total Asignado', max_length=8, null=True)

    class Meta:
        verbose_name = _("Asignacion")
        verbose_name_plural = _("Asignaciones")

    def __str__(self):
        return self.puntoServicio.NombrePServicio

class AsignacionDet(models.Model):
    asignacionCab =  models.ForeignKey(AsignacionCab, blank=True, null=True, on_delete=models.SET_NULL)
    lunEnt = models.TimeField('Lunes entradas', blank=True, null=True)
    lunSal = models.TimeField('Lunes salida', blank=True, null=True)
    marEnt = models.TimeField('Martes entrada', blank=True, null=True)
    marSal = models.TimeField('Martes salida', blank=True, null=True)
    mieEnt = models.TimeField('Miercoles entrada', blank=True, null=True)
    mieSal = models.TimeField('Miercoles salida', blank=True, null=True)
    jueEnt = models.TimeField('Jueves entrada', blank=True, null=True)
    jueSal = models.TimeField('Jueves salida', blank=True, null=True)
    vieEnt = models.TimeField('Viernes entrada', blank=True, null=True)
    vieSal = models.TimeField('Viernes salida', blank=True, null=True)
    sabEnt = models.TimeField('Sabado entrada', blank=True, null=True)
    sabSal = models.TimeField('Sabado salida', blank=True, null=True)
    domEnt = models.TimeField('Domingo entrada', blank=True, null=True)
    domSal = models.TimeField('Domingo salida', blank=True, null=True)
    operario = models.ForeignKey(Operario, blank=True, null=True, on_delete=models.CASCADE)
    fechaInicio = models.DateField('Fecha Inicio Operario', null=True)
    totalHoras = models.CharField('Total Asignado', max_length=8, null=True)

    

    class Meta:
        verbose_name = _("Asignacion Detalle")
        verbose_name_plural = _("Asignacion Detalles")

class AsignacionDetAux(models.Model):
    asignacionCab =  models.ForeignKey(AsignacionCab, blank=True, null=True, on_delete=models.SET_NULL)
    lunEnt = models.TimeField('Lunes entradas', blank=True, null=True)
    lunSal = models.TimeField('Lunes salida', blank=True, null=True)
    marEnt = models.TimeField('Martes entrada', blank=True, null=True)
    marSal = models.TimeField('Martes salida', blank=True, null=True)
    mieEnt = models.TimeField('Miercoles entrada', blank=True, null=True)
    mieSal = models.TimeField('Miercoles salida', blank=True, null=True)
    jueEnt = models.TimeField('Jueves entrada', blank=True, null=True)
    jueSal = models.TimeField('Jueves salida', blank=True, null=True)
    vieEnt = models.TimeField('Viernes entrada', blank=True, null=True)
    vieSal = models.TimeField('Viernes salida', blank=True, null=True)
    sabEnt = models.TimeField('Sabado entrada', blank=True, null=True)
    sabSal = models.TimeField('Sabado salida', blank=True, null=True)
    domEnt = models.TimeField('Domingo entrada', blank=True, null=True)
    domSal = models.TimeField('Domingo salida', blank=True, null=True)
    operario = models.ForeignKey(Operario, blank=True, null=True, on_delete=models.CASCADE)
    fechaInicio = models.DateField('Fecha Inicio Operario', null=True)

    class Meta:
        verbose_name = _("Asignacion Detalle Auxiliar")
        verbose_name_plural = _("Asignacion Detalles Auxiliares")


class HorasProcesadas(models.Model):
    NumCedulaOperario = models.CharField('N° Cedula', max_length=30)
    puntoServicio = models.ForeignKey(PuntoServicio, on_delete=models.CASCADE)
    Hentrada = models.TimeField('Horario de entrada', blank=True, null=True)
    Hsalida = models.TimeField('Horario de salida', blank=True, null=True)
    total = models.TimeField('Total de Horas', blank=True, null=True)
    fecha = models.DateField('Fecha')
    TipoHora = models.CharField('Tipo de Hora', max_length=10)
    comentario = models.CharField('comentarios', max_length=500, blank=True, null=True)
    asignacionDet =  models.ForeignKey(AsignacionDet, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("Hora Procesada")
        verbose_name_plural = _("Horas Procesadass")

    def __str__(self):
        return self.NumCedulaOperario

class HorasNoProcesadas(models.Model):
    NumCedulaOperario = models.CharField('N° Cedula', max_length=30)
    puntoServicio = models.ForeignKey(PuntoServicio, on_delete=models.CASCADE)
    Hentrada = models.TimeField('Horario de entrada', blank=True, null=True)
    Hsalida = models.TimeField('Horario de salida', blank=True, null=True)
    total = models.TimeField('Total de Horas', blank=True, null=True)
    fecha = models.DateField('Fecha')
    TipoHora = models.CharField('Tipo de Hora', max_length=10)
    comentario = models.CharField('comentarios', max_length=500, blank=True, null=True)

    class Meta:
        verbose_name = _("Hora No Procesada")
        verbose_name_plural = _("Horas No Procesadas")

    def __str__(self):
        return self.NumCedulaOperario

class EsmeEmMarcaciones(models.Model):
    idpersonaevento = models.AutoField(db_column='IdPersonaEvento', primary_key=True)  # Field name made lowercase.
    codoperacion = models.CharField(db_column='CodOperacion', max_length=2, blank=True, null=True)  # Field name made lowercase.
    codpersona = models.CharField(db_column='CodPersona', max_length=10, blank=True, null=True)  # Field name made lowercase.
    codcategoria = models.CharField(db_column='CodCategoria', max_length=2, blank=True, null=True)  # Field name made lowercase.
    numlinea = models.CharField(db_column='NumLinea', max_length=10, blank=True, null=True)  # Field name made lowercase.
    codubicacion = models.CharField(db_column='CodUbicacion', max_length=30, blank=True, null=True)  # Field name made lowercase.
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    estado = models.CharField(db_column='Estado', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ESME_EM_Marcaciones'

