import logging
from django.shortcuts import render, redirect, render_to_response
from django.core import serializers
from datetime import datetime
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, permission_required
from Operarios.models import Operario, DiaLibre, AsignacionDet
from django.db.models import Q
from openpyxl import Workbook
import json

@login_required
def AsigPorOperario(request):
    operarios=Operario.objects.all()
    print("ACA ES UN: ",request.method)
    contexto={
        'operarios':operarios
    }
    return render(request,'reportes/reporte_operarios_asig.html',contexto)


def datosOperario(request):
    operario=Operario.objects.get(Q(id=request.GET.get("id")))
    asignaciones=AsignacionDet.objects.filter(operario_id=operario.id)
    asigAux={}
    listaAsignaciones=[]
    total=0
    diasLibres=[]
    for a in asignaciones:
        asigAux['id']=int(a.id)
        asigAux['totalHoras']=int(a.totalHoras)
        if(a.lunEnt!=None and a.lunSal!=None):
            h=str(a.lunEnt).split(':')
            asigAux['lunEnt']=h[0]+':'+h[1]
            h=str(a.lunSal).split(':')
            asigAux['lunSal']=h[0]+':'+h[1]
        if(a.marEnt!=None and a.marSal!=None):
            h=str(a.marEnt).split(':')
            asigAux['marEnt']=h[0]+':'+h[1]
            h=str(a.marSal).split(':')
            asigAux['marSal']=h[0]+':'+h[1]
        if(a.mieEnt!=None and a.mieSal!=None):
            h=str(a.mieEnt).split(':')
            asigAux['mieEnt']=h[0]+':'+h[1]
            h=str(a.mieSal).split(':')
            asigAux['mieSal']=h[0]+':'+h[1]
        if(a.jueEnt!=None and a.jueSal!=None):
            h=str(a.jueEnt).split(':')
            asigAux['jueEnt']=h[0]+':'+h[1]
            h=str(a.jueSal).split(':')
            asigAux['jueSal']=h[0]+':'+h[1]
        if(a.vieEnt!=None and a.vieSal!=None):
            h=str(a.vieEnt).split(':')
            asigAux['vieEnt']=h[0]+':'+h[1]
            h=str(a.vieSal).split(':')
            asigAux['vieSal']=h[0]+':'+h[1]
        if(a.sabEnt!=None and a.sabSal!=None):
            h=str(a.sabEnt).split(':')
            asigAux['sabEnt']=h[0]+':'+h[1]
            h=str(a.sabSal).split(':')
            asigAux['sabSal']=h[0]+':'+h[1]
        if(a.domEnt!=None and a.domSal!=None):
            h=str(a.domEnt).split(':')
            asigAux['domEnt']=h[0]+':'+h[1]
            h=str(a.domSal).split(':')
            asigAux['domSal']=h[0]+':'+h[1]
        listaAsignaciones.append(asigAux)
        asigAux=asigAux.copy()
        total=total+int(a.totalHoras)
    print("lista asignaciones: ",listaAsignaciones)
    dia={
        'nombre':'',
        'hEntrada':'',
        'hSalida':''
        }
    asi=AsignacionDet.objects.filter(operario_id=operario.id).values()
    if DiaLibre.objects.filter(Q(id_operario_id=operario.id)).exists():
        diaLibre=DiaLibre.objects.get(Q(id_operario_id=operario.id))
        if(diaLibre.lunEnt!=None and diaLibre.lunSal!=None):
            dia=dia.copy()
            dia["nombre"]="Lunes"
            dia["hEntrada"]=str(diaLibre.lunEnt)
            dia["hSalida"]=str(diaLibre.lunSal)
            diasLibres.append(dia)
        if(diaLibre.marEnt!=None and diaLibre.marSal!=None):
            dia["nombre"]="Martes"
            dia["hEntrada"]=str(diaLibre.marEnt)
            dia["hSalida"]=str(diaLibre.marSal)
            diasLibres.append(dia)
        if(diaLibre.mieEnt!=None and diaLibre.mieSal!=None):
            dia["nombre"]="Miercoles"
            dia["hEntrada"]=str(diaLibre.mieEnt)
            dia["hSalida"]=str(diaLibre.mieSal)
            diasLibres.append(dia)
        if(diaLibre.jueEnt!=None and diaLibre.jueSal!=None):
            dia=dia.copy()
            dia["nombre"]="Jueves"
            dia["hEntrada"]=str(diaLibre.jueEnt)
            dia["hSalida"]=str(diaLibre.jueSal)
            diasLibres.append(dia)
        if(diaLibre.vieEnt!=None and diaLibre.vieSal!=None):
            dia=dia.copy()
            dia["nombre"]="Viernes"
            dia["hEntrada"]=str(diaLibre.vieEnt)
            dia["hSalida"]=str(diaLibre.vieSal)
            diasLibres.append(dia)
        if(diaLibre.sabEnt!=None and diaLibre.sabSal!=None):
            dia=dia.copy()
            dia["nombre"]="Sábado"
            dia["hEntrada"]=str(diaLibre.sabEnt)
            dia["hSalida"]=str(diaLibre.sabSal)
            diasLibres.append(dia)
        if(diaLibre.domEnt!=None and diaLibre.domSal!=None):
            dia=dia.copy()
            dia["nombre"]="Domingo"
            dia["hEntrada"]=str(diaLibre.domEnt)
            dia["hSalida"]=str(diaLibre.domSal)
            diasLibres.append(dia)
    diaLibre1=diasLibres[0]["nombre"]
    hora=diasLibres[0]["hEntrada"].split(':')
    hora1=hora[0]+':'+hora[1]
    diaLibre2=diasLibres[len(diasLibres)-1]["nombre"]
    hora=diasLibres[len(diasLibres)-1]["hSalida"].split(':')
    hora2=hora[0]+':'+hora[1]
    data={
        'nombre':operario.nombre,
        'apellido':operario.apellido,
        'legajo':operario.nroLegajo,
        'total':total,
        'diaLibre1':diaLibre1,
        'hora1':hora1,
        'diaLibre2':diaLibre2,
        'hora2':hora2,
        'asignaciones':listaAsignaciones
    }
    return HttpResponse(json.dumps(data),content_type="application/json")


