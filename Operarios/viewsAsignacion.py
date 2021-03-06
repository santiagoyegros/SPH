import logging
from django.shortcuts import render, redirect, render_to_response
from django.template.loader import render_to_string
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
from django.db import connection, transaction
import datetime
from datetime import date
from django.core import serializers
from Operarios.models import PuntoServicio, Operario, RelevamientoCab, RelevamientoDet, RelevamientoEsp, RelevamientoCupoHoras, RelevamientoMensualeros, PlanificacionCab, PlanificacionOpe, PlanificacionEsp, Cargo, CargoAsignado, AsigFiscalPuntoServicio, AsigJefeFiscal, AsignacionCab, AsignacionDet, DiaLibre, OperariosAsignacionDet, Especializacion, AsignacionesDet, AsignacionDetTemp
from Operarios.forms import PuntoServicioForm, OperarioForm, RelevamientoForm, RelevamientoDetForm, RelevamientoEspForm, RelevamientoCupoHorasForm, RelevamientoMensualerosForm, PlanificacionForm, PlanificacionOpeForm, PlanificacionEspForm, AsignacionCabForm, AsignacionDetForm
from ast import literal_eval
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime as dt
import json
from django.db.models import Q



@login_required
@permission_required('Operarios.view_asignacioncab', raise_exception=True)
def Asignacion_agregar(request,id_puntoServicio=None,id_asignacionDetalle=None):
    perfiles = Especializacion.objects.all() 
    if request.method == 'POST':
        print("ES POST")
    else:
        print("NO ES POST",id_puntoServicio)
        totalHora=totalHoraAsig=None
        if RelevamientoCab.objects.filter(Q(puntoServicio_id=id_puntoServicio)).exists():
            relevamientoCab = RelevamientoCab.objects.get(Q(puntoServicio_id=id_puntoServicio))
            totalHora = relevamientoCab.cantidadHrTotal
        if AsignacionCab.objects.filter(puntoServicio_id=id_puntoServicio).exists():
            asignacionCab=AsignacionCab.objects.get(puntoServicio_id=id_puntoServicio)
            if asignacionCab.totalasignado == None:
                totalHoraAsig = "00:00"
            else:
                totalHoraAsig = asignacionCab.totalasignado
    
    contexto = {
        'title': 'Asignación de Operarios',
        'totalHora':totalHora,
        'totalHoraAsig':totalHoraAsig,
        'perfiles':perfiles,
        'id_puntoServicio':id_puntoServicio,
        'id_asignacionDetalle':id_asignacionDetalle
    }
    return render(request, 'asignacion/asignacion_agregar_detalle.html',context=contexto)

@login_required
@permission_required('Operarios.view_asignacioncab', raise_exception=True)
def Asignacion_ver(request,id_puntoServicio=None):
    perfiles = Especializacion.objects.all() 

    totalHora=totalHoraAsig=None
    if RelevamientoCab.objects.filter(Q(puntoServicio_id=id_puntoServicio)).exists():
        relevamientoCab = RelevamientoCab.objects.get(Q(puntoServicio_id=id_puntoServicio))
        totalHora = relevamientoCab.cantidadHrTotal
    if AsignacionCab.objects.filter(puntoServicio_id=id_puntoServicio).exists():
        asignacionCab=AsignacionCab.objects.get(puntoServicio_id=id_puntoServicio)
        if asignacionCab.totalasignado == None:
            totalHoraAsig = "00:00"
        else:
            totalHoraAsig = asignacionCab.totalasignado
    
    contexto = {
        'title': 'Asignación de Operarios',
        'totalHora':totalHora,
        'totalHoraAsig':totalHoraAsig,
        'perfiles':perfiles,
        'id_puntoServicio':id_puntoServicio,
        'id_asignacion':asignacionCab.id
    }
    return render(request, 'asignacion/asignacion_ver_detalle.html',context=contexto)


def getAsignacionDetalleByTipo(request,id_asignacionDetalle):
    try:
        response = {}
        tipo = request.POST.get('tipo')
        asignacion=None
        if tipo.lower() == 'temporal':
            if  AsignacionDetTemp.objects.filter(id=id_asignacionDetalle).exists():
                asignacion = AsignacionDetTemp.objects.get(id=id_asignacionDetalle)
        elif tipo.lower() == 'persistido':
            if  AsignacionDet.objects.filter(id=id_asignacionDetalle).exists():
                asignacion = AsignacionDet.objects.get(id=id_asignacionDetalle)
        if asignacion:
            operario = Operario.objects.get(id=asignacion.operario_id)
            perfil = Especializacion.objects.get(id = asignacion.perfil_id)
            fechaIni=fechaFin=""
            if asignacion.fechaInicio:
                fechaIni=asignacion.fechaInicio.strftime('%d/%m/%Y')
            if asignacion.fechaFin:
                fechaFin =asignacion.fechaFin.strftime('%d/%m/%Y') 
            asignacion_response = {
                "perfil_id":asignacion.perfil_id,
                "perfilNombre":perfil.especializacion,
                "operario_id":asignacion.operario_id,
                "operarioNombre":operario.nombre + " " + operario.apellido,
                "lunEnt":"" if str(asignacion.lunEnt) == "None" else str(asignacion.lunEnt),
                "lunSal":"" if str(asignacion.lunSal) == "None" else str(asignacion.lunSal),
                "marEnt":"" if str(asignacion.marEnt) == "None" else str(asignacion.marEnt),
                "marSal":"" if str(asignacion.marSal) == "None" else str(asignacion.marSal),
                "mieEnt":"" if str(asignacion.mieEnt) == "None" else str(asignacion.mieEnt),
                "mieSal":"" if str(asignacion.mieSal) == "None" else str(asignacion.mieSal),
                "jueEnt":"" if str(asignacion.jueEnt) == "None" else str(asignacion.jueEnt),
                "jueSal":"" if str(asignacion.jueSal) == "None" else str(asignacion.jueSal),
                "vieEnt":"" if str(asignacion.vieEnt) == "None" else str(asignacion.vieEnt),
                "vieSal":"" if str(asignacion.vieSal) == "None" else str(asignacion.vieSal),
                "sabEnt":"" if str(asignacion.sabEnt) == "None" else str(asignacion.sabEnt),
                "sabSal":"" if str(asignacion.sabSal) == "None" else str(asignacion.sabSal),
                "domEnt":"" if str(asignacion.domEnt) == "None" else str(asignacion.domEnt),
                "domSal":"" if str(asignacion.domSal) == "None" else str(asignacion.domSal),
                "fechaInicio":str(fechaIni),
                "fechaFin":str(fechaFin),
                "supervisor": "true" if str(asignacion.supervisor) == "True" else "false"
            }
        if asignacion:
            response['codigo']=0
            response['dato']=asignacion_response
            response['mensaje']="Asignación obtenida con éxito"
            return HttpResponse(
                json.dumps(response),
                content_type="application/json"
                )
        else:
            response['codigo']=1
            response['dato']=[]
            response['mensaje']="La asignación detalle no existe"
            return HttpResponse(
                json.dumps(response),
                content_type="application/json"
                )
    except Exception as err:
        #transaction.rollback()
        logging.getLogger("error_logger").error('Ocurrió un error al listar la asignacion: {0}'.format(err))
        response['codigo']=1
        response['dato']=[]
        response['mensaje']="Ocurrió un error al listar la asignacion"
        return HttpResponse(
            json.dumps(response),
            content_type="application/json"
        )       

def Eliminar_asignacion(request,id_asignacionDetalle):
    try:
        response = {}
        tipo = request.POST.get('tipo')
        asignacion=None
        if tipo.lower() == 'temporal':
            if  AsignacionDetTemp.objects.filter(id=id_asignacionDetalle).exists():
                asignacion = AsignacionDetTemp.objects.get(id=id_asignacionDetalle)
        elif tipo.lower() == 'persistido':
            if  AsignacionDet.objects.filter(id=id_asignacionDetalle).exists():
                asignacion = AsignacionDet.objects.get(id=id_asignacionDetalle)
        if asignacion:
            asignacion.eliminado = True
            asignacion.save()
            request.session['eliminar']="false"
            response['codigo']=0
            response['dato']=[]
            response['mensaje']="Asignacion eliminada con éxito"
            return HttpResponse(
                json.dumps(response),
                content_type="application/json"
                )
    except Exception as err:
        #transaction.rollback()
        logging.getLogger("error_logger").error('Ocurrió un error al eliminar la asignacion: {0}'.format(err))
        response['codigo']=1
        response['dato']=[]
        response['mensaje']="Ocurrió un error al eliminar la asignacion"
        return HttpResponse(
            json.dumps(response),
            content_type="application/json"
        )       

