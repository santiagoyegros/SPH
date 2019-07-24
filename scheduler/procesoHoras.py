import logging
import datetime as dt
from Operarios.models import HorasNoProcesadas, HorasProcesadas, EsmeEmMarcaciones, AsignacionDet, AsignacionCab, PuntoServicio, AsignacionesProcesadas, AsigFiscalPuntoServicio, AsigJefeFiscal, Feriados

from django.db.models import Q
def procesarEntradaSalida(marcacion, marcacion2):
    print("PROCESO HORAS")
    #Paso 1: Busco la asignacion de la persona en el contrato, en el dia. 
    CodPersona = marcacion.codpersona
    PuntoServicioCod = marcacion.codubicacion
    HorarioEntrada = marcacion.fecha.time()
    HorarioSalida = marcacion2.fecha.time()
    DiaSemana = marcacion.fecha.weekday()
    fecha = marcacion.fecha.date()

    Asignaciones = AsignacionDet.objects.filter(Q(asignacionCab__puntoServicio__CodPuntoServicio=PuntoServicioCod) & Q(operario_id__NumCedula=CodPersona) & Q(vfechaFin=None))
    consulta = AsignacionDet.objects.filter(Q(asignacionCab__puntoServicio__CodPuntoServicio=PuntoServicioCod) & Q(operario_id__NumCedula=CodPersona) & Q(vfechaFin=None)).query
    logging.getLogger("error_logger").error('La consulta para buscar las asignaciones es: {0}'.format(consulta))
    
    try:
        PuntoServicioObj = PuntoServicio.objects.filter(Q(CodPuntoServicio=PuntoServicioCod) & Q(vfechaFin=None)).first()
    except PuntoServicio.DoesNotExist as err:
        logging.getLogger("error_logger").error('Punto de Servicio no existe: {0}'.format(err))
        pass


    #Paso 2: Si existe asignacion se almacena las horas
    print ("Se encontraron {0}".format(len(Asignaciones)) )
    if len(Asignaciones) != 0:
        hits = 0
        repetida = 0

        for asignacion in Asignaciones:
            if DiaSemana == 0:
                EntradaAsig = asignacion.lunEnt
                SalidaAsig = asignacion.lunSal
            elif DiaSemana == 1:
                EntradaAsig = asignacion.marEnt
                SalidaAsig = asignacion.marSal
            elif DiaSemana == 2:
                EntradaAsig = asignacion.mieEnt
                SalidaAsig = asignacion.mieSal
            elif DiaSemana == 3:
                EntradaAsig = asignacion.jueEnt
                SalidaAsig = asignacion.jueSal
            elif DiaSemana == 4:
                EntradaAsig = asignacion.vieEnt
                SalidaAsig = asignacion.vieSal
            elif DiaSemana == 5:
                EntradaAsig = asignacion.sabEnt
                SalidaAsig = asignacion.sabSal
            elif DiaSemana == 6:
                EntradaAsig = asignacion.domEnt
                SalidaAsig = asignacion.domSal

            if (not((EntradaAsig is None) or (SalidaAsig is None))):
                
                if ((HorarioEntrada >= EntradaAsig and HorarioEntrada < SalidaAsig) or
                        (HorarioSalida > EntradaAsig and HorarioSalida <= SalidaAsig) or
                        (HorarioEntrada < EntradaAsig and HorarioSalida > SalidaAsig)):
                    
                    #Determinamos le limite Inferior
                    if (HorarioEntrada >= EntradaAsig):
                        LimiteInferior = HorarioEntrada
                    else:
                        LimiteInferior = EntradaAsig

                    #Determinamos le limite superior
                    if (SalidaAsig >= HorarioSalida):
                        LimiteSuperior = HorarioSalida
                    else:
                        LimiteSuperior = SalidaAsig

                    # Calculamos por fin las horas trabajadas
                    #HorasTrabajadas = LimiteSuperior - LimiteInferior
                    HorasTrabajadas = dt.datetime.combine(dt.date.min, LimiteSuperior) - dt.datetime.combine(dt.date.min, LimiteInferior)
                    HorasTrabajadas_segundos = HorasTrabajadas.total_seconds() 
                    hours   = divmod(HorasTrabajadas_segundos, 3600)
                    minutes = divmod(hours[1], 60)
                    seconds = divmod(minutes[1], 1) 

                    total_horas = dt.time(hour=int(hours[0]), minute=int(minutes[0]), second=int(seconds[0]))

                    #Determinamos si la asiginacion ya fue procesado
                    AsignacionesPro = AsignacionesProcesadas.objects.filter(NumCedulaOperario=CodPersona, puntoServicio__CodPuntoServicio=PuntoServicioCod, fecha=fecha, asignacionDet=asignacion)
                    consulta = AsignacionesProcesadas.objects.filter(NumCedulaOperario=CodPersona, puntoServicio__CodPuntoServicio=PuntoServicioCod, fecha=fecha, asignacionDet=asignacion).query
                    logging.getLogger("error_logger").error('La consulta para buscar las asignaciones ya procesadas es: {0}'.format(consulta))

                    if (len(AsignacionesPro) == 0): 
                        #Si la asignacion no fue procesada anteriormente.
                        procesayguardahoras(CodPersona, PuntoServicioObj, LimiteInferior, LimiteSuperior, total_horas, fecha, 1, asignacion)
                        hits +=1

                        #Guardamos que la asignacion ya fue procesada para esta fecha
                        AsigPro = AsignacionesProcesadas(
                            NumCedulaOperario=CodPersona,
                            puntoServicio=PuntoServicioObj,
                            fecha=fecha,
                            asignacionDet=asignacion
                        )
                        AsigPro.save()
                    else:
                        #Si la asignacion si fue procesada anteriormente, guardamos el evento
                        procesayguardahoras(CodPersona, PuntoServicioObj, LimiteInferior, LimiteSuperior, total_horas, fecha, 5, None)
                        repetida +=1

                    #return 'PRO'
                else:
                    #Procesamos como sin Asignacion
                    print("Sin A")
                    HorasTrabajadas = dt.datetime.combine(dt.date.min, HorarioSalida) - dt.datetime.combine(dt.date.min, HorarioEntrada)
                    HorasTrabajadas_sinA_segundos = HorasTrabajadas.total_seconds() 
                    hours   = divmod(HorasTrabajadas_sinA_segundos, 3600)
                    minutes = divmod(hours[1], 60)
                    seconds = divmod(minutes[1], 1)
                    total_horas_sinA = dt.time(hour=int(hours[0]), minute=int(minutes[0]), second=int(seconds[0]))

                    #Procesamos la hora
                    procesayguardahoras(CodPersona, PuntoServicioObj, HorarioEntrada, HorarioSalida, total_horas_sinA, fecha, 2, None)

                #Fin If
            #Fin If
        #Fin for
        if(repetida):
            return 'REPE'
        else:
            if(hits > 0):
                return 'PRO'
            else:
                return 'SINA'

    #Paso 3: Si no existe asignacion se almacena las horas sin aginacion.
    else:
        #Paso 3.1: Revisamos si la marcacion es de un fiscal
        Esfiscal = AsigFiscalPuntoServicio.objects.filter(userFiscal__username=CodPersona, puntoServicio__CodPuntoServicio=PuntoServicioCod, puntoServicio__vfechaFin=None)
        consulta = AsigFiscalPuntoServicio.objects.filter(userFiscal__username=CodPersona, puntoServicio__CodPuntoServicio=PuntoServicioCod, puntoServicio__vfechaFin=None).query
        logging.getLogger("error_logger").error('La consulta para buscar las asignaciones ya procesadas es: {0}'.format(consulta))

        #Paso 3.2: Revisamos si la marcacion es de una jefa de operaciones
        #EsJefe = AsigJefeFiscal.objects.filter(userJefe__username=CodPersona, puntoServicio__CodPuntoServicio=PuntoServicioCod)
        EsJefe = AsigJefeFiscal.objects.raw("""SELECT asig.id           AS id, 
                                                asig.userfiscal_id      AS userFiscal_id, 
                                                asig.userjefe_id        AS userJefe_id, 
                                                usu.username 
                                            FROM   [dbo].[operarios_asigjefefiscal] AS asig 
                                                JOIN [dbo].[auth_user] AS usu 
                                                    ON asig.userjefe_id = usu.id 
                                                JOIN [dbo].[operarios_asigfiscalpuntoservicio] AS asigFP 
                                                    ON asig.userfiscal_id = asigFP.userfiscal_id 
                                            WHERE  asigFP.puntoservicio_id = %s 
                                                AND usu.username = %s """, [PuntoServicioObj.id, CodPersona]  
        )
        consulta = AsigJefeFiscal.objects.raw("""SELECT asig.id           AS id, 
                                                asig.userfiscal_id      AS userFiscal_id, 
                                                asig.userjefe_id        AS userJefe_id, 
                                                usu.username 
                                            FROM   [dbo].[operarios_asigjefefiscal] AS asig 
                                                JOIN [dbo].[auth_user] AS usu 
                                                    ON asig.userjefe_id = usu.id 
                                                JOIN [dbo].[operarios_asigfiscalpuntoservicio] AS asigFP 
                                                    ON asig.userfiscal_id = asigFP.userfiscal_id 
                                            WHERE  asigFP.puntoservicio_id = %s 
                                                AND usu.username = %s """, [PuntoServicioObj.id, CodPersona] 
        ).query
        logging.getLogger("error_logger").error('La consulta para buscar las asignaciones ya procesadas es: {0}'.format(consulta))

        #Si es fiscal 
        if (len(Esfiscal) > 0):
            print("Es Fiscal")
            # Calculamos por fin las horas trabajadas del fiscal
            HorasTrabajadas = dt.datetime.combine(dt.date.min, HorarioSalida) - dt.datetime.combine(dt.date.min, HorarioEntrada)
            HorasTrabajadas_segundos = HorasTrabajadas.total_seconds() 
            hours   = divmod(HorasTrabajadas_segundos, 3600)
            minutes = divmod(hours[1], 60)
            seconds = divmod(minutes[1], 1) 

            total_horas = dt.time(hour=int(hours[0]), minute=int(minutes[0]), second=int(seconds[0]))
            #TipoDeHora = gettipohora(HorarioEntrada, HorarioSalida, DiaSemana, fecha)

            procesayguardahoras(CodPersona, PuntoServicioObj, HorarioEntrada, HorarioSalida, total_horas, fecha, 3, None)
            return 'PRO'
        
        #Si es Jefe de Operacion
        if (len(EsJefe) > 0):
            print("Es Jefe de Operacion")
            # Calculamos por fin las horas trabajadas del jefe de operaciones
            HorasTrabajadas = dt.datetime.combine(dt.date.min, HorarioSalida) - dt.datetime.combine(dt.date.min, HorarioEntrada)
            HorasTrabajadas_segundos = HorasTrabajadas.total_seconds() 
            hours   = divmod(HorasTrabajadas_segundos, 3600)
            minutes = divmod(hours[1], 60)
            seconds = divmod(minutes[1], 1) 

            total_horas = dt.time(hour=int(hours[0]), minute=int(minutes[0]), second=int(seconds[0]))
            #TipoDeHora = gettipohora(HorarioEntrada, HorarioSalida, DiaSemana, fecha)

            procesayguardahoras(CodPersona, PuntoServicioObj, HorarioEntrada, HorarioSalida, total_horas, fecha, 4, None)
            return 'PRO'

        else:
            #Si NO es fiscal del punto del punto de servicio, registramos la sin asignacion
            print("Sin A")
            diff = dt.datetime.combine(dt.date.min, HorarioSalida) - dt.datetime.combine(dt.date.min, HorarioEntrada)
            HorasTrabajadas_sinA_segundos = diff.total_seconds() 
            hours   = divmod(HorasTrabajadas_sinA_segundos, 3600)
            minutes = divmod(hours[1], 60)
            seconds = divmod(minutes[1], 1)
            total_horas_sinA = dt.time(hour=int(hours[0]), minute=int(minutes[0]), second=int(seconds[0]))

            #fecha_sinA = marcacion.fecha.date()
            #TipoDeHora_sinA = gettipohora(HorarioEntrada, HorarioSalida, DiaSemana, fecha)
            procesayguardahoras(CodPersona, PuntoServicioObj, HorarioEntrada, HorarioSalida, total_horas_sinA, fecha, 2, None)
            return 'SINA'
    
