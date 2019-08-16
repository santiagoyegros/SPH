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
from Operarios.models import Operario, DiaLibre, AsignacionDet, AsignacionCab
from django.db.models import Q
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm,inch
from reportlab.lib.colors import HexColor
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.utils import ImageReader
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
    diasLibres=getDiaLibre(request.GET.get("id"))
    for a in asignaciones:
        asigAux['id']=int(a.id)
        asigAux['totalHoras']=int(a.totalHoras)
        cab=AsignacionCab.objects.get(id=a.asignacionCab_id)
        asigAux['puntoServicio']=cab.puntoServicio.NombrePServicio
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



    i=1
    data=[]
    for a in asignaciones:
        listaAsigs=[]
        cab=AsignacionCab.objects.get(id=a.asignacionCab_id)
        puntoServ=cab.puntoServicio.NombrePServicio
        if(a.lunEnt and a.lunSal):
            h1=str(a.lunEnt).split(':')
            h2=str(a.lunSal).split(':')
            lunes=h1[0]+':'+h1[1]+" a "+h2[0]+':'+h2[1]
        else:
            lunes=""
        if(a.marEnt and a.marSal):
            h1=str(a.marEnt).split(':')
            h2=str(a.marSal).split(':')
            martes=h1[0]+':'+h1[1]+" a "+h2[0]+':'+h2[1]
        else:
            martes=""
        if(a.mieEnt and a.mieSal):
            h1=str(a.mieEnt).split(':')
            h2=str(a.mieSal).split(':')
            miercoles=h1[0]+':'+h1[1]+" a "+h2[0]+':'+h2[1]
        else:
            miercoles=""
        if(a.jueEnt and a.jueSal):
            h1=str(a.jueEnt).split(':')
            h2=str(a.jueSal).split(':')
            jueves=h1[0]+':'+h1[1]+" a "+h2[0]+':'+h2[1]
        else:
            jueves=""
        if(a.vieEnt and a.vieSal):
            h1=str(a.vieEnt).split(':')
            h2=str(a.vieSal).split(':')
            viernes=h1[0]+':'+h1[1]+" a "+h2[0]+':'+h2[1]
        else:
            viernes=""
        if(a.sabEnt and a.sabSal):
            h1=str(a.sabEnt).split(':')
            h2=str(a.sabSal).split(':')
            sabado=h1[0]+':'+h1[1]+" a "+h2[0]+':'+h2[1]
        else:
            sabado=""
        if(a.domEnt and a.domSal):
            h1=str(a.domEnt).split(':')
            h2=str(a.domSal).split(':')
            domingo=h1[0]+':'+h1[1]+" a "+h2[0]+':'+h2[1]
        else:
            domingo=""
        listaAsigs=[i,puntoServ,a.totalHoras,lunes,martes,miercoles,jueves,viernes,sabado,domingo]
        data.append(listaAsigs)
        i+=1
    print("data es: ",data)

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
        'asignaciones':data
    }
    return HttpResponse(json.dumps(data),content_type="application/json")


