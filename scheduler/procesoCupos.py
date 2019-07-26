import logging
import datetime as dt
from Operarios.models import  PuntoServicio, PlanificacionOpe, PlanificacionCab,AsignacionCab,AsignacionDet, CalendarioCupo, CupoReal
from django.db.models import Q
from math import floor
import datetime


def SumaHoras(h1,h2):
    sp = h1.split(":")
    hora1 = sp[0]
    min1 = sp[1]

    sp = h2.split(":")
    hora2 = sp[0]
    min2 = sp[1]

    hora_total = int(hora1) + int(hora2)
    min_pre = int(min1) + int(min2)

    horas_adicionales = floor((min_pre / 60))
    hora_total =hora_total + horas_adicionales
    min_total = (min_pre - (horas_adicionales * 60))
    p=str(min_total).zfill(2)
    x= str(hora_total).zfill(2) + ":" + p + ":00"
    return x


def generarCantidadCupos():
    puntosServ=PuntoServicio.objects.all()
    asignacion=AsignacionDet.objects.all()
    asigCabecera= AsignacionCab.objects.all()
    mes ='0'+ str(datetime.datetime.now().month)
    anho=str(datetime.datetime.now().year)
    cantLunes=""
    cantMartes=""
    cantMiercoles=""
    cantJueves=""
    cantViernes=""
    cantSabado=""
    cantDomingo=""
    if(CalendarioCupo.objects.filter(Q(mes=mes )  & Q(anho=anho)).exists()):
        calendario=CalendarioCupo.objects.get(Q(mes=mes))
        cantLunes=calendario.cantLunes
        cantMartes=calendario.cantMartes
        cantMiercoles=calendario.cantMiercoles
        cantJueves=calendario.cantJueves
        cantViernes=calendario.cantViernes
        cantSabado=calendario.cantSabado
        cantDomingo=calendario.cantDomingo
    for p in puntosServ:
        date_time_str ='00:00:00'
        totalCalculado='00:00:00'
        Hrslunes=datetime.datetime.strptime(date_time_str, '%H:%M:%S')
        HrsMartes=datetime.datetime.strptime(date_time_str, '%H:%M:%S')
        HrsMiercoles=datetime.datetime.strptime(date_time_str, '%H:%M:%S')
        HrsJueves=datetime.datetime.strptime(date_time_str, '%H:%M:%S')
        HrsViernes=datetime.datetime.strptime(date_time_str, '%H:%M:%S')
        HrsSabados=datetime.datetime.strptime(date_time_str, '%H:%M:%S')
        HrsDomingo=datetime.datetime.strptime(date_time_str, '%H:%M:%S')
        for asigCab in asigCabecera:
            if asigCab.puntoServicio_id == p.id:
                for a in asignacion:
                    if a.asignacionCab_id==asigCab.id:
                        if(a.lunEnt!=None and a.lunSal!=None ):
                            difLunes=datetime.datetime.combine(datetime.date.today(), a.lunSal) - datetime.datetime.combine(datetime.date.today(), a.lunEnt)
                            Hrslunes=Hrslunes + difLunes
                        if(a.marEnt!=None and a.marSal!=None ):
                            difMartes=datetime.datetime.combine(datetime.date.today(), a.marSal) - datetime.datetime.combine(datetime.date.today(), a.marEnt)
                            HrsMartes=HrsMartes + difMartes
                        if(a.mieEnt!=None and a.mieSal!=None ):
                            difMier=datetime.datetime.combine(datetime.date.today(), a.mieSal) - datetime.datetime.combine(datetime.date.today(), a.mieEnt)
                            HrsMiercoles=HrsMiercoles + difMier
                        if(a.jueEnt!=None and a.jueSal!=None ):
                            difJue=datetime.datetime.combine(datetime.date.today(), a.jueSal) - datetime.datetime.combine(datetime.date.today(), a.jueEnt)
                            HrsJueves=HrsJueves + difJue
                        if(a.vieEnt!=None and a.vieSal!=None ):
                            difVier=datetime.datetime.combine(datetime.date.today(), a.vieSal) - datetime.datetime.combine(datetime.date.today(), a.vieEnt)
                            HrsViernes=HrsViernes + difVier
                        if(a.sabEnt!=None and a.sabSal!=None ):
                            difSab=datetime.datetime.combine(datetime.date.today(), a.sabSal) - datetime.datetime.combine(datetime.date.today(), a.sabEnt)
                            HrsSabados=HrsSabados + difSab
                        if(a.domEnt!=None and a.domSal!=None ):
                            difVDom=datetime.datetime.combine(datetime.date.today(), a.domSal) - datetime.datetime.combine(datetime.date.today(), a.domEnt)
                            HrsDomingo=HrsDomingo + difVDom
        if(str(Hrslunes.time())!=date_time_str or str(HrsMartes.time())!=date_time_str or str(HrsMiercoles.time()) !=date_time_str or
          str(HrsJueves.time())!=date_time_str or str(HrsViernes.time()) !=date_time_str or str(HrsSabados.time())!=date_time_str
          or str(HrsDomingo.time()) !=date_time_str):
            print("\nEste es el punto de servicio:")
            print(p.NombrePServicio)
            print(p.id)
            print("Mes: "+mes)
            print("año: "+anho)
        if(str(Hrslunes.time())!=date_time_str):
            totalLunes='00:00:00'
            for i in range(0,cantLunes):
                totalLunes=SumaHoras(totalLunes,str(Hrslunes.time()))
            print("BUENO ACA total lunes: ")
            print(totalLunes)
            totalCalculado=SumaHoras(totalCalculado,totalLunes)
        if(str(HrsMartes.time())!=date_time_str):
            totalMartes='00:00:00'
            for i in range(0,cantMartes):
                totalMartes=SumaHoras(totalMartes,str(HrsMartes.time()))
            print("BUENO ACA total martes: ")
            print(totalMartes)
            totalCalculado=SumaHoras(totalCalculado,totalMartes)
        if(str(HrsMiercoles.time())!=date_time_str):
            totalMiercoles='00:00:00'
            for i in range(0,cantMiercoles):
                totalMiercoles=SumaHoras(totalMiercoles,str(HrsMiercoles.time()))
            print("BUENO ACA total MIERCOLES: ")
            print(totalMiercoles)
            totalCalculado=SumaHoras(totalCalculado,totalMiercoles)
        if(str(HrsJueves.time())!=date_time_str):
            totalJueves='00:00:00'
            for i in range(0,cantJueves):
                totalJueves=SumaHoras(totalJueves,str(HrsJueves.time()))
            print("BUENO ACA total jueves: ")
            print(totalJueves)
            totalCalculado=SumaHoras(totalCalculado,totalJueves)
        if(str(HrsViernes.time()) !=date_time_str):
            totalViernes='00:00:00'
            for i in range(0,cantViernes):
                totalViernes=SumaHoras(totalViernes,str(HrsViernes.time()))
            print("BUENO ACA total viernes: ")
            print(totalViernes)
            totalCalculado=SumaHoras(totalCalculado,totalViernes)
        if(str(HrsSabados.time())!=date_time_str ):
            totalSabado='00:00:00'
            for i in range(0,cantSabado):
                totalSabado=SumaHoras(totalSabado,str(HrsSabados.time()))
            print("BUENO ACA total sabado: ")
            print(totalSabado)
            totalCalculado=SumaHoras(totalCalculado,totalSabado)
        if(str(HrsDomingo.time()) !=date_time_str):
            totalDomingo='00:00:00'
            for i in range(0,cantDomingo):
                totalDomingo=SumaHoras(totalDomingo,str(HrsDomingo.time()))
            print("BUENO ACA total domingo: ")
            print(totalDomingo)
            totalCalculado=SumaHoras(totalCalculado,totalDomingo)
        if(str(Hrslunes.time())!=date_time_str or str(HrsMartes.time())!=date_time_str or str(HrsMiercoles.time()) !=date_time_str or
          str(HrsJueves.time())!=date_time_str or str(HrsViernes.time()) !=date_time_str or str(HrsSabados.time())!=date_time_str
          or str(HrsDomingo.time()) !=date_time_str):
            print("Total Calculado: ")
            print(totalCalculado)