def formateoFecha(fechaIni):
    if fechaIni:
        date_time_obj = datetime.datetime.strptime(fechaIni,'%d/%m/%Y')
        fechaIni=date_time_obj.strftime('%Y-%m-%d')
        return fechaIni
    return ""
def guardarAsignacionOperario(request):
    request.session['eliminar'] = "false"
    if request.method == 'POST':
        try:
            response={}
            id_puntoServicio=request.POST.get('puntoServicio')
                    
            ''' Obtenemos el punto de servicio'''
            puntoSer = PuntoServicio.objects.get(Q(pk=id_puntoServicio))
                
            ''' Obtenemos la asignacion en caso de que exista una '''
            asignacion = AsignacionCab.objects.filter(Q(puntoServicio_id = puntoSer.id)).first()

            if asignacion == None:
                asignacion = AsignacionCab()

            if request.POST.get('error') is not None and request.POST.get('error')=='true':
                response['codigo']=1
                response['dato']=[]
                response['mensaje']="No se pudo guardar la asignacion, favor verifique las horas asignadas..."

                return HttpResponse(
                    json.dumps(response),
                    content_type="application/json"
                    ) 
            #se crea objeto para el guardado
            totalHoras =  request.POST.get('asignaciondet-totalHoras')
            if totalHoras:
                totalHoras = totalHoras.split(":")[0]
            lunEnt=lunSal=marEnt=marSal=mieEnt=mieSal=jueEnt=jueSal=vieEnt=vieSal=sabEnt=sabSal=domEnt=domSal=None
            fechaFin = "None"
            #SI NO SE INGRESO HORAS O FECHAS, SE ENVIA NONE
            if request.POST.get('asignaciondet-lunEnt'):
                lunEnt = request.POST.get('asignaciondet-lunEnt')
            if request.POST.get('asignaciondet-marEnt'):
                marEnt = request.POST.get('asignaciondet-marEnt')
            if request.POST.get('asignaciondet-mieEnt'):
                mieEnt = request.POST.get('asignaciondet-mieEnt')
            if request.POST.get('asignaciondet-jueEnt'):
                jueEnt = request.POST.get('asignaciondet-jueEnt')
            if request.POST.get('asignaciondet-vieEnt'):
                vieEnt = request.POST.get('asignaciondet-vieEnt')
            if request.POST.get('asignaciondet-sabEnt'):
                sabEnt = request.POST.get('asignaciondet-sabEnt')
            if request.POST.get('asignaciondet-domEnt'):
                domEnt = request.POST.get('asignaciondet-domEnt')

            if request.POST.get('asignaciondet-lunSal'):
                lunSal = request.POST.get('asignaciondet-lunSal')
            if request.POST.get('asignaciondet-marSal'):
                marSal = request.POST.get('asignaciondet-marSal')
            if request.POST.get('asignaciondet-mieSal'):
                mieSal = request.POST.get('asignaciondet-mieSal')
            if request.POST.get('asignaciondet-jueSal'):
                jueSal = request.POST.get('asignaciondet-jueSal')
            if request.POST.get('asignaciondet-vieSal'):
                vieSal = request.POST.get('asignaciondet-vieSal')
            if request.POST.get('asignaciondet-sabSal'):
                sabSal = request.POST.get('asignaciondet-sabSal')
            if request.POST.get('asignaciondet-domSal'):
                domSal = request.POST.get('asignaciondet-domSal')
            
            if request.POST.get('asignaciondet-fechaFin'):
                fechaFin = formateoFecha(str(request.POST.get('asignaciondet-fechaFin')))
            asg_det=""
            asg_det+=str({
                'asignacionCab_id': str(asignacion.id),
                'operario_id':str(str(request.POST.get('asignaciondet-operario')) if request.POST.get('asignaciondet-operario') is not None else 'None'),
                'fechaInicio':formateoFecha(str(request.POST.get('asignaciondet-fechaInicio'))),
                'fechaFin':fechaFin,
                'lunEnt':str(lunEnt),
                'lunSal':str(lunSal),
                'marEnt':str(marEnt),
                'marSal':str(marSal),
                'mieEnt':str(mieEnt),
                'mieSal':str(mieSal),
                'jueEnt':str(jueEnt),
                'jueSal':str(jueSal),
                'vieEnt':str(vieEnt),
                'vieSal':str(vieSal),
                'sabEnt':str(sabEnt),
                'sabSal':str(sabSal),
                'domEnt':str(domEnt),
                'domSal':str(domSal),
                'perfil_id':str(request.POST.get('asignaciondet-perfil')),
                'supervisor': 'True' if request.POST.get('asignaciondet-supervisor') is not None else 'False',
                'totalHoras':totalHoras
            })
            conn= connection.cursor()
            params=(asg_det.replace('\'','\"'),0)
            print("PARAMS",params)
            conn.execute('asignaciondet_tmptrg %s,%s',params)
            result = conn.fetchone()[0]
            conn.close()
            if result==0:
                response['codigo']=0
                response['dato']=[]
                response['mensaje']="Se agregó correctamente la asignación"
                messages.success(request, 'Se agregó correctamente la asignacion')
            else:
                response['codigo']=0
                response['dato']=[]
                response['mensaje']="Ocurrió un error en el procedimiento"
            return HttpResponse(
                json.dumps(response),
                content_type="application/json"
                )
        except Exception as err:
            #transaction.rollback()
            logging.getLogger("error_logger").error('Ocurrió un error al guardar la asignación: {0}'.format(err))
            response['codigo']=1
            response['dato']=[]
            response['mensaje']="Ocurrió un error al guardar la asignación"
            return HttpResponse(
                json.dumps(response),
                content_type="application/json"
                )

def changeStorage(request): 
    request.session['eliminar']="true"
    response=  {}
    response['codigo']=0
    response['dato']=[]
    response['mensaje']="Actualización de temporales realizada correctamente"
    return HttpResponse(
        json.dumps(response),
        content_type="application/json"
    )

def asignacionesTmpConf(asignacionCab_id):
    conn= connection.cursor()
    params=[asignacionCab_id]
    conn.execute('SELECT * FROM [dbo].[listarasignaciones] (%s)',params)
    result = conn.fetchall()
    conn.close()
    return [AsignacionesDet(*row) for row in result]

def limpiarTemporales(puntoServicio,asignacionCab_id): 
    asignacionCab=AsignacionCab.objects.get(puntoServicio_id=puntoServicio)
    conn= connection.cursor()
    params=(asignacionCab.id,0)
    conn.execute('clean_asignaciondet %s,%s',params)
    result = conn.fetchone()[0]
    conn.close()
    response ={}
    if result == 0:
        print("RESULT 0 LISTA LIMPIA DE TEMPORALES")
        #SE OBTIENEN LAS ASIGNACIONES SIN TEMPORALES
        conn= connection.cursor()
        params=[asignacionCab_id]
        conn.execute('SELECT * FROM [dbo].[listarasignaciones] (%s)',params)
        result = conn.fetchall()
        print(result)
        conn.close()
        return [AsignacionesDet(*row) for row in result]
    else:
        response['dato']=[]
        response['codigo']=1
        response['mensaje']="Ocurrió un error al eliminar los temporales"
   
    return HttpResponse(
        json.dumps(response),
        content_type="application/json")  

                
#############################################################################################

