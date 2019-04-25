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

from Operarios.models import PuntoServicio, Operario, RelevamientoCab, RelevamientoDet, RelevamientoEsp, RelevamientoCupoHoras, RelevamientoMensualeros, PlanificacionCab, PlanificacionOpe, PlanificacionEsp, Cargo, CargoAsignado, AsigFiscalPuntoServicio, AsigJefeFiscal, AsignacionCab, AsignacionDet
from Operarios.forms import PuntoServicioForm, OperarioForm, RelevamientoForm, RelevamientoDetForm, RelevamientoEspForm, RelevamientoCupoHorasForm, RelevamientoMensualerosForm, PlanificacionForm, PlanificacionOpeForm, PlanificacionEspForm, AsignacionCabForm, AsignacionDetForm

def index(request):
    return HttpResponse("Vista de Operarios")

def index_alert(request):
    messages.debug(request, ' SQL statements were executed.')
    messages.info(request, 'Mensaje Informativo.')
    messages.success(request, 'Mensaje de Exito')
    messages.warning(request, 'Mensaje de Error.')
    messages.error(request, 'Document deleted.')
    return render(request, 'base_example.html')

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('Operarios.view_puntoservicio', raise_exception=True), name='dispatch')
class PuntosServicioList(ListView):
    #model = PuntoServicio
    context_object_name = 'PuntoServicio'
    template_name = "puntoServicio/puntoServicio_list.html"
    def get_queryset(self):
        try:
            #Traemos el cargo asignado
            ConsultaCargoUsuario = Cargo.objects.filter(cargoasignado__user=self.request.user.id).query
            logging.getLogger("error_logger").error('La consulta del cargo del usuario logueado ejecutada es: {0}'.format(ConsultaCargoUsuario))
            cargoUsuario = Cargo.objects.get(cargoasignado__user=self.request.user.id)

            if (cargoUsuario.cargo == 'Fiscal'):
                #Si es fiscal, le trae sus puntos de servicios. 'Fiscal'
                consulta = PuntoServicio.objects.filter(puntoServicioAsigFiscalPuntoServicio__userFiscal=self.request.user.id).query
                logging.getLogger("error_logger").error('La consulta de puntos de Servicio List ejecutada es: {0}'.format(consulta))
                return PuntoServicio.objects.filter(puntoServicioAsigFiscalPuntoServicio__userFiscal=self.request.user.id)

            elif (cargoUsuario.cargo == 'Jefe de Operaciones'):
                #Si es jefe de operaciones -> Trae todo los puntos de servicio de sus fiscales. 'Jefe de Operaciones'
                consulta = PuntoServicio.objects.filter(puntoServicioAsigFiscalPuntoServicio__userFiscal=self.request.user.id).query
                logging.getLogger("error_logger").error('La consulta de puntos de Servicio List ejecutada es: {0}'.format(consulta))
                return PuntoServicio.objects.filter(puntoServicioAsigFiscalPuntoServicio__userFiscal=self.request.user.id)
                pass
            elif (cargoUsuario.cargo == 'Gerente de Operaciones'):
                #Si es Gerente de Operaciones/SubGerente -> Todos los contratos. 'Gerente de Operaciones'
                consulta = PuntoServicio.objects.filter(puntoServicioAsigFiscalPuntoServicio__userFiscal=self.request.user.id).query
                logging.getLogger("error_logger").error('La consulta de puntos de Servicio List ejecutada es: {0}'.format(consulta))
                return PuntoServicio.objects.filter(puntoServicioAsigFiscalPuntoServicio__userFiscal=self.request.user.id)
                pass

            else:
                #Else: algun error, de no tener el rol correcto.
                pass
        except Cargo.DoesNotExist:
            raise Http404("El usuario no tiene el cargo requerido para ingresar")        

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('Operarios.add_puntoservicio', raise_exception=True), name='dispatch')
class PuntoServicioCreate(SuccessMessageMixin, CreateView):
    model = PuntoServicio
    form_class = PuntoServicioForm
    template_name = "puntoServicio/puntoServicio_form.html"
    success_url = reverse_lazy('Operarios:puntoServicio_list')
    success_message = 'Punto de Servicio Creado correctamente'
    extra_context = {'title': 'Nuevo Punto de Servicio'}

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('Operarios.change_puntoservicio', raise_exception=True), name='dispatch')
class PuntoServicioUpdateView(SuccessMessageMixin, UpdateView):
    model = PuntoServicio
    form_class = PuntoServicioForm
    template_name = "puntoServicio/puntoServicio_form.html"
    success_url = reverse_lazy('Operarios:puntoServicio_list')
    success_message = 'Punto de Servicio modificado correctamente'
    extra_context = {'title': 'Editar Punto de Servicio '}

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('Operarios.delete_puntoservicio', raise_exception=True), name='dispatch')
class PuntoServicioDeleteView(SuccessMessageMixin, DeleteView):
    model = PuntoServicio
    template_name = "puntoServicio/puntoServicio_delete.html"
    success_url = reverse_lazy('Operarios:puntoServicio_list')
    success_message = 'Punto de Servicio eliminado correctamente'

    def delete(self, request, *args, **kwargs):
        messages.warning(self.request, self.success_message)
        return super(PuntoServicioDeleteView, self).delete(request, *args, **kwargs)