def getAsignacionesExcel(request,id_operario=None):
    operario=Operario.objects.get(Q(id=id_operario))
    asignaciones=AsignacionDet.objects.filter(operario_id=operario.id)
    asigAux={}
    listaAsignaciones=[]
    total=0
    diasLibres=getDiaLibre(id_operario)
    cantAsignaciones=0
    for a in asignaciones:
        cantAsignaciones+=1
        total=total+int(a.totalHoras)

 
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
    worksheet.row_dimensions[1].height=20
    worksheet.column_dimensions['A'].width=25
    worksheet.column_dimensions['B'].width=20
    worksheet.column_dimensions['C'].width=20
    worksheet.column_dimensions['D'].width=20
    worksheet.column_dimensions['E'].width=25
    worksheet.column_dimensions['F'].width=20
    worksheet.column_dimensions['G'].width=20
    worksheet.column_dimensions['H'].width=20
    worksheet.column_dimensions['I'].width=20
    worksheet.column_dimensions['J'].width=20
    color=PatternFill(start_color='86273e',end_color='86273e',fill_type='solid')

    columns = [
    'Reporte de operario'
    ]
    row_num = 1
    worksheet.row_dimensions[row_num].font=Font(bold=True,color='FFFFFF',size=18)
    worksheet.row_dimensions[row_num].fill=color
    for col_num, column_title in enumerate(columns, 1):
        cell = worksheet.cell(row=row_num, column=col_num)
        cell.value = column_title
    # Define the titles for columns
    columns = [
        'Nombre',
        'Apellido',
        'Legajo',
        'Día libre inicio',
        'hora',
        'Día libre fin',
        'hora'
    ]
    row_num += 1

    worksheet.row_dimensions[row_num].font=Font(bold=True,color='FFFFFF')
    worksheet.row_dimensions[row_num].alignment=Alignment(horizontal='center')
    worksheet.row_dimensions[row_num].fill=color
    # Assign the titles for each cell of the header
    for col_num, column_title in enumerate(columns, 1):
        cell = worksheet.cell(row=row_num, column=col_num)
        cell.value = column_title

    row = [
        operario.nombre,
        operario.apellido,
        operario.nroLegajo,
        diaLibre1,
        hora1,
        diaLibre2,
        hora2
    ]
    row_num += 1
    worksheet.row_dimensions[row_num].alignment=Alignment(horizontal='center')
    for col_num, cell_value in enumerate(row, 1):
        cell = worksheet.cell(row=row_num, column=col_num)
        cell.value = cell_value

            
    # Define the data for each cell in the row 

    columns = []
    row_num += 1
    for col_num, column_title in enumerate(columns, 1):
        cell = worksheet.cell(row=row_num, column=col_num)
        cell.value = column_title
    total=str(total)+" hrs"
    columns = [
        'Total horas asignadas',
        total
    ]
    row_num += 1
    worksheet["A5"].font=Font(bold=True,size=12,color='FFFFFF')
    worksheet["A5"].fill=color
    worksheet["B5"].font=Font(size=12,color='FFFFFF')
    worksheet["B5"].alignment=Alignment(horizontal='left')
    worksheet["B5"].fill=color

    for col_num, column_title in enumerate(columns, 1):
        cell = worksheet.cell(row=row_num, column=col_num)
        cell.value = column_title

    #Titulos para la tabla
    columns = [
        'Nro',
        'Punto de servicio',
        'Total Horas',
        'Lunes',
        'Martes',
        'Miércoles',
        'Jueves',
        'Viernes',
        'Sábado',
        'Domingo'
    ]
    row_num += 1
    worksheet.row_dimensions[row_num].font=Font(bold=True,color='FFFFFF')
    worksheet.row_dimensions[row_num].alignment=Alignment(horizontal='center')
    worksheet.row_dimensions[row_num].fill=color
    for col_num, column_title in enumerate(columns, 1):
        cell = worksheet.cell(row=row_num, column=col_num)
        cell.value = column_title

    i=1
    for a in asignaciones:
        cab=AsignacionCab.objects.get(id=a.asignacionCab_id)
        puntoServ=cab.puntoServicio.NombrePServicio
        if(a.lunEnt and a.lunSal):
            lunes=str(a.lunEnt)+" a "+str(a.lunSal)
        else:
            lunes=""
        if(a.marEnt and a.marSal):
            martes=str(a.marEnt)+" a "+str(a.marSal)
        else:
            martes=""
        if(a.mieEnt and a.mieSal):
            miercoles=str(a.mieEnt)+" a "+str(a.mieSal)
        else:
            miercoles=""
        if(a.jueEnt and a.jueSal):
            jueves=str(a.jueEnt)+" a "+str(a.jueSal)
        else:
            jueves=""
        if(a.vieEnt and a.vieSal):
            viernes=str(a.vieEnt)+" a "+str(a.vieSal)
        else:
            viernes=""
        if(a.sabEnt and a.sabSal):
            sabado=str(a.sabEnt)+" a "+str(a.sabSal)
        else:
            sabado=""
        if(a.domEnt and a.domSal):
            domingo=str(a.domEnt)+" a "+str(a.domSal)
        else:
            domingo=""
        row = [
            i,
            puntoServ,
            a.totalHoras,
            lunes,
            martes,
            miercoles,
            jueves,
            viernes,
            sabado,
            domingo
        ]
        row_num += 1

        for col_num, cell_value in enumerate(row, 1):
            cell = worksheet.cell(row=row_num, column=col_num)
            cell.value = cell_value
        worksheet.row_dimensions[row_num].alignment=Alignment(horizontal='center')
        i=i+1


    workbook.save(response)
    print("Lista de asignaciiones: ")
    print(listaAsignaciones)
    return response