'''
Este metodo procesa y guarda las horas procesadas y no procesadas
Tipo: 1 (Hora Procesada)
Tipo: 2 (Hora Sin Asignacion)
Tipo: 3 (Hora Fiscal)
Tipo: 4 (Hora Jefe)
Tipo: 5 (Hora Repetida)
'''
def procesayguardahoras(NumCedulaOperario, puntoServicio, horaInicio, HoraFin, Total, Fecha, Tipo, Asignacion):
    limiteDiurnoSuperior = dt.time(20, 0)
    limiteDiurnoInferior = dt.time(6, 0)
    DiaSemana = Fecha.weekday()
    TipoDeHora = ''

    #Pasos Previos, determinar si es feriado y/o su dia libre
    feriado = False
    diaLibre = False
    
    #Previo.1.Determinamos si la fecha es un feriado
    Esferiado = Feriados.objects.filter(fecha=Fecha)
    consulta = Feriados.objects.filter(fecha=Fecha).query
    logging.getLogger("error_logger").error('La consulta para buscar si la fecha es feriado: {0}'.format(consulta))
    
    if (len(Esferiado) > 0):
        feriado = True
    #Previo.2.Determinar si es dia libre del operario
    #Falta


    #Semana Lunes a Sabado
    if(DiaSemana >= 0 and DiaSemana <= 5 and not feriado):
        if (horaInicio >= limiteDiurnoInferior and HoraFin <= limiteDiurnoSuperior):
            TipoDeHora = 'HNORM'
        elif (horaInicio < limiteDiurnoInferior and HoraFin <= limiteDiurnoInferior) or (horaInicio > limiteDiurnoSuperior and HoraFin >= limiteDiurnoSuperior):
            TipoDeHora =  'HNOCT'
        elif (limiteDiurnoInferior > horaInicio and limiteDiurnoInferior < HoraFin):
            TipoDeHora = 'MIXTO-INF'
            TipoDeHoraSub1 = 'HNOCT'
            TipoDeHoraSub2 = 'HNORM'
        elif (limiteDiurnoSuperior > horaInicio and limiteDiurnoSuperior < HoraFin):
            TipoDeHora = 'MIXTO-SUP'
            TipoDeHoraSub1 = 'HNORM'
            TipoDeHoraSub2 = 'HNOCT'
    
    #Domingo
    elif(DiaSemana == 6 and not feriado):
        if (horaInicio >= limiteDiurnoInferior and HoraFin <= limiteDiurnoSuperior):
            TipoDeHora = 'DOMI'
        elif (horaInicio < limiteDiurnoInferior and HoraFin <= limiteDiurnoInferior) or (horaInicio > limiteDiurnoSuperior and HoraFin >= limiteDiurnoSuperior):
            TipoDeHora =  'DONOC'
        elif (limiteDiurnoInferior > horaInicio and limiteDiurnoInferior < HoraFin):
            TipoDeHora = 'DMIXTO-INF'
            TipoDeHoraSub1 = 'DONOC'
            TipoDeHoraSub2 = 'DOMI'
        elif (limiteDiurnoSuperior > horaInicio and limiteDiurnoSuperior < HoraFin):
            TipoDeHora = 'DMIXTO-SUP' 
            TipoDeHoraSub1 = 'DOMI'
            TipoDeHoraSub2 = 'DONOC'
    #Feriado
    elif(feriado):
        if (horaInicio >= limiteDiurnoInferior and HoraFin <= limiteDiurnoSuperior):
            TipoDeHora = 'FERIA'
        elif (horaInicio < limiteDiurnoInferior and HoraFin <= limiteDiurnoInferior) or (horaInicio > limiteDiurnoSuperior and HoraFin >= limiteDiurnoSuperior):
            TipoDeHora =  'FENOC'
        elif (limiteDiurnoInferior > horaInicio and limiteDiurnoInferior < HoraFin):
            TipoDeHora = 'FMIXTO-INF'
            TipoDeHoraSub1 = 'FENOC'
            TipoDeHoraSub2 = 'FERIA'
        elif (limiteDiurnoSuperior > horaInicio and limiteDiurnoSuperior < HoraFin):
            TipoDeHora = 'FMIXTO-SUP'
            TipoDeHoraSub1 = 'FERIA'
            TipoDeHoraSub2 = 'FENOC'

    if (Tipo in [1, 3, 4]):
        #Procesamos una hora procesada
        if(Tipo == 1):
            Comentario = 'Hora Procesada'
        elif(Tipo == 3):
            Comentario = 'Hora Procesada - Fiscal'
        elif (Tipo == 4):
            Comentario = 'Hora Procesada - Jefe'

        if (TipoDeHora.find('MIXTO') >= 0):

            if (TipoDeHora.find('MIXTO-INF') >= 0):
                TotalSub1 = CalcularDifHoras(horaInicio, limiteDiurnoInferior)
                TotalSub2 = CalcularDifHoras(limiteDiurnoInferior, HoraFin)

                HoraPro1 = HorasProcesadas(
                    NumCedulaOperario=NumCedulaOperario,
                    puntoServicio=puntoServicio,
                    Hentrada=horaInicio,
                    Hsalida=limiteDiurnoInferior,
                    total=TotalSub1,
                    fecha=Fecha,
                    TipoHora=TipoDeHoraSub1,
                    comentario=Comentario,
                    asignacionDet=Asignacion
                )
                HoraPro1.save()

                HoraPro2 = HorasProcesadas(
                    NumCedulaOperario=NumCedulaOperario,
                    puntoServicio=puntoServicio,
                    Hentrada=limiteDiurnoInferior,
                    Hsalida=HoraFin,
                    total=TotalSub2,
                    fecha=Fecha,
                    TipoHora=TipoDeHoraSub2,
                    comentario=Comentario,
                    asignacionDet=Asignacion
                )
                HoraPro2.save()

            elif (TipoDeHora.find('MIXTO-SUP') >= 0):
                TotalSub1 = CalcularDifHoras(horaInicio, limiteDiurnoSuperior)
                TotalSub2 = CalcularDifHoras(limiteDiurnoSuperior, HoraFin)

                HoraPro1 = HorasProcesadas(
                    NumCedulaOperario=NumCedulaOperario,
                    puntoServicio=puntoServicio,
                    Hentrada=horaInicio,
                    Hsalida=limiteDiurnoSuperior,
                    total=TotalSub1,
                    fecha=Fecha,
                    TipoHora=TipoDeHoraSub1,
                    comentario=Comentario,
                    asignacionDet=Asignacion
                )
                HoraPro1.save()

                HoraPro2 = HorasProcesadas(
                    NumCedulaOperario=NumCedulaOperario,
                    puntoServicio=puntoServicio,
                    Hentrada=limiteDiurnoSuperior,
                    Hsalida=HoraFin,
                    total=TotalSub2,
                    fecha=Fecha,
                    TipoHora=TipoDeHoraSub2,
                    comentario=Comentario,
                    asignacionDet=Asignacion
                )
                HoraPro2.save()
            
        else:
            HoraPro = HorasProcesadas(
                NumCedulaOperario=NumCedulaOperario,
                puntoServicio=puntoServicio,
                Hentrada=horaInicio,
                Hsalida=HoraFin,
                total=Total,
                fecha=Fecha,
                TipoHora=TipoDeHora,
                comentario=Comentario,
                asignacionDet=Asignacion
            )
            HoraPro.save()
        return 'PRO'

    elif(Tipo in [2, 5]):
        #Procesamos una hora no procesadas (Sin A y Repetidas)
        if(Tipo == 2):
            Comentario = 'Hora sin asignacion'
        elif(Tipo == 5):
            Comentario = 'Hora repetida'

        if (TipoDeHora.find('MIXTO') >= 0):

            if (TipoDeHora.find('MIXTO-INF') >= 0):
                TotalSub1 = CalcularDifHoras(horaInicio, limiteDiurnoInferior)
                TotalSub2 = CalcularDifHoras(limiteDiurnoInferior, HoraFin)

                HoraPro1 = HorasNoProcesadas(
                    NumCedulaOperario=NumCedulaOperario,
                    puntoServicio=puntoServicio,
                    Hentrada=horaInicio,
                    Hsalida=limiteDiurnoInferior,
                    total=TotalSub1,
                    fecha=Fecha,
                    TipoHora=TipoDeHoraSub1,
                    comentario=Comentario
                )
                HoraPro1.save()

                HoraPro2 = HorasNoProcesadas(
                    NumCedulaOperario=NumCedulaOperario,
                    puntoServicio=puntoServicio,
                    Hentrada=limiteDiurnoInferior,
                    Hsalida=HoraFin,
                    total=TotalSub2,
                    fecha=Fecha,
                    TipoHora=TipoDeHoraSub2,
                    comentario=Comentario
                )
                HoraPro2.save()

            elif (TipoDeHora.find('MIXTO-SUP') >= 0):
                TotalSub1 = CalcularDifHoras(horaInicio, limiteDiurnoSuperior)
                TotalSub2 = CalcularDifHoras(limiteDiurnoSuperior, HoraFin)

                HoraPro1 = HorasNoProcesadas(
                    NumCedulaOperario=NumCedulaOperario,
                    puntoServicio=puntoServicio,
                    Hentrada=horaInicio,
                    Hsalida=limiteDiurnoSuperior,
                    total=TotalSub1,
                    fecha=Fecha,
                    TipoHora=TipoDeHoraSub1,
                    comentario=Comentario
                )
                HoraPro1.save()

                HoraPro2 = HorasNoProcesadas(
                    NumCedulaOperario=NumCedulaOperario,
                    puntoServicio=puntoServicio,
                    Hentrada=limiteDiurnoSuperior,
                    Hsalida=HoraFin,
                    total=TotalSub2,
                    fecha=Fecha,
                    TipoHora=TipoDeHoraSub2,
                    comentario=Comentario
                )
                HoraPro2.save()  
        else:

            HoraNoPro = HorasNoProcesadas(
                NumCedulaOperario=NumCedulaOperario,
                puntoServicio=puntoServicio,
                Hentrada=horaInicio,
                Hsalida=HoraFin,
                total=Total,
                fecha=Fecha,
                TipoHora=TipoDeHora,
                comentario=Comentario
            )
            HoraNoPro.save()
        return 'SINA'

    return 'DESCONOCIDO'

