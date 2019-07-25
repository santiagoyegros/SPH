import logging
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, Http404,JsonResponse
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
import datetime
from datetime import date
from datetime import datetime as dt 
import json
from django.core import serializers
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from Operarios.models import DiaLibre

def setearEnColumna(entidad,dia,hora):
    if dia != None and dia != "''":
        print("en setear en columna ",dia)
        if hora != '' and hora != None:
            if dia == 'lunEnt':
                entidad.lunEnt = hora
            elif dia == 'lunSal':
                entidad.lunSal = hora
            elif dia == 'marEnt':
                entidad.marEnt = hora
            elif dia == 'marSal':
                entidad.marSal = hora
            elif dia == 'mieEnt':
                entidad.mieEnt = hora
            elif dia == 'mieSal':
                entidad.mieSal = hora
            elif dia == 'jueEnt':
                entidad.jueEnt = hora
            elif dia == 'jueSal':
                entidad.jueSal = hora
            elif dia == 'vieEnt':
                entidad.vieEnt = hora
            elif dia == 'vieSal':
                entidad.vieSal = hora
            elif dia == 'sabEnt':
                entidad.sabEnt = hora
            elif dia == 'sabSal':
                entidad.sabSal = hora
            elif dia == 'domEnt':
                entidad.domEnt = hora
            elif dia == 'domSal':
                entidad.domSal = hora

    return entidad