@login_required
@permission_required('Operarios.view_asignacioncab', raise_exception=True)
def Asignacion_list(request):
    if request.method == 'POST':
        pk_puntoServSeleccionado = request.POST.get('asig_puntoServ')
        return redirect('Operarios:asignacion_create', id_puntoServicio=pk_puntoServSeleccionado)
    else:
        asignaciones=AsigFiscalPuntoServicio.objects.filter(userFiscal_id=request.user).only("puntoServicio_id")
        puntoServi = PuntoServicio.objects.all()
        contexto = {'PuntosServicio': puntoServi}
        #contexto = {'PuntosServicio': asignaciones}
        return render(request, 'asignacion/asignacion_list.html', context=contexto)

def restarHoras(totalHora,asigHora,totalMin,asigMin):
    totalHorasMinutos = totalHora*60
    totalAsigHorasMinutos = asigHora*60
    cantidadTotalDeMinutos = (totalHorasMinutos+totalMin)-(totalAsigHorasMinutos+asigMin)
    cantidadTotalHoras = cantidadTotalDeMinutos//60
    cantidadTotalDeMinutos = cantidadTotalDeMinutos%60
    return "{}:{}".format(cantidadTotalHoras,int(cantidadTotalDeMinutos))

def getPuntosServicios(request):
    puntoServi = PuntoServicio.objects.all().order_by('NombrePServicio')
    puntos =[]
    i=1
    for p in puntoServi:
        totalHora=""
        horasAsig=""
        horas=""
        minutos=""
        horasRestante=""
        minutosRestante=""
        cantidadMinutos=""
        estado=""
        if RelevamientoCab.objects.filter(Q(puntoServicio_id=p.id)).exists():
            relevamientoCab = RelevamientoCab.objects.get(Q(puntoServicio_id=p.id))
            totalHora = relevamientoCab.cantidadHrTotal
        if AsignacionCab.objects.filter(Q(puntoServicio_id=p.id)).exists():
            asignacionCab = AsignacionCab.objects.get(Q(puntoServicio_id=p.id))
            estado = asignacionCab.reAsignar
            horasAsig = asignacionCab.totalasignado
        if  totalHora and horasAsig:
            horasTotales,minutosTotales = totalHora.split(':')
            horasAsignadas,minutosAsignadas = horasAsig.split(':')
            cantidadMinutos = restarHoras( int(horasTotales),int(horasAsignadas),int(minutosTotales),int(minutosAsignadas))

        puntos.append({
            "id":i,
            "idPunto":p.id,
            "puntservnombre":p.NombrePServicio,
            "horatotal":totalHora,
            "horasasignada":horasAsig,
            "horafaltante":cantidadMinutos,
            "estado":estado
        })
        i=i+1
    
    ordered_puntos = []
    clean_array = puntos.copy()
    for p in puntos:
        if p['estado']:
            ordered_puntos.append(p)
            clean_array.remove(p)
    print()        
    for cleanp in clean_array:
        ordered_puntos.append(cleanp)         
         
    response={}
    response['dato']=ordered_puntos
    return HttpResponse(json.dumps(response),content_type="application/json")

def agregar_detalle(request):
    response = {}
    if request.method == 'POST':
        print(request.POST)
        try:
            id_puntoServicio=request.POST.get('id_puntoServicio')
            
            ''' Obtenemos el punto de servicio'''
            puntoSer = PuntoServicio.objects.get(Q(pk=id_puntoServicio))
        
            ''' Obtenemos la asignacion en caso de que exista una '''
            asignacion = AsignacionCab.objects.filter(Q(puntoServicio_id = puntoSer.id)).first()

            if asignacion == None:
                asignacion = AsignacionCab()

            asignacionDetFormSet = inlineformset_factory(AsignacionCab, AsignacionDet, form=AsignacionDetForm, extra=1, can_delete=True)
            
            """Se le dio click a agregar detalle"""
            form = AsignacionCabForm(request.POST, instance=asignacion)
            AsigDetFormSet = asignacionDetFormSet(request.POST, instance=asignacion)
            
            response['codigo']=0
            response['mensaje']="Se agregó con éxito"
            return HttpResponse(
            json.dumps(response),
            content_type="application/json"
            )
        except Exception as err:
                logging.getLogger("error_logger").error('No se pudo agregar un detalle: {0}'.format(err))
                response['codigo']=1
                response['mensaje']="No se pudo agregar un nuevo detalle"
                return HttpResponse(
                json.dumps(response),
                content_type="application/json"
                )
    else:
        return HttpResponse(
            json.dumps({"nada para ver":"esto no está pasando"}),
            content_type="application/json"
        )

