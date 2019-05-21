import logging
import datetime as dt
from Operarios.models import HorasNoProcesadas, HorasProcesadas, EsmeEmMarcaciones, AsignacionDet, AsignacionCab, PuntoServicio, AsignacionesProcesadas

def procesarEntradaSalida(marcacion, marcacion2):
    #Paso 1: Busco la asignacion de la persona en el contrato, en el dia. 
    CodPersona = marcacion.codpersona
    PuntoServicioCod = marcacion.codubicacion
    HorarioEntrada = marcacion.fecha.time()
    HorarioSalida = marcacion2.fecha.time()
    DiaSemana = marcacion.fecha.weekday()
    fecha = marcacion.fecha.date()

    #AsignacionesPro = AsignacionesProcesadas.objects.filter(NumCedulaOperario=CodPersona, puntoServicio__CodPuntoServicio=PuntoServicioCod, fecha=fecha).values('asignacionDet_id')
    #consulta = AsignacionesProcesadas.objects.filter(NumCedulaOperario=CodPersona, puntoServicio__CodPuntoServicio=PuntoServicioCod, fecha=fecha).values('asignacionDet_id').query
    #logging.getLogger("error_logger").error('La consulta para buscar las asignaciones ya procesadas es: {0}'.format(consulta))

    Asignaciones = AsignacionDet.objects.filter(asignacionCab__puntoServicio__CodPuntoServicio=PuntoServicioCod, operario_id__NumCedula=CodPersona)
    consulta = AsignacionDet.objects.filter(asignacionCab__puntoServicio__CodPuntoServicio=PuntoServicioCod, operario_id__NumCedula=CodPersona).query
    logging.getLogger("error_logger").error('La consulta para buscar las asignaciones es: {0}'.format(consulta))
    
    try:
        PuntoServicioObj = PuntoServicio.objects.filter(CodPuntoServicio=PuntoServicioCod).first()
    except PuntoServicio.DoesNotExist as err:
        logging.getLogger("error_logger").error('Punto de Servicio no existe: {0}'.format(err))
        pass


    #Paso 2: Si existe asginacion se almacena las horas
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
                    #fecha = marcacion.fecha.date()
                    TipoDeHora = 'HNORM'

                    #Determinamos si la asiginacion ya fue procesado
                    AsignacionesPro = AsignacionesProcesadas.objects.filter(NumCedulaOperario=CodPersona, puntoServicio__CodPuntoServicio=PuntoServicioCod, fecha=fecha, asignacionDet=asignacion)
                    consulta = AsignacionesProcesadas.objects.filter(NumCedulaOperario=CodPersona, puntoServicio__CodPuntoServicio=PuntoServicioCod, fecha=fecha, asignacionDet=asignacion).query
                    logging.getLogger("error_logger").error('La consulta para buscar las asignaciones ya procesadas es: {0}'.format(consulta))

                    if (len(AsignacionesPro) == 0): 
                        #Si la asignacion no fue procesada anteriormente.
                        HoraPro = HorasProcesadas(
                            NumCedulaOperario=CodPersona,
                            puntoServicio=PuntoServicioObj,
                            Hentrada=LimiteInferior,
                            Hsalida=LimiteSuperior,
                            total=total_horas,
                            fecha=fecha,
                            TipoHora=TipoDeHora,
                            comentario='Hora Procesada',
                            asignacionDet=asignacion
                        )
                        HoraPro.save()
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
                        HoraNoPro = HorasNoProcesadas(
                            NumCedulaOperario=CodPersona,
                            puntoServicio=PuntoServicioObj,
                            Hentrada=LimiteInferior,
                            Hsalida=LimiteSuperior,
                            total=total_horas,
                            fecha=fecha,
                            TipoHora=TipoDeHora,
                            comentario='Hora repetida',
                        )
                        HoraNoPro.save()
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

                    #fecha_sinA = marcacion.fecha.date()
                    TipoDeHora_sinA = 'HNORM'

                    HoraNoPro = HorasNoProcesadas(
                            NumCedulaOperario=CodPersona,
                            puntoServicio=PuntoServicioObj,
                            Hentrada=HorarioEntrada,
                            Hsalida=HorarioSalida,
                            total=total_horas_sinA,
                            fecha=fecha,
                            TipoHora=TipoDeHora_sinA,
                            comentario='Hora sin asignacion',
                        )
                    HoraNoPro.save()
                    #return 'SINA'
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
        #Registramos la sin asignacion
        print("Sin A")
        diff = dt.datetime.combine(dt.date.min, HorarioSalida) - dt.datetime.combine(dt.date.min, HorarioEntrada)
        HorasTrabajadas_sinA_segundos = diff.total_seconds() 
        hours   = divmod(HorasTrabajadas_sinA_segundos, 3600)
        minutes = divmod(hours[1], 60)
        seconds = divmod(minutes[1], 1)
        total_horas_sinA = dt.time(hour=int(hours[0]), minute=int(minutes[0]), second=int(seconds[0]))

        #fecha_sinA = marcacion.fecha.date()
        TipoDeHora_sinA = 'HNORM'

        HoraNoPro = HorasNoProcesadas(
                NumCedulaOperario=CodPersona,
                puntoServicio=PuntoServicioObj,
                Hentrada=HorarioEntrada,
                Hsalida=HorarioSalida,
                total=total_horas_sinA,
                fecha=fecha,
                TipoHora=TipoDeHora_sinA,
                comentario='Hora sin asignacion',
            )
        HoraNoPro.save()
        return 'SINA'
    


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