@login_required
@permission_required('Operarios.add_operario', raise_exception=True)
def Operarios_create(request):
    diasEntrada = [{"id":"lunEnt","dia":"Lunes"},{"id":"marEnt","dia":"Martes"},{"id":"mieEnt", "dia":"Miercoles"},{"id":"jueEnt", "dia":"Jueves"},{"id":"vieEnt", "dia":"Viernes"},{"id":"sabEnt", "dia":"Sabado"}, {"id":"domEnt", "dia":"Domingo"}]
    diasSalida = [{"id":"lunSal","dia":"Lunes"},{"id":"marSal","dia":"Martes"},{"id":"mieSal", "dia":"Miercoles"},{"id":"jueSal", "dia":"Jueves"},{"id":"vieSal", "dia":"Viernes"},{"id":"sabSal", "dia":"Sabado"}, {"id":"domSal", "dia":"Domingo"}]
    diaIniDefault = "domEnt"
    diaFDefault = "domSal"
    horaIniDefault = "00:00"
    lugarNacimientoId=""
    nacionalidadId=""
    horaFDefault="23:59"
    is_valid = True
    if request.method == 'POST': 
        print("POST create",request.POST)
        form = OperarioForm(request.POST)
        print (form.errors)
        if not request.POST.get('diaInicio'):
            is_valid=False
        if not request.POST.get('diaFin'):
            is_valid=False
        if not request.POST.get('horaInicio'):
            is_valid=False
        if not request.POST.get('horaFin'):
            is_valid=False
        
        if form.is_valid() and is_valid:

            new_operario = form.save()
            diaLibre = DiaLibre(fechaCreacion=datetime.datetime.now(),id_operario=new_operario)
            diaLibre = setearEnColumna(diaLibre,request.POST.get('diaInicio'),request.POST.get('horaInicio') )
            diaLibre = setearEnColumna(diaLibre,request.POST.get('diaFin'),request.POST.get('horaFin'))                
            print(diaLibre)
            diaLibre.save()
            messages.success(request, 'Operario creado correctamente.')
            return redirect('Operarios:operarios_vista')
        else:
            lugarNacimientoId = ciudadId = profesionesId = ""
            if request.POST.get('lugarNacimiento'):
                lugarNacimientoId = int(request.POST.get('lugarNacimiento'))
            if request.POST.get('ciudad'):
                ciudadId = int(request.POST.get('ciudad'))
            if request.POST.get('nacionalidad'):
                nacionalidadId =  int(request.POST.get('nacionalidad'))
            if request.POST.get('profesion'):
                profesionesId = str(request.POST.getlist('profesion'))
            #DIA LIBRE
            if request.POST.get('diaInicio'):
                diaIniDefault = request.POST.get('diaInicio') 
            if request.POST.get('diaFin'):
                diaFDefault = request.POST.get('diaFin')
            if request.POST.get('horaInicio'):
                horaIniDefault = request.POST.get('horaInicio') 
            if request.POST.get('horaFin'):
                horaFDefault = request.POST.get('horaFin')

            messages.warning(request, 'No se pudo cargar el Operario, verifique los campos')
            nacionalidadList=Nacionalidad.objects.all()
            ciudadesList=Ciudad.objects.all()
            especialidadesList=Especializacion.objects.all()
            for espe in especialidadesList:
                espe.id_str = str(espe.id)
            
            contexto = {
            'title': 'Nuevo Operario',
            'form': form, 
            'lugarNacimientoId':lugarNacimientoId,
            'ciudadId':ciudadId,
            'nacionalidadId':nacionalidadId,
            'profesionesId':profesionesId,
            'is_valid':is_valid, 
            'diasSalida':diasSalida,
            'diasEntrada':diasEntrada,
            'diaIniDefault':diaIniDefault,
            'diaFDefault':diaFDefault,
            'horaIniDefault':horaIniDefault,
            'horaFDefault':horaFDefault,
            'nacionalidadList': nacionalidadList, 
            'ciudadesList': ciudadesList, 
            'especialidadesList': especialidadesList
            }
    else:
        nacionalidadList=Nacionalidad.objects.all()
        ciudadesList=Ciudad.objects.all()
        print("CIUDADES ",ciudadesList)
        especialidadesList=Especializacion.objects.all()
        form = OperarioForm(initial={'nombre':'', 'apellido':'', 'direccion':'', 'numCedula':'', 'numPasaporte':'', 'barrios':'', 'banco':'', 'ctaBanco':'', 'nombreContacto':'', 'email':'', 'nroLegajo':'', 'latitud':0, 'longitud':0,'lugarNacimiento':'' })
        contexto = {
            'title': 'Nuevo Operario',
            'form': form, 
            'is_valid':is_valid,
            'diasSalida':diasSalida,
            'diasEntrada':diasEntrada,
            'diaIniDefault':diaIniDefault,
            'diaFDefault':diaFDefault,
            'horaIniDefault':horaIniDefault,
            'horaFDefault':horaFDefault,
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
        operarios=operarios.filter(nroLegajo__contains=request.GET.get('nroLegajo'))
    
    if request.GET.get('nombre'):
        operarios=operarios.filter(nombre__contains=request.GET.get('nombre'))

    if request.GET.get('apellido'):
        operarios=operarios.filter(apellido__contains=request.GET.get('apellido'))
        
    if request.GET.get('nroCedula') :
        operarios=operarios.filter(nroCedula__contains=request.GET.get('nroCedula'))
    paginado=Paginator(operarios.order_by('apellido').values("pk", "nombre", "apellido", "nroLegajo", "numCedula", "id"),  request.GET.get('pageSize'))
    listaPaginada=paginado.page(request.GET.get('pageIndex')).object_list
    dataOperarios=list(listaPaginada)

    """
    Filtro nuevo
    """
    lista=dataOperarios
    response_data={}
    response_data["data"]=lista
    response_data["itemsCount"]=len(operarios)
    
    return JsonResponse(response_data)
def checkDiaInicio(diaLibre):
    if diaLibre.domEnt:
        return ["domEnt",diaLibre.domEnt]
    if diaLibre.lunEnt:
        return ["lunEnt",diaLibre.lunEnt]
    if diaLibre.marEnt:
        return ["marEnt",diaLibre.marEnt]
    if diaLibre.mieEnt:
        return ["mieEnt",diaLibre.mieEnt]
    if diaLibre.jueEnt:
        return ["jueEnt",diaLibre.jueEnt]
    if diaLibre.vieEnt:
        return ["vieEnt",diaLibre.vieEnt]
    if diaLibre.sabEnt:
        return ["sabEnt",diaLibre.sabEnt]
    
def checkDiaFin(diaLibre):
    if diaLibre.domSal:
        return ["domSal",diaLibre.domSal]
    if diaLibre.lunSal:
        return ["lunSal",diaLibre.lunSal]
    if diaLibre.marSal:
        return ["marSal",diaLibre.marSal]
    if diaLibre.mieSal:
        return ["mieSal",diaLibre.mieSal]
    if diaLibre.jueSal:
        return ["jueSal",diaLibre.jueSal]
    if diaLibre.vieSal:
        return ["vieSal",diaLibre.vieSal]
    if diaLibre.sabSal:
        return ["sabSal",diaLibre.sabSal]

@login_required
@permission_required('Operarios.change_operario', raise_exception=True)
def Operarios_update(request, pk):
    operarios = Operario.objects.get(id=pk)
    diasEntrada = [{"id":"lunEnt","dia":"Lunes"},{"id":"marEnt","dia":"Martes"},{"id":"mieEnt", "dia":"Miercoles"},{"id":"jueEnt", "dia":"Jueves"},{"id":"vieEnt", "dia":"Viernes"},{"id":"sabEnt", "dia":"Sabado"}, {"id":"domEnt", "dia":"Domingo"}]
    diasSalida = [{"id":"lunSal","dia":"Lunes"},{"id":"marSal","dia":"Martes"},{"id":"mieSal", "dia":"Miercoles"},{"id":"jueSal", "dia":"Jueves"},{"id":"vieSal", "dia":"Viernes"},{"id":"sabSal", "dia":"Sabado"}, {"id":"domSal", "dia":"Domingo"}]
   
    """
        'is_valid' controla la existencia de dia libre en un operario
    """
    is_valid = True
    diaIniDefault = "domEnt"
    diaFDefault = "domSal"
    horaIniDefault = "00:00"
    horaFDefault="23:59"
    if DiaLibre.objects.filter(id_operario=operarios).exists():
        diaLibre = DiaLibre.objects.get(id_operario=operarios)
        diaIniDefault, horaIniDefault= checkDiaInicio(diaLibre)
        diaFDefault, horaFDefault = checkDiaFin(diaLibre)
        print(diaIniDefault,diaFDefault)
    else:
        print("no tiene")
    if request.method == 'GET':
        formatedDateInicio = operarios.fechaInicio.strftime("%d-%m-%Y")
        formatedDateNacimiento = operarios.fechaNacimiento.strftime("%d-%m-%Y")
        operarios.fechaInicio=formatedDateInicio
        operarios.fechaNacimiento=formatedDateNacimiento

        if operarios.fechaFin != None:
            formatedDateFin = operarios.fechaFin.strftime("%d-%m-%Y")
            operarios.fechaFin=formatedDateFin

        form = OperarioForm(instance=operarios)
        ciudadId=""
        lugarNacimientoId=""
        nacionalidadId=""
        ciudadesList=Ciudad.objects.all()
        nacionalidades = Nacionalidad.objects.all()
        for ciudad in ciudadesList:
            if str(ciudad.NombreCiudad) == str(operarios.ciudad):
                ciudadId = ciudad.id
            if str(ciudad.id) == str(operarios.lugarNacimiento_id):
                lugarNacimientoId=ciudad.id
        for nacion in nacionalidades:
            if str(nacion.id) == str(operarios.nacionalidad_id):
                nacionalidadId=nacion.id

        especialidadesList=Especializacion.objects.all()
        for espe in especialidadesList:
                espe.id_str = str(espe.id)

        profesionesId = []
        for pro in operarios.profesion.all():
            profesionesId.append(str(pro.id))
        print("PROFESIONES ",profesionesId)
        nacionalidadList=Nacionalidad.objects.all()
        nacionalidadSelect=operarios.nacionalidad

        lugarSelect=operarios.lugarNacimiento

        contexto = {
            'title': 'Editar Operario',
            'form': form,
            'ciudadId':ciudadId,
            'lugarNacimientoId':lugarNacimientoId,
            'nacionalidadId':nacionalidadId,
            'profesionesId':profesionesId,
            'is_valid':is_valid,
            'diasSalida':diasSalida,
            'diasEntrada':diasEntrada,
            'diaIniDefault':diaIniDefault,
            'diaFDefault':diaFDefault,
            'horaIniDefault':horaIniDefault,
            'horaFDefault':horaFDefault,
            'ciudadesList':ciudadesList,
            'especialidadesList':especialidadesList,
            'nacionalidadList':nacionalidadList,
            'nacionalidadSelect':nacionalidadSelect,
            'lugarSelect':lugarSelect
        }
    else:
        form = OperarioForm(request.POST, instance=operarios)
        print(request.POST)
        if form.is_valid():
            new_operario= form.save()
            if DiaLibre.objects.filter(id_operario=new_operario.id).exists():
                diaLibre = DiaLibre.objects.get(id_operario=new_operario.id)
                diaLibre.delete()
            #Se crea un nuevo registro
            diaLibreNew = DiaLibre(fechaCreacion=datetime.datetime.now(),id_operario=new_operario)
            diaLibreNew = setearEnColumna(diaLibreNew,request.POST.get('diaInicio'),request.POST.get('horaInicio') )
            diaLibreNew = setearEnColumna(diaLibreNew,request.POST.get('diaFin'),request.POST.get('horaFin'))                
            
            diaLibreNew.save()
            messages.success(request, 'Operario modificado correctamente.')
            return redirect('Operarios:operarios_vista')
        else:
            messages.warning(request, 'No se pudo modificar el Operario, verifique los campos')
            profesionesId=lugarNacimientoId=ciudadId=nacionalidadId=""
            if request.POST.get('profesion'):
                profesionesId = str(request.POST.getlist('profesion'))
            if request.POST.get('lugarNacimiento'):
                lugarNacimientoId = int(request.POST.get('lugarNacimiento'))
            if request.POST.get('ciudad'):
                ciudadId = int(request.POST.get('ciudad'))
            if request.POST.get('nacionalidad'):
                nacionalidadId =  int(request.POST.get('nacionalidad'))
            ciudadSelect=operarios.ciudad
            ciudadesList=Ciudad.objects.all()
        
            especialidadesList=Especializacion.objects.all()
            for espe in especialidadesList:
                espe.id_str = str(espe.id)

            nacionalidadList=Nacionalidad.objects.all()
            nacionalidadSelect=operarios.nacionalidad
   
            lugarSelect=operarios.lugarNacimiento
            contexto = {
                'title': 'Editar Operario',
                'form': form,
                'profesionesId':profesionesId,
                'lugarNacimientoId':lugarNacimientoId,
                'ciudadId':ciudadId,
                'nacionalidadId':nacionalidadId,
                'ciudadSelect':ciudadSelect, 
                'is_valid':is_valid,
                'diasSalida':diasSalida,
                'diaIniDefault':diaIniDefault,
                'diaFDefault':diaFDefault,
                'diasEntrada':diasEntrada,
                'horaIniDefault':horaIniDefault,
                'horaFDefault':horaFDefault,
                'ciudadesList':ciudadesList,
                'especialidadesList':especialidadesList,
                'nacionalidadList':nacionalidadList,
                'nacionalidadSelect':nacionalidadSelect,
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