def getDiasLibres(request):
    response = {}
    if request.method == 'GET':
        
        try:
            id_operarios=[]
            diasLibre=[]
            lunEnt=lunSal=marEnt=marSal=mieEnt=mieSal=jueEnt=jueSal=vieEnt=vieSal=sabEnt=sabSal=domEnt=domSal=""
            id_operarios=literal_eval(request.GET.get('operarios'))
            i=0
            for id in id_operarios:
                print(id,DiaLibre.objects.filter(id_operario=id))
                if DiaLibre.objects.filter(id_operario=id).exists():
                    print("existe operario")
                    diasLibre.append(
                    {
                        'operario_id':id,
                        'diasLibres':
                            {
                                'entrada':{
                                        'label':'',
                                        'hora':'',
                                },
                                'salida':{
                                        'label':'',
                                        'hora':'',
                                }
                            }
                    })
                    diaLibres = DiaLibre.objects.filter(id_operario=id).first()
                    if diaLibres.lunEnt:
                        lunEnt=diaLibres.lunEnt.strftime('%H:%M:%S:%f')
                        diasLibre[i]['diasLibres']['entrada']['label']='lunEnt'
                        diasLibre[i]['diasLibres']['entrada']['hora']=lunEnt
                    if diaLibres.lunSal:
                        lunSal=diaLibres.lunSal.strftime('%H:%M:%S:%f')
                        diasLibre[i]['diasLibres']['salida']['label']='lunSal'
                        diasLibre[i]['diasLibres']['salida']['hora']=lunSal
                    if diaLibres.marEnt:
                        marEnt=diaLibres.marEnt.strftime('%H:%M:%S:%f')
                        diasLibre[i]['diasLibres']['entrada']['label']='marEnt'
                        diasLibre[i]['diasLibres']['entrada']['hora']=marEnt
                    if diaLibres.marSal:
                        marSal=diaLibres.marSal.strftime('%H:%M:%S:%f')
                        diasLibre[i]['diasLibres']['salida']['label']='marSal'
                        diasLibre[i]['diasLibres']['salida']['hora']=marSal
                    if diaLibres.mieEnt:
                        mieEnt=diaLibres.mieEnt.strftime('%H:%M:%S:%f')
                        diasLibre[i]['diasLibres']['entrada']['label']='mieEnt'
                        diasLibre[i]['diasLibres']['entrada']['hora']=mieEnt
                    if diaLibres.mieSal:
                        mieSal=diaLibres.mieSal.strftime('%H:%M:%S:%f')
                        diasLibre[i]['diasLibres']['salida']['label']='mieSal'
                        diasLibre[i]['diasLibres']['salida']['hora']=mieSal
                    if diaLibres.jueEnt:
                        jueEnt=diaLibres.jueEnt.strftime('%H:%M:%S:%f')
                        diasLibre[i]['diasLibres']['entrada']['label']='jueEnt'
                        diasLibre[i]['diasLibres']['entrada']['hora']=jueEnt
                    if diaLibres.jueSal:
                        jueSal=diaLibres.jueSal.strftime('%H:%M:%S:%f')
                        diasLibre[i]['diasLibres']['salida']['label']='jueSal'
                        diasLibre[i]['diasLibres']['salida']['hora']=jueSal
                    if diaLibres.vieEnt:
                        vieEnt=diaLibres.vieEnt.strftime('%H:%M:%S:%f')
                        diasLibre[i]['diasLibres']['entrada']['label']='vieEnt'
                        diasLibre[i]['diasLibres']['entrada']['hora']=vieEnt
                    if diaLibres.vieSal:
                        vieSal=diaLibres.vieSal.strftime('%H:%M:%S:%f')
                        diasLibre[i]['diasLibres']['salida']['label']='vieSal'
                        diasLibre[i]['diasLibres']['salida']['hora']=vieSal
                    if diaLibres.sabEnt:
                        sabEnt=diaLibres.sabEnt.strftime('%H:%M:%S:%f')
                        diasLibre[i]['diasLibres']['entrada']['label']='sabEnt'
                        diasLibre[i]['diasLibres']['entrada']['hora']=sabEnt
                    if diaLibres.sabSal:
                        sabSal=diaLibres.sabSal.strftime('%H:%M:%S:%f')
                        diasLibre[i]['diasLibres']['salida']['label']='sabSal'
                        diasLibre[i]['diasLibres']['salida']['hora']=sabSal
                    if diaLibres.domEnt:
                        domEnt=diaLibres.domEnt.strftime('%H:%M:%S:%f')
                        diasLibre[i]['diasLibres']['entrada']['label']='domEnt'
                        diasLibre[i]['diasLibres']['entrada']['hora']=domEnt
                    if diaLibres.domSal:
                        domSal=diaLibres.domSal.strftime('%H:%M:%S:%f')
                        diasLibre[i]['diasLibres']['salida']['label']='domSal'
                        diasLibre[i]['diasLibres']['salida']['hora']=domSal
                    i=i+1
            response['dato']=diasLibre
            response['codigo']=0
            response['mensaje']="Se listaron con éxito"
            return HttpResponse(json.dumps(response),content_type="application/json")
        except Exception as err:
                logging.getLogger("error_logger").error('Ocurrió un error al listar los dias libres: {0}'.format(err))
                response['codigo']=1
                response['dato']=[]
                response['mensaje']="Ocurrió un error al listar los dias libres"
                messages.warning(request, 'Ocurrió un error al listar los dias libres')
                return HttpResponse(
                json.dumps(response),
                content_type="application/json"
                )
    else:
        return HttpResponse(
            json.dumps({"nada para ver":"esto no está pasando"}),
            content_type="application/json"
        )
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
def guardarAsignacion(request):
    if request.method=="POST":
        print("REQUEST.POST ",request.POST)
        try:
            response={}
            id_puntoServicio=request.POST.get('puntoServicio')
                    
            ''' Obtenemos el punto de servicio'''
            puntoSer = PuntoServicio.objects.get(Q(pk=id_puntoServicio))
                
            ''' Obtenemos la asignacion en caso de que exista una '''
            asignacion = AsignacionCab.objects.filter(Q(puntoServicio_id = puntoSer.id)).first()

            if asignacion == None:
                asignacion = AsignacionCab()

            if request.POST.get('error') is not None and request.POST.get('error')=='true':
                response['codigo']=1
                response['dato']=[]
                response['mensaje']="No se pudo guardar la asignación, favor verifique las horas asignadas..."
                return HttpResponse(
                    json.dumps(response),
                    content_type="application/json"
                    )
            else:
                conn= connection.cursor()
                params=(
                    str({
                        'id': str(asignacion.id),
                        'puntoServicio_id':str(puntoSer.id),
                        'totalasignado':str(0 if request.POST.get('totalasignado')is None else request.POST.get('totalasignado')),
                        'usuario_id':"None" if request.user is None else str(request.user.id)
                        }).replace('\'','\"'),
                        asignacion.id,
                    0)
                print(params)
                conn.execute('asignacion_manager %s,%s,%s ',params)
                result = conn.fetchone()[0]
                conn.close()
                if result==0:
                    messages.success(request, 'Se guardó correctamente la asignacion')
                else:
                    response['dato']=[]
                    response['codigo']=1
                    response['mensaje']="No se pudo guardar los cambios"
                    return HttpResponse(
                    json.dumps(response),
                    content_type="application/json")  
            response['dato']=[]
            response['codigo']=0
            response['mensaje']="Asignacion guardada con éxito"
            return HttpResponse(
            json.dumps(response),
            content_type="application/json")
        except Exception as err:
            logging.getLogger("error_logger").error('Ocurrió un error al listar los dias libres: {0}'.format(err))
            response['codigo']=1
            response['dato']=[]
            response['mensaje']="Ocurrió un error al listar los dias libres"
            messages.warning(request, 'Ocurrió un error al listar los dias libres')
            return HttpResponse(
            json.dumps(response),
            content_type="application/json"
            )
           
