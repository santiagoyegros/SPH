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

from Operarios.models import PuntoServicio, Operario, RelevamientoCab, RelevamientoDet, RelevamientoEsp, PlanificacionCab, PlanificacionDet, PlanificacionEsp
from Operarios.forms import PuntoServicioForm, OperarioForm, RelevamientoForm, RelevamientoDetForm, RelevamientoEspForm, PlanificacionForm, PlanificacionDetForm, PlanificacionEspForm

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
    model = PuntoServicio
    template_name = "puntoServicio/puntoServicio_list.html"

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
    try:
        """
        Obtenemos el punto de servicio
        """
        puntoSer = PuntoServicio.objects.get(pk=id_puntoServicio)
    except PuntoServicio.DoesNotExist:
        raise Http404("Punto de Servicio no existe")

    relevamiento = RelevamientoCab.objects.filter(puntoServicio_id = puntoSer.id).first()

    if relevamiento == None:
        relevamiento = RelevamientoCab()

       
    relevamientoDetFormSet = inlineformset_factory(RelevamientoCab, RelevamientoDet, form=RelevamientoDetForm, extra=1, can_delete=True)
    relevamientoEspFormSet = inlineformset_factory(RelevamientoCab, RelevamientoEsp, form=RelevamientoEspForm, extra=1, can_delete=True)

    if request.method == 'POST':
        form = RelevamientoForm(request.POST, instance=relevamiento)
        relevamDetFormSet = relevamientoDetFormSet(request.POST, instance=relevamiento)
        relevamEspFormSet = relevamientoEspFormSet(request.POST, instance=relevamiento)

        if form.is_valid() and relevamDetFormSet.is_valid() and relevamEspFormSet.is_valid():
            form.save()
            relevamDetFormSet.save()
            relevamEspFormSet.save()
            return redirect('Operarios:puntoServicio_list')
        else:
            messages.warning(request, 'No se pudo guardar los cambios')
    else:
        """
        Seteamos el punto de servicio
        """
        relevamiento.puntoServicio = puntoSer

        form = RelevamientoForm(instance=relevamiento)
        relevamDetFormSet = relevamientoDetFormSet(instance=relevamiento)
        relevamEspFormSet = relevamientoEspFormSet(instance=relevamiento)

    contexto = {
            'title': 'Nuevo Relevamiento',
            'form': form,
            'relevamDetFormSet': relevamDetFormSet,
            'relevamEspFormSet': relevamEspFormSet,
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

    if planificacion == None:
        planificacion = PlanificacionCab()

    planificacionDetFormSet = inlineformset_factory(PlanificacionCab, PlanificacionDet, form=PlanificacionDetForm, extra=1, can_delete=True)
    planificacionEspFormSet = inlineformset_factory(PlanificacionCab, PlanificacionEsp, form=PlanificacionEspForm, extra=1, can_delete=True)

    if request.method == 'POST':
        form = PlanificacionForm(request.POST, instance=planificacion)
        planifDetFormSet = planificacionDetFormSet(request.POST, instance=planificacion)
        planifEspFormSet = planificacionEspFormSet(request.POST, instance=planificacion)

        if form.is_valid(relevamiento.cantidad, relevamiento.cantidadHrTotal, relevamiento.cantidadHrEsp) and planifDetFormSet.is_valid() and planifEspFormSet.is_valid():
            form.save()
            planifDetFormSet.save()
            planifEspFormSet.save()
            messages.success(request, 'Se guardo correctamente la planificación')
            return redirect('Operarios:planificar_list')
        #else:
            #messages.warning(request, 'No se pudo guardar los cambios')
    else:
        """
        Seteamos el punto de servicio
        """
        planificacion.puntoServicio = puntoSer

        form = PlanificacionForm(instance=planificacion)
        planifDetFormSet = planificacionDetFormSet(instance=planificacion)
        planifEspFormSet = planificacionEspFormSet(instance=planificacion)

    contexto = {
            'title': 'Nueva Planificación',
            'form': form,
            'planifDetFormSet': planifDetFormSet,
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