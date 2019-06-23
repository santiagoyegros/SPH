import logging
from django.utils.translation import gettext as _
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator
from django.db import connection
from django.utils.timezone import now
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
    nombre = models.CharField(max_length=70, blank=False)
    apellido=models.CharField(max_length=70, blank=False, default="")
    direccion = models.CharField(max_length=100, blank=False)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE, blank=False)
    barrios = models.CharField(max_length=70, blank=False)
    nroLegajo = models.CharField('Numero de Legajo', max_length=6, blank=True)
    telefono = models.BigIntegerField(blank=False, validators=[MaxValueValidator(9999999999)], null=True)
    email = models.CharField(max_length=30, blank=True)
    fechaNacimiento = models.DateField('Fecha Nacimiento', blank=False)
    lugarNacimiento = models.ForeignKey(Ciudad, on_delete=models.CASCADE, related_name='%(class)s_requests_created')
    numCedula = models.CharField('N° Cedula', max_length=30, blank=False)
    numPasaporte = models.CharField('Numero de Pasaporte', max_length=10, blank=True)
    banco = models.CharField(max_length=30, blank=True)
    ctaBanco = models.CharField(max_length=20, blank=True)
    nombreContacto = models.CharField(max_length=70, blank=True)
    telefonoContacto=models.BigIntegerField('Telefono Contacto', blank=False, null=True, validators=[MaxValueValidator(9999999999)])
    nacionalidad = models.ForeignKey(Nacionalidad, on_delete=models.CASCADE)
    fechaInicio = models.DateField('Fecha Inicio', blank=False, null=True)
    fechaFin = models.DateField('Fecha Fin', blank=True, null=True)
    latitud=models.CharField('Latitud', max_length=20,blank=True)
    longitud=models.CharField('Longitud', max_length=20,blank=True)
    escolaridad= models.CharField('Escolaridad', max_length=70, blank=True)
    profesion=models.ManyToManyField(Especializacion)


    def __str__(self):
        return self.numCedula + ' - ' +  self.nombre  

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
    fechaFin= models.DateField('Fecha Fin Cobertura', blank=True, null=True)
    estado=models.CharField('Estado del relevamiento', max_length=30, blank=False, default='Aprobado')
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
    fechaFin = models.DateField('Fecha Fin Operario', null=True,blank=True)
    totalHoras = models.CharField('Total Asignado', max_length=8, null=True)
    supervisor=models.BooleanField('Supervisor', default=False)
    perfil = models.ForeignKey(Especializacion, on_delete=models.CASCADE, null=True)
    

    

    class Meta:
        verbose_name = _("Asignacion Detalle")
        verbose_name_plural = _("Asignacion Detalles")

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
    idpersonaevento = models.AutoField(db_column='IdPersonaEvento', primary_key=True,verbose_name='ID Marcacion')  # Field name made lowercase.
    codoperacion = models.CharField(db_column='CodOperacion', max_length=2, blank=True, null=True,verbose_name='Codigo de Operacion')  # Field name made lowercase.
    codpersona = models.CharField(db_column='CodPersona', max_length=10, blank=True, null=True,verbose_name='Codigo de Persona')  # Field name made lowercase.
    codcategoria = models.CharField(db_column='CodCategoria', max_length=2, blank=True, null=True,verbose_name='Codigo de Categoria')  # Field name made lowercase.
    numlinea = models.CharField(db_column='NumLinea', max_length=10, blank=True, null=True,verbose_name='Numero de Linea')  # Field name made lowercase.
    codubicacion = models.CharField(db_column='CodUbicacion', max_length=30, blank=True, null=True,verbose_name='Codigo de ubicacion')  # Field name made lowercase.
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True,verbose_name='Fecha')  # Field name made lowercase.
    estado = models.CharField(db_column='Estado', max_length=20, blank=True, null=True,verbose_name='Estado')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ESME_EM_Marcaciones'

    