@login_required
@permission_required('Operarios.add_asignacioncab', raise_exception=True)
def Asignacion_create(request, id_puntoServicio=None):
    sem_diurno = '00:00'
    sem_nocturno = '00:00'
    dom_diurno = '00:00'
    dom_nocturno = '00:00'
    operarios = []
    paginator=''
    operariosList=[]
    diaInicioSelected = []
    diaFinSelected = []
    horaInicioSelected=[]
    horaFinSelected=[]
    diasEntrada = [{"id":"lunEnt","dia":"Lunes"},{"id":"marEnt","dia":"Martes"},{"id":"mieEnt", "dia":"Miercoles"},{"id":"jueEnt", "dia":"Jueves"},{"id":"vieEnt", "dia":"Viernes"},{"id":"sabEnt", "dia":"Sabado"}, {"id":"domEnt", "dia":"Domingo"}]
    diasSalida = [{"id":"lunSal","dia":"Lunes"},{"id":"marSal","dia":"Martes"},{"id":"mieSal", "dia":"Miercoles"},{"id":"jueSal", "dia":"Jueves"},{"id":"vieSal", "dia":"Viernes"},{"id":"sabSal", "dia":"Sabado"}, {"id":"domSal", "dia":"Domingo"}]
    allOperarios = Operario.objects.all()
    perfiles = Especializacion.objects.all()
    openModal=False
    idModal = None
    
    
    logging.getLogger("error_logger").error('Se ingreso en el metodo asignacion_create')
    ''' Obtenemos el punto de servicio, en caso de error se muesta un error 404 '''
    try:
        puntoSer = PuntoServicio.objects.get(Q(pk=id_puntoServicio))
    except PuntoServicio.DoesNotExist as err:
        logging.getLogger("error_logger").error('Punto de Servicio no existe: {0}'.format(err))
        raise Http404("Punto de Servicio no existe")
    """try:
        asigCab = AsignacionCab.objects.get(puntoServicio_id=id_puntoServicio)
        asigDet = AsignacionDet.objects.filter(asignacionCab_id=asigCab.id)
    except AsignacionCab.DoesNotExist as err:
        logging.getLogger("error_logger").error('Asignacion cabecera no existe: {0}'.format(err))
        raise Http404("Asignacion cabecera no existe")
    """

    ''' Obtenemos el relevamiento para mostrar en la pantalla '''
    relevamiento = RelevamientoCab.objects.filter(Q(puntoServicio_id = puntoSer.id)).first()
    if relevamiento == None:
        logging.getLogger("error_logger").error('El punto de servicio no tiene servicio aprobado')
        raise Http404("El punto de servicio no tiene Servicio aprobado")

    if relevamiento.relevamientocupohoras_set.exists():
        logging.getLogger("error_logger").error('Estamos revisando si existe detalle de cupo de horas')
        for cupo in relevamiento.relevamientocupohoras_set.iterator():
            """SI ES LA ULTIMA VERSION DE RELEVAMIENTO CUPOS HORAS"""
            if cupo.tipoHora.tipoHorario == 'Diurno' and cupo.frecuencia == 'SEM':
                sem_diurno = cupo.cantCHoras
            elif cupo.tipoHora.tipoHorario == 'Nocturno' and cupo.frecuencia == 'SEM':
                sem_nocturno = cupo.cantCHoras
            elif cupo.tipoHora.tipoHorario == 'Diurno' and cupo.frecuencia == 'DOM':
                dom_diurno = cupo.cantCHoras
            elif cupo.tipoHora.tipoHorario == 'Diurno' and cupo.frecuencia == 'DOM':
                dom_nocturno = cupo.cantCHoras

        

    ''' Obtenemos la asignacion en caso de que exista una '''
    asignacion = AsignacionCab.objects.filter(Q(puntoServicio_id = puntoSer.id)).first()
    if asignacion == None:
        asignacion = AsignacionCab(puntoServicio=puntoSer,usuario=request.user)
        asignacion.save()
    
    if request.session['eliminar'] == "true":
        print("Se muestra lista limpia")
        asignaciones = limpiarTemporales(id_puntoServicio,asignacion.id)
    else:
        print("SE MUESTRA lista con temporales")
        asignaciones = asignacionesTmpConf(asignacion.id)
    
    asignaciones_aux =asignaciones.copy()
    for asig in asignaciones_aux:
        if asig.eliminado:
            asignaciones.remove(asig)
        else:
            if asig.perfil:
                perfil = Especializacion.objects.get(id = asig.perfil)
                asig.perfil_nombre = perfil.especializacion
            if asig.operario_id:
                operario = Operario.objects.get(id = asig.operario_id)
                asig.operario_nombre = operario.nombre + " " + operario.apellido
            asig.puntoServicio_id = id_puntoServicio
            if asig.lunEnt == datetime.time(0,0) and asig.lunSal == datetime.time(0,0):
                asig.lunEnt = asig.lunSal = None
            if asig.marEnt == datetime.time(0,0) and asig.marSal == datetime.time(0,0):
                asig.marEnt = asig.marSal = None
            if asig.mieEnt == datetime.time(0,0) and asig.mieSal == datetime.time(0,0):
                asig.mieEnt = asig.mieSal = None
            if asig.jueEnt == datetime.time(0,0) and asig.jueSal == datetime.time(0,0):
                asig.jueEnt = asig.jueSal = None
            if asig.jueEnt == datetime.time(0,0) and asig.jueSal == datetime.time(0,0):
                asig.jueEnt = asig.jueSal = None
            if asig.vieEnt == datetime.time(0,0) and asig.vieSal == datetime.time(0,0):
                asig.vieEnt = asig.vieSal = None
            if asig.sabEnt == datetime.time(0,0) and asig.sabSal == datetime.time(0,0):
                asig.sabEnt = asig.sabSal = None
            if asig.domEnt == datetime.time(0,0) and asig.domSal == datetime.time(0,0):
                asig.domEnt = asig.domSal = None

    asignacionDetFormSet = inlineformset_factory(AsignacionCab, AsignacionDet, form=AsignacionDetForm, extra=1, can_delete=True)

    if request.method == 'POST':
        print(request.POST)
        if  request.POST.get('action') == 'add_det': 
            """Se le dio click a agregar detalle"""
            form = AsignacionCabForm(request.POST, instance=asignacion)
            AsigDetFormSet = asignacionDetFormSet(request.POST, instance=asignacion)
            """se prepara para agregar otro"""
        elif  'filter_operario' in request.POST.get('action'):
                
            """Se le dio click a buscar operario"""
            form = AsignacionCabForm(request.POST,instance=asignacion)
            AsigDetFormSet = asignacionDetFormSet(request.POST, instance=asignacion)

            i=0
            formOperarioID = int(request.POST.get('action')[request.POST.get('action').rfind('-')+1:None],10)
            
            for form in AsigDetFormSet:
                totalHoras=idPunto="" 
                lunEnt=lunSal=marEnt=marSal=mieEnt=mieSal=jueEnt=jueSal=vieEnt=vieSal=sabEnt=sabSal=domEnt=domSal=""
                fechaIni = ""
                diaInicio=diaFin=""
                horaInicio=horaFin=""
                supervisor=False
                perfil=""
                fechaFin=""
                request.session['diaInicio-' + str(i)]=request.POST.get('diaInicio-' + str(i))
                diaInicioSelected.append(request.session['diaInicio-' + str(i)])

                request.session['diaFin-' + str(i)]=request.POST.get('diaFin-' + str(i))
                diaFinSelected.append(request.session['diaFin-' + str(i)])

                request.session['horaInicio-' + str(i)]=request.POST.get('horaInicio-' + str(i))
                horaInicioSelected.append(request.session['horaInicio-' + str(i)])

                request.session['horaFin-' + str(i)]=request.POST.get('horaFin-' + str(i))
                horaFinSelected.append(request.session['horaFin-' + str(i)])
                
                if i == formOperarioID:
                    
                    if request.POST.get('asignaciondet_set-' + str(i) + '-totalHoras') != 'None':
                        totalHoras = request.POST.get('asignaciondet_set-' + str(i) +'-totalHoras')
                    if  id_puntoServicio:
                        idPunto = id_puntoServicio
                    if request.POST.get('asignaciondet_set-' + str(i) + '-fechaInicio'):
                        fechaIni = request.POST.get('asignaciondet_set-' + str(i) + '-fechaInicio')
                        date_time_obj = datetime.datetime.strptime(fechaIni,'%d/%m/%Y')
                        fechaIni=date_time_obj.strftime('%Y-%m-%d')
                    if request.POST.get('asignaciondet_set-' + str(i) + '-fechaFin'):
                        fechaFin = request.POST.get('asignaciondet_set-' + str(i) + '-fechaFin')
                        date_time_obj = datetime.datetime.strptime(fechaFin,'%d/%m/%Y')
                        fechaFin=date_time_obj.strftime('%Y-%m-%d')
                    if request.POST.get('asignaciondet_set-' + str(i) + '-lunEnt'):
                        lunEnt = request.POST.get('asignaciondet_set-' + str(i) + '-lunEnt')
                    if request.POST.get('asignaciondet_set-' + str(i) + '-lunSal'):
                        lunSal = request.POST.get('asignaciondet_set-' + str(i) + '-lunSal')
                    if request.POST.get('asignaciondet_set-' + str(i) + '-marEnt'):
                        marEnt = request.POST.get('asignaciondet_set-' + str(i) + '-marEnt')
                    if request.POST.get('asignaciondet_set-' + str(i) + '-marSal'):
                        marSal = request.POST.get('asignaciondet_set-' + str(i) + '-marSal')
                    if request.POST.get('asignaciondet_set-' + str(i) + '-mieEnt'):
                        mieEnt = request.POST.get('asignaciondet_set-' + str(i) + '-mieEnt')
                    if request.POST.get('asignaciondet_set-' + str(i) + '-mieSal'):
                        mieSal = request.POST.get('asignaciondet_set-' + str(i) + '-mieSal')
                    if request.POST.get('asignaciondet_set-' + str(i) + '-jueEnt'):
                        jueEnt = request.POST.get('asignaciondet_set-' + str(i) + '-jueEnt')
                    if request.POST.get('asignaciondet_set-' + str(i) + '-jueSal'):
                        jueSal = request.POST.get('asignaciondet_set-' + str(i) + '-jueSal')
                    if request.POST.get('asignaciondet_set-' + str(i) + '-vieEnt'):
                        vieEnt = request.POST.get('asignaciondet_set-' + str(i) + '-vieEnt')
                    if request.POST.get('asignaciondet_set-' + str(i) + '-vieSal'):
                        vieSal = request.POST.get('asignaciondet_set-' + str(i) + '-vieSal')
                    if request.POST.get('asignaciondet_set-' + str(i) + '-sabEnt'):
                        sabEnt = request.POST.get('asignaciondet_set-' + str(i) + '-sabEnt')
                    if request.POST.get('asignaciondet_set-' + str(i) + '-sabSal'):
                        sabSal = request.POST.get('asignaciondet_set-' + str(i) + '-sabSal')
                    if request.POST.get('asignaciondet_set-' + str(i) + '-domEnt'):
                        domEnt = request.POST.get('asignaciondet_set-' + str(i) + '-domEnt')
                    if request.POST.get('asignaciondet_set-' + str(i) + '-domSal'):
                        domSal = request.POST.get('asignaciondet_set-' + str(i) + '-domSal')
                    if request.POST.get('asignaciondet_set-' + str(i) + '-totalHoras'):
                        totalHoras = request.POST.get('asignaciondet_set-' + str(i) + '-totalHoras')
                    if request.POST.get('asignaciondet_set-' + str(i) + '-perfil'):
                        perfil = request.POST.get('asignaciondet_set-' + str(i) + '-perfil')
                    if request.POST.get('asignaciondet_set-' + str(i) + '-supervisor')=="on":
                        supervisor = True
                    if request.POST.get('diaInicio-' + str(i) ):
                        diaInicio = request.POST.get('diaInicio-' + str(i))
                    if request.POST.get('horaInicio-' + str(i)):
                        horaInicio = request.POST.get('horaInicio-' + str(i))
                        

                    if request.POST.get('diaFin-' + str(i) ):
                        diaFin = request.POST.get('diaFin-' + str(i) )

                    if request.POST.get('horaFin-' + str(i)):
                        horaFin = request.POST.get('horaFin-' + str(i))

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
                    
                    if len(operarios)>0:
                        
                        """ 
                            verificar que este contenido el operario en la lista, para evitar solapamiento, datos detalle anterior y actual
                        """
                        """
                            obtenemos los datos del operario asignados anteriormente
                        """
                        if i>0:
                            index=1
                           
                            while (index <= i):      
                                lunEntAnt=None
                                lunSalAnt=None
                                marEntAnt=None
                                marSalAnt=None
                                mieSalAnt=None
                                mieEntAnt=None
                                jueEntAnt=None
                                jueSalAnt=None
                                vieSalAnt=None
                                vieEntAnt=None
                                sabEntAnt=None
                                sabSalAnt=None
                                domEntAnt=None
                                domSalAnt=None
                                fechaFinAnt=None
                                if request.POST.get("id_asignaciondet_set-" + str(index-1) + "-DELETE")==None:
                                    
                                    if request.POST.get('asignaciondet_set-' + str(index-1) + '-fechaInicio'):
                                        fechaIniAnt = request.POST.get('asignaciondet_set-' + str(index-1) + '-fechaInicio')
                                    if request.POST.get('asignaciondet_set-' + str(index-1) + '-fechaFin'):
                                        fechaFinAnt = request.POST.get('asignaciondet_set-' + str(index-1) + '-fechaFin')
                                    if request.POST.get('asignaciondet_set-' + str(index-1) + '-lunEnt'):
                                        lunEntAnt = request.POST.get('asignaciondet_set-' + str(index-1) + '-lunEnt')
                                        
                                    if request.POST.get('asignaciondet_set-' + str(index-1) + '-lunSal'):
                                        lunSalAnt = request.POST.get('asignaciondet_set-' + str(index-1) + '-lunSal')
                                    if request.POST.get('asignaciondet_set-' + str(index-1) + '-marEnt'):
                                        marEntAnt = request.POST.get('asignaciondet_set-' + str(index-1) + '-marEnt')
                                    if request.POST.get('asignaciondet_set-' + str(index-1) + '-marSal'):
                                        marSalAnt = request.POST.get('asignaciondet_set-' + str(index-1) + '-marSal')
                                    if request.POST.get('asignaciondet_set-' + str(index-1) + '-mieEnt'):
                                        mieEntAnt = request.POST.get('asignaciondet_set-' + str(index-1) + '-mieEnt')
                                    if request.POST.get('asignaciondet_set-' + str(index-1) + '-mieSal'):
                                        mieSalAnt = request.POST.get('asignaciondet_set-' + str(index-1) + '-mieSal')
                                    if request.POST.get('asignaciondet_set-' + str(index-1) + '-jueEnt'):
                                        jueEntAnt = request.POST.get('asignaciondet_set-' + str(index-1) + '-jueEnt')
                                    if request.POST.get('asignaciondet_set-' + str(index-1) + '-jueSal'):
                                        jueSalAnt = request.POST.get('asignaciondet_set-' + str(index-1) + '-jueSal')
                                    if request.POST.get('asignaciondet_set-' + str(index-1) + '-vieEnt'):
                                        vieEntAnt = request.POST.get('asignaciondet_set-' + str(index-1) + '-vieEnt')
                                    if request.POST.get('asignaciondet_set-' + str(index-1) + '-vieSal'):
                                        vieSalAnt = request.POST.get('asignaciondet_set-' + str(index-1) + '-vieSal')
                                    if request.POST.get('asignaciondet_set-' + str(index-1) + '-sabEnt'):
                                        sabEntAnt = request.POST.get('asignaciondet_set-' + str(index-1) + '-sabEnt')
                                    if request.POST.get('asignaciondet_set-' + str(index-1) + '-sabSal'):
                                        sabSalAnt = request.POST.get('asignaciondet_set-' + str(index-1) + '-sabSal')
                                    if request.POST.get('asignaciondet_set-' + str(index-1) + '-domEnt'):
                                        domEntAnt = request.POST.get('asignaciondet_set-' + str(index-1) + '-domEnt')
                                    if request.POST.get('asignaciondet_set-' + str(index-1) + '-domSal'):
                                        domSalAnt = request.POST.get('asignaciondet_set-' + str(index-1) + '-domSal')
                                    
                                    """ 
                                        se comienzan las comparaciones
                                    """
                                    """
                                    si se cumple algunas de estas condiciones entonces se pregunta por la fecha de inicio
                                    """
                                    if lunEnt and lunEntAnt and lunSalAnt and ((lunEnt>= lunEntAnt and lunEnt <=lunSalAnt) or (lunSal>= lunEntAnt and (lunSal <=lunSalAnt or lunSal>=lunSalAnt))):
                                        # anterior = dt.strptime(fechaFinAnt, "%D-%M-%Y")
                                        # actual = dt.strptime(fechaIni, "%D-%M/%Y")
                                        """
                                        Si la fecha de inicio actual del operario es menor a la de la fecha de finalizacion de la 
                                        asignacion anterior 
                                        """
                                        print ("Hola lunes")
                                        print (fechaFinAnt)
                                        if fechaFinAnt==None or fechaIni <= fechaFinAnt:
                                            """
                                            Ahora obtenemos el operario para borrar de la lista
                                            """
                                            print ("Comparacion de fechas")
                                            
                                            id_operario=request.POST.get('asignaciondet_set-' + str(index-1) +'-operario')
                                            
                                            if id_operario!='':
                                                for op in operarios:
                                                    
                                                    if int(op.id_operario) == int(id_operario):
                                                        print ("Encuentra")
                                                        operarios.remove(op)
                                                        break
                                    elif marEnt and marEntAnt and marSalAnt and ((marEnt >= marEntAnt and marEnt <= marEntAnt) or ((marSal>= marEntAnt and marSal <=marSalAnt) or (marSal>=marSalAnt))):
                                            
                                            if fechaFinAnt==None or fechaIni <= fechaFinAnt:
                                                """
                                                Ahora obtenemos el operario para borrar de la lista
                                                """
                                                
                                                id_operario=request.POST.get('asignaciondet_set-' + str(index-1) +'-operario')
                                                
                                                if id_operario!='':
                                                    for op in operarios:
                                                        print (op.id_operario)
                                                        if int(op.id_operario) == int(id_operario):
                                                            
                                                            operarios.remove(op)
                                                            break
                                    elif mieEnt and mieEntAnt and mieSalAnt and ((mieEnt >= mieEntAnt and mieEnt <= mieEntAnt) or ((mieSal>= mieEntAnt and mieSal <=mieSalAnt) or (mieSal>=mieSalAnt))):
                                            if fechaFinAnt==None or fechaIni <= fechaFinAnt:
                                                """
                                                Ahora obtenemos el operario para borrar de la lista
                                                """
                                                
                                                id_operario=request.POST.get('asignaciondet_set-' + str(index-1) +'-operario')
                                                
                                                if id_operario!='':
                                                    for op in operarios:
                                                        print (op.id_operario)
                                                        if int(op.id_operario) == int(id_operario):
                                                            
                                                            operarios.remove(op)
                                                            break
                                    elif jueEnt and jueEntAnt and jueSalAnt and ((jueEnt >= jueEntAnt and jueEnt <=jueEntAnt) or ((jueSal>= jueEntAnt and jueSal <=jueSalAnt) or (jueSal>=jueSalAnt))):
                                            if fechaFinAnt==None or fechaIni <= fechaFinAnt:
                                                """
                                                Ahora obtenemos el operario para borrar de la lista
                                                """
                                               
                                                id_operario=request.POST.get('asignaciondet_set-' + str(index-1) +'-operario')
                                                
                                                if id_operario!='':
                                                    for op in operarios:
                                                        
                                                        if int(op.id_operario) == int(id_operario):
                                                            
                                                            operarios.remove(op)
                                                            break
                                    elif vieEnt and vieEntAnt and vieSalAnt and ((vieEnt >= vieEntAnt and vieEnt <= vieEntAnt) or ((vieSal>= vieEntAnt and vieSal <=vieSalAnt ) or (vieSal>=vieSalAnt))):
                                            if fechaFinAnt==None or fechaIni <= fechaFinAnt:
                                                """
                                                Ahora obtenemos el operario para borrar de la lista
                                                """
                                                
                                                id_operario=request.POST.get('asignaciondet_set-' + str(index-1) +'-operario')
                                                
                                                if id_operario!='':
                                                    for op in operarios:
                                                        
                                                        if int(op.id_operario) == int(id_operario):
                                                           
                                                            operarios.remove(op)
                                                            break
                                    elif sabEnt and sabEntAnt and sabSalAnt and ((sabEnt >= sabEntAnt and sabEnt <= sabEntAnt) or ((sabSal>= sabEntAnt and sabSal <=sabSalAnt) or (sabSal>=sabEntAnt))):
                                            if fechaFinAnt==None or fechaIni <= fechaFinAnt:
                                                """
                                                Ahora obtenemos el operario para borrar de la lista
                                                """
                                                print ("Holaaaa")
                                                id_operario=request.POST.get('asignaciondet_set-' + str(index-1) +'-operario')
                                                if id_operario!='':
                                                    for op in operarios:
                                                        
                                                        if int(op.id_operario) == int(id_operario):
                                                            
                                                            operarios.remove(op)
                                                            break
                                    elif domEnt and domEntAnt and domSalAnt and ((domEnt >= domEntAnt and domEnt <= domEntAnt) or ((domSal>= domEntAnt and domSal <=domSalAnt) or (sabSal>=sabEntAnt))):
                                            if fechaFinAnt==None or fechaIni <= fechaFinAnt:
                                                """
                                                Ahora obtenemos el operario para borrar de la lista
                                                """
                                                print ("Holaaaa")
                                                id_operario=request.POST.get('asignaciondet_set-' + str(index-1) +'-operario')
                                                if id_operario!='':
                                                    for op in operarios:
                                                        print (op.id_operario)
                                                        if int(op.id_operario) == int(id_operario):
                                                            
                                                            operarios.remove(op)
                                                            break
                                
                                index+=1
                            if len(operarios)>0:
                                openModal=True
                                idModal = formOperarioID
                               
                            else:
                                messages.info(request, 'No se encontraron operarios con esos parametros') 
                        else:
                            openModal=True
                            idModal = formOperarioID
                    else:
                        messages.info(request, 'No se encontraron operarios con esos parametros')
                i=i+1
        elif request.POST.get('action') == 'btn_eliminar': 
            """Se le dio click a buscar operario"""
            form = AsignacionCabForm(request.POST,instance=asignacion)
            AsigDetFormSet = asignacionDetFormSet(request.POST, instance=asignacion)    
        else: 
            """Se le dio click al boton guardar"""
            form = AsignacionCabForm(request.POST, instance=asignacion)
            AsigDetFormSet = asignacionDetFormSet(request.POST,instance=asignacion)
               
            print ("form error",form.errors)
            print ("asign error",AsigDetFormSet.errors)
            if form.is_valid() and AsigDetFormSet.is_valid():
                """Se guarda completo"""
                #form.save()
                #AsigDetFormSet.save()
                emptyvar={}
                asg_det="[ "
                print("ENTRE A VALID")
                for item in  AsigDetFormSet.cleaned_data:
                    if item != emptyvar:
                        asg_det+=str({
                                'id':str(str(item.get('id').id) if item.get('id') is not None else 'None'),
                                'DELETE':str(item.get('DELETE')),
                                'asignacionCab_id': str(asignacion.id),
                                'operario':str(item.get('operario')),
                                'operario_id':str(str(item.get('operario').id) if item.get('operario') is not None else 'None'),
                                'fechaInicio':str(item.get('fechaInicio')),
                                'fechaFin':str(item.get('fechaFin')),
                                'lunEnt':str(item.get('lunEnt')),
                                'lunSal':str(item.get('lunSal')),
                                'marEnt':str(item.get('marEnt')),
                                'marSal':str(item.get('marSal')),
                                'mieEnt':str(item.get('mieEnt')),
                                'mieSal':str(item.get('mieSal')),
                                'jueEnt':str(item.get('jueEnt')),
                                'jueSal':str(item.get('jueSal')),
                                'vieEnt':str(item.get('vieEnt')),
                                'vieSal':str(item.get('vieSal')),
                                'sabEnt':str(item.get('sabEnt')),
                                'sabSal':str(item.get('sabSal')),
                                'domEnt':str(item.get('domEnt')),
                                'domSal':str(item.get('domSal')),
                                'perfil':str(item.get('perfil')),
                                'supervisor':str(item.get('supervisor')),
                                'totalHoras':str(item.get('totalHoras'))
                                })
                        asg_det+=","
                asg_det=asg_det[:-1]
                asg_det+="]"
                conn= connection.cursor()
                params=(
                    str({'id': str(asignacion.id),'puntoServicio_id':str(puntoSer.id),
                        'totalasignado':str(form.cleaned_data.get('totalasignado')),
                        'comentario':form.cleaned_data.get('comentario')}).replace('\'','\"'),
                    asg_det.replace('\'','\"'),
                    0)
                print(params)
                conn.execute('asignacion_manager %s,%s,%s ',params)
                result = conn.fetchone()[0]
                conn.close()
                print(result)
                if result==0:
                    messages.success(request, 'Se guardo correctamente la asignación')
                else:
                    messages.warning(request, 'No se pudo guardar los cambios')    
                return redirect('Operarios:asignacion_list')
            else:
                print("ENTRE A INVAAALID")
                print(form.errors)
                print(AsigDetFormSet.errors)
                messages.warning(request, 'No se pudo guardar los cambios')

    else:
        """
        Seteamos el punto de servicio
        """
        asignacion.puntoServicio = puntoSer
        form = AsignacionCabForm(instance=asignacion)
        AsigDetFormSet = asignacionDetFormSet(instance=asignacion)


    #operarios_json = json.dumps(operarios)
    contexto = {
            'title': 'Detalle de Asignaciones',
            'asignaciones':asignaciones,
            'pservicio': puntoSer,
            'form': form,
            'operarios':operarios,
            'asigDetFormSet': AsigDetFormSet,
            'relevamiento' : relevamiento,
            'paginator':paginator,
            'sem_diurno' : sem_diurno,
            'sem_nocturno' : sem_nocturno,
            'dom_diurno' : dom_diurno,
            'diasEntrada':diasEntrada,
            'diasSalida':diasSalida,
            'perfiles':perfiles,
            'diaInicioSelected':diaInicioSelected,
            'diaFinSelected':diaFinSelected,
            'horaInicioSelected':horaInicioSelected,
            'horaFinSelected':horaFinSelected,
            'dom_nocturno' : dom_nocturno,
            'operarios':operarios,
            'allOperarios':allOperarios,
            'openModal':openModal,
            'idModal':idModal
        }

    return render(request, 'asignacion/asignacion_crear.html', context=contexto)