@login_required
@permission_required(['Operarios.add_relevamientocab', 'Operarios.view_relevamientocab'], raise_exception=True)
def Relevamiento(request, id_puntoServicio=None):
    primeraVez = 0

    try:
        """
        Obtenemos el punto de servicio
        """
        puntoSer = PuntoServicio.objects.get(pk=id_puntoServicio)
    except PuntoServicio.DoesNotExist:
        raise Http404("Punto de Servicio no existe")

    relevamiento = RelevamientoCab.objects.filter(puntoServicio_id = puntoSer.id).first()

    if relevamiento == None:
        primeraVez = 1
        relevamiento = RelevamientoCab()

       
    relevamientoDetFormSet =        inlineformset_factory(RelevamientoCab, RelevamientoDet, form=RelevamientoDetForm, extra=3, can_delete=True)
    relevamientoEspFormSet =        inlineformset_factory(RelevamientoCab, RelevamientoEsp, form=RelevamientoEspForm, extra=2, can_delete=True)
    relevamientoCupoHorasFormSet =  inlineformset_factory(RelevamientoCab, RelevamientoCupoHoras, form=RelevamientoCupoHorasForm, extra=3, can_delete=True)
    relevamientoMensuFormSet =      inlineformset_factory(RelevamientoCab, RelevamientoMensualeros, form=RelevamientoMensualerosForm, extra=1, can_delete=True)

    if request.method == 'POST':
        if  (request.POST.get('action') == 'add_det'):
            form = RelevamientoForm(request.POST, instance=relevamiento)
            relevamDetFormSet = relevamientoDetFormSet(request.POST, instance=relevamiento)
            relevamEspFormSet = relevamientoEspFormSet(request.POST, instance=relevamiento)
            relevamCuHrFormSet = relevamientoCupoHorasFormSet(request.POST, instance=relevamiento)
            relevamMenFormSet = relevamientoMensuFormSet(request.POST, instance=relevamiento)
        else:
            form = RelevamientoForm(request.POST, instance=relevamiento)
            relevamDetFormSet = relevamientoDetFormSet(request.POST, instance=relevamiento)
            relevamEspFormSet = relevamientoEspFormSet(request.POST, instance=relevamiento)
            relevamCuHrFormSet = relevamientoCupoHorasFormSet(request.POST, instance=relevamiento)
            relevamMenFormSet = relevamientoMensuFormSet(request.POST, instance=relevamiento)

            if form.is_valid() and relevamDetFormSet.is_valid() and relevamEspFormSet.is_valid() and relevamCuHrFormSet.is_valid() and relevamMenFormSet.is_valid():
                form.save()
                relevamDetFormSet.save()
                relevamEspFormSet.save()
                relevamCuHrFormSet.save()
                relevamMenFormSet.save()
                return redirect('Operarios:puntoServicio_list')
            else:
                messages.warning(request, 'No se pudo guardar los cambios')
    else:
        """
        Seteamos el punto de servicio
        """
        relevamiento.puntoServicio = puntoSer

        if primeraVez == 1:
            form = RelevamientoForm(instance=relevamiento, initial={'tipoSalario': 1})
        else:
            form = RelevamientoForm(instance=relevamiento)

        relevamDetFormSet =     relevamientoDetFormSet(instance=relevamiento)
        relevamEspFormSet =     relevamientoEspFormSet(instance=relevamiento)
        relevamCuHrFormSet =    relevamientoCupoHorasFormSet(instance=relevamiento)
        relevamMenFormSet =     relevamientoMensuFormSet(instance=relevamiento)

    contexto = {
            'title': 'Servicio Aprobado',
            'form': form,
            'relevamDetFormSet': relevamDetFormSet,
            'relevamEspFormSet': relevamEspFormSet,
            'relevamCuHrFormSet': relevamCuHrFormSet,
            'relevamMenFormSet': relevamMenFormSet,
        }
    #return render_to_response('puntoServicio/puntoServicio_relevamiento.html', locals())
    return render(request, 'puntoServicio/puntoServicio_relevamiento.html', context=contexto)

