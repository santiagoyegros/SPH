import logging
from django.shortcuts import render, redirect, render_to_response
from django.core import serializers
from datetime import datetime
from django.http import HttpResponse, Http404
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from django.forms.models import inlineformset_factory
from django.template import RequestContext
from django_tables2.views import SingleTableMixin
from django_tables2.export.views import ExportMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from openpyxl import Workbook
from Operarios.models import Ciudad, Cliente, Nacionalidad
from django_tables2.paginators import Paginator
from Operarios.models import PuntoServicio, Operario, RelevamientoCab, RelevamientoDet, RelevamientoEsp, RelevamientoCupoHoras, RelevamientoMensualeros, PlanificacionCab, PlanificacionOpe, PlanificacionEsp, Cargo, CargoAsignado, AsigFiscalPuntoServicio, AsigJefeFiscal, AsignacionCab, AsignacionDet,EsmeEmMarcaciones, Feriados
from Operarios.tables import MarcacionTable

from Operarios.forms import PuntoServicioForm, OperarioForm, RelevamientoForm, RelevamientoDetForm, RelevamientoEspForm, RelevamientoCupoHorasForm, RelevamientoMensualerosForm, PlanificacionForm, PlanificacionOpeForm, PlanificacionEspForm, AsignacionCabForm, AsignacionDetForm
from Operarios.filters import MarcacionFilter
import json

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
    ciudades = Ciudad.objects.all()
    clientes = Cliente.objects.all()
    form_class = PuntoServicioForm
    template_name = "puntoServicio/puntoServicio_form.html"
    success_url = reverse_lazy('Operarios:puntoServicio_list')
    success_message = 'Punto de Servicio Creado correctamente'
    extra_context = {'title': 'Nuevo Punto de Servicio','ciudades':ciudades,'clientes':clientes}

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('Operarios.change_puntoservicio', raise_exception=True), name='dispatch')
class PuntoServicioUpdateView(SuccessMessageMixin, UpdateView):
    model = PuntoServicio
    form_class = PuntoServicioForm
    template_name = "puntoServicio/puntoServicio_form.html"
    success_url = reverse_lazy('Operarios:puntoServicio_list')
    success_message = 'Punto de Servicio modificado correctamente'
    extra_context = {'title': 'Editar Punto de Servicio '}


@login_required
@permission_required('Operarios.change_puntoservicio', raise_exception=True)
def PuntosServicios_update(request, pk):
    puntoServicio = PuntoServicio.objects.get(id=pk)
  
    if request.method == 'GET':
        form = PuntoServicioForm(instance=puntoServicio)
        contexto = {
            'title': 'Editar Punto de servicio',
            'form': form,
            'puntoServicio':puntoServicio 
        }
    else:
        form = PuntoServicioForm(request.POST, instance=puntoServicio)
        if form.is_valid():
            form.save()
            messages.success(request, 'Punto de Servicio modificado correctamente.')
        return redirect('Operarios:puntoServicio_list')

    return render(request, 'operarios/puntoServicio_list.html', context=contexto)

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

       
    relevamientoDetFormSet =        inlineformset_factory(RelevamientoCab, RelevamientoDet, form=RelevamientoDetForm, extra=1, can_delete=True)
    relevamientoEspFormSet =        inlineformset_factory(RelevamientoCab, RelevamientoEsp, form=RelevamientoEspForm, extra=1, can_delete=True)
    relevamientoCupoHorasFormSet =  inlineformset_factory(RelevamientoCab, RelevamientoCupoHoras, form=RelevamientoCupoHorasForm, extra=1, can_delete=True)
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
    ciudades = Ciudad.objects.all()
    nacionalidades = Nacionalidad.objects.all()
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
            'form': form,
            'ciudades':ciudades,
            'nacionalidades':nacionalidades
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
    operario = Operario.objects.get(id=pk)
    print(operario.FechaNacimiento)
    FechaNacimiento = operario.FechaNacimiento.strftime("%d/%m/%Y")
    FechaInicio = operario.FechaInicio.strftime("%d/%m/%Y")
    ciudades = Ciudad.objects.all()
    nacionalidades = Nacionalidad.objects.all()
    if request.method == 'GET':
        form = OperarioForm(instance=operario)
        contexto = {
            'title': 'Editar Operario',
            'form': form,
            'operario':operario ,
            'ciudades':ciudades,
            'FechaNacimiento':FechaNacimiento,
            'FechaInicio':FechaInicio,
            'nacionalidades':nacionalidades
        }
    else:
        form = OperarioForm(request.POST, instance=operario)
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