def getOperarios(request):
    totalHoras=idPunto="" 
    lunEnt=lunSal=marEnt=marSal=mieEnt=mieSal=jueEnt=jueSal=vieEnt=vieSal=sabEnt=sabSal=domEnt=domSal=""
    fechaIni = ""
    diaInicio=diaFin=""
    horaInicio=horaFin=""
    supervisor=False
    perfil=""
    fechaFin=""
    operarios = []
    print(request.GET)
    if request.GET.get('idPunto')  is not None and request.GET.get('idPunto')!='':
        idPunto=request.GET.get('idPunto')
    if request.GET.get('totalHorasProc')  is not None and request.GET.get('totalHorasProc')!='':
        totalHoras=request.GET.get('totalHorasProc') 
    if request.GET.get('lunEnt')  is not None and request.GET.get('lunEnt')!='':
        lunEnt=request.GET.get('lunEnt') 
    if request.GET.get('lunSal')  is not None and request.GET.get('lunSal')!='':
        lunSal=request.GET.get('lunSal') 
    if request.GET.get('marEnt')  is not None and request.GET.get('marEnt')!='':
        marEnt=request.GET.get('marEnt')
    if request.GET.get('marSal')  is not None and request.GET.get('marSal')!='':
        marSal=request.GET.get('marSal')
    if request.GET.get('mieEnt')  is not None and request.GET.get('mieEnt')!='':
        mieEnt=request.GET.get('mieEnt')
    if request.GET.get('mieSal')  is not None and request.GET.get('mieSal')!='':
        mieSal=request.GET.get('mieSal')
    if request.GET.get('jueEnt')  is not None and request.GET.get('jueEnt')!='':
        jueEnt=request.GET.get('jueEnt')
    if request.GET.get('jueSal')  is not None and request.GET.get('jueSal')!='':
        jueSal=request.GET.get('jueSal')
    if request.GET.get('vieEnt')  is not None and request.GET.get('vieEnt')!='':
        vieEnt=request.GET.get('vieEnt')
    if request.GET.get('vieSal')  is not None and request.GET.get('vieSal')!='':
        vieSal=request.GET.get('vieSal')
    if request.GET.get('sabEnt')  is not None and request.GET.get('sabEnt')!='':
        sabEnt=request.GET.get('sabEnt')
    if request.GET.get('sabSal')  is not None and request.GET.get('sabSal')!='':
        sabSal=request.GET.get('sabSal')
    if request.GET.get('domEnt')  is not None and request.GET.get('domEnt')!='':
        domEnt=request.GET.get('domEnt')
    if request.GET.get('domSal')  is not None and request.GET.get('domSal')!='':
        domSal=request.GET.get('domSal')
    if request.GET.get('supervisor')  is not None and request.GET.get('supervisor')!='' and request.GET.get('supervisor')=="true":
        supervisor=True
    elif request.GET.get('supervisor')=="false":
        supervisor=False
    if request.GET.get('diaFin')  is not None and request.GET.get('diaFin')!='':
        diaFin=request.GET.get('diaFin')
    if request.GET.get('diaInicio')  is not None and request.GET.get('diaInicio')!='':
        diaInicio=request.GET.get('diaInicio')
    if request.GET.get('horaFin')  is not None and request.GET.get('horaFin')!='':
        horaFin=request.GET.get('horaFin')
    if request.GET.get('horaInicio')  is not None and request.GET.get('horaInicio')!='':
        horaInicio=request.GET.get('horaInicio')
    if request.GET.get('perfilproc')  is not None and request.GET.get('perfilproc')!='':
        perfil=request.GET.get('perfilproc')
    if request.GET.get('fechaFin')  is not None and request.GET.get('fechaFin')!='':
        fechaFin=request.GET.get('fechaFin')
        date_time_obj = datetime.datetime.strptime(fechaFin,'%d/%m/%Y')
        fechaFin=date_time_obj.strftime('%Y-%m-%d')
    if request.GET.get('fechaIni')  is not None and request.GET.get('fechaIni')!='':
        fechaIni=request.GET.get('fechaIni')
        date_time_obj = datetime.datetime.strptime(fechaIni,'%d/%m/%Y')
        fechaIni=date_time_obj.strftime('%Y-%m-%d')
    print("SUPERVISOR ",supervisor)
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
        
    #Se filtra el resultado

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

    return HttpResponse(serializers.serialize("json",operarios ), content_type = 'application/json', status = 200);