@login_required
@permission_required('Operarios.add_operario', raise_exception=True)
def Operarios_create(request):
    if request.method == 'POST': 
        form = OperarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Operario creado correctamente.')
        else:
            messages.warning(request, 'No se pudo cargar el Operario')
        return redirect('Operarios:operarios_list')
    else:
        form = OperarioForm()
        contexto = {
            'title': 'Nuevo Operario',
            'form': form
        }
    
    return render(request, 'operarios/operarios_form.html', context=contexto)

@login_required
@permission_required('Operarios.view_operario', raise_exception=True)
def Operarios_list(request):
    operarios = Operario.objects.all()
    contexto = {'Operarios': operarios}
    return render(request, 'operarios/operarios_list.html', context=contexto)

@login_required
@permission_required('Operarios.change_operario', raise_exception=True)
def Operarios_update(request, pk):
    operarios = Operario.objects.get(id=pk)
    if request.method == 'GET':
        form = OperarioForm(instance=operarios)
        contexto = {
            'title': 'Editar Operario',
            'form': form
        }
    else:
        form = OperarioForm(request.POST, instance=operarios)
        if form.is_valid():
            form.save()
            messages.success(request, 'Operario modificado correctamente.')
        return redirect('Operarios:operarios_list')

    return render(request, 'operarios/operarios_form.html', context=contexto)

@login_required
@permission_required('Operarios.delete_operario', raise_exception=True)
def Operarios_delete(request, pk):
    operarios = Operario.objects.get(id=pk)
    if request.method == 'POST':
        operarios.delete()
        messages.warning(request, 'Operario eliminado correctamente')
        return redirect('Operarios:operarios_list')
    return render(request, 'operarios/operarios_delete.html', {'operarios': operarios})


@login_required
@permission_required('Operarios.add_planificacioncab', raise_exception=True)
def Planificacion_create(request, id_puntoServicio=None):
    logging.getLogger("error_logger").error('Se ingreso en el metodo planificacion_create')
    ''' Obtenemos el punto de servicio, en caso de error se muesta un error 404 '''
    try:
        puntoSer = PuntoServicio.objects.get(pk=id_puntoServicio)
    except PuntoServicio.DoesNotExist as err:
        logging.getLogger("error_logger").error('Punto de Servicio no existe: {0}'.format(err))
        raise Http404("Punto de Servicio no existe")

    ''' Obtenemos el relevamiento para mostrar en la pantalla '''
    relevamiento = RelevamientoCab.objects.filter(puntoServicio_id = puntoSer.id).first()

    ''' Obtenemos la planificacion en caso de que exista una '''
    planificacion = PlanificacionCab.objects.filter(puntoServicio_id = puntoSer.id).first()

    initial = []
    CantlimpiezaProf = 1
    if planificacion == None:
        planificacion = PlanificacionCab()

        if relevamiento:
            for relevesp in relevamiento.relevamientoesp_set.all():
                initial.append({'tipo': relevesp.tipo, 
                                'frecuencia': relevesp.dia,
                                'dia': relevesp.dia,
                                'cantHoras': relevesp.cantHoras})
                # initial=[
                #         {'especialista': 2, 
                #         'tipo': 2,
                #         'frecuencia': 'ANUAL',
                #         'dia': 'SAB',
                #         'cantHoras': 99}
                #         ]
            CantlimpiezaProf = len(initial)

    planificacionOpeFormSet = inlineformset_factory(PlanificacionCab, PlanificacionOpe, form=PlanificacionOpeForm, extra=1, can_delete=True)
    planificacionEspFormSet = inlineformset_factory(PlanificacionCab, PlanificacionEsp, form=PlanificacionEspForm, extra=CantlimpiezaProf, can_delete=True)

    if request.method == 'POST':

        if  (request.POST.get('action') == 'add_det') or (request.POST.get('action') == 'add_esp'):
            form = PlanificacionForm(request.POST, instance=planificacion)
            planifOpeFormSet = planificacionOpeFormSet(request.POST, instance=planificacion)
            planifEspFormSet = planificacionEspFormSet(request.POST, instance=planificacion)
        else:
            form = PlanificacionForm(request.POST, instance=planificacion)
            planifOpeFormSet = planificacionOpeFormSet(request.POST, instance=planificacion)
            planifEspFormSet = planificacionEspFormSet(request.POST, instance=planificacion)

            if form.is_valid(relevamiento.cantidad, relevamiento.cantidadHrTotal, relevamiento.cantidadHrEsp) and planifOpeFormSet.is_valid() and planifEspFormSet.is_valid():
                form.save()
                planifOpeFormSet.save()
                planifEspFormSet.save()
                messages.success(request, 'Se guardo correctamente la planificación')
                return redirect('Operarios:planificar_list')
            else:
                messages.warning(request, 'No se pudo guardar los cambios')
    else:
        """
        Seteamos el punto de servicio
        """
        planificacion.puntoServicio = puntoSer

        form = PlanificacionForm(instance=planificacion)
        planifOpeFormSet = planificacionOpeFormSet(instance=planificacion)
        if len(initial) > 0:
            planifEspFormSet = planificacionEspFormSet(instance=planificacion, initial=initial)
        else:
            planifEspFormSet = planificacionEspFormSet(instance=planificacion)

    contexto = {
            'title': 'Nueva Planificación',
            'form': form,
            'planifOpeFormSet': planifOpeFormSet,
            'planifEspFormSet': planifEspFormSet,
            'relevamiento' : relevamiento,
        }

    return render(request, 'planificacion/planificacion_crear.html', context=contexto)