class MarcacionListView(ExportMixin,SingleTableMixin,FilterView):
    table_class= MarcacionTable
    model= EsmeEmMarcaciones
    template_name='marcacion/marcacion_list.html'
    filterset_class= MarcacionFilter
    table_pagination={"per_page":10}



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
                                'frecuencia': relevesp.frecuencia,
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
def Fiscales_list(request):
    fiscales = User.objects.filter(cargoasignado__cargo__cargo='Fiscal')
    contexto = {'Fiscales':fiscales} 
    return render(request, 'fiscales/fiscales_list.html', context=contexto) 

@login_required
@permission_required('Operarios.view_operario', raise_exception=True)
def Jefes_asig(request, id_user_jefe=None, id_user_fiscal=None): 

    try:
        user_jefe = User.objects.get(pk=id_user_jefe)   
    except User.DoesNotExist as err:
        logging.getLogger("error_logger").error('Usuario de Jefe de Operaciones no existe: {0}'.format(err))


    #Se traen todos los fiscales que estan asignados al jefe de operaciones en cuestion
    fiscales_asig = User.objects.filter(FiscalAsigJefeFiscal__userJefe=id_user_jefe)
    consulta = User.objects.filter(FiscalAsigJefeFiscal__userJefe=id_user_jefe).query
    logging.getLogger("error_logger").error('La consulta ejecutada es: {0}'.format(consulta))

    ''' El if siguiente es utilizado en la version anterior de asignacion de fiscales'''   
    # if id_user_fiscal != None:
    #     print("Hola, aca obtengo los fiscales")
    #     user_fiscal = User.objects.get(pk=id_user_fiscal)
    #     asignacion = AsigJefeFiscal(userJefe=user_jefe, userFiscal=user_fiscal)
    #     asignacion.save()
    
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

@permission_required('Operarios.view_operario', raise_exception=True)
def asignarFiscales(request,id_user_jefe=None ):

    try:
        user_jefe = User.objects.get(pk=id_user_jefe)   
    except User.DoesNotExist as err:
        logging.getLogger("error_logger").error('Usuario de Jefe de Operaciones no existe: {0}'.format(err))

    #Se traen todos los fiscales que estan asignados al jefe de operaciones en cuestion
    fiscales_asig = User.objects.filter(FiscalAsigJefeFiscal__userJefe=id_user_jefe)
    consulta = User.objects.filter(FiscalAsigJefeFiscal__userJefe=id_user_jefe).query
    logging.getLogger("error_logger").error('La consulta ejecutada es: {0}'.format(consulta))
    
    '''Se obtienen todos los ids seleccionados'''
    if request.method == 'POST':
        if request.POST.getlist('fiscales_disp') != None:
            print(request.POST.getlist('fiscales_disp')) 
            for fisAsig in fiscales_asig:
                asignacion = AsigJefeFiscal.objects.get(userJefe=user_jefe, userFiscal=fisAsig)
                asignacion.delete()

            for fd_id in request.POST.getlist('fiscales_disp'):
                user_fiscal = User.objects.get(pk=fd_id)
                asignacion = AsigJefeFiscal(userJefe=user_jefe, userFiscal=user_fiscal)
                asignacion.save() 

    return redirect('Operarios:jefes_asigFiscales', id_user_jefe=id_user_jefe)

@login_required
@permission_required('Operarios.delete_operario', raise_exception=True)
def Jefes_delete(request, id_user_jefe=None, id_user_fiscal=None):
    user_fiscal = User.objects.get(pk=id_user_fiscal)
    user_jefe = User.objects.get(pk=id_user_jefe)

    if request.method == 'POST':
        asignacion = AsigJefeFiscal.objects.get(userJefe=user_jefe, userFiscal=user_fiscal)
        asignacion.delete()
        messages.warning(request, 'Asignación eliminada correctamente')
        return redirect('Operarios:jefes_asigFiscales', id_user_jefe=id_user_jefe)
    
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
    print("Asignados",puntosServ_asig)
   
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


