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
from Operarios.models import Alertas
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Operarios.models import PuntoServicio, Operario, AsignacionCab, AsignacionDet, AsigFiscalPuntoServicio
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


def gestion_alertas(request,alerta_id=None):
    

    alerta=Alertas.objects.get(id=alerta_id)
    """obtener operario"""
    operario=Operario.objects.get(id=alerta.Operario.id)
    puntoServicio=PuntoServicio.objects.get(id=alerta.PuntoServicio.id)
    """obtener el horario de ese punto de servicio para ese personaje"""
    asignacionCab=AsignacionCab.objects.get(puntoServicio=puntoServicio)
    asignacionOperario=AsignacionDet.objects.get(asignacionCab=asignacionCab, operario=operario)
    fiscal=AsigFiscalPuntoServicio.objects.get(puntoServicio=puntoServicio)
    supervisor=AsignacionDet.objects.filter(asignacionCab=asignacionCab, supervisor=True)[0]
    alertasSinAsig=Alertas.objects.filter(Tipo__contains="SIN-ASIG",Estado__contains="ABIERTA", PuntoServicio=puntoServicio)
    """CAMBIAMOS EL ESTADO DE LA ALERTA"""
    if request.method == GET:
        setattr(alerta,Estado, "EN GESTION")
    else: 
        print ("Es POST")
    
    contexto = {
        'title': 'Gestion de Alertas',
        'operario':operario,
        'puntoServicio':puntoServicio ,
        'alerta':alerta,
        'asignacion':asignacionOperario,
        'fiscal':fiscal,
        'supervisor':supervisor,
        'alertasSinAsig':alertasSinAsig
    }
    return render(request, 'alertas/alerta_gestionar.html', context=contexto)