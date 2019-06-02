from django.urls import path

from . import views
from django.views.generic import TemplateView, RedirectView
from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from Operarios.views import Relevamiento, Operarios_list, Operarios_create, Operarios_update, Operarios_delete
from Operarios.views import PuntosServicioList, PuntoServicioCreate, PuntoServicioUpdateView, PuntoServicioDeleteView,EsmeEmMarcacionesClass
from Operarios.views import Planificacion_list, Planificacion_create, Jefes_list,Fiscales_list, Jefes_asig, Jefes_delete, asignarFiscales, asignarPuntosServicio
from Operarios.views import Fiscales_asig, Fiscales_delete
from Operarios.views import obtenerMarcacion,getMarcaciones,obtenerFeriado,getFeriados,makeFeriados,editFeriados,deleteFeriados,descargarMarcaciones
from Operarios import viewsAsignacion 
from Operarios import viewsOperario
from Operarios.views import PuntosServicios_update
from Operarios.viewsAsignacion import AsignacionListView,cargarOperarios
app_name = 'Operarios'

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^bootstrap/$', TemplateView.as_view(template_name='bootstrap/example.html')),
    url(r'^test/', views.index_alert, name='index_alert'),
    url(r'^operaciones/puntoServicio/listar/', PuntosServicioList.as_view(), name='puntoServicio_list'),
    url(r'^operaciones/puntoServicio/nuevo/', PuntoServicioCreate.as_view(), name='puntoServicio_create'),
    url(r'^operaciones/puntoServicio/editar/(?P<pk>\d+)/$', PuntosServicios_update, name='puntoServicio_update'),
    url(r'^operaciones/puntoServicio/eliminar/(?P<pk>\d+)/$', PuntoServicioDeleteView.as_view(), name='puntoServicio_delete'),
    url(r'^puntoServicio/relevamiento/(?P<id_puntoServicio>\d+)/$', Relevamiento, name='relevamiento'),
    url(r'^puntoServicio/relevamiento/$', Relevamiento, name='relevamiento_nuevo'),
    url(r'^operaciones/operarios/listar/', viewsOperario.Operarios_list , name='operarios_list'),
    url(r'^operaciones/operarios/nuevo/', viewsOperario.Operarios_create, name='operarios_create'),
    url(r'^operaciones/operarios/editar/(?P<pk>\d+)/$', viewsOperario.Operarios_update, name='operarios_update'),
    url(r'^operaciones/operarios/eliminar/(?P<pk>\d+)/$', viewsOperario.Operarios_delete, name='operarios_delete'),
    url(r'^planificacion/listar/', Planificacion_list, name='planificar_list'),
    url(r'^planificacion/planificar/(?P<id_puntoServicio>\d+)/$', Planificacion_create, name='planificar_create'),
    url(r'^operaciones/jefes/listar/', Jefes_list, name='jefes_list'),
    url(r'^operaciones/fiscales/listar/', Fiscales_list, name='fiscales_list'),
    url(r'^operaciones/jefes/asignar/(?P<id_user_jefe>\d+)/$', Jefes_asig, name='jefes_asig'),
    url(r'^jefes/asig/(?P<id_user_jefe>\d+)/(?P<id_user_fiscal>\d+)/$', Jefes_asig, name='jefes_asig'),
    url(r'^jefes/asigFiscales/(?P<id_user_jefe>\d+)/$', Jefes_asig, name='jefes_asigFiscales'),
    url(r'^jefes/asignarfiscales/(?P<id_user_jefe>\d+)/$', asignarFiscales, name='jefes_fiscales'),
    url(r'^jefes/eliminar/(?P<id_user_jefe>\d+)/(?P<id_user_fiscal>\d+)/$', Jefes_delete, name='jefes_del'),
    url(r'^operaciones/fiscales/asignar/(?P<id_user_fiscal>\d+)/$', Fiscales_asig, name='fiscales_asig'),
    url(r'^fiscales/asig/(?P<id_user_fiscal>\d+)/(?P<id_puntoServicio>\d+)/$', Fiscales_asig, name='fiscales_asig'),
    url(r'^fiscales/asignarPuntos/(?P<id_user_fiscal>\d+)/$', asignarPuntosServicio, name='fiscales_puntos'),
    url(r'^fiscales/eliminar/(?P<id_user_fiscal>\d+)/(?P<id_puntoServicio>\d+)/$', Fiscales_delete, name='fiscales_del'),
    url(r'^asignacion/listar/', viewsAsignacion.Asignacion_list, name='asignacion_list'),
    url(r'^asignacion/asignar/(?P<id_puntoServicio>\d+)/$', viewsAsignacion.Asignacion_create, name='asignacion_create'),
    url(r'^marcacion/vista', obtenerMarcacion , name='marcaciones_url'),
    url(r'^marcacion/listar/', getMarcaciones , name='marcaciones_get'),
    url(r'^asignacion/operarios'+
   '/(?P<totalHoras>\d+)/(?P<puntoServicio>\d+)/(?P<lunEntReq>\d+)/(?P<lunSalReq>\d+)/'+
   '(?P<marEntReq>\d+)/(?P<marSalReq>\d+)/(?P<mierEntReq>\d+)/(?P<mierSalReq>\d+)/(?P<juevEntReq>\d+)'+
   '/(?P<juevSalReq>\d+)/(?P<vieEntReq>\d+)/(?P<vieSlReq>\d+)/(?P<sabEntReq>\d+)/(?P<sabSalReq>\d+)/'+
   '(?P<domEntReq>\d+)/(?P<domSalReq>\d+)/(?P<fechaInicioOp>\d+)/$', 
    cargarOperarios , name='filter_operarios'),
    url(r'^marcacion/descargar', descargarMarcaciones , name='marcaciones_xls'),

    url(r'^feriados/vista', obtenerFeriado , name='feriados_url'),
    url(r'^feriados/listar', getFeriados , name='feriados_get'),
    url(r'^feriados/crear', makeFeriados , name='feriados_post'),
    url(r'^feriados/editar/(?P<feriado_id>\d+)', editFeriados , name='feriados_put'),
    url(r'^feriados/eliminar/(?P<feriado_id>\d+)', deleteFeriados , name='feriados_delete'),
    url(r'^operaciones/operarios/vista/', viewsOperario.getOperariosVista , name='operarios_vista'),
]   