def getAsignacionesExcel(request):
    print("ENTRO ACA EN EL GET EXCEL")
    print("el operario es: ",request.GET.get("id"))
    operario=Operario.objects.get(Q(id=request.GET.get("id")))
    asignaciones=AsignacionDet.objects.filter(operario_id=operario.id)
    asigAux={}
    listaAsignaciones=[]
    total=0
    diasLibres=[]
    for a in asignaciones:
        asigAux['id']=int(a.id)
        asigAux['totalHoras']=int(a.totalHoras)
        if(a.lunEnt!=None and a.lunSal!=None):
            h=str(a.lunEnt).split(':')
            asigAux['lunEnt']=h[0]+':'+h[1]
            h=str(a.lunSal).split(':')
            asigAux['lunSal']=h[0]+':'+h[1]
        if(a.marEnt!=None and a.marSal!=None):
            h=str(a.marEnt).split(':')
            asigAux['marEnt']=h[0]+':'+h[1]
            h=str(a.marSal).split(':')
            asigAux['marSal']=h[0]+':'+h[1]
        if(a.mieEnt!=None and a.mieSal!=None):
            h=str(a.mieEnt).split(':')
            asigAux['mieEnt']=h[0]+':'+h[1]
            h=str(a.mieSal).split(':')
            asigAux['mieSal']=h[0]+':'+h[1]
        if(a.jueEnt!=None and a.jueSal!=None):
            h=str(a.jueEnt).split(':')
            asigAux['jueEnt']=h[0]+':'+h[1]
            h=str(a.jueSal).split(':')
            asigAux['jueSal']=h[0]+':'+h[1]
        if(a.vieEnt!=None and a.vieSal!=None):
            h=str(a.vieEnt).split(':')
            asigAux['vieEnt']=h[0]+':'+h[1]
            h=str(a.vieSal).split(':')
            asigAux['vieSal']=h[0]+':'+h[1]
        if(a.sabEnt!=None and a.sabSal!=None):
            h=str(a.sabEnt).split(':')
            asigAux['sabEnt']=h[0]+':'+h[1]
            h=str(a.sabSal).split(':')
            asigAux['sabSal']=h[0]+':'+h[1]
        if(a.domEnt!=None and a.domSal!=None):
            h=str(a.domEnt).split(':')
            asigAux['domEnt']=h[0]+':'+h[1]
            h=str(a.domSal).split(':')
            asigAux['domSal']=h[0]+':'+h[1]
        listaAsignaciones.append(asigAux)
        asigAux=asigAux.copy()
        total=total+int(a.totalHoras)


    dia={
    'nombre':'',
    'hEntrada':'',
    'hSalida':''
    }
    
    if DiaLibre.objects.filter(Q(id_operario_id=operario.id)).exists():
        diaLibre=DiaLibre.objects.get(Q(id_operario_id=operario.id))
        if(diaLibre.lunEnt!=None and diaLibre.lunSal!=None):
            dia=dia.copy()
            dia["nombre"]="Lunes"
            dia["hEntrada"]=str(diaLibre.lunEnt)
            dia["hSalida"]=str(diaLibre.lunSal)
            diasLibres.append(dia)
        if(diaLibre.marEnt!=None and diaLibre.marSal!=None):
            dia["nombre"]="Martes"
            dia["hEntrada"]=str(diaLibre.marEnt)
            dia["hSalida"]=str(diaLibre.marSal)
            diasLibres.append(dia)
        if(diaLibre.mieEnt!=None and diaLibre.mieSal!=None):
            dia["nombre"]="Miercoles"
            dia["hEntrada"]=str(diaLibre.mieEnt)
            dia["hSalida"]=str(diaLibre.mieSal)
            diasLibres.append(dia)
        if(diaLibre.jueEnt!=None and diaLibre.jueSal!=None):
            dia=dia.copy()
            dia["nombre"]="Jueves"
            dia["hEntrada"]=str(diaLibre.jueEnt)
            dia["hSalida"]=str(diaLibre.jueSal)
            diasLibres.append(dia)
        if(diaLibre.vieEnt!=None and diaLibre.vieSal!=None):
            dia=dia.copy()
            dia["nombre"]="Viernes"
            dia["hEntrada"]=str(diaLibre.vieEnt)
            dia["hSalida"]=str(diaLibre.vieSal)
            diasLibres.append(dia)
        if(diaLibre.sabEnt!=None and diaLibre.sabSal!=None):
            dia=dia.copy()
            dia["nombre"]="Sábado"
            dia["hEntrada"]=str(diaLibre.sabEnt)
            dia["hSalida"]=str(diaLibre.sabSal)
            diasLibres.append(dia)
        if(diaLibre.domEnt!=None and diaLibre.domSal!=None):
            dia=dia.copy()
            dia["nombre"]="Domingo"
            dia["hEntrada"]=str(diaLibre.domEnt)
            dia["hSalida"]=str(diaLibre.domSal)
            diasLibres.append(dia)
    diaLibre1=diasLibres[0]["nombre"]
    hora=diasLibres[0]["hEntrada"].split(':')
    hora1=hora[0]+':'+hora[1]
    diaLibre2=diasLibres[len(diasLibres)-1]["nombre"]
    hora=diasLibres[len(diasLibres)-1]["hSalida"].split(':')
    hora2=hora[0]+':'+hora[1]


    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename={operario}-asignaciones.xlsx'.format(
        operario=str(operario.nombre)+" "+str(operario.apellido) + " - "+str(operario.nroLegajo)
    )
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = 'Asignaciones operario - ' + operario.nombre + ' '+operario.apellido+' - '+operario.nroLegajo
    # Define the titles for columns
    columns = [
        'Nombre',
        'Apellido',
        'Dia libre inicio',
        'hora',
        'Dia libre fin',
        'hora',
        'Total horas asignadas'
    ]
    row_num = 1

    # Assign the titles for each cell of the header
    for col_num, column_title in enumerate(columns, 1):
        cell = worksheet.cell(row=row_num, column=col_num)
        cell.value = column_title

    # Iterate through all movies
    
            
    # Define the data for each cell in the row 
    row = [
        operario.nombre,
        operario.apellido,
        operario.nroLegajo,
        diaLibre1,
        hora1,
        diaLibre2,
        hora2,
        total
    ]
            
    # Assign the data for each cell of the row 
    for col_num, cell_value in enumerate(row, 1):
        cell = worksheet.cell(row=row_num, column=col_num)
        cell.value = cell_value

    workbook.save(response)
    print("response")
    return response