def do_paginate(data_list, page_number):
    ret_data_list=data_list
    result_per_page=5
    paginator=Paginator(data_list, result_per_page)
    try:
        ret_data_list=paginator.page(page_number)
    except EmptyPage:
        ret_data_list=paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        ret_data_list=paginator.page(1)
    return [ret_data_list, paginator]

def buscar_operarios(puntoServicio, totalHoras, lunEntReq, lunSalReq, marEntReq, marSalReq, mierEntReq, mierSalReq, juevEntReq, juevSalReq, vieEntReq, vieSlReq, sabEntReq, sabSalReq, domEntReq, domSalReq,perfil,supervisor, fechaInicioOp,fechaFinOp,horaInicio,horaFin,diaInicio,diaFin):
        conn= connection.cursor()
        sql = """\
            DECLARE @out nvarchar(max);
            EXEC [dbo].[operarios_disponibles_v2] @puntoServicio=?, @totalHoras=?, @lunEntReq=?, @lunSalReq=?, @marEntReq=?, @marSalReq=?, @mierEntReq=?, @mierSalReq=?, @juevEntReq=?, @juevSalReq=?, @vieEntReq=?, @vieSlReq=?, @sabEntReq=?, @sabSalReq=?, @domEntReq=?, @domSalReq=?, @fechaInicioOperario=?, @fechaFinOperario=?,@perfil=?, @param_out = @out OUTPUT;
            SELECT @out AS the_output;
        """
        """conn.callproc('operarios_disponibles_v3', [puntoServicio, totalHoras, lunEntReq, lunSalReq, marEntReq, marSalReq, mierEntReq, mierSalReq, juevEntReq, juevSalReq, vieEntReq, vieSlReq, sabEntReq, sabSalReq, domEntReq, domSalReq, fechaInicioOp])"""
        params=(puntoServicio,  '' if totalHoras is None else float(totalHoras), 
        None if lunEntReq  is None or lunEntReq  == '' else lunEntReq,
        None if lunSalReq  is None or lunSalReq  == '' else lunSalReq,
        None if marEntReq  is None or marEntReq  == '' else marEntReq,
        None if marSalReq  is None or marSalReq  == '' else marSalReq,
        None if mierEntReq is None or mierEntReq == '' else mierEntReq,
        None if mierSalReq is None or mierSalReq == '' else mierSalReq,
        None if juevEntReq is None or juevEntReq == '' else juevEntReq,
        None if juevSalReq is None or juevSalReq == '' else juevSalReq,
        None if vieEntReq  is None or vieEntReq  == '' else vieEntReq,
        None if vieSlReq   is None or vieSlReq   == '' else vieSlReq,
        None if sabEntReq  is None or sabEntReq  == '' else sabEntReq,
        None if sabSalReq  is None or sabSalReq  == '' else sabSalReq,
        None if domEntReq  is None or domEntReq  == '' else domEntReq,
        None if domSalReq  is None or domSalReq  == '' else domSalReq,
        fechaInicioOp, fechaFinOp,perfil)
        conn.execute('operarios_disponibles_v3 %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s',params)
        result = conn.fetchall()
        conn.close()
        return [OperariosAsignacionDet(*row) for row in result]

