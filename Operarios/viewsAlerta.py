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
import datetime
from django.core import serializers
from Operarios.models import Alertas
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Operarios.models import OperariosAsignacionDet
from Operarios.models import PuntoServicio, Operario, AsignacionCab, AsignacionDet, AsigFiscalPuntoServicio, EsmeEmMarcaciones,HorasNoProcesadas, HorariosOperario, RemplazosCab, RemplazosDet, AlertaResp, Parametros, Motivos, CupoReal, CupoUtilizado,HorasProcesadas,TipoHorario
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db import connection, transaction
from Operarios.models import Motivos
from django.db.models import Q
import json
@login_required

def alertasList (request):
    estado="Abierta"
    fechaDesde=request.GET.get('fechaDesde')
    fechaHasta=request.GET.get('fechaHasta')
    horaInicio=request.GET.get('horaInicio')
    horaFin=request.GET.get('horaFin')
    puntoServicio=None
    operario=None
    tipoAlerta=None
    """query por defecto con fecha del dia"""
    hoy= datetime.datetime.now()
    hoyIni=hoy.replace(hour=0,minute=0,second=0, microsecond=0)

    hoyFin=hoyIni.replace(hour=23,minute=59,second=59)
    alertasList=Alertas.objects.filter(FechaHora__gte=hoyIni,FechaHora__lte=hoyFin)
    operarios = Operario.objects.all()
    motivos = Motivos.objects.all()
    PuntosServicio = PuntoServicio.objects.all()
    alertasList=alertasList.filter(Estado="ABIERTA")
    alertasList=alertasList.order_by("-FechaHora")
   


    """query por filtro segun el usuario"""
    print (request.GET.get('puntoServicio'))
    print (request.GET.get('fechaDesde'))
    print (request.GET.get('fechaHasta'))
    print(request.GET.get('horaInicio'))
    print(request.GET.get('horaFin'))
    print (request.GET.get('estado'))
    print (request.GET.get('tipoAlerta'))
    print (request.GET.get('operario'))


    
    if request.GET.get("fechaDesde") and request.GET.get("fechaHasta") and request.GET.get("horaInicio") and request.GET.get("horaFin"):
        fechaDesdeAux=datetime.datetime.strptime(request.GET.get('fechaDesde'), "%d/%m/%Y").replace(hour=0,minute=0,second=0, microsecond=0)
        fechaHastaAux=datetime.datetime.strptime(request.GET.get('fechaHasta'), "%d/%m/%Y").replace(hour=23,minute=59,second=59, microsecond=0)     
        aux1=str(request.GET.get("fechaDesde")).split('/')
        aux2=str(request.GET.get("fechaHasta")).split('/')
        fDesdeAux=aux1[2]+'-'+aux1[1]+'-'+aux1[0]+' '+request.GET.get("horaInicio")+':00'
        fHastaAux=aux2[2]+'-'+aux2[1]+'-'+aux2[0]+' '+request.GET.get("horaFin")+':00'
        alertasList=Alertas.objects.filter(FechaHora__gte=fDesdeAux,FechaHora__lte=fHastaAux)

    if request.GET.get('estado'):
        alertasList=alertasList.filter(Estado__contains=request.GET.get('estado'))
        estado=request.GET.get('estado')
    if request.GET.get('tipoAlerta'):
        print(request.GET.get('tipoAlerta'))
        if(request.GET.get('tipoAlerta')=="TODOS"):
             alertasList=alertasList.all()
        else:
            alertasList=alertasList.filter(Tipo__contains=request.GET.get('tipoAlerta'))
        tipoAlerta=request.GET.get('tipoAlerta')
    if request.GET.get('operario') :
        alertasList=alertasList.filter(Operario_id=request.GET.get('operario'))
        operario=int(request.GET.get('operario'))
    if request.GET.get('puntoServicio') :
        alertasList=alertasList.filter(PuntoServicio_id=request.GET.get('puntoServicio'))
        puntoServicio=int(request.GET.get('puntoServicio'))
    
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
                punto = PuntoServicio.objects.get(Q(id=a.PuntoServicio_id))
                a.Punto_nombre = punto.NombrePServicio
            except PuntoServicio.DoesNotExist:
                raise Http404("Punto de Servicio relacionado a una Alerta no existe")  

    contexto = {
        'title': 'Filtrado de Alertas',
        'alertasList':alertasList,
        'paginator':paginator,
        'operarios':operarios,
        'motivos':motivos,
        'PuntosServicio':PuntosServicio,
        "fechaDesde":fechaDesde,
        "fechaHasta":fechaHasta,
        "horaInicio":horaInicio,
        "horaFin":horaFin, 
        "estado":estado,
        "puntoServicio":puntoServicio,
        "operario":operario,
        "tipoAlerta":tipoAlerta
    
        
    }

    return render(request, 'alertas/alerta_list.html', context=contexto)