@login_required
@permission_required('Operarios.view_planificacioncab', raise_exception=True)
def Planificacion_list(request):
    if request.method == 'POST':
        pk_puntoServSeleccionado = request.POST.get('plani_puntoServ')
        return redirect('Operarios:planificar_create', id_puntoServicio=pk_puntoServSeleccionado)
    else:
        puntoServi = PuntoServicio.objects.all()
        contexto = {'PuntosServicio': puntoServi}
        return render(request, 'planificacion/planificacion_list.html', context=contexto)

@login_required
@permission_required('Operarios.view_operario', raise_exception=True)
def Jefes_list(request):
    jefes = User.objects.filter(cargoasignado__cargo__cargo='Jefe de Operaciones')
    contexto = {'Jefes': jefes}
    return render(request, 'jefes/jefes_list.html', context=contexto)

@login_required
@permission_required('Operarios.view_operario', raise_exception=True)
def Jefes_asig(request, id_user_jefe=None, id_user_fiscal=None):
    try:
        user_jefe = User.objects.get(pk=id_user_jefe)   
    except User.DoesNotExist as err:
        logging.getLogger("error_logger").error('Usuario de Jefe de Operaciones no existe: {0}'.format(err))

    if id_user_fiscal != None:
        user_fiscal = User.objects.get(pk=id_user_fiscal)
        asignacion = AsigJefeFiscal(userJefe=user_jefe, userFiscal=user_fiscal)
        asignacion.save()
        
    #Se traen todos los fiscales que estan asignados al jefe de operaciones en cuestion
    fiscales_asig = User.objects.filter(FiscalAsigJefeFiscal__userJefe=id_user_jefe)
    consulta = User.objects.filter(FiscalAsigJefeFiscal__userJefe=id_user_jefe).query
    logging.getLogger("error_logger").error('La consulta ejecutada es: {0}'.format(consulta))

    #se trae los fiscales disponibles
    fiscales_disp = User.objects.filter(FiscalAsigJefeFiscal__userJefe__isnull=True, cargoasignado__cargo__cargo='Fiscal')
    consulta2 = User.objects.filter(FiscalAsigJefeFiscal__userJefe__isnull=True, cargoasignado__cargo__cargo='Fiscal').query
    logging.getLogger("error_logger").error('La consulta de fiscales disponibles ejecutada es: {0}'.format(consulta2))

    #cargamos el contexto
    contexto = {'Fiscales': fiscales_asig,
                'Jefe': user_jefe,
                'Fiscales_disp': fiscales_disp
            }
    return render(request, 'jefes/jefes_asig.html', context=contexto)

@login_required
@permission_required('Operarios.delete_operario', raise_exception=True)
def Jefes_delete(request, id_user_jefe=None, id_user_fiscal=None):
    user_fiscal = User.objects.get(pk=id_user_fiscal)
    user_jefe = User.objects.get(pk=id_user_jefe)

    if request.method == 'POST':
        asignacion = AsigJefeFiscal.objects.get(userJefe=user_jefe, userFiscal=user_fiscal)
        asignacion.delete()
        messages.warning(request, 'Asignación eliminada correctamente')
        return redirect('Operarios:jefes_asig', id_user_jefe=id_user_jefe)
    
    #cargamos el contexto
    contexto = {'Jefe': user_jefe,
                'Fiscal': user_fiscal
                }
    return render(request, 'jefes/jefes_delete.html', context=contexto)

