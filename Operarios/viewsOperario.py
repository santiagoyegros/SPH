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
from Operarios.forms import  OperarioForm
from Operarios.models import Operario, Nacionalidad, Ciudad, Especializacion
from django.contrib import messages
from datetime import datetime
import json
from django.core import serializers
@login_required
@permission_required('Operarios.add_operario', raise_exception=True)
def Operarios_create(request):
    if request.method == 'POST': 
        form = OperarioForm(request.POST)
        print (form.errors)
        if form.is_valid():
            form.save()
            messages.success(request, 'Operario creado correctamente.')
            return redirect('Operarios:operarios_vista')
        else:
            messages.warning(request, 'No se pudo cargar el Operario, verifique los campos')
            nacionalidadList=Nacionalidad.objects.all()
            ciudadesList=Ciudad.objects.all()
            especialidadesList=Especializacion.objects.all()
            
            contexto = {
            'title': 'Nuevo Operario',
            'form': form, 
            'nacionalidadList': nacionalidadList, 
            'ciudadesList': ciudadesList, 
            'especialidadesList': especialidadesList,
            
            
            }
        
    else:
        nacionalidadList=Nacionalidad.objects.all()
        ciudadesList=Ciudad.objects.all()
        especialidadesList=Especializacion.objects.all()
        form = OperarioForm(initial={'nombre':'', 'apellido':'', 'direccion':'', 'numCedula':'', 'numPasaporte':'', 'barrios':'', 'banco':'', 'ctaBanco':'', 'nombreContacto':'', 'email':'', 'nroLegajo':'', 'latitud':0, 'longitud':0,'lugarNacimiento':'' })
        contexto = {
            'title': 'Nuevo Operario',
            'form': form, 
            'nacionalidadList': nacionalidadList, 
            'ciudadesList': ciudadesList, 
            'especialidadesList': especialidadesList
            
        }
    
    return render(request, 'operarios/operarios_form.html', context=contexto)

@login_required
@permission_required('Operarios.view_operario', raise_exception=True)
def Operarios_list(request):

    operarios = Operario.objects.all()
    
    if request.GET.get('nroLegajo'):
        operarios=operarios.filter(nroLegajo=request.GET.get('nroLegajo'))
    
    if request.GET.get('nombre'):
        operarios=operarios.filter(nombre=request.GET.get('nombre'))

    if request.GET.get('apellido'):
        operarios=operarios.filter(apellido=request.GET.get('apellido'))
        
    if request.GET.get('nroCedula') :
        operarios=operarios.filter(nroCedula=request.GET.get('nroCedula'))

    return HttpResponse(serializers.serialize('json', operarios), content_type = 'application/json', status = 200)

@login_required
@permission_required('Operarios.change_operario', raise_exception=True)
def Operarios_update(request, pk):
    operarios = Operario.objects.get(id=pk)
    if request.method == 'GET':
        formatedDateInicio = operarios.fechaInicio.strftime("%d-%m-%Y")
        formatedDateNacimiento = operarios.fechaNacimiento.strftime("%d-%m-%Y")
        operarios.fechaInicio=formatedDateInicio
        operarios.fechaNacimiento=formatedDateNacimiento

        if operarios.fechaFin != None:
            formatedDateFin = operarios.fechaFin.strftime("%d-%m-%Y")
            operarios.fechaFin=formatedDateFin

  
        form = OperarioForm(instance=operarios)
        ciudadSelect=operarios.ciudad
        ciudadesList=Ciudad.objects.all()
        
        especialidadesList=Especializacion.objects.all()
        especialidadSelect=operarios.profesion.all()

        nacionalidadList=Nacionalidad.objects.all()
        nacionalidadSelect=operarios.nacionalidad

        lugarSelect=operarios.lugarNacimiento
        contexto = {
            'title': 'Editar Operario',
            'form': form,
            'ciudadSelect':ciudadSelect, 
            'ciudadesList':ciudadesList,
            'especialidadesList':especialidadesList,
            'especialidadSelect':especialidadSelect,
            'nacionalidadList':nacionalidadList,
            'nacionalidadSelect':nacionalidadSelect,
            'especialidadSelect':especialidadSelect, 
            'lugarSelect':lugarSelect
        }
    else:
        form = OperarioForm(request.POST, instance=operarios)
       
        if form.is_valid():
            form.save()
            messages.success(request, 'Operario modificado correctamente.')
            return redirect('Operarios:operarios_vista')
        else:
            messages.warning(request, 'No se pudo modificar el Operario, verifique los campos')
            ciudadSelect=operarios.ciudad
            ciudadesList=Ciudad.objects.all()
        
            especialidadesList=Especializacion.objects.all()
            especialidadSelect=operarios.profesion.all()

            nacionalidadList=Nacionalidad.objects.all()
            nacionalidadSelect=operarios.nacionalidad

            lugarSelect=operarios.lugarNacimiento
            contexto = {
                'title': 'Editar Operario',
                'form': form,
                'ciudadSelect':ciudadSelect, 
                'ciudadesList':ciudadesList,
                'especialidadesList':especialidadesList,
                'especialidadSelect':especialidadSelect,
                'nacionalidadList':nacionalidadList,
                'nacionalidadSelect':nacionalidadSelect,
                'especialidadSelect':especialidadSelect,
                 'lugarSelect':lugarSelect
            }
        

    return render(request, 'operarios/operarios_form.html', context=contexto)

@login_required
@permission_required('Operarios.delete_operario', raise_exception=True)
def Operarios_delete(request, pk):
    operarios = Operario.objects.get(id=pk)
    operarios.delete()
    messages.success(request, 'Operario eliminado correctamente')
    return render(request, 'operarios/operarios_list.html')

@login_required
@permission_required('Operarios.view_operario', raise_exception=True)
def getOperariosVista(request):
   return render(request, 'operarios/operarios_list.html')

