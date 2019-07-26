import logging
import datetime
from django.db.models import Q
from Operarios.models import Alertas,User,Operario,AsignacionDet,AsignacionCab,EsmeEmMarcaciones


def registrar_alerta():

    tolerancia=10
    intervalo=15
    print('Procedimiento de registro de alertas: ' + str(datetime.datetime.now()))
    hoy=datetime.date.today()
    ahora=datetime.datetime.now().time()
    
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
        existeMarcacion=EsmeEmMarcaciones.objects.filter(codpersona__contains=operario.numCedula,fecha__lt=hastaCompleto,fecha_gt=desdeCompleto)
        if existeMarcacion.len() == 0:
            alerta = Alertas(
                FechaHora=ahoraCompleto,     
                Operario=operario,
                Asignacion=asig,
                PuntoServicio=cabecera.PuntoServicio,
                Estado='Nueva',
                Tipo='NO-MARC' )
            alerta.save()