def cargarOperarios(request, id_puntoServicio:None):
    try:
        buscar_operarios(5,8, (datetime.datetime.strptime('08:00:00','%H:%M:%S')).time(),  (datetime.datetime.strptime('08:00:00','%H:%M:%S')).time(),  (datetime.datetime.strptime('08:00:00','%H:%M:%S')).time(),  (datetime.datetime.strptime('08:00:00','%H:%M:%S')).time(),  (datetime.datetime.strptime('08:00:00','%H:%M:%S')).time(),  (datetime.datetime.strptime('08:00:00','%H:%M:%S')).time(),  (datetime.datetime.strptime('08:00:00','%H:%M:%S')).time(),  (datetime.datetime.strptime('08:00:00','%H:%M:%S')).time(),  (datetime.datetime.strptime('08:00:00','%H:%M:%S')).time(),  (datetime.datetime.strptime('08:00:00','%H:%M:%S')).time(),  (datetime.datetime.strptime('08:00:00','%H:%M:%S')).time(),  (datetime.datetime.strptime('08:00:00','%H:%M:%S')).time(),  (datetime.datetime.strptime('08:00:00','%H:%M:%S')).time(),  (datetime.datetime.strptime('08:00:00','%H:%M:%S')).time(),datetime.datetime.strptime('1996-08-08','%Y-%m-%d'))
    except Operario.DoesNotExist as err:
        logging.getLogger("error_logger").error('No se encontraron operarios: {0}'.format(err))
        raise Http404("No existen coincidencias de operarios")
    
    return redirect('Operarios:asignacion_create', id_puntoServicio=pk_puntoServSeleccionado)


    