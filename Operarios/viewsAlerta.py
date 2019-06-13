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
import datetime
from datetime import date
from Operarios.models import Alertas
from Operarios.forms import FiltroAlertaForm
def alertasList (request):
    filtrosForm=FiltroAlertaForm
    if request.method == 'POST':
        if request.POST.get('action') == 'filtrar': 
            alertasList=Alertas.objects.filter(FechaHora_range=[filtrosForm.cleaned_data.get('fechaDesde'),filtrosForm.cleaned_data.get('fechaHasta')])
            alertasList=alertasList.filter(Estado=filtrosForm.cleaned_data.get('estado'))
            if filtrosForm.cleaned_data.get('estado'):
                alertasList=alertasList.filter(Estado=filtrosForm.cleaned_data.get('estado'))
            if filtrosForm.cleaned_data.get('tipoAlerta'):
                alertasList=alertasList.filter(TipoAlerta=filtrosForm.cleaned_data.get('tipoAlerta'))
            if filtrosForm.cleaned_data.get('tipoAlerta'):
                alertasList=alertasList.filter(TipoAlerta=filtrosForm.cleaned_data.get('tipoAlerta'))
            if filtrosForm.cleaned_data.get('operario'):
                alertasList=alertasList.filter(Operario_id=filtrosForm.cleaned_data.get('operario'))
            if filtrosForm.cleaned_data.get('puntoServicio'):
                alertasList=alertasList.filter(PuntoServicio_id=filtrosForm.cleaned_data.get('puntoServicio'))

            print ("Es post y filtrar")

        if request.POST.get('action') == 'limpiar': 
            print ("Es post y limpiar, debe quedar inicialmente")
            filtrosForm=FiltroAlertaForm
            alertasList=Alertas.objects.filter(FechaHora_range=[filtrosForm.cleaned_data.get('fechaDesde'),filtrosForm.cleaned_data.get('fechaHasta')]).orderBy("desc")
            alertasList=alertasList.filter(Estado="Abierto")
            print (alertasList) 
    else:
        """devolver el listado inicial con la fecha por defecto"""
        print ("Filtrar las alertas del dia")
        alertasList=Alertas.objects.filter(FechaHora_range=[filtrosForm.cleaned_data.get('fechaDesde'),filtrosForm.cleaned_data.get('fechaHasta')])
        alertasList=alertasList.filter(Estado="Abierto")
        print (alertasList)
    contexto = {
            'title': 'Filtrado de Alertas',
            'alertasList':alertasList,
            'filtrosForm':filtrosForm
            
        }

    return render(request, 'alertas/alerta_list.html', context=contexto)