def mostrarCupos(request):
    alerta=Alertas.objects.get(Q(id=request.GET.get("id")))
    puntoServ_id=alerta.PuntoServicio_id
    fecha=alerta.FechaHora.strftime("%d/%m/%Y").split('/')
    mes=fecha[1]
    mes='07'
    anho=fecha[2]
    totalUtilizado=0
    cuposUtilizados=CupoUtilizado.objects.all()
    if(CupoReal.objects.filter(Q(puntoServicio_id=puntoServ_id) & Q(mes=mes) & Q(anho=anho) ).exists()):
        cupo=CupoReal.objects.get(Q(puntoServicio_id=puntoServ_id) & Q(mes=mes) & Q(anho=anho) )
        cupoTotal=cupo.cupoCalculado
        for c in cuposUtilizados:
            if (str(c.mes)==mes and str(c.anho)==anho and c.puntoServicio_id==int(puntoServ_id)):
                totalUtilizado=totalUtilizado + c.cupoUtilizado
    else:
        totalUtilizado=0
        cupoTotal=0
    
    data = {
        "cupoTotal":cupoTotal,
        "cupoUtilizado":totalUtilizado
    }
    return HttpResponse(json.dumps(data),content_type="application/json")



def guardarSinAsignacion(request,id_alerta=None):
    if request.method == 'POST':
        alerta=Alertas.objects.get(id=id_alerta)
        motivo=request.POST.get('motivo')
        observacion=request.POST.get('observacion')
        puntoServicio=PuntoServicio.objects.get(Q(id=alerta.PuntoServicio.id))
        horarios=[]
        if alerta.Asignacion:
            horarios=horasOperario(alerta.Asignacion.id, alerta.FechaHora.strftime("%Y-%m-%d %H:%M:%S"))        
        tipoHorarios=TipoHorario.objects.all()
        horas={'tipoHorario':' ','total':0}
        start = datetime.datetime.strptime(str(horarios[0].horaEntrada), "%H:%M:%S")
        end = datetime.datetime.strptime(str(horarios[0].horaSalida), "%H:%M:%S")
        diferencia=end-start
        for tipo in tipoHorarios:
            if(horarios[0].horaEntrada>=tipo.horaInicio and horarios[0].horaSalida<=tipo.horaFin):
                horas["tipoHorario"]=tipo.tipoHorario
                horas["total"]=str(diferencia)

        try:
            """Se cambia el estado de la alerta"""
            setattr(alerta,"Estado", "CERRADA")
            alerta.save()
            """Se guarda la gestion de sin asignacion en respuesta alerta"""
            respAlerta=AlertaResp.objects.create(accion='SINA-JUSTIFICADO',id_alerta=alerta, motivo_id=motivo, comentarios=observacion, usuario=request.user,fecha_creacion=datetime.datetime.now())
            respAlerta.save()
            """Se guarda en respuestas procesadas"""
            horasProcesadas=HorasProcesadas.objects.create(NumCedulaOperario=alerta.Operario.numCedula, puntoServicio=alerta.PuntoServicio ,Hentrada=horarios[0].horaEntrada, Hsalida=horarios[0].horaSalida, comentario= 'Hora Procesada - SinA', fecha=alerta.FechaHora.date(), total=horas["total"],TipoHora=horas["tipoHorario"])
            horasProcesadas.save()
        except Exception as err:
            transaction.rollback()
            logging.getLogger("error_logger").error('No se pudo gestionar la alerTa: {0}'.format(err))
            messages.warning(request, 'No se pudo gestionar la alerta') 
        else:
            transaction.commit()
            messages.success(request, 'Alerta gestionada con exito')
        finally:
            transaction.set_autocommit(True)
            return redirect('Operarios:alertas_list')



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