@permission_required('Operarios.view_operario', raise_exception=True)
def asignarPuntosServicio(request,id_user_fiscal=None):

    try:
        user_fiscal = User.objects.get(pk=id_user_fiscal)   
    except User.DoesNotExist as err:
        logging.getLogger("error_logger").error('Usuario de Fiscal no existe: {0}'.format(err))

    #Se traen todos los puntos de servicio que estan asignados al fiscal en cuestion
    puntosServ_asig = PuntoServicio.objects.filter(puntoServicioAsigFiscalPuntoServicio__userFiscal=id_user_fiscal)
    consulta = PuntoServicio.objects.filter(puntoServicioAsigFiscalPuntoServicio__userFiscal=id_user_fiscal).query
    logging.getLogger("error_logger").error('La consulta ejecutada es: {0}'.format(consulta))
    
    '''Se obtienen todos los ids seleccionados'''
    if request.method == 'POST':
        print("HOOOOOOLA",request.POST.getlist('puntos_disp'),puntosServ_asig)
        if request.POST.getlist('puntos_disp') != None:
            for PSAsig in puntosServ_asig:
                print("Punto de servicio",PSAsig)
                asignacion = AsigFiscalPuntoServicio.objects.get(userFiscal=user_fiscal, puntoServicio=PSAsig)
                print("BORRADO")
                asignacion.delete()

            for PS_id in request.POST.getlist('puntos_disp'):
                nuevoPunto = PuntoServicio.objects.get(pk=PS_id)
                print(nuevoPunto)
                asignacion = AsigFiscalPuntoServicio(userFiscal=user_fiscal, puntoServicio=nuevoPunto)
                asignacion.save() 

    return redirect('Operarios:fiscales_asig', id_user_fiscal=id_user_fiscal)

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

def obtenerMarcacion(request):
    return render(request, 'marcacion/marcacion_list.html');

def obtenerFeriado(request):
    return render(request, 'feriados/feriados_list.html');

def getMarcaciones(request):
        marcacion = EsmeEmMarcaciones.objects.all();
        if request.GET.get('codoperacion')  is not None and request.GET.get('codoperacion')!='':
            marcacion=marcacion.filter(codoperacion__contains = request.GET.get('codoperacion'));
        if request.GET.get('codpersona')  is not None and request.GET.get('codpersona')!='':
            marcacion=marcacion.filter(codpersona=request.GET.get('codpersona'));
        if request.GET.get('codcategoria')  is not None  and request.GET.get('codcategoria')!='':
            marcacion=marcacion.filter(codcategoria=request.GET.get('codcategoria'));
        if request.GET.get('numlinea')  is not None  and request.GET.get('numlinea')!='':
            marcacion=marcacion.filter(numlinea__contains = request.GET.get('numlinea'));
        if request.GET.get('codubicacion')  is not None and request.GET.get('codubicacion')!='':
            marcacion=marcacion.filter(codubicacion__contains = request.GET.get('codubicacion'));
        if request.GET.get('fecha')  is not None and request.GET.get('fecha')!='':
            dtd=datetime.strptime(request.GET.get('fecha'),'%Y-%m-%dT%H:%M:%S.%fZ');
            dtd=dtd.replace(hour=0,minute=0,second=0,microsecond=0);
            marcacion=marcacion.filter(fecha__gte=dtd);
            dtd=dtd.replace(hour=23,minute=59,second=59);
            marcacion=marcacion.filter(fecha__lte=dtd);
        if request.GET.get('estado') is not None and request.GET.get('estado')!='':
            marcacion=marcacion.filter(estado__contains = request.GET.get('estado'));
        return HttpResponse(serializers.serialize('json', marcacion), content_type = 'application/json', status = 200);


def descargarMarcaciones(request):
        marcacion = EsmeEmMarcaciones.objects.all();
        if request.GET.get('codoperacion')  is not None and request.GET.get('codoperacion')!='':
            marcacion=marcacion.filter(codoperacion__contains = request.GET.get('codoperacion'));
        if request.GET.get('codpersona')  is not None and request.GET.get('codpersona')!='':
            marcacion=marcacion.filter(codpersona=request.GET.get('codpersona'));
        if request.GET.get('codcategoria')  is not None  and request.GET.get('codcategoria')!='':
            marcacion=marcacion.filter(codcategoria=request.GET.get('codcategoria'));
        if request.GET.get('numlinea')  is not None  and request.GET.get('numlinea')!='':
            marcacion=marcacion.filter(numlinea__contains = request.GET.get('numlinea'));
        if request.GET.get('codubicacion')  is not None and request.GET.get('codubicacion')!='':
            marcacion=marcacion.filter(codubicacion__contains = request.GET.get('codubicacion'));
        if request.GET.get('fecha')  is not None and request.GET.get('fecha')!='':
            dtd=datetime.strptime(request.GET.get('fecha'),'%Y-%m-%dT%H:%M:%S.%fZ');
            dtd=dtd.replace(hour=0,minute=0,second=0,microsecond=0);
            marcacion=marcacion.filter(fecha__gte=dtd);
            dtd=dtd.replace(hour=23,minute=59,second=59);
            marcacion=marcacion.filter(fecha__lte=dtd);
        if request.GET.get('estado') is not None and request.GET.get('estado')!='':
            marcacion=marcacion.filter(estado__contains = request.GET.get('estado'));

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        response['Content-Disposition'] = 'attachment; filename={date}-marcaciones.xlsx'.format(
            date=datetime.now().strftime('%Y-%m-%d'),
        )
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = 'Marcaciones'
        # Define the titles for columns
        columns = [
            'Operacion',
            'Cedula',
            'Codigo Categoria',
            'Numero de Linea',
            'Ubicacion',
            'Fecha',
            'Estado',
        ]
        row_num = 1

        # Assign the titles for each cell of the header
        for col_num, column_title in enumerate(columns, 1):
            cell = worksheet.cell(row=row_num, column=col_num)
            cell.value = column_title

        # Iterate through all movies
        for marc in marcacion:
            row_num += 1
            
            # Define the data for each cell in the row 
            row = [
                marc.codoperacion,
                marc.codpersona,
                marc.codcategoria,
                marc.numlinea,
                marc.codubicacion,
                marc.fecha,
                marc.estado
            ]
            
            # Assign the data for each cell of the row 
            for col_num, cell_value in enumerate(row, 1):
                cell = worksheet.cell(row=row_num, column=col_num)
                cell.value = cell_value

        workbook.save(response)
        return response;



