import logging
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, Http404
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.forms.models import inlineformset_factory
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from datetime import date
from datetime import datetime
from django.core import serializers
from Operarios.models import Alertas
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Operarios.models import PuntoServicio, Operario, AsignacionCab, AsignacionDet, AsigFiscalPuntoServicio, EsmeEmMarcaciones
from django.db import connection
from Operarios.models import OperariosAsignacionDet
import datetime
def alertasList (request):
    estado="Abierta"
    fechaDesde=request.GET.get('fechaDesde')
    fechaHasta=request.GET.get('fechaHasta')
    puntoServicio=None
    operario=None
    tipoAlerta=None
    """query por defecto con fecha del dia"""
    hoy= datetime.now()
    hoyIni=hoy.replace(hour=0,minute=0,second=0, microsecond=0)

    hoyFin=hoyIni.replace(hour=23,minute=59,second=59)
    alertasList=Alertas.objects.filter(FechaHora__gte=hoyIni,FechaHora__lte=hoyFin)
    operarios = Operario.objects.all()
    PuntosServicio = PuntoServicio.objects.all()
    alertasList=alertasList.filter(Estado="ABIERTA")
    alertasList=alertasList.order_by("-FechaHora")
    """query por filtro segun el usuario"""
    print (request.GET.get('puntoServicio'))
    print (request.GET.get('fechaDesde'))
    print (request.GET.get('fechaHasta'))
    print (request.GET.get('estado'))
    print (request.GET.get('tipoAlerta'))
    print (request.GET.get('operario'))
    if request.GET.get("fechaDesde") and request.GET.get("fechaHasta"):
        fechaDesdeAux=datetime.strptime(request.GET.get('fechaDesde'), "%d/%m/%Y").replace(hour=0,minute=0,second=0, microsecond=0)
        fechaHastaAux=datetime.strptime(request.GET.get('fechaHasta'), "%d/%m/%Y").replace(hour=23,minute=59,second=59, microsecond=0)     
        alertasList=Alertas.objects.filter(FechaHora__gte=fechaDesdeAux,FechaHora__lte=fechaHastaAux)
        
    if request.GET.get('estado'):
        alertasList=alertasList.filter(Estado__contains=request.GET.get('estado'))
        estado=request.GET.get('estado')
    if request.GET.get('tipoAlerta'):
        alertasList=alertasList.filter(Tipo__contains=request.GET.get('tipoAlerta'))
        tipoAlerta=request.GET.get('tipoAlerta')
    if request.GET.get('operario') :
        alertasList=alertasList.filter(Operario_id=request.GET.get('operario'))
        operario=int(request.GET.get('operario'))
    if request.GET.get('puntoServicio') :
        alertasList=alertasList.filter(PuntoServicio_id=request.GET.get('puntoServicio'))
        puntoServicio=int(request.GET.get('puntoServicio'))
    """se procede a obtener la paginacion"""
    pageNumber=request.GET.get("page",1)
    paginar=do_paginate(alertasList.order_by("-FechaHora"), pageNumber)
    alertasList=paginar[0]
    paginator=paginar[1]
    print (len(alertasList))

    for a in alertasList:
        if a.FechaHora:
            fecha = (a.FechaHora).strftime("%d/%m/%Y")
            a.Fecha = fecha
            hora = (a.FechaHora).strftime("%H:%M:%S")
            a.Hora = hora

        if a.Operario_id:
            try:
                operario = Operario.objects.get(id=a.Operario_id)
                a.Operario_nombre = operario.nombre
            except Operario.DoesNotExist:
                raise Http404("Operario relacionado a una Alerta no existe")  

        if a.PuntoServicio_id:
            try:
                punto = PuntoServicio.objects.get(id=a.PuntoServicio_id)
                a.Punto_nombre = punto.NombrePServicio
            except PuntoServicio.DoesNotExist:
                raise Http404("Punto de Servicio relacionado a una Alerta no existe")  

    contexto = {
        'title': 'Filtrado de Alertas',
        'alertasList':alertasList,
        'paginator':paginator,
        'operarios':operarios,
        'PuntosServicio':PuntosServicio,
        "fechaDesde":fechaDesde,
        "fechaHasta":fechaHasta, 
        "estado":estado,
        "puntoServicio":puntoServicio,
        "operario":operario,
        "tipoAlerta":tipoAlerta
    
        
    }

    return render(request, 'alertas/alerta_list.html', context=contexto)


def do_paginate(data_list, page_number):
    ret_data_list=data_list
    result_per_page=10
    paginator=Paginator(data_list, result_per_page)
    try:
        ret_data_list=paginator.page(page_number)
    except EmptyPage:
        ret_data_list=paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        ret_data_list=paginator.page(1)
    return [ret_data_list, paginator]


def getMarcaciones(request):
    print(request.GET.get('alerta_id'))
    alerta_id= request.GET.get('alerta_id')
    alerta=Alertas.objects.get(id=alerta_id)
    operario=Operario.objects.get(id=alerta.Operario.id)
    ultimasMarcaciones=EsmeEmMarcaciones.objects.filter(codpersona__contains=operario.numCedula).order_by("fecha")[:10]
    
    return HttpResponse(serializers.serialize("json",ultimasMarcaciones), content_type = 'application/json', status = 200);

def getReemplazos(request):
    print(request.GET.get('alerta_id'))
    totalHoras=idPunto="" 
    lunEnt=lunSal=marEnt=marSal=mieEnt=mieSal=jueEnt=jueSal=vieEnt=vieSal=sabEnt=sabSal=domEnt=domSal=""
    fechaIni = ""
    diaInicio=diaFin=""
    horaInicio=horaFin=""
    supervisor=False
    perfil=""
    fechaFin=""
    operarios = []
    if request.GET.get('id_puntoServicio')  is not None and request.GET.get('id_puntoServicio')!='':
        idPunto = request.GET.get('id_puntoServicio')
    if request.GET.get('fechaInicio')  is not None and request.GET.get('fechaInicio')!='':
        fechaIni = request.GET.get('fechaInicio')
        date_time_obj = datetime.datetime.strptime(fechaIni,'%d/%m/%Y')
        fechaIni=date_time_obj.strftime('%Y-%m-%d')
    if request.GET.get('horarioInicio')  is not None and request.GET.get('horarioInicio')!='' and "lun" in request.GET.get('diaRequerido'):
        lunEnt = request.GET.get('horarioInicio') 
    if request.GET.get('horarioFin')  is not None and request.GET.get('horarioFin')!='' and "lun" in request.GET.get('diaRequerido'):
        lunSal = request.GET.get('horarioFin') 
    if request.GET.get('horarioInicio')  is not None and request.GET.get('horarioInicio')!='' and "mar" in request.GET.get('diaRequerido'):
        marEnt = request.GET.get('horarioInicio') 
    if request.GET.get('horarioFin')  is not None and request.GET.get('horarioFin')!='' and "mar" in request.GET.get('diaRequerido'):
        marSal = request.GET.get('horarioFin')
    if request.GET.get('horarioInicio')  is not None and request.GET.get('horarioInicio')!='' and "mie" in request.GET.get('diaRequerido'):
        mieEnt = request.GET.get('horarioInicio') 
    if request.GET.get('horarioFin')  is not None and request.GET.get('horarioFin')!='' and "mie" in request.GET.get('diaRequerido'):
        mieSal = request.GET.get('horarioFin')
    if request.GET.get('horarioInicio')  is not None and request.GET.get('horarioInicio')!='' and "jue" in request.GET.get('diaRequerido'):
        jueEnt = request.GET.get('horarioInicio') 
    if request.GET.get('horarioFin')  is not None and request.GET.get('horarioFin')!='' and "jue" in request.GET.get('diaRequerido'):
        jueSal = request.GET.get('horarioFin')
    if request.GET.get('horarioInicio')  is not None and request.GET.get('horarioInicio')!='' and "vie" in request.GET.get('diaRequerido'):
        vieEnt = request.GET.get('horarioInicio') 
    if request.GET.get('horarioFin')  is not None and request.GET.get('horarioFin')!='' and "vie" in request.GET.get('diaRequerido'):
        vieSal = request.GET.get('horarioFin')
    if request.GET.get('horarioInicio')  is not None and request.GET.get('horarioInicio')!='' and "sab" in request.GET.get('diaRequerido'):
        sabEnt = request.GET.get('horarioInicio') 
    if request.GET.get('horarioFin')  is not None and request.GET.get('horarioFin')!='' and "sab" in request.GET.get('diaRequerido'):
        sabSal = request.GET.get('horarioFin')
    if request.GET.get('horarioInicio')  is not None and request.GET.get('horarioInicio')!='' and "dom" in request.GET.get('diaRequerido'):
        domEnt = request.GET.get('horarioInicio') 
    if request.GET.get('horarioFin')  is not None and request.GET.get('horarioFin')!='' and "dom" in request.GET.get('diaRequerido'):
        domSal = request.GET.get('horarioFin')

    operarios = buscar_operarios(
        idPunto,
        totalHoras, 
        lunEnt,  
        lunSal,  
        marEnt,  
        marSal,  
        mieEnt,  
        mieSal,  
        jueEnt,  
        jueSal,  
        vieEnt,  
        vieSal,  
        sabEnt,  
        sabSal,  
        domEnt,  
        domSal,
        perfil,
        supervisor,
        fechaIni,
        fechaFin,
        horaInicio,
        horaFin,
        diaInicio,
        diaFin,
        )
        
    if request.GET.get('nombres')  is not None and request.GET.get('nombres')!='':
        operarios = [x for x in operarios if (request.GET.get('nombres')).lower() in (x.nombres).lower()]
    if request.GET.get('nroLegajo')  is not None and request.GET.get('nroLegajo')!='':
        operarios = [x for x in operarios if (request.GET.get('nroLegajo')).lower() in (x.nroLegajo).lower()]
    if request.GET.get('antiguedad')  is not None and request.GET.get('antiguedad')!='':
        operarios = [x for x in operarios if str(request.GET.get('antiguedad')) in str(x.antiguedad)]
    if request.GET.get('nombres_puntoServicio')  is not None and request.GET.get('nombres_puntoServicio')!='':
        operarios = [x for x in operarios if (request.GET.get('nombres_puntoServicio')).lower() in (x.nombres_puntoServicio).lower()]
    if request.GET.get('totalHoras')  is not None and request.GET.get('totalHoras')!='':
        operarios = [x for x in operarios if str(request.GET.get('totalHoras')) in str(x.totalHoras)]
    if request.GET.get('perfil')  is not None and request.GET.get('perfil')!='':
        operarios = [x for x in operarios if (request.GET.get('perfil')).lower() in (x.perfil).lower()]
    
    return HttpResponse(serializers.serialize("json",operarios), content_type = 'application/json', status = 200)

