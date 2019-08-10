from django.urls import path

from . import views
from django.views.generic import TemplateView, RedirectView
from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from Operarios.views import Relevamiento, Operarios_list, Operarios_create, Operarios_update, Operarios_delete
from Operarios.views import PuntosServicioList,PuntosServicioAprobados, PuntoServicioCreate, PuntoServicioUpdateView, PuntoServicioDeleteView,EsmeEmMarcacionesClass
from Operarios.views import Planificacion_list,getPuntosServicios, Planificacion_create, Jefes_list,JefesAsignar_list,Fiscales_list, Jefes_asig, Jefes_delete, asignarFiscales, asignarPuntosServicio
from Operarios.views import Fiscales_asig, Fiscales_delete, FiscalAsignar_list
from Operarios.views import obtenerMarcacion,getMarcaciones,obtenerFeriado,getFeriados,makeFeriados,editFeriados,deleteFeriados,descargarMarcaciones
from Operarios import viewsAsignacion 
from Operarios import viewsOperario, viewsAlerta
from Operarios.views import PuntosServicios_update
from Operarios.views import getClientes
from Operarios.viewsAsignacion import cargarOperarios
app_name = 'Operarios'

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^bootstrap/$', TemplateView.as_view(template_name='bootstrap/example.html')),
    url(r'^test/', views.index_alert, name='index_alert'),

    url(r'^clientes/puntoServicio/listar/', PuntosServicioList.as_view(), name='puntoServicio_list'),
    url(r'^clientes/puntoServicio/aprobado/', PuntosServicioAprobados.as_view() , name='servicio_aprobado'),
    url(r'^clientes/puntoServicio/nuevo/', PuntoServicioCreate.as_view(), name='puntoServicio_create'),
    url(r'^clientes/puntoServicio/editar/(?P<pk>\d+)/$', PuntosServicios_update, name='puntoServicio_update'),
    url(r'^clientes/puntoServicio/eliminar/(?P<pk>\d+)/$', PuntoServicioDeleteView.as_view(), name='puntoServicio_delete'),
    url(r'^clientes/punto_Servicio/listar/', views.PuntoServicio_list , name='punto_servicio_list'),
    url(r'^clientes/puntoServicio/relevamiento/(?P<id_puntoServicio>\d+)/$', Relevamiento, name='relevamiento'),
    url(r'^clientes/puntoServicio/relevamiento/$', Relevamiento, name='relevamiento_nuevo'),
    url(r'^operaciones/puntoServicio/clientes/', getClientes, name='getClientes'),

    url(r'^operaciones/operarios/listar/', viewsOperario.Operarios_list , name='operarios_list'),
    url(r'^operaciones/operarios/nuevo/', viewsOperario.Operarios_create, name='operarios_create'),
    url(r'^operaciones/operarios/editar/(?P<pk>\d+)/$', viewsOperario.Operarios_update, name='operarios_update'),
    url(r'^operaciones/operarios/eliminar/(?P<pk>\d+)/$', viewsOperario.Operarios_delete, name='operarios_delete'),
    url(r'^operaciones/planificacion/listar/', Planificacion_list, name='planificar_list'),
    url(r'^operaciones/planificacion/puntoServicios/', getPuntosServicios, name='getPuntosServiciosPla'),
    url(r'^operaciones/planificacion/planificar/(?P<id_puntoServicio>\d+)/$', Planificacion_create, name='planificar_create'),
    url(r'^operaciones/jefes/listar/', Jefes_list, name='jefes_list'),
    url(r'^operaciones/jefesAsignar/listar/', JefesAsignar_list, name='jefes_asignar_list'),
    url(r'^operaciones/fiscales/listar/', Fiscales_list, name='fiscales_list'),
    url(r'^operaciones/fiscalesAsignar/listar/', FiscalAsignar_list, name='fiscal_asignar_list'),
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
    url(r'^asignacion/asignar/operarios', viewsAsignacion.getOperarios, name='getOperarios'),
    #SERVICIO QUE AGREGABA DETALLE SIN RECARGAR PAGINA
    #url(r'^asignacion/agregarDetalle', viewsAsignacion.agregar_detalle, name='addDetalle'),
    #NUEVA VERSION DE ASIGNACION DETALLE
    url(r'^asignacion/agregarDetalle/(?P<id_puntoServicio>\d+)/$', viewsAsignacion.Asignacion_agregar, name='addDetalle'),
    url(r'^asignacion/verDetalle/(?P<id_puntoServicio>\d+)/$', viewsAsignacion.Asignacion_ver, name='verDetalle'),
    url(r'^asignacion/getAsignacionByTipo/(?P<id_asignacionDetalle>\d+)/$', viewsAsignacion.getAsignacionDetalleByTipo, name='getAsignacionByTipo'),
    url(r'^asignacion/limpiarTemporales/(?P<puntoServicio>\d+)/$', viewsAsignacion.limpiarTemporales, name='limpiarTemporales'),
    url(r'^asignacion/changeStorage', viewsAsignacion.changeStorage, name='changeStorage'),
    url(r'^asignacion/eliminar/(?P<id_asignacionDetalle>\d+)/$', viewsAsignacion.Eliminar_asignacion, name='eliminarDetalle'),
    url(r'^asignacion/guardarAsigOperario', viewsAsignacion.guardarAsignacionOperario, name='saveDetalle'),
    ##################################################################################################
    
    url(r'^asignacion/diasLibres', viewsAsignacion.getDiasLibres, name='getDiasLibres'),
    url(r'^asignacion/guardarAsignacion', viewsAsignacion.guardarAsignacion, name='guardarAsignacion'),
    url(r'^asignacion/puntoServicios', viewsAsignacion.getPuntosServicios, name='getPuntosServicios'),
    url(r'^marcacion/vista', obtenerMarcacion , name='marcaciones_url'),
    url(r'^marcacion/listar/', getMarcaciones , name='marcaciones_get'),
    url(r'^asignacion/operarios'+
   '/(?P<totalHoras>\d+)/(?P<puntoServicio>\d+)/(?P<lunEntReq>\d+)/(?P<lunSalReq>\d+)/'+
   '(?P<marEntReq>\d+)/(?P<marSalReq>\d+)/(?P<mierEntReq>\d+)/(?P<mierSalReq>\d+)/(?P<juevEntReq>\d+)'+
   '/(?P<juevSalReq>\d+)/(?P<vieEntReq>\d+)/(?P<vieSlReq>\d+)/(?P<sabEntReq>\d+)/(?P<sabSalReq>\d+)/'+
   '(?P<domEntReq>\d+)/(?P<domSalReq>\d+)/(?P<fechaInicioOp>\d+)/$', 
    cargarOperarios , name='filter_operarios'),
    url(r'^marcacion/descargar', descargarMarcaciones , name='marcaciones_xls'),
    url(r'^operaciones/feriados/vista', obtenerFeriado , name='feriados_url'),
    url(r'^feriados/listar', getFeriados , name='feriados_get'),
    url(r'^feriados/crear', makeFeriados , name='feriados_post'),
    url(r'^feriados/editar/(?P<feriado_id>\d+)', editFeriados , name='feriados_put'),
    url(r'^feriados/eliminar/(?P<feriado_id>\d+)', deleteFeriados , name='feriados_delete'),
    url(r'^operaciones/operarios/vista/', viewsOperario.getOperariosVista , name='operarios_vista'),
    url(r'^alertas/listar/', viewsAlerta.alertasList , name='alertas_list'),
    url(r'^alertas/gestionar/(?P<alerta_id>\d+)', viewsAlerta.gestion_alertas , name='alertas_gestionar'),
    url(r'^alertas/guardarSinAsignacion/(?P<id_alerta>\d+)', viewsAlerta.guardarSinAsignacion , name='guardar_sin_asignacion'),
    url(r'^alertas/mostrarCupos', viewsAlerta.mostrarCupos , name='mostrar_cupos'),
    url(r'^alertas/gestionar/marcaciones', viewsAlerta.getMarcaciones , name='getMarcacines'),
    url(r'^alertas/gestionar/reemplazo', viewsAlerta.getReemplazos , name='getReemplazos'),
    url(r'^alertas/gestionar/emparejar/(?P<alerta_id>\d+)/(?P<emparejamiento_id>\d+)', viewsAlerta.emparejar , name='alertas_emparejar')

]   