def getMarcaciones(request):
    print(request.GET.get('alerta_id'))
    alerta_id= request.GET.get('alerta_id')
    alerta=Alertas.objects.get(id=alerta_id)
    operario=Operario.objects.get(id=alerta.Operario.id)
    ultimasMarcaciones=EsmeEmMarcaciones.objects.filter(codpersona__contains=operario.numCedula).order_by("fecha")[:10]

    return HttpResponse(serializers.serialize("json",ultimasMarcaciones), content_type = 'application/json', status = 200);

def getReemplazos(request):
    print(request.GET.get('alerta_id'))
    totalHoras=idPunto="" 
    lunEnt=lunSal=marEnt=marSal=mieEnt=mieSal=jueEnt=jueSal=vieEnt=vieSal=sabEnt=sabSal=domEnt=domSal=""
    fechaIni = ""
    diaInicio=diaFin=""
    horaInicio=horaFin=""
    supervisor=False
    perfil=""
    fechaFin=""
    operarios = []
    if request.GET.get('id_puntoServicio')  is not None and request.GET.get('id_puntoServicio')!='':
        idPunto = request.GET.get('id_puntoServicio')
    if request.GET.get('fechaInicio')  is not None and request.GET.get('fechaInicio')!='':
        fechaIni = request.GET.get('fechaInicio')
        date_time_obj = datetime.datetime.strptime(fechaIni,'%d/%m/%Y')
        fechaIni=date_time_obj.strftime('%Y-%m-%d')
    if request.GET.get('horarioInicio')  is not None and request.GET.get('horarioInicio')!='' and "lun" in request.GET.get('diaRequerido'):
        lunEnt = request.GET.get('horarioInicio') 
    if request.GET.get('horarioFin')  is not None and request.GET.get('horarioFin')!='' and "lun" in request.GET.get('diaRequerido'):
        lunSal = request.GET.get('horarioFin') 
    if request.GET.get('horarioInicio')  is not None and request.GET.get('horarioInicio')!='' and "mar" in request.GET.get('diaRequerido'):
        marEnt = request.GET.get('horarioInicio') 
    if request.GET.get('horarioFin')  is not None and request.GET.get('horarioFin')!='' and "mar" in request.GET.get('diaRequerido'):
        marSal = request.GET.get('horarioFin')
    if request.GET.get('horarioInicio')  is not None and request.GET.get('horarioInicio')!='' and "mie" in request.GET.get('diaRequerido'):
        mieEnt = request.GET.get('horarioInicio') 
    if request.GET.get('horarioFin')  is not None and request.GET.get('horarioFin')!='' and "mie" in request.GET.get('diaRequerido'):
        mieSal = request.GET.get('horarioFin')
    if request.GET.get('horarioInicio')  is not None and request.GET.get('horarioInicio')!='' and "jue" in request.GET.get('diaRequerido'):
        jueEnt = request.GET.get('horarioInicio') 
    if request.GET.get('horarioFin')  is not None and request.GET.get('horarioFin')!='' and "jue" in request.GET.get('diaRequerido'):
        jueSal = request.GET.get('horarioFin')
    if request.GET.get('horarioInicio')  is not None and request.GET.get('horarioInicio')!='' and "vie" in request.GET.get('diaRequerido'):
        vieEnt = request.GET.get('horarioInicio') 
    if request.GET.get('horarioFin')  is not None and request.GET.get('horarioFin')!='' and "vie" in request.GET.get('diaRequerido'):
        vieSal = request.GET.get('horarioFin')
    if request.GET.get('horarioInicio')  is not None and request.GET.get('horarioInicio')!='' and "sab" in request.GET.get('diaRequerido'):
        sabEnt = request.GET.get('horarioInicio') 
    if request.GET.get('horarioFin')  is not None and request.GET.get('horarioFin')!='' and "sab" in request.GET.get('diaRequerido'):
        sabSal = request.GET.get('horarioFin')
    if request.GET.get('horarioInicio')  is not None and request.GET.get('horarioInicio')!='' and "dom" in request.GET.get('diaRequerido'):
        domEnt = request.GET.get('horarioInicio') 
    if request.GET.get('horarioFin')  is not None and request.GET.get('horarioFin')!='' and "dom" in request.GET.get('diaRequerido'):
        domSal = request.GET.get('horarioFin')

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
    
    return HttpResponse(serializers.serialize("json",operarios), content_type = 'application/json', status = 200)

