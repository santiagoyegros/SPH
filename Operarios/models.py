from django.db import models

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
    Nombre = models.CharField(max_length=70)
    Direccion = models.CharField(max_length=100)
    Ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)
    Barrios = models.CharField(max_length=70)
    NroLegajo = models.CharField('Numero de Legajo', max_length=6, blank=True)
    Telefono = models.CharField(max_length=15)
    Email = models.CharField(max_length=30, blank=True)
    FechaNacimiento = models.DateField('Fecha Nacimiento')
    LugarNacimiento = models.CharField('Lugar de Nacimiento', max_length=30)
    NumCedula = models.CharField('N° Cedula', max_length=30)
    NumPasaporte = models.CharField('Numero de Pasaporte', max_length=10)
    Especialidad = models.ForeignKey(Especializacion, blank=True, null=True, on_delete=models.CASCADE)
    Banco = models.CharField(max_length=30, blank=True)
    CtaBanco = models.CharField(max_length=20, blank=True)
    Clase = models.CharField(max_length=10, blank=True)
    NombreContacto = models.CharField(max_length=70, blank=True)
    Profesion = models.CharField(max_length=20, blank=True)
    Nacionalidad = models.ForeignKey(Nacionalidad, on_delete=models.CASCADE)
    FechaInicio = models.DateField('Fecha Inicio')
    FechaFin = models.DateField('Fecha Fin')

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
        verbose_name_plural = "Tipos de Servicio"

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

    def __str__(self):
        return self.CodPuntoServicio

    class Meta:
        verbose_name_plural = "Puntos de Servicio"

class RelevamientoCab(models.Model):
    puntoServicio = models.ForeignKey(PuntoServicio, blank=True, null=True, on_delete=models.SET_NULL)
    fecha = models.DateTimeField('Fecha Relevamiento', auto_now_add=True)
    cantidad = models.IntegerField('Cantidad de Operarios', blank=True, null=True)
    cantidadHrTotal = models.CharField('Cantidad de Horas total por Semana', max_length=8, blank=True, null=True)
    cantidadHrEsp = models.CharField('Cantidad de Horas Especiales por Semana', max_length=8, blank=True, null=True)
    
    def __str__(self):
        return self.puntoServicio.NombrePServicio

    class Meta:
        verbose_name_plural = "Relevamientos"

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

    class Meta:
        verbose_name_plural = "Relevamientos Cupo de Horas"

class RelevamientoEsp(models.Model):
    
    DIARIO = 'DIA'
    SEMANAL = 'SEM'
    MENSUAL = 'MEN'
    BIMESTRAL = 'BIM'
    TRIMESTRAL = 'TRI'
    SEMESTRAL = 'SEM'
    ANUAL = 'ANU'

    FRECUENCIA = (
        (DIARIO, 'Diario'),
        (SEMANAL, 'Semanal'),
        (MENSUAL, 'Mensual'),
        (BIMESTRAL, 'Bimestral'),
        (TRIMESTRAL, 'Trimestral'),
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
    dia = models.CharField('Dia', max_length = 3, choices = DIA)
    cantHoras = models.IntegerField('Cantidad de Horas', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Relevamientos Cupo de Horas Especiales"

class PlanificacionCab(models.Model):
    puntoServicio = models.ForeignKey(PuntoServicio, blank=True, null=True, on_delete=models.SET_NULL)
    fecha = models.DateTimeField('Fecha Planificación', auto_now_add=True)
    cantidad = models.IntegerField('Cantidad de Operarios', blank=True, null=True)
    #cantHoras = models.IntegerField('Cantidad de Horas Normales', blank=True, null=True)
    #cantHorasNoc = models.IntegerField('Cantidad de Horas Nocturnas', blank=True, null=True)
    #cantHorasEsp = models.IntegerField('Cantidad de Horas Especiales', blank=True, null=True)
    cantHoras = models.CharField('Cantidad de Horas Normales', max_length=8, blank=True, null=True)
    cantHorasNoc = models.CharField('Cantidad de Horas Nocturnas', max_length=8, blank=True, null=True)
    cantHorasEsp = models.CharField('Cantidad de Horas Especiales', max_length=8, blank=True, null=True)
    
    def __str__(self):
        return self.puntoServicio.NombrePServicio

    class Meta:
        verbose_name_plural = "Planificación"

class PlanificacionDet(models.Model):
    planificacionCab =  models.ForeignKey(PlanificacionCab, blank=True, null=True, on_delete=models.SET_NULL)
    especialista = models.ForeignKey(Especializacion, blank=True, null=True, on_delete=models.SET_NULL)
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

    class Meta:
        verbose_name_plural = "Planificaciones de Operarios"

class PlanificacionEsp(models.Model):
    
    DIARIO = 'DIA'
    SEMANAL = 'SEM'
    MENSUAL = 'MEN'
    BIMESTRAL = 'BIM'
    TRIMESTRAL = 'TRI'
    SEMESTRAL = 'SEM'
    ANUAL = 'ANU'

    FRECUENCIA = (
        (DIARIO, 'Diario'),
        (SEMANAL, 'Semanal'),
        (MENSUAL, 'Mensual'),
        (BIMESTRAL, 'Bimestral'),
        (TRIMESTRAL, 'Trimestral'),
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
    dia = models.CharField('Dia', max_length = 3, choices = DIA)
    cantHoras = models.IntegerField('Cantidad de Horas', blank=True, null=True)