def getFeriados(request):
        feriados = Feriados.objects.all();
        if request.GET.get('anho')  is not None  and request.GET.get('anho')!='':
            feriados=feriados.filter(anho = request.GET.get('anho'));
        if request.GET.get('descripcion')  is not None and request.GET.get('descripcion')!='':
            feriados=feriados.filter(descripcion__contains = request.GET.get('descripcion'));
        if request.GET.get('fecha')  is not None and request.GET.get('fecha')!='':
            dtd=datetime.strptime(request.GET.get('fecha'),'%Y-%m-%dT%H:%M:%S.%fZ');
            dtd=dtd.replace(hour=0,minute=0,second=0,microsecond=0);
            feriados=feriados.filter(fecha__gte=dtd);
            dtd=dtd.replace(hour=23,minute=59,second=59);
            feriados=feriados.filter(fecha__lte=dtd);
        return HttpResponse(serializers.serialize('json', feriados), content_type = 'application/json', status = 200);
def makeFeriados(request):
        Feriados.objects.create(
            anho= request.POST.get("anho"),
            fecha=datetime.strptime(request.POST.get('fecha'),'%Y-%m-%dT%H:%M:%S.%fZ'),
            descripcion= request.POST.get("descripcion"))
        return HttpResponse(status = 201)
def editFeriados(request,feriado_id):
        feriado=Feriados.objects.get(id = feriado_id);
        if request.POST.get('anho') is not None:
            feriado.anho=request.POST.get('anho');
        if request.POST.get('descripcion') is not None:
            feriado.descripcion=request.POST.get('descripcion');
        if request.POST.get('fecha') is not None:
            feriado.fecha=datetime.strptime(request.POST.get('fecha'),'%Y-%m-%dT%H:%M:%S.%fZ');
        feriado.save();
        return HttpResponse(status = 201)
def deleteFeriados(request,feriado_id):
        feriado=Feriados.objects.get(id = feriado_id);
        feriado.delete();
        return HttpResponse(status = 201)


class EsmeEmMarcacionesClass(ListView):

    def index(request):
        return render(request, 'marcacion/marcacion_list.html');

    

    def post(self, request):
        EsmeEmMarcaciones.objects.create(
            codoperacion= request.POST.get("codoperacion"),
            codpersona= request.POST.get("codpersona"),
            codcategoria= request.POST.get("codcategoria"),
            numlinea= request.POST.get("numlinea"),
            codubicacion= request.POST.get("codubicacion"),
            fecha= request.POST.get("fecha"),
            estado= request.POST.get("estado")

        )
        return HttpResponse(status = 201)

    def put(self, request, marcacion_id):
        marcacion = EsmeEmMarcaciones.objects.get(idpersonaevento = marcacion_id)
        marcacion.codoperacion= request.PUT.get("codoperacion"),
        marcacion.codpersona= request.PUT.get("codpersona"),
        marcacion.codcategoria= request.PUT.get("codcategoria"),
        marcacion.numlinea= request.PUT.get("numlinea"),
        marcacion.codubicacion= request.PUT.get("codubicacion"),
        marcacion.fecha= request.PUT.get("fecha"),
        marcacion.estado= request.PUT.get("estado")
        marcacion.save()
        return HttpResponse(status = 200)

    def delete(self, request, marcacion_id):
        marcacion = EsmeEmMarcaciones.objects.get(idpersonaevento = marcacion_id)
        marcacion.delete()
        return HttpResponse(status = 200)

    def to_json(self, objects):
        return serializers.serialize('json', objects)