@login_required
@permission_required('Operarios.view_operario', raise_exception=True)
def Fiscales_asig(request, id_user_fiscal=None, id_puntoServicio=None):
    try:
        user_fiscal = User.objects.get(pk=id_user_fiscal)   
    except User.DoesNotExist as err:
        logging.getLogger("error_logger").error('Usuario de Fiscal no existe: {0}'.format(err))

    if id_puntoServicio != None:
        puntoServicio = PuntoServicio.objects.get(pk=id_puntoServicio)
        asignacion = AsigFiscalPuntoServicio(userFiscal=user_fiscal, puntoServicio=puntoServicio)
        asignacion.save()
        
    #Se traen todos los puntos de servicio que estan asignados al fiscal en cuestion
    puntosServ_asig = PuntoServicio.objects.filter(puntoServicioAsigFiscalPuntoServicio__userFiscal=id_user_fiscal)
    consulta = PuntoServicio.objects.filter(puntoServicioAsigFiscalPuntoServicio__userFiscal=id_user_fiscal).query
    logging.getLogger("error_logger").error('La consulta ejecutada es: {0}'.format(consulta))

    #se trae los puntos de servicio disponibles
    puntosServ_disp = PuntoServicio.objects.filter(puntoServicioAsigFiscalPuntoServicio__userFiscal__isnull=True)
    consulta2 = PuntoServicio.objects.filter(puntoServicioAsigFiscalPuntoServicio__userFiscal__isnull=True).query
    logging.getLogger("error_logger").error('La consulta de puntos de servicio disponibles ejecutada es: {0}'.format(consulta2))

    #cargamos el contexto
    contexto = {'PuntosSer': puntosServ_asig,
                'Fiscal': user_fiscal,
                'PuntosSer_disp': puntosServ_disp
            }
    return render(request, 'fiscales/fiscales_asig.html', context=contexto)

@login_required
@permission_required('Operarios.delete_operario', raise_exception=True)
def Fiscales_delete(request, id_user_fiscal=None, id_puntoServicio=None):
    user_fiscal = User.objects.get(pk=id_user_fiscal) 
    puntoServicio = PuntoServicio.objects.get(pk=id_puntoServicio)

    if request.method == 'POST':
        asignacion = AsigFiscalPuntoServicio.objects.get(userFiscal=user_fiscal, puntoServicio=puntoServicio)
        asignacion.delete()
        messages.warning(request, 'Asignación eliminada correctamente')
        return redirect('Operarios:fiscales_asig', id_user_fiscal=id_user_fiscal)
    
    #cargamos el contexto
    contexto = {'Fiscal': user_fiscal,
                'PuntoServicio': puntoServicio,
                }
    return render(request, 'fiscales/fiscales_delete.html', context=contexto)

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

    if asignacion == None:
        asignacion = AsignacionCab()

    asignacionDetFormSet = inlineformset_factory(AsignacionCab, AsignacionDet, form=AsignacionDetForm, extra=1, can_delete=True)

    if request.method == 'POST':

        if  (request.POST.get('action') == 'add_det'):
            form = AsignacionCabForm(request.POST, instance=asignacion)
            AsigDetFormSet = asignacionDetFormSet(request.POST, instance=asignacion)
        else:
            form = AsignacionCabForm(request.POST, instance=asignacion)
            AsigDetFormSet = asignacionDetFormSet(request.POST, instance=asignacion)

            if form.is_valid() and AsigDetFormSet.is_valid():
                form.save()
                AsigDetFormSet.save()
                messages.success(request, 'Se guardo correctamente la asignacion')
                return redirect('Operarios:asignacion_list')
            else:
                messages.warning(request, 'No se pudo guardar los cambios')
    else:
        """
        Seteamos el punto de servicio
        """
        asignacion.puntoServicio = puntoSer

        form = AsignacionCabForm(instance=asignacion)
        AsigDetFormSet = asignacionDetFormSet(instance=asignacion)

    contexto = {
            'title': 'Nueva Asignación',
            'pservicio': puntoSer,
            'form': form,
            'asigDetFormSet': AsigDetFormSet,
            'relevamiento' : relevamiento,
            'sem_diurno' : sem_diurno,
            'sem_nocturno' : sem_nocturno,
            'dom_diurno' : dom_diurno,
            'dom_nocturno' : dom_nocturno,
        }

    return render(request, 'asignacion/asignacion_crear.html', context=contexto)