class AsignacionesProcesadas(models.Model):
    NumCedulaOperario = models.CharField('N° Cedula', max_length=30)
    fecha = models.DateField('Fecha')
    puntoServicio = models.ForeignKey(PuntoServicio, on_delete=models.CASCADE)
    asignacionDet = models.ForeignKey(AsignacionDet, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("Asignacion Procesada")
        verbose_name_plural = _("Asignaciones Procesadas")

class Parametros(models.Model):
    tipo = models.CharField('Tipo de Parametro', max_length=30)
    parametro = models.CharField('Parametro', max_length=50)
    valor = models.CharField('Parametro', max_length=150)

    class Meta:
        verbose_name = _("Parametro de Sistema")
        verbose_name_plural = _("Parametros de Sistema")

class Feriados(models.Model):
    anho = models.IntegerField('Año', blank=True, null=True)
    fecha = models.DateField('Fecha Inicio Cobertura', null=True)
    descripcion = models.CharField('Parametro', max_length=200)

    class Meta:
        verbose_name = _("Parametro de Sistema")
        verbose_name_plural = _("Parametros de Sistema")

class Alertas(models.Model):
    FechaHora = models.DateTimeField('Fecha hora del Alerta')
    Operario = models.ForeignKey(Operario, on_delete=models.CASCADE)
    Asignacion = models.ForeignKey(AsignacionDet, blank=True, null=True, on_delete=models.SET_NULL)
    PuntoServicio = models.ForeignKey(PuntoServicio, blank=True, null=True, on_delete=models.SET_NULL)
    Estado = models.CharField(_("Estado"), max_length=10)
    Tipo = models.CharField(_('Tipo de Alerta'), max_length=10)


class DiaLibre(models.Model):
    asignacionDet =  models.ForeignKey(AsignacionDet, blank=True, null=True, on_delete=models.SET_NULL)
    diaInicio=models.CharField(_("Dia Inicio Libre"), max_length=10)
    horaInicio=models.TimeField('Hora Inicio Libre', blank=True, null=True)
    diaFin=models.CharField(_("Dia Fin Libre"), max_length=10)
    horaFin=models.TimeField('Hora Fin Libre', blank=True, null=True)
    fechaCreacion=models.DateTimeField('Fecha Relevamiento', auto_now_add=True)
class OperariosAsignacionDet (models.Model):
    id_operario= models.IntegerField(db_column='id_opeario', primary_key=True,verbose_name=' ')
    nombres=models.CharField(db_column='nombres',verbose_name='Nombres',max_length=200)
    nroLegajo=models.CharField(db_column='nroLegajo',verbose_name='Numero de legajo',max_length=6)
    nombres_puntoServicio=models.CharField(db_column='nombres_puntoServicio',verbose_name='Nombres Puntos de Servicio',max_length=200)
    ids_puntoServicio=models.CharField(db_column='ids_puntoServicio',verbose_name=' ',max_length=100)
    totalHoras=models.FloatField(db_column='totalHoras',verbose_name='Total Horas')
    perfil=models.CharField(db_column='perfil',verbose_name='Perfil',max_length=400)
    antiguedad=models.IntegerField(db_column='antiguedad',verbose_name='Antiguedad')
    ids_perfil=models.CharField(db_column='ids_perfil',verbose_name=' ',max_length=100, default='')
    managed=False
    class Meta:
        verbose_name = _("Operario disponible")
        verbose_name_plural = _("Operarios disponibles")

class HorariosOperario(models.Model):
    idOrden= models.IntegerField(db_column='idOrden',verbose_name='idOrden', primary_key=True)  
    diaEntrada=models.CharField( db_column='diaEntrada',verbose_name='diaEntrada', max_length=30)
    horaEntrada=models.TimeField( db_column='horaEntrada',verbose_name='horaEntrada', blank=True)
    diaSalida=models.CharField(db_column='diaSalida',verbose_name='diaSalida',max_length=30)
    horaSalida=models.TimeField(db_column='horaSalida',verbose_name='horaSalida', blank=True)
    totalHoras=models.TimeField(db_column='totalHoras',verbose_name='totalHoras', blank=True, null=True)
    managed=False
    class Meta:
        verbose_name = _("Horarios Operario")
        verbose_name_plural = _("Horarios Operario")

class RemplazosCab(models.Model):
    fechaInicio = models.DateField('Fecha Inicio Remplazo', null=True)
    fechaFin = models.DateField('Fecha Inicio Remplazo', null=True)
    FechaHoraRemplazo = models.DateTimeField('Fecha hora del Remplazo')
    tipoRemplazo = models.CharField(_('Tipo de Remplazo'), max_length=10)
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    

class RemplazosDet(models.Model):
    Asignacion = models.ForeignKey(AsignacionDet, blank=True, null=True, on_delete=models.SET_NULL)
    fecha = models.DateField('Fecha Inicio Remplazo', null=True)
    remplazo = models.ForeignKey(Operario, on_delete=models.CASCADE)

class AlertaResp (models.Model):
    accion=models.CharField(max_length=30, verbose_name='Accion')
    hora=models.TimeField(blank=True, null=True, verbose_name='Hora Aproximada')
    motivo= models.CharField(max_length=1000, verbose_name='Motivo')
    fechaRetorno=models.DateField(blank=True, verbose_name='Fecha de Retorno', null=True)
    comentarios=models.CharField(max_length=1000, verbose_name='Comentarios')
    escalado=models.BooleanField(default=False, verbose_name='Escalado')
    id_alerta=models.ForeignKey(Alertas, on_delete=models.CASCADE)
    id_reemplazo=models.ForeignKey(RemplazosCab, blank=True, null=True,on_delete=models.CASCADE)
    usuario=models.ForeignKey(User, blank=True, null=True,on_delete=models.SET_NULL)
    fecha_creacion = models.DateTimeField('Fecha Relevamiento', auto_now_add=True, blank=True, null=True)