def getAsignacionesPDF(request,id_operario=None):
    operario=Operario.objects.get(Q(id=id_operario))
    asignaciones=AsignacionDet.objects.filter(operario_id=operario.id)
    asigAux={}
    listaAsignaciones=[]
    total=0
    diasLibres=diasLibres=getDiaLibre(id_operario)
    cantAsignaciones=0
    for a in asignaciones:
        cantAsignaciones+=1
        total=total+int(a.totalHoras)

    diaLibre1=diasLibres[0]["nombre"]
    hora=diasLibres[0]["hEntrada"].split(':')
    hora1=hora[0]+':'+hora[1]
    diaLibre2=diasLibres[len(diasLibres)-1]["nombre"]
    hora=diasLibres[len(diasLibres)-1]["hSalida"].split(':')
    hora2=hora[0]+':'+hora[1]


    
    response=HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename='+operario.nombre+' '+operario.apellido+' - '+operario.nroLegajo+'.pdf'
    buffer = BytesIO()
    c=canvas.Canvas(buffer,pagesize=A4)

    c.setFont('Helvetica-Bold',18)
    c.setFillColor(HexColor('#86273e'))
    c.drawString(30,750,'Reporte de Operario')
    c.setFont('Helvetica',12)
    c.drawString(30,700,'Nombre')
    c.drawString(150,700,'Apellido')
    c.drawString(300,700,'Legajo')
    c.drawString(30,650,'Dia Libre Inicio')
    c.drawString(140,650,'Hora')
    c.drawString(220,650,'Dia Libre Fin')
    c.drawString(300,650,'Hora')
    c.setFillColor(HexColor('#000000'))
    c.drawString(30,680,operario.nombre)
    c.drawString(150,680,operario.apellido)
    c.drawString(300,680,operario.nroLegajo)
    c.drawString(30,630,diaLibre1)
    c.drawString(140,630,hora1)
    c.drawString(220,630,diaLibre2)
    c.drawString(300,630,hora2)
    c.setFont('Helvetica-Bold',14)
    c.setFillColor(HexColor('#86273e'))
    c.drawString(30,580,'Total Horas Asignadas:')
    c.setFillColor(HexColor('#000000'))
    total=str(total)+" hrs."
    c.drawString(200,580,total) 
    logo=ImageReader('http://www.elmejor.com.py/images/logo@2x.png')
    c.drawImage(logo,450,750,width=100,height=70,mask='auto')

    styles=getSampleStyleSheet()
    styleBH=styles["Normal"]
    styleBH.alignment=TA_CENTER
    styleBH.fontSize=10

    nro=Paragraph('''Nro''',styleBH)
    pSer=Paragraph('''Punto Servicio''',styleBH)
    totalHrs=Paragraph('''Total Horas''',styleBH)
    lns=Paragraph('''Lunes''',styleBH)
    mrts=Paragraph('''Martes''',styleBH)
    mrcls=Paragraph('''Miércoles''',styleBH)
    jvs=Paragraph('''Jueves''',styleBH)
    vrns=Paragraph('''Viernes''',styleBH)
    sbd=Paragraph('''Sábado''',styleBH)
    dmg=Paragraph('''Domingo''',styleBH)

    data=[]
    encabezados=[nro,pSer,totalHrs,lns,mrts,mrcls,jvs,vrns,sbd,dmg]
    data.append(encabezados)

    styleN=styles["BodyText"]
    styleN.alignment=TA_CENTER
    styleN.fontSize=7

    i=1
    l=[]
    high=530
    for a in asignaciones:
        listaAsigs=[]
        cab=AsignacionCab.objects.get(id=a.asignacionCab_id)
        puntoServ=cab.puntoServicio.NombrePServicio
        if(a.lunEnt and a.lunSal):
            h1=str(a.lunEnt).split(':')
            h2=str(a.lunSal).split(':')
            lunes=h1[0]+':'+h1[1]+" a "+h2[0]+':'+h2[1]
            lunes=Paragraph(lunes,styleN)
        else:
            lunes=""
        if(a.marEnt and a.marSal):
            h1=str(a.marEnt).split(':')
            h2=str(a.marSal).split(':')
            martes=h1[0]+':'+h1[1]+" a "+h2[0]+':'+h2[1]
            martes=Paragraph(martes,styleN)
        else:
            martes=""
        if(a.mieEnt and a.mieSal):
            h1=str(a.mieEnt).split(':')
            h2=str(a.mieSal).split(':')
            miercoles=h1[0]+':'+h1[1]+" a "+h2[0]+':'+h2[1]
            miercoles=Paragraph(miercoles,styleN)
        else:
            miercoles=""
        if(a.jueEnt and a.jueSal):
            h1=str(a.jueEnt).split(':')
            h2=str(a.jueSal).split(':')
            jueves=h1[0]+':'+h1[1]+" a "+h2[0]+':'+h2[1]
            jueves=Paragraph(jueves,styleN)
        else:
            jueves=""
        if(a.vieEnt and a.vieSal):
            h1=str(a.vieEnt).split(':')
            h2=str(a.vieSal).split(':')
            viernes=h1[0]+':'+h1[1]+" a "+h2[0]+':'+h2[1]
            viernes=Paragraph(viernes,styleN)
        else:
            viernes=""
        if(a.sabEnt and a.sabSal):
            h1=str(a.sabEnt).split(':')
            h2=str(a.sabSal).split(':')
            sabado=h1[0]+':'+h1[1]+" a "+h2[0]+':'+h2[1]
            sabado=Paragraph(sabado,styleN)
        else:
            sabado=""
        if(a.domEnt and a.domSal):
            h1=str(a.domEnt).split(':')
            h2=str(a.domSal).split(':')
            domingo=h1[0]+':'+h1[1]+" a "+h2[0]+':'+h2[1]
            domingo=Paragraph(domingo,styleN)
        else:
            domingo=""
        nro=Paragraph('''Nro''',styleBH)
        puntoServ=Paragraph(puntoServ,styleN)
        totalHrs=Paragraph(a.totalHoras,styleN)
        listaAsigs=[i,puntoServ,totalHrs,lunes,martes,miercoles,jueves,viernes,sabado,domingo]
        data.append(listaAsigs)
        i+=1
        high-=18

    width,height=A4
    table=Table(data,colWidths=[1 * cm, 2.5 * cm, 2 * cm, 2 * cm, 2 * cm, 2 * cm, 2 * cm, 2 * cm, 2 * cm, 2 * cm])
    table.setStyle(TableStyle([
        ('INNEGRID',(0,0),(-1,-1),0.25,colors.black),
        ('BOX',(0,0),(-1,-1),0.25,colors.black),
    ]))

    table.wrapOn(c,width,height)
    table.drawOn(c,30,high)
    c.showPage()


    c.save()
    pdf=buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response




def getDiaLibre(id_operario):
    diasLibres=[]
    dia={
    'nombre':'',
    'hEntrada':'',
    'hSalida':''
    }
    
    if DiaLibre.objects.filter(Q(id_operario_id=id_operario)).exists():
        diaLibre=DiaLibre.objects.get(Q(id_operario_id=id_operario))
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


    return diasLibres