def CalcularDifHoras(HoraInicio, HoraFin):

    diff = dt.datetime.combine(dt.date.min, HoraFin) - dt.datetime.combine(dt.date.min, HoraInicio)
    HorasTrabajadas_sinA_segundos = diff.total_seconds() 
    hours   = divmod(HorasTrabajadas_sinA_segundos, 3600)
    minutes = divmod(hours[1], 60)
    seconds = divmod(minutes[1], 1)

    return dt.time(hour=int(hours[0]), minute=int(minutes[0]), second=int(seconds[0]))

def proceso_de_horas():
    print('La hora exacta es:' + str(dt.datetime.now()))

    #Paso 1: Seleccionar todas las marcaciones sin procesar
    Marcaciones = EsmeEmMarcaciones.objects.filter(estado__isnull=True).order_by('fecha')
    consulta = EsmeEmMarcaciones.objects.filter(estado__isnull=True).order_by('fecha').query
    logging.getLogger("error_logger").error('La consulta ejecutada en el paso 1 es: {0}'.format(consulta))

    #Paso 2: Recorro las marcaciones de forma ordenada los HE y busco su par de HS
    if Marcaciones:
        seleccionado = None
        for i, marcacion in enumerate(Marcaciones, start=0):
            
            if marcacion.codoperacion == 'HE':
                for marcacion2 in Marcaciones[i+1:]:
                    #print('Test' + str(i))
                    if (marcacion.codpersona == marcacion2.codpersona 
                        and marcacion.codubicacion == marcacion2.codubicacion 
                        and marcacion2.codoperacion == 'HS' and marcacion2.estado != 'PROCESADO'
                        and marcacion.fecha.date() == marcacion2.fecha.date()):

                        print('Encontre una pareja')
                        print(marcacion.fecha)
                        print(marcacion2.fecha)
                        procesado = procesarEntradaSalida(marcacion, marcacion2)
                        if procesado == 'PRO':
                            marcacion.estado = 'PROCESADO'
                            marcacion2.estado = 'PROCESADO'
                        elif procesado == 'SINA':
                            marcacion.estado = 'SIN ASIGNACION'
                            marcacion2.estado = 'SIN ASIGNACION'
                        elif procesado == 'REPE':
                            marcacion.estado = 'REPETIDA'
                            marcacion2.estado = 'REPETIDA'

                        marcacion.save()
                        marcacion2.save()
                        #Al procesar una pareja de marcacion, se rompe el loop
                        break

                        
    #Paso 3: Recorrer el resto de las marcaciones no emparejada, para registrar la sin entrada
    if Marcaciones:
        for i, marcacion in enumerate(Marcaciones, start=0):
            if marcacion.codoperacion == 'HS' and marcacion.estado != 'PROCESADO' and marcacion.estado != 'SIN ASIGNACION':
                marcacion.estado = 'SIN ENTRADA'
                marcacion.save()

    #Paso 4:

    #Paso 5:

