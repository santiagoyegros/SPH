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
import datetime
from datetime import date

from Operarios.models import PuntoServicio, Operario, RelevamientoCab, RelevamientoDet, RelevamientoEsp, RelevamientoCupoHoras, RelevamientoMensualeros, PlanificacionCab, PlanificacionOpe, PlanificacionEsp, Cargo, CargoAsignado, AsigFiscalPuntoServicio, AsigJefeFiscal, AsignacionCab, AsignacionDet, DiaLibre, OperariosAsignacionDet
from Operarios.forms import PuntoServicioForm, OperarioForm, RelevamientoForm, RelevamientoDetForm, RelevamientoEspForm, RelevamientoCupoHorasForm, RelevamientoMensualerosForm, PlanificacionForm, PlanificacionOpeForm, PlanificacionEspForm, AsignacionCabForm, AsignacionDetForm,DiaLibreForm


from django.db import connection

from datetime import datetime as dt
@login_required
@permission_required('Operarios.view_asignacioncab', raise_exception=True)
def Asignacion_list(request):
    if request.method == 'POST':
        pk_puntoServSeleccionado = request.POST.get('asig_puntoServ')
        return redirect('Operarios:asignacion_create', id_puntoServicio=pk_puntoServSeleccionado)
    else:
        puntoServi = PuntoServicio.objects.all()
        contexto = {'PuntosServicio': puntoServi}
        return render(request, 'asignacion/asignacion_list.html', context=contexto)

@login_required
@permission_required('Operarios.add_asignacioncab', raise_exception=True)
def Asignacion_create(request, id_puntoServicio=None):
    sem_diurno = '0'
    sem_nocturno = '0'
    dom_diurno = '0'
    dom_nocturno = '0'
    operarios = []
    diaInicioSelected = []
    diaFinSelected = []
    horaInicioSelected=[]
    horaFinSelected=[]
    dias = ["Lunes","Martes",'Miercoles',"Jueves","Viernes","Sabado","Domingo"]
    allOperarios = Operario.objects.all()
    openModal=False
    idModal = None
  
    
    logging.getLogger("error_logger").error('Se ingreso en el metodo asignacion_create')
    ''' Obtenemos el punto de servicio, en caso de error se muesta un error 404 '''
    try:
        puntoSer = PuntoServicio.objects.get(pk=id_puntoServicio)
    except PuntoServicio.DoesNotExist as err:
        logging.getLogger("error_logger").error('Punto de Servicio no existe: {0}'.format(err))
        raise Http404("Punto de Servicio no existe")

    ''' Obtenemos el relevamiento para mostrar en la pantalla '''
    relevamiento = RelevamientoCab.objects.filter(puntoServicio_id = puntoSer.id).first()
    if relevamiento == None:
        logging.getLogger("error_logger").error('El punto de servicio no tiene servicio aprobado')
        raise Http404("El punto de servicio no tiene Servicio aprobado")

    if relevamiento.relevamientocupohoras_set.exists():
        logging.getLogger("error_logger").error('Estamos revisando si existe detalle de cupo de horas')
        for cupo in relevamiento.relevamientocupohoras_set.iterator():
            if cupo.tipoHora.tipoHorario == 'Diurno' and cupo.frecuencia == 'SEM':
                sem_diurno = cupo.cantCHoras
            elif cupo.tipoHora.tipoHorario == 'Nocturno' and cupo.frecuencia == 'SEM':
                sem_nocturno = cupo.cantCHoras
            elif cupo.tipoHora.tipoHorario == 'Diurno' and cupo.frecuencia == 'DOM':
                dom_diurno = cupo.cantCHoras
            elif cupo.tipoHora.tipoHorario == 'Diurno' and cupo.frecuencia == 'DOM':
                dom_nocturno = cupo.cantCHoras

        

    ''' Obtenemos la asignacion en caso de que exista una '''
    asignacion = AsignacionCab.objects.filter(puntoServicio_id = puntoSer.id).first()
    formDiaLibre = DiaLibreForm(request.POST)
    print("ASIGNACION", asignacion)
    if asignacion == None:
        asignacion = AsignacionCab()
    

    asignacionDetFormSet = inlineformset_factory(AsignacionCab, AsignacionDet, form=AsignacionDetForm, extra=1, can_delete=True)
    print("#1")
    if request.method == 'POST':
        if  request.POST.get('action') == 'add_det': 
            """Se le dio click a agregar detalle"""
            form = AsignacionCabForm(request.POST, instance=asignacion)
            AsigDetFormSet = asignacionDetFormSet(request.POST, instance=asignacion)
            i=0
            for form in AsigDetFormSet:
                if i < len(AsigDetFormSet)-1:
                    if request.session['diaInicio-' + str(i)]:
                        diaInicioSelected.append(request.session['diaInicio-' + str(i)])
                    else:
                        diaInicioSelected.append(None)
                    
                    if request.session['diaFin-' + str(i)]:
                        diaFinSelected.append(request.session['diaFin-' + str(i)])
                    else:
                        diaFinSelected.append(None)

                    if request.session['horaInicio-' + str(i)]:
                        horaInicioSelected.append(request.session['horaInicio-' + str(i)])
                    else:
                        horaInicioSelected.append(None)

                    if request.session['horaFin-' + str(i)]:
                        horaFinSelected.append(request.session['horaFin-' + str(i)])
                    else:
                        horaFinSelected.append(None)
                i=i+1
            print("ARRAYS EN SESION AGREGAR DETALLE")
            print(diaInicioSelected)
            print(horaInicioSelected)
            print(diaFinSelected)
            print(horaFinSelected)
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
                request.session['diaInicio-' + str(i)]=request.POST.get('diaInicio-' + str(i))
                diaInicioSelected.append(request.session['diaInicio-' + str(i)])

                request.session['diaFin-' + str(i)]=request.POST.get('diaFin-' + str(i))
                diaFinSelected.append(request.session['diaFin-' + str(i)])

                request.session['horaInicio-' + str(i)]=request.POST.get('horaInicio-' + str(i))
                horaInicioSelected.append(request.session['horaInicio-' + str(i)])

                request.session['horaFin-' + str(i)]=request.POST.get('horaFin-' + str(i))
                horaFinSelected.append(request.session['horaFin-' + str(i)])
                
                print("ARRAYS EN SESION FILTRAR OPERARIO")
                print(diaInicioSelected)
                print(horaInicioSelected)
                print(diaFinSelected)
                print(horaFinSelected)
                if i == formOperarioID:
                    
                    if request.POST.get('asignaciondet_set-' + str(i) + '-totalHoras') != 'None':
                        totalHoras = request.POST.get('asignaciondet_set-' + str(i) +'-totalHoras')
                    if  id_puntoServicio:
                        idPunto = id_puntoServicio
                    if request.POST.get('asignaciondet_set-' + str(i) + '-fechaInicio'):
                        fechaIni = request.POST.get('asignaciondet_set-' + str(i) + '-fechaInicio')
                        date_time_obj = datetime.datetime.strptime(fechaIni,'%d/%m/%Y')
                        fechaIni=date_time_obj.strftime('%Y-%m-%d')
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
                                print ("Para verificar horario")     
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
                                print (request.POST.get("id_asignaciondet_set-" + str(index-1) + "-DELETE"))
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
            print (request.POST)
        else: 
            """Se le dio click al boton guardar"""
            

            form = AsignacionCabForm(request.POST, instance=asignacion)
            
            AsigDetFormSet = asignacionDetFormSet(request.POST,instance=asignacion)
            print (form.errors)
            print (AsigDetFormSet.errors)
            if form.is_valid() and AsigDetFormSet.is_valid():
                """Se guarda completo"""
                form.save()
                AsigDetFormSet.save()
                messages.success(request, 'Se guardo correctamente la asignacion')
                return redirect('Operarios:asignacion_list')
            else:
                messages.warning(request, 'No se pudo guardar los cambios')

    else:
        print("NO ES POST")
        """
        Seteamos el punto de servicio
        """
        asignacion.puntoServicio = puntoSer
        form = AsignacionCabForm(instance=asignacion)
        AsigDetFormSet = asignacionDetFormSet(instance=asignacion)
    
    print("ARRAYS",diaFinSelected,diaInicioSelected)
    contexto = {
            'title': 'Nueva Asignación',
            'pservicio': puntoSer,
            'form': form,
            'formDiaLibre':formDiaLibre,
            'asigDetFormSet': AsigDetFormSet,
            'relevamiento' : relevamiento,
            'sem_diurno' : sem_diurno,
            'sem_nocturno' : sem_nocturno,
            'dom_diurno' : dom_diurno,
            'dias':dias,
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

def buscar_operarios(puntoServicio, totalHoras, lunEntReq, lunSalReq, marEntReq, marSalReq, mierEntReq, mierSalReq, juevEntReq, juevSalReq, vieEntReq, vieSlReq, sabEntReq, sabSalReq, domEntReq, domSalReq,perfil,supervisor, fechaInicioOp,horaInicio,horaFin,diaInicio,diaFin):
        conn= connection.cursor()
        sql = """\
            DECLARE @out nvarchar(max);
            EXEC [dbo].[operarios_disponibles] @puntoServicio=?, @totalHoras=?, @lunEntReq=?, @lunSalReq=?, @marEntReq=?, @marSalReq=?, @mierEntReq=?, @mierSalReq=?, @juevEntReq=?, @juevSalReq=?, @vieEntReq=?, @vieSlReq=?, @sabEntReq=?, @sabSalReq=?, @domEntReq=?, @domSalReq=?, @fechaInicioOperario=?, @perfil=?, @param_out = @out OUTPUT;
            SELECT @out AS the_output;
        """
        """conn.callproc('operarios_disponibles', [puntoServicio, totalHoras, lunEntReq, lunSalReq, marEntReq, marSalReq, mierEntReq, mierSalReq, juevEntReq, juevSalReq, vieEntReq, vieSlReq, sabEntReq, sabSalReq, domEntReq, domSalReq, fechaInicioOp])"""
        params=(puntoServicio, totalHoras, lunEntReq, lunSalReq, marEntReq, marSalReq, mierEntReq, mierSalReq, juevEntReq, juevSalReq, vieEntReq, vieSlReq, sabEntReq, sabSalReq, domEntReq, domSalReq, fechaInicioOp, perfil)
        print(params)
        conn.execute('operarios_disponibles %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s',params)
        result = conn.fetchall()
       
        print("RESULTADO",result)
        conn.close()
        return [OperariosAsignacionDet(*row) for row in result]


def cargarOperarios(request, id_puntoServicio:None):
    try:
        buscar_operarios(5,8, (datetime.datetime.strptime('08:00:00','%H:%M:%S')).time(),  (datetime.datetime.strptime('08:00:00','%H:%M:%S')).time(),  (datetime.datetime.strptime('08:00:00','%H:%M:%S')).time(),  (datetime.datetime.strptime('08:00:00','%H:%M:%S')).time(),  (datetime.datetime.strptime('08:00:00','%H:%M:%S')).time(),  (datetime.datetime.strptime('08:00:00','%H:%M:%S')).time(),  (datetime.datetime.strptime('08:00:00','%H:%M:%S')).time(),  (datetime.datetime.strptime('08:00:00','%H:%M:%S')).time(),  (datetime.datetime.strptime('08:00:00','%H:%M:%S')).time(),  (datetime.datetime.strptime('08:00:00','%H:%M:%S')).time(),  (datetime.datetime.strptime('08:00:00','%H:%M:%S')).time(),  (datetime.datetime.strptime('08:00:00','%H:%M:%S')).time(),  (datetime.datetime.strptime('08:00:00','%H:%M:%S')).time(),  (datetime.datetime.strptime('08:00:00','%H:%M:%S')).time(),datetime.datetime.strptime('1996-08-08','%Y-%m-%d'))
    except Operario.DoesNotExist as err:
        logging.getLogger("error_logger").error('No se encontraron operarios: {0}'.format(err))
        raise Http404("No existen coincidencias de operarios")
    
    return redirect('Operarios:asignacion_create', id_puntoServicio=pk_puntoServSeleccionado)


    