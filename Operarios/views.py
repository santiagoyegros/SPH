from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, Http404
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.forms.models import inlineformset_factory
from django.template import RequestContext

from Operarios.models import PuntoServicio, Operario, RelevamientoCab, RelevamientoDet, RelevamientoEsp, PlanificacionCab, PlanificacionDet, PlanificacionEsp
from Operarios.forms import PuntoServicioForm, OperarioForm, RelevamientoForm, RelevamientoDetForm, RelevamientoEspForm



def index(request):
    return HttpResponse("Vista de Operarios")

def index_alert(request):
    messages.debug(request, ' SQL statements were executed.')
    messages.info(request, 'Mensaje Informativo.')
    messages.success(request, 'Mensaje de Exito')
    messages.warning(request, 'Mensaje de Error.')
    messages.error(request, 'Document deleted.')
    return render(request, 'base.html')

class PuntosServicioList(ListView):
    model = PuntoServicio
    template_name = "puntoServicio/puntoServicio_list.html"

class PuntoServicioCreate(SuccessMessageMixin, CreateView):
    model = PuntoServicio
    form_class = PuntoServicioForm
    template_name = "puntoServicio/puntoServicio_form.html"
    success_url = reverse_lazy('Operarios:puntoServicio_list')
    success_message = 'Punto de Servicio Creado correctamente'
    extra_context = {'title': 'Nuevo Punto de Servicio'}

class PuntoServicioUpdateView(SuccessMessageMixin, UpdateView):
    model = PuntoServicio
    form_class = PuntoServicioForm
    template_name = "puntoServicio/puntoServicio_form.html"
    success_url = reverse_lazy('Operarios:puntoServicio_list')
    success_message = 'Punto de Servicio modificado correctamente'
    extra_context = {'title': 'Editar Punto de Servicio '}

class PuntoServicioDeleteView(SuccessMessageMixin, DeleteView):
    model = PuntoServicio
    template_name = "puntoServicio/puntoServicio_delete.html"
    success_url = reverse_lazy('Operarios:puntoServicio_list')
    success_message = 'Punto de Servicio eliminado correctamente'

    def delete(self, request, *args, **kwargs):
        messages.warning(self.request, self.success_message)
        return super(PuntoServicioDeleteView, self).delete(request, *args, **kwargs)

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

def Operarios_list(request):
    operarios = Operario.objects.all()
    contexto = {'Operarios': operarios}
    return render(request, 'operarios/operarios_list.html', context=contexto)

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
def Operarios_delete(request, pk):
    operarios = Operario.objects.get(id=pk)
    if request.method == 'POST':
        operarios.delete()
        messages.warning(request, 'Operario eliminado correctamente')
        return redirect('Operarios:operarios_list')
    return render(request, 'operarios/operarios_delete.html', {'operarios': operarios})


def Planificacion_create(request, id_puntoServicio=None):
    """
        Obtenemos el punto de servicio, en caso de error se muesta un error 404
    """
    try:
        puntoSer = PuntoServicio.objects.get(pk=id_puntoServicio)
    except PuntoServicio.DoesNotExist:
        raise Http404("Punto de Servicio no existe")

    planificacion = PlanificacionCab.objects.filter(puntoServicio_id = puntoSer.id).first()

    if planificacion == None:
        planificacion = PlanificacionCab()

    return render(request, 'planificacion/planificacion_list.html', context=contexto)