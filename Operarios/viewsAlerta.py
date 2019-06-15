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
from Operarios.models import PuntoServicio, Operario
def alertasList (request):
    estado="Abierto"
    fechaDesde=request.GET.get('fechaDesde')
    fechaHasta=request.GET.get('fechaHasta')
    puntoServicio=None
    operario=None
    """query por defecto con fecha del dia"""
    hoy= date.today()
    alertasList=Alertas.objects.filter(FechaHora__gte=hoy,FechaHora__lte=hoy)
    operarios = Operario.objects.all()
    PuntosServicio = PuntoServicio.objects.all()
    alertasList=alertasList.filter(Estado="Abierto")
    alertasList=alertasList.order_by("-FechaHora")
    """query por filtro segun el usuario"""
    print (request.GET.get('puntoServicio'))
    print (request.GET.get('fechaDesde'))
    print (request.GET.get('fechaHasta'))
    print (request.GET.get('estado'))
    print (request.GET.get('tipoAlerta'))
    print (request.GET.get('operario'))
    if request.GET.get("fechaDesde") and request.GET.get("fechaHasta"):
        alertasList=Alertas.objects.filter(FechaHora__gte=datetime.strptime(request.GET.get('fechaDesde'), "%d/%m/%Y").strftime("%Y-%m-%d"),FechaHora__lte=datetime.strptime(request.GET.get('fechaHasta'), "%d/%m/%Y").strftime("%Y-%m-%d"))
    if request.GET.get('estado'):
        alertasList=alertasList.filter(Estado=request.GET.get('estado'))
        estado=request.GET.get('estado')
    if request.GET.get('tipoAlerta'):
        alertasList=alertasList.filter(Tipo=request.GET.get('tipoAlerta'))
    if request.GET.get('operario') :
        alertasList=alertasList.filter(Operario_id=request.GET.get('operario'))
        operario=int(request.GET.get('operario'))
    if request.GET.get('puntoServicio') :
        alertasList=alertasList.filter(PuntoServicio_id=request.GET.get('puntoServicio'))
        puntoServicio=int(request.GET.get('puntoServicio'))
    """se procede a obtener la paginacion"""
    pageNumber=request.GET.get("page",1)
    paginar=do_paginate(alertasList, pageNumber)
    alertasList=paginar[0]
    paginator=paginar[1]
    print (alertasList)

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
    
        
    }

    return render(request, 'alertas/alerta_list.html', context=contexto)
def filtrarAlertas (request):
    if request.method == 'POST':
        print ("Es POST")
    print ("Intenta filtrar")
    print (request.POST.get('puntoServicio'))
    print (request.POST.get('fechaDesde'))
    print (request.POST.get('fechaHasta'))
    print (request.POST.get('estado'))
    print (request.POST.get('tipoAlerta'))
    print (request.POST.get('operario'))
    fechaDesde=request.POST.get('fechaDesde')
    fechaHasta=request.POST.get('fechaHasta')
    alertasList=Alertas.objects.filter(FechaHora__gte=datetime.strptime(request.POST.get('fechaDesde'), "%d/%m/%Y").strftime("%Y-%m-%d"),FechaHora__lte=datetime.strptime(request.POST.get('fechaHasta'), "%d/%m/%Y").strftime("%Y-%m-%d"))
    print (fechaDesde)
    estado=""
   
    if request.POST.get('estado'):
        alertasList=alertasList.filter(Estado=request.POST.get('estado'))
        estado=request.POST.get('estado')
    if request.POST.get('tipoAlerta'):
        alertasList=alertasList.filter(Tipo=request.POST.get('tipoAlerta'))
    if request.POST.get('operario') :
        alertasList=alertasList.filter(Operario_id=request.POST.get('operario'))
    if request.POST.get('puntoServicio') :
        alertasList=alertasList.filter(PuntoServicio_id=request.POST.get('puntoServicio'))
    pageNumber=request.GET.get("page",1)
    paginar=do_paginate(alertasList, pageNumber)
    alertasList=paginar[0]
    paginator=paginar[1]
    base_url="/alertas/filtrar/?fechaDesde="+request.POST.get('fechaDesde')+"&fechaHasta="+fechaHasta+"&estado="+estado #aca tiene que ir todos los parametros armados
    contexto = {
        'title': 'Filtrado de Alertas',
        'alertasList':alertasList,
        'paginator':paginator,
        'base_url':base_url,
        "fechaDesde":fechaDesde,
        "fechaHasta":fechaHasta #aca ls datos que se pasaron desde el filtro, cada uno fechaDesde, hasta, estado, etc
    
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