def buscar_operarios(puntoServicio, totalHoras, lunEntReq, lunSalReq, marEntReq, marSalReq, mierEntReq, mierSalReq, juevEntReq, juevSalReq, vieEntReq, vieSlReq, sabEntReq, sabSalReq, domEntReq, domSalReq,perfil,supervisor, fechaInicioOp,fechaFinOp,horaInicio,horaFin,diaInicio,diaFin):
        conn= connection.cursor()
        sql = """\
            DECLARE @out nvarchar(max);
            EXEC [dbo].[operarios_disponibles_v2] @puntoServicio=?, @totalHoras=?, @lunEntReq=?, @lunSalReq=?, @marEntReq=?, @marSalReq=?, @mierEntReq=?, @mierSalReq=?, @juevEntReq=?, @juevSalReq=?, @vieEntReq=?, @vieSlReq=?, @sabEntReq=?, @sabSalReq=?, @domEntReq=?, @domSalReq=?, @fechaInicioOperario=?, @fechaFinOperario=?,@perfil=?, @param_out = @out OUTPUT;
            SELECT @out AS the_output;
        """
        """conn.callproc('operarios_disponibles_v2', [puntoServicio, totalHoras, lunEntReq, lunSalReq, marEntReq, marSalReq, mierEntReq, mierSalReq, juevEntReq, juevSalReq, vieEntReq, vieSlReq, sabEntReq, sabSalReq, domEntReq, domSalReq, fechaInicioOp])"""
        params=(puntoServicio, totalHoras, lunEntReq, lunSalReq, marEntReq, marSalReq, mierEntReq, mierSalReq, juevEntReq, juevSalReq, vieEntReq, vieSlReq, sabEntReq, sabSalReq, domEntReq, domSalReq, fechaInicioOp, fechaFinOp,perfil)
        print(params)
        conn.execute('operarios_disponibles_v2 %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s',params)
        result = conn.fetchall()
       
        conn.close()
        return [OperariosAsignacionDet(*row) for row in result]

