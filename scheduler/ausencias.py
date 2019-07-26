import logging
import datetime as dt
from datetime import datetime, timedelta
import datetime
from django.db.models import Q
from Operarios.models import Parametros,Alertas,User,Motivos, AsignacionesProcesadas,AlertaResp, HorasNoProcesadas,Operario,AsignacionDet
from django.conf import settings

def getHoraDia(id_dia,id_asignacion):
    asignacionDet = AsignacionDet.objects.get(id = id_asignacion )
    print("getHora",id_asignacion, "dia",id_dia)
    if id_dia == 0:
        return [asignacionDet.lunEnt,asignacionDet.lunSal]
    if id_dia == 1:
        return [asignacionDet.marEnt,asignacionDet.marSal]
    if id_dia == 2:
        return [asignacionDet.mieEnt,asignacionDet.mieSal]
    if id_dia == 3:
        return [asignacionDet.jueEnt,asignacionDet.jueSal]
    if id_dia == 4:
        return [asignacionDet.vieEnt,asignacionDet.vieSal]
    if id_dia == 5:
        return [asignacionDet.sabEnt,asignacionDet.sabSal]
    if id_dia == 6:
        return [asignacionDet.domEnt,asignacionDet.domSal]

def getTipoHorario(entrada,salida):
    limiteDiurnoSuperior = dt.time(20, 0)
    limiteDiurnoInferior = dt.time(6, 0)
    if entrada >= limiteDiurnoInferior and salida < limiteDiurnoSuperior:
        return "Diurno"
    else:
        return "Nocturno"
def registrar_ausencia():
    print('Procedimiento de registro de ausencias: ' + str(dt.datetime.now()))
    alertas = Alertas.objects.all()
    for a in alertas:
        callcenter_time = settings.GLOBAL_SETTINGS['MAX_CALLCENTER']
        if Parametros.objects.filter(parametro = 'MAX_CALLCENTER').exists():
            callcenter_db = Parametros.objects.get(parametro = 'MAX_CALLCENTER')
            callcenter_time = callcenter_db.valor
        dateParametro=datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%mm-%dd %H:%M:%S"),"%Y-%mm-%dd %H:%M:%S") - datetime.timedelta(minutes=int(callcenter_time))
        dateAlerta= datetime.datetime.strptime(a.FechaHora.strftime("%Y-%mm-%dd %H:%M:%S"),"%Y-%mm-%dd %H:%M:%S")
        if not a.Estado == 'PENDIENTE':
            if dateAlerta <= dateParametro:
                if AsignacionDet.objects.filter(id=a.Asignacion_id).exists():
                    """SI LA ASIGNACION DE LA ALERTA NO FUE PROCESADA"""
                    if not AsignacionesProcesadas.objects.filter(asignacionDet_id=a.Asignacion_id).exists():
                        """Corroboramos la consistencia de los datos"""
                        if Operario.objects.filter(id=a.Operario_id).exists():
                            operario = Operario.objects.get(id=a.Operario_id)
                            entrada, salida = getHoraDia(dateAlerta.weekday(),a.Asignacion_id)
                            if entrada and salida:
                                """Obtiene total horas de la Alerta"""
                                tentrada = timedelta(hours = entrada.hour, minutes= entrada.minute)
                                tsalida = timedelta(hours = salida.hour, minutes= salida.minute)
                                totalHoras = tsalida- tentrada
                                """Se otiene el tipo de horario """
                                tipoHorario = getTipoHorario(entrada,salida)
                                noProcesada = HorasNoProcesadas(
                                    NumCedulaOperario = operario.numCedula, 
                                    Hentrada = entrada, 
                                    Hsalida = salida, 
                                    fecha = dateAlerta,
                                    puntoServicio_id=a.PuntoServicio_id, 
                                    total = totalHoras, 
                                    TipoHora = tipoHorario,
                                    comentario="AUSENCIA")
                                """Se guarda el registro de hora no procesada"""
                                #noProcesada.save() 

                                """Se cierra la alerta"""
                                a.Estado = "CERRADA"
                                #a.save()
                                
                                """Se guarda la respuesta de la alerta"""
                                user_parametrico = settings.GLOBAL_SETTINGS['USER_CALLCENTER']
                                if Parametros.objects.filter(parametro = 'USER_CALLCENTER').exists():
                                    user_db = Parametros.objects.get(parametro = 'USER_CALLCENTER')
                                    user_parametrico = user_db.valor

                                usuario = User.objects.get(id = user_parametrico)
                                motivo = Motivos.objects.get(descripcion= "Gestión Automática")
                                alerta_respuesta = AlertaResp(
                                    motivo = motivo,
                                    accion = "AusenciaAuto",
                                    hora = a.FechaHora,
                                    fechaRetorno = a.FechaHora,
                                    escalado = False,
                                    comentarios = "Ausencia Automática",
                                    usuario = usuario
                                )
                                #alerta_respuesta.save()