def buscar_operarios(puntoServicio, totalHoras, lunEntReq, lunSalReq, marEntReq, marSalReq, mierEntReq, mierSalReq, juevEntReq, juevSalReq, vieEntReq, vieSlReq, sabEntReq, sabSalReq, domEntReq, domSalReq,perfil,supervisor, fechaInicioOp,fechaFinOp,horaInicio,horaFin,diaInicio,diaFin):
        conn= connection.cursor()
        sql = """\
            DECLARE @out nvarchar(max);
            EXEC [dbo].[operarios_disponibles_v2] @puntoServicio=?, @totalHoras=?, @lunEntReq=?, @lunSalReq=?, @marEntReq=?, @marSalReq=?, @mierEntReq=?, @mierSalReq=?, @juevEntReq=?, @juevSalReq=?, @vieEntReq=?, @vieSlReq=?, @sabEntReq=?, @sabSalReq=?, @domEntReq=?, @domSalReq=?, @fechaInicioOperario=?, @fechaFinOperario=?,@perfil=?, @param_out = @out OUTPUT;
            SELECT @out AS the_output;
        """
        """conn.callproc('operarios_disponibles_v2', [puntoServicio, totalHoras, lunEntReq, lunSalReq, marEntReq, marSalReq, mierEntReq, mierSalReq, juevEntReq, juevSalReq, vieEntReq, vieSlReq, sabEntReq, sabSalReq, domEntReq, domSalReq, fechaInicioOp])"""
        params=(puntoServicio, totalHoras, lunEntReq, lunSalReq, marEntReq, marSalReq, mierEntReq, mierSalReq, juevEntReq, juevSalReq, vieEntReq, vieSlReq, sabEntReq, sabSalReq, domEntReq, domSalReq, fechaInicioOp, fechaFinOp,perfil)
        print(params)
        conn.execute('operarios_disponibles_v2 %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s',params)
        result = conn.fetchall()
       
        conn.close()
        return [OperariosAsignacionDet(*row) for row in result]

def gestion_alertas(request,alerta_id=None):
    

    alerta=Alertas.objects.get(id=alerta_id)
    if alerta.FechaHora:
            fecha = (alerta.FechaHora).strftime("%d/%m/%Y")
            alerta.Fecha = fecha 
            hora = (alerta.FechaHora).strftime("%H:%M:%S")
            alerta.Hora = hora
    print(alerta.Fecha)
    """obtener operario"""
    operario=Operario.objects.get(id=alerta.Operario.id)
    puntoServicio=PuntoServicio.objects.get(id=alerta.PuntoServicio.id)
    """obtener el horario de ese punto de servicio para ese personaje"""
    asignacionCab=AsignacionCab.objects.get(puntoServicio=puntoServicio)
    asignacionOperario=AsignacionDet.objects.get(asignacionCab=asignacionCab, operario=operario)
    fiscal=AsigFiscalPuntoServicio.objects.get(puntoServicio=puntoServicio)
    supervisor=AsignacionDet.objects.filter(asignacionCab=asignacionCab, supervisor=True)[0]
    alertasSinAsig=Alertas.objects.filter(Tipo__contains="SIN-ASIG",Estado__contains="ABIERTA", PuntoServicio=puntoServicio)
    ultimasMarcaciones=EsmeEmMarcaciones.objects.filter(codpersona__contains=operario.numCedula).order_by("fecha")[:10]
    print ("ultimas 10 marcaciones",ultimasMarcaciones)
    """CAMBIAMOS EL ESTADO DE LA ALERTA"""
    if request.method == 'GET':
        setattr(alerta,"Estado", "EN GESTION")
    else: 
        print ("Es POST")
        print(request.POST)
    
    contexto = {
        'title': 'Gestion de Alertas',
        'operario':operario,
        'puntoServicio':puntoServicio ,
        'alerta':alerta,
        'alerta_id':alerta_id,
        'asignacion':asignacionOperario,
        'fiscal':fiscal,
        'supervisor':supervisor,
        'alertasSinAsig':alertasSinAsig
    }
    return render(request, 'alertas/alerta_gestionar.html', context=contexto)