@login_required
def gestion_alertas(request,alerta_id=None):
    alerta=Alertas.objects.get(id=alerta_id)
    horario = ""
    diaRequerido=""
    prox_marcacion = ""
    horaConPenalizacion = ""
    fiscal=""
    motivos=[]
    motivos = Motivos.objects.all()
    supervisor=None
    if alerta.FechaHora:
            fecha = (alerta.FechaHora).strftime("%d/%m/%Y")
            alerta.Fecha = fecha 
            hora = (alerta.FechaHora).strftime("%H:%M:%S")
            alerta.Hora = hora
    """Se obtiene el horario del operario"""
    horarios=[]
    print("ALERTA ASIGNACION", alerta.Asignacion)
    if alerta.Asignacion:
        horarios=horasOperario(alerta.Asignacion.id, alerta.FechaHora.strftime("%Y-%m-%d %H:%M:%S"))
        penalizacionFinal=Parametros.objects.get(tipo__contains="ALERTAS", parametro__contains="PENALIZACION")
        if horarios:
            if horarios[0]:
                if horarios[0].horaEntrada:
                    horario = horarios[0].horaEntrada.strftime("%H:%M:%S")
                    horaFinal=datetime.datetime.strptime(horarios[0].horaEntrada.strftime("%H:%M:%S"), "%H:%M:%S") 
                    horaConPenalizacion=horaFinal+datetime.timedelta(minutes=int(penalizacionFinal.valor))
                    horaConPenalizacion = horaConPenalizacion.strftime("%H:%M:%S")
                if horarios[0].horaSalida:
                    horario = horario + " - " + horarios[0].horaSalida.strftime("%H:%M:%S")
            
                diaRequerido = horarios[0].diaEntrada
            if len(horarios)>1:
                if horarios[1].horaEntrada:
                    prox_marcacion = horarios[1].horaEntrada.strftime("%H:%M:%S") 
                if horarios[1].horaSalida:
                    prox_marcacion = prox_marcacion + " - " + horarios[1].horaSalida.strftime("%H:%M:%S")
    """obtener operario"""
    operario=Operario.objects.get(id=alerta.Operario.id)
    puntoServicio=PuntoServicio.objects.get(Q(id=alerta.PuntoServicio.id))
    """obtener el horario de ese punto de servicio para ese personaje"""
    print ("Punto de servicio ", puntoServicio)
    asignacionOperario=AsignacionDet.objects.get(id=alerta.Asignacion.id)
    print ("Asignacion operario ",asignacionOperario )
    if AsigFiscalPuntoServicio.objects.filter(Q(puntoServicio=puntoServicio)).exists():
        fiscal=AsigFiscalPuntoServicio.objects.get(Q(puntoServicio=puntoServicio))
    supervisores=AsignacionDet.objects.filter(Q(asignacionCab=asignacionCab) & Q(supervisor=1))
    if supervisores:
        supervisor=supervisores[0]
    alertasSinAsig=Alertas.objects.filter(Tipo__contains="SIN-ASIG",Estado__contains="ABIERTA", PuntoServicio=puntoServicio)
    ultimasMarcaciones=EsmeEmMarcaciones.objects.filter(codpersona__contains=operario.numCedula).order_by("fecha")[:10]
    """CAMBIAMOS EL ESTADO DE LA ALERTA"""
    if request.method == 'GET':
        setattr(alerta,"Estado", "EN GESTION")
        alerta.save()
        
    else: 
        print ("Es POST")
        print(request.POST)
        """En el lugar"""
        if request.POST.get('accion')=='1': 
            try:
                if horaConPenalizacion ==None or horaConPenalizacion=='':
                    messages.warning(request,"El operario no posee hora de entrada")

                else:
                    #horaNueva=datetime.datetime.strptime(request.POST.get('horaEntrada'), "%H:%M")
                    """procedemos a cerrar el alerta"""
                    setattr(alerta,"Estado", "CERRADA")
                    alerta.save()
                    """obtenemos la penalizacion"""
                    penalizacion=Parametros.objects.get(tipo__contains="ALERTAS", parametro__contains="PENALIZACION")
                    horaEntrada=datetime.datetime.strptime(horaConPenalizacion, "%H:%M:%S")
                    print("horaPenalizacion",horaEntrada)
                    nuevaFecha=datetime.datetime.combine(alerta.FechaHora.date(), datetime.datetime.strptime(horaConPenalizacion, "%H:%M:%S").time())
                    """generamos la marcacion"""
                    nuevaMarcacion=EsmeEmMarcaciones.objects.create(codpersona=alerta.Operario.numCedula,codoperacion="HE",fecha=nuevaFecha,codcategoria="EM",codubicacion=puntoServicio.CodPuntoServicio)
                    nuevaMarcacion.save()
                    """guardamos la respuesta a la alerta"""
                    respAlerta=AlertaResp.objects.create(accion='En el lugar',id_alerta=alerta, usuario=request.user, hora=horaEntrada)
                    respAlerta.save()
               
            except Exception as err:
                transaction.rollback()
                logging.getLogger("error_logger").error('No se pudo gestionar el alerta: {0}'.format(err))
                messages.warning(request, 'No se pudo gestionar el alerta') 
            else:
                if horaConPenalizacion !=None and horaConPenalizacion!='':
                    transaction.commit()
                    messages.success(request, 'Alerta gestionada con exito')
            finally:
                if horaConPenalizacion !=None and horaConPenalizacion!='':
                    transaction.set_autocommit(True)
                    return redirect('Operarios:alertas_list')
        """Si va a asistir"""
        if request.POST.get('accion')=='2': 
            try:
                """procedemos a cerrar el alerta"""
                setattr(alerta,"Estado", "CERRADA")
                alerta.save()
                """procedemos a crear una nueva alerta, con estado reprogramacion"""
                if request.POST.get('horaAprox') == None or request.POST.get('horaAprox') =='':
                    messages.error(request,"Favor ingrese la hora aproximada")


                else:
                    horaNueva=datetime.datetime.strptime(request.POST.get('horaAprox'), "%H:%M")
                    nuevaFecha=datetime.datetime.combine(alerta.FechaHora.date(), horaNueva.time())
                    newAlerta=Alertas.objects.create(Estado="RE PROGRAMACION", Asignacion=alerta.Asignacion, PuntoServicio=puntoServicio, Tipo="NO-MARC",FechaHora=nuevaFecha, Operario=alerta.Operario)
                    newAlerta.save()
                    """guardamos la respuesta a la alerta"""
                    respAlerta=AlertaResp.objects.create(accion='Va a asistir',id_alerta=alerta, usuario=request.user, hora=horaNueva.time())
                    respAlerta.save()
               
            except Exception as err:
                transaction.rollback()
                logging.getLogger("error_logger").error('No se pudo gestionar el alera: {0}'.format(err))
                messages.warning(request, 'No se pudo gestionar el alerta') 
            else:
                if request.POST.get('horaAprox') != None and request.POST.get('horaAprox') !='':
                    transaction.commit()
                    messages.success(request, 'Alerta gestionada con exito')
            finally:
                if request.POST.get('horaAprox') != None and request.POST.get('horaAprox') !='':
                    transaction.set_autocommit(True)
                    return redirect('Operarios:alertas_list')
        """No se va a cubrir"""
        if request.POST.get('accion')=='3':
            try:
                """guardamos las horas no procesadas"""
                horasNoProcesadas=HorasNoProcesadas.objects.create(NumCedulaOperario=alerta.Operario.numCedula, puntoServicio=puntoServicio,Hentrada=horarios[0].horaEntrada, Hsalida=horarios[0].horaSalida, comentario= 'AUSENCIA', fecha=alerta.FechaHora.date(), total=horarios[0].totalHoras)
                horasNoProcesadas.save()
                """procedemos a cerrar el alerta"""
                setattr(alerta,"Estado", "CERRADA")
                alerta.save()
                
                """guardamos la respuesta a la alerta"""
                respAlerta=AlertaResp.objects.create(accion='No se va a cubrir',id_alerta=alerta, usuario=request.user)
                respAlerta.save()
               
            except Exception as err:
                transaction.rollback()
                logging.getLogger("error_logger").error('No se pudo gestionar el alerTa: {0}'.format(err))
                messages.warning(request, 'No se pudo gestionar el alerta') 
            else:
                transaction.commit()
                messages.success(request, 'Alerta gestionada con exito')
            finally:
                transaction.set_autocommit(True)
                return redirect('Operarios:alertas_list')
        """REMPLAZO"""
        if request.POST.get('accion')=='4': 
            escalar=False
            try:
                print(request.POST)
                if request.POST.get('idreemplazante') != None and request.POST.get('idreemplazante')!='':
                    """procedemos a cerrar el alerta"""
                    setattr(alerta,"Estado", "CERRADA")
                    
                    """guardamos las horas no procesadas"""
                    entradaHora=None
                    salidaHora=None
                    horasTotales=None
                    if len(horarios)>1:
                        if horarios[0].horaEntrada:
                            entradaHora = horarios[0].horaEntrada
                        if horarios[0].horaSalida:
                            salidaHora = horarios[0].horaSalida
                        if horarios[0].totalHoras:
                            horasTotales = horarios[0].totalHoras
                    horasNoProcesadas=HorasNoProcesadas.objects.create(NumCedulaOperario=alerta.Operario.numCedula, puntoServicio=puntoServicio,Hentrada=entradaHora, Hsalida=salidaHora, comentario= 'AUSENCIA', fecha=alerta.FechaHora.date(), total=horasTotales)
                    horasNoProcesadas.save()
                    """"procedemos a guardar el remplazo"""

                    hora=""
                    if request.POST.get('horaRetorno'):
                        hora=datetime.datetime.strptime(request.POST.get('horaRetorno'), "%H:%M")
                    fechaRetorno=""
                    if request.POST.get('fechaRetorno'):
                        fechaRetorno=datetime.datetime.strptime(request.POST.get('fechaRetorno'), "%d/%m/%Y")
                    
                    """se guarda el reemplazo"""
                    horarioOperario=""
                    date_time_obj =  datetime.datetime.now().replace(hour=0,minute=0,second=0)
                    fechaAlerta = alerta.FechaHora.strftime("%d/%m/%Y")
                    if request.POST.get('horarioOperario'):
                        horarioOperario = request.POST.get('horarioOperario')
                        horarioOperario = horarioOperario[0:8]
                        date_time_obj = datetime.datetime.strptime(horarioOperario,'%H:%M:%S')

                    remplazoCab=RemplazosCab.objects.create(fechaInicio=alerta.FechaHora.date(),fechaFin=alerta.FechaHora.date(), tipoRemplazo='REEMPLAZO-1', FechaHoraRemplazo=datetime.datetime.strptime(fechaAlerta, "%d/%m/%Y").replace(hour=date_time_obj.hour,minute=date_time_obj.minute,second=date_time_obj.second, microsecond=0), usuario=request.user)
                    
                    asignacion_reemp = None
                    if alerta.Asignacion_id: 
                      asignacion_reemp =  AsignacionDet.objects.get(id=alerta.Asignacion_id) 
                      asignacion_reempActualizada =  AsignacionDet.objects.get(Q(vregistro=asignacion_reemp.vregistro)) 
                    operario_reemp  =Operario.objects.get(id=request.POST.get('idreemplazante'))
                    remplazoDet=RemplazosDet.objects.create(Asignacion=asignacion_reempActualizada, remplazo=operario_reemp, fecha=alerta.FechaHora.date(), remplazoCab=remplazoCab)
                    
                    
                    """guardamos la respuesta a la alerta"""
                    if request.POST.get('escalable'):
                        escalar=request.POST.get('escalable')
                    print("REEMPLAZO ID",remplazoCab.id) 
                    if request.POST.get("motivo"):
                        motivoObj =Motivos.objects.get(id=request.POST.get("motivo"))
                    respAlerta=AlertaResp.objects.create(accion='Reemplazo',id_alerta=alerta,id_reemplazo=remplazoCab, usuario=request.user, hora=hora,fechaRetorno=fechaRetorno, motivo=motivoObj,comentarios=request.POST.get("comentarios"), escalado=escalar)
                    
                    alerta.save()
                    remplazoCab.save()
                    remplazoDet.save()
                    respAlerta.save()
                else:
                    messages.warning(request, 'No se seleccionó un reemplazante') 
            except Exception as err:
                transaction.rollback()
                logging.getLogger("error_logger").error('No se pudo gestionar la alerta: {0}'.format(err))
                messages.warning(request, 'No se pudo gestionar la alerta') 
            else: 
                if request.POST.get('idreemplazante') != None and request.POST.get('idreemplazante')!='':
                    transaction.commit()
                    messages.success(request, 'Alerta gestionada con exito')
            finally:
                if request.POST.get('idreemplazante') != None and request.POST.get('idreemplazante')!='':
                    transaction.set_autocommit(True)
                    return redirect('Operarios:alertas_list')

    
    contexto = {
        'title': 'Gestion de Alertas',
        'operario':operario,
        'horario':horario,
        'motivos':motivos,
        'diaRequerido':diaRequerido,
        'prox_marcacion':prox_marcacion,
        'horaConPenalizacion':horaConPenalizacion,
        'puntoServicio':puntoServicio ,
        'alerta':alerta,
        'alerta_id':alerta_id,
        'asignacion':asignacionOperario,
        'fiscal':fiscal,
        'supervisor':supervisor,
        'alertasSinAsig':alertasSinAsig
    }
    return render(request, 'alertas/alerta_gestionar.html', context=contexto)




