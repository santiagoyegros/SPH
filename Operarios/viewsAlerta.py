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
from Operarios.forms import FiltroAlertaForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def alertasList (request):

        
    """devolver el listado inicial con la fecha por defecto"""
    print ("Filtrar las alertas del dia")    
    hoy= date.today()
    print (hoy)
    
    alertasList=Alertas.objects.filter(FechaHora__gte=hoy,FechaHora__lte=hoy)
    alertasList=alertasList.filter(Estado="Abierto")
    print (alertasList)
    alertasList=alertasList.order_by("-FechaHora")
    pageNumber=request.GET.get("page",1)
    paginar=do_paginate(alertasList, pageNumber)
    alertasList=paginar[0]
    paginator=paginar[1]
    base_url="/alertas/listar/?"

    contexto = {
        'title': 'Filtrado de Alertas',
        'alertasList':alertasList,
        'paginator':paginator,
        'base_url':base_url
    
        
    }

    return render(request, 'alertas/alerta_list.html', context=contexto)
def filtrarAlertas (request):
    alertasList=Alertas.objects.filter(FechaHora__gte=request.POST.get('fechaDesde').strftime("%d-%m-%Y"),FechaHora__lte=request.POST.get('fechaHasta').strftime("%d-%m-%Y"))
    alertasList=alertasList.filter(Estado=request.POST.get('estado'))
    if request.POST.get('estado'):
        alertasList=alertasList.filter(Estado=request.POST.get('estado'))
    if request.POST.get('tipoAlerta'):
        alertasList=alertasList.filter(TipoAlerta=request.POST.get('tipoAlerta'))
    if request.POST.get('tipoAlerta'):
        alertasList=alertasList.filter(TipoAlerta=request.POST.get('tipoAlerta'))
    if request.POST.get('operario'):
        alertasList=alertasList.filter(Operario_id=request.POST.get('operario'))
    if request.POST.get('puntoServicio'):
        alertasList=alertasList.filter(PuntoServicio_id=request.POST.get('puntoServicio'))
    pageNumber=request.GET.get("page",1)
    paginar=do_paginate(alertasList, pageNumber)
    alertasList=paginar[0]
    paginator=paginar[1]
    base_url="/alertas/filtrar/?fechaDesde=" #aca tiene que ir todos los parametros armados
    contexto = {
        'title': 'Filtrado de Alertas',
        'alertasList':alertasList,
        'paginator':paginator,
        'base_url':base_url,
        "fechaDesde":"xxxx" #aca ls datos que se pasaron desde el filtro, cada uno fechaDesde, hasta, estado, etc
    
    }
    return render(request, 'alertas/alerta_list.html', context=contexto)
def limpiarAlertas (request):
    print ("Es post y limpiar, debe quedar inicialmente")
    alertasList=Alertas.objects.filter(FechaHora__gte=request.POST.get('fechaDesde').strftime("%d-%m-%Y"),FechaHora__lte=request.POST.get('fechaHasta').strftime("%d-%m-%Y")).orderBy("desc")
    alertasList=alertasList.filter(Estado="Abierto")
    print (alertasList)
    paginar=do_paginate(alertasList, 1)
    return render(request, 'alertas/alerta_list.html', context=contexto)
    
def do_paginate(data_list, page_number):
    ret_data_list=data_list
    result_per_page=10
    paginator=Paginator(data_list, result_per_page)
    try:
        ret_data_list=paginator.page(page_number)
    except EmptyPage:
        red_data_list=paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        ret_data_list=paginator.page(1)
    return [ret_data_list, paginator]
