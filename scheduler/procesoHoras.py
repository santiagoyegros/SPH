import logging
import datetime
from Operarios.models import HorasNoProcesadas, HorasProcesadas, EsmeEmMarcaciones, AsignacionDet, AsignacionCab, PuntoServicio

def procesarEntradaSalida(marcacion, marcacion2):
    #Paso 1: Busco la asignacion de la persona en el contrato, en el dia. 
    CodPersona = marcacion.codpersona
    PuntoServicioCod = marcacion.codubicacion
    HorarioEntrada = marcacion.fecha
    HorarioSalida = marcacion2.fecha
    DiaSemana = marcacion.fecha.weekday()

    Asignaciones = AsignacionDet.objects.filter(asignacionCab__puntoServicio__CodPuntoServicio=PuntoServicioCod, operario_id__NumCedula=CodPersona)
    consulta = AsignacionDet.objects.filter(asignacionCab__puntoServicio__CodPuntoServicio=PuntoServicioCod, operario_id__NumCedula=CodPersona).query
    logging.getLogger("error_logger").error('La consulta para buscar las asignaciones es: {0}'.format(consulta))
    
    PuntoServicioObj = PuntoServicio.objects.get(CodPuntoServicio=PuntoServicioCod)

    #Paso 2: Si existe asginacion se almacena las horas
    if len(Asignaciones) != 0:
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
                        (HorarioSalida > EntradaAsig and HorarioSalida >= SalidaAsig) or
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
                    HorasTrabajadas = LimiteInferior - LimiteInferior
                    HorasTrabajadas_segundos = HorasTrabajadas.total_seconds() 
                    hours   = divmod(HorasTrabajadas_segundos, 3600)
                    minutes = divmod(hours[1], 60)
                    seconds = divmod(minutes[1], 1) 

                    total_horas = datetime.time(hour=hours, minute=minutes, second=seconds)
                    fecha = marcacion.fecha.date()
                    TipoDeHora = 'HNORM'

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

            else:
                #Procesamos como sin Asignacion
                print("Sin A")
                diff = HorarioSalida - HorarioEntrada
                HorasTrabajadas_sinA_segundos = diff.total_seconds() 
                hours   = divmod(HorasTrabajadas_sinA_segundos, 3600)
                minutes = divmod(hours[1], 60)
                seconds = divmod(minutes[1], 1)
                total_horas_sinA = datetime.time(hour=hours, minute=minutes, second=seconds)

                fecha_sinA = marcacion.fecha.date()
                TipoDeHora_sinA = 'HNORM'

                HoraNoPro = HorasNoProcesadas(
                        NumCedulaOperario=CodPersona,
                        puntoServicio=PuntoServicioObj,
                        Hentrada=HorarioEntrada,
                        Hsalida=HorarioSalida,
                        total=total_horas_sinA,
                        fecha=fecha_sinA,
                        TipoHora=TipoDeHora_sinA,
                        comentario='Hora sin asignacion',
                    )
                HoraNoPro.save()
    #Paso 3: Si no existe asignacion se almacena las horas sin aginacion.
    else:
        #Registramos la sin asignacion
        print("Sin A")
        diff = HorarioSalida - HorarioEntrada
        HorasTrabajadas_sinA_segundos = diff.total_seconds() 
        hours   = divmod(HorasTrabajadas_sinA_segundos, 3600)
        minutes = divmod(hours[1], 60)
        seconds = divmod(minutes[1], 1)
        total_horas_sinA = datetime.time(hour=int(hours[0]), minute=int(minutes[0]), second=int(seconds[0]))

        fecha_sinA = marcacion.fecha.date()
        TipoDeHora_sinA = 'HNORM'

        HoraNoPro = HorasNoProcesadas(
                NumCedulaOperario=CodPersona,
                puntoServicio=PuntoServicioObj,
                Hentrada=HorarioEntrada,
                Hsalida=HorarioSalida,
                total=total_horas_sinA,
                fecha=fecha_sinA,
                TipoHora=TipoDeHora_sinA,
                comentario='Hora sin asignacion',
            )
        HoraNoPro.save()
    


def proceso_de_horas():
    print('La hora exacta es:' + str(datetime.datetime.now()))

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
                    if (marcacion.codpersona == marcacion2.codpersona and marcacion.codubicacion == marcacion2.codubicacion and marcacion2.codoperacion == 'HS'):
                        print('Encontre una pareja')
                        print(marcacion.fecha)
                        print(marcacion2.fecha)
                        procesado = procesarEntradaSalida(marcacion, marcacion2)

        #Paso 2.1: Por cada par de HE y HS, busco su asignacion por cedula, punto de servicio, y fecha/dia.

            #Paso 2.1:1: Si hay una asignacion para el horario marcado, se procesa la hora
            
            #Paso 2.1.2: Si no existe asignacion se procesa la SIN A.  

    #Paso 3: Recorrer el resto de las marcaciones no emparejada, para registrar la sin entrada

    #Paso 4:

    #Paso 5:

