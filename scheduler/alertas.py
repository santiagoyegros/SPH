import logging
import datetime
from django.utils import timezone
from django.db.models import Q
from Operarios.models import Alertas,User,Operario,Parametros,AsignacionDet,AsignacionCab,EsmeEmMarcaciones


def registrar_alerta():

    intervalo=int(Parametros.objects.get(tipo__contains="ALERTAS", parametro__contains="INTERVALO").valor)
    tolerancia=int(Parametros.objects.get(tipo__contains="ALERTAS", parametro__contains="TOLERANCIA").valor)
    print('Procedimiento de registro de alertas: ' + str(datetime.datetime.now()))
    hoy=datetime.date.today()
    ahora=datetime.datetime.now().time()
    ahoraCompleto=datetime.datetime.now()
    hastaCompleto=(datetime.datetime.now()-datetime.timedelta(minutes=tolerancia))
    hasta=hastaCompleto.time()
    desdeCompleto=(datetime.datetime.now()-datetime.timedelta(minutes=tolerancia+intervalo))
    desde=desdeCompleto.time()

    dia=datetime.date.weekday(hoy)
    if dia==0:
        asignaciones= AsignacionDet.objects.filter(fechaInicio__lte=hoy,fechaFin__gte=hoy,lunEnt__lt=hasta,lunEnt__gt=desde)
    elif dia==1:
        asignaciones= AsignacionDet.objects.filter(fechaInicio__lte=hoy,fechaFin__gte=hoy,marEnt__lt=hasta,marEnt__gt=desde)
    elif dia==2:
        asignaciones= AsignacionDet.objects.filter(fechaInicio__lte=hoy,fechaFin__gte=hoy,mieEnt__lt=hasta,mieEnt__gt=desde)
    elif dia==3:
        asignaciones= AsignacionDet.objects.filter(fechaInicio__lte=hoy,fechaFin__gte=hoy,jueEnt__lt=hasta,jueEnt__gt=desde)
    elif dia==4:
        asignaciones= AsignacionDet.objects.filter(fechaInicio__lte=hoy,fechaFin__gte=hoy,vieEnt__lt=hasta,vieEnt__gt=desde)
    elif dia==5:
        asignaciones= AsignacionDet.objects.filter(fechaInicio__lte=hoy,fechaFin__gte=hoy,sabEnt__lt=hasta,sabEnt__gt=desde)
    else:
        asignaciones= AsignacionDet.objects.filter(fechaInicio__lte=hoy,fechaFin__gte=hoy,domEnt__lt=hasta,domEnt__gt=desde)

    for asig in asignaciones:
        operario=Operario.objects.get(id=asig.operario.id)
        cabecera=AsignacionCab.objects.get(id=asig.asignacionCab.id)
        desdeMod=timezone.make_aware(desdeCompleto,timezone.get_current_timezone())
        hastaMod=timezone.make_aware(hastaCompleto,timezone.get_current_timezone())
        ahoraMod=timezone.make_aware(ahoraCompleto,timezone.get_current_timezone())
        existeMarcacion=EsmeEmMarcaciones.objects.filter(codpersona__contains=operario.numCedula,
        fecha__lt=hastaMod,fecha__gt=desdeMod)
        existeAlerta=Alertas.objects.filter(FechaHora__gt=desdeMod,FechaHora__lt=ahoraMod,Asignacion=asig)
        cuentaAlerta=existeAlerta.count()
        cuenta=existeMarcacion.count()
        print(cuenta)
        print(cuentaAlerta)
        if cuenta == 0 and cuentaAlerta==0:
            alerta = Alertas(FechaHora=ahoraMod,Operario=operario,Asignacion=asig,PuntoServicio=cabecera.puntoServicio,Estado='Nueva',Tipo='NO-MARC' )
            print("Cree una alerta")
            alerta.save()
        else:
            print("Ya existe la alarma")   