def emparejar(request, alerta_id=None, emparejamiento_id=None):
    print ("Hola emparejar")
    """alerta generada"""
    alerta=Alertas.objects.get(id=alerta_id)
    """obtener operario que se ausento"""
    puntoServicio=PuntoServicio.objects.get(Q(id=alerta.PuntoServicio.id))
    emparejamiento=Alertas.objects.get(id=emparejamiento_id)
    try :
        
        """procedemos a guardar las horas no procesadas"""
        horarios=[]
        horarios=horasOperario(alerta.Asignacion.id, alerta.FechaHora.strftime("%Y-%m-%d %H:%M:%S"))
        print (horarios[0].idOrden)
        print (horarios[0].diaEntrada)
        print (horarios[0].horaEntrada)
        print (horarios[0].diaSalida)
        print(horarios[0].horaSalida)
        print (horarios[0].totalHoras)
        print (alerta.FechaHora.date())
        print (alerta.Operario.numCedula)
        
        horasNoProcesadas=HorasNoProcesadas.objects.create(NumCedulaOperario=alerta.Operario.numCedula, puntoServicio=puntoServicio,Hentrada=horarios[0].horaEntrada, Hsalida=horarios[0].horaSalida, comentario= 'AUSENCIA', fecha=alerta.FechaHora.date(), total=horarios[0].totalHoras)
        horasNoProcesadas.save()
        """procedemos a guardar el reemplazo"""
        remplazoCab=RemplazosCab.objects.create(fechaInicio=alerta.FechaHora.date(),fechaFin=alerta.FechaHora.date(), tipoRemplazo='Emparejar', FechaHoraRemplazo=alerta.FechaHora, usuario=request.user)
        remplazoCab.save()
        remplazoDet=RemplazosDet.objects.create(Asignacion=alerta.Asignacion, remplazo=emparejamiento.Operario, fecha=alerta.FechaHora.date(), remplazoCab=remplazoCab)
        remplazoDet.save()

        """procedemos a guardar la respuesta del alerta no-marcacion"""
        respAlerta=AlertaResp.objects.create(accion='Emparejar',id_alerta=alerta, id_reemplazo=remplazoCab, usuario=request.user, hora=alerta.FechaHora.time())
        respAlerta.save()
        """procedemos a cerrar el alerta"""
        setattr(alerta,"Estado", "CERRADA")
        alerta.save()
        """procedemos a cerrar la sinasignacion"""
        setattr(emparejamiento,"Estado", "CERRADA")
        emparejamiento.save()
    except Exception as err:
        transaction.rollback()
        logging.getLogger("error_logger").error('No se pudo guardar el emparejamiento: {0}'.format(err))
        messages.error(request, 'No se pudo guardar el emparejamiento, favor verifique') 
    else:
        transaction.commit()
        messages.success(request, 'Emparejamiento guardado con exito')
    finally:
        transaction.set_autocommit(True)
    

    return redirect('Operarios:alertas_list')

def horasOperario(asignacion, fechaAlerta):
    conn= connection.cursor()
    params=(asignacion, fechaAlerta)
    print(params)
    conn.execute('operario_horario %s,%s',params)
    result = conn.fetchall()
    conn.close()
    print ("Resultado del procedimiento ", result)
    return [HorariosOperario(*row) for row in result]