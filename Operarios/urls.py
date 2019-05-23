from django.urls import path

from . import views
from django.views.generic import TemplateView, RedirectView
from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from Operarios.views import PuntosServicioList, PuntoServicioCreate, PuntoServicioUpdateView, PuntoServicioDeleteView
from Operarios.views import Relevamiento, Operarios_list, Operarios_create, Operarios_update, Operarios_delete
from Operarios.views import Planificacion_list, Planificacion_create, Jefes_list, Jefes_asig, Jefes_delete
from Operarios.views import Fiscales_asig, Fiscales_delete
from Operarios import viewsAsignacion
app_name = 'Operarios'

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^bootstrap/$', TemplateView.as_view(template_name='bootstrap/example.html')),
    url(r'^test/', views.index_alert, name='index_alert'),
    url(r'^puntoServicio/listar/', PuntosServicioList.as_view(), name='puntoServicio_list'),
    url(r'^puntoServicio/nuevo/', PuntoServicioCreate.as_view(), name='puntoServicio_create'),
    url(r'^puntoServicio/editar/(?P<pk>\d+)/$', PuntoServicioUpdateView.as_view(), name='puntoServicio_update'),
    url(r'^puntoServicio/eliminar/(?P<pk>\d+)/$', PuntoServicioDeleteView.as_view(), name='puntoServicio_delete'),
    url(r'^puntoServicio/relevamiento/(?P<id_puntoServicio>\d+)/$', Relevamiento, name='relevamiento'),
    url(r'^puntoServicio/relevamiento/$', Relevamiento, name='relevamiento_nuevo'),
    url(r'^operarios/listar/', Operarios_list , name='operarios_list'),
    url(r'^operarios/nuevo/', Operarios_create, name='operarios_create'),
    url(r'^operarios/editar/(?P<pk>\d+)/$', Operarios_update, name='operarios_update'),
    url(r'^operarios/eliminar/(?P<pk>\d+)/$', Operarios_delete, name='operarios_delete'),
    url(r'^planificacion/listar/', Planificacion_list, name='planificar_list'),
    url(r'^planificacion/planificar/(?P<id_puntoServicio>\d+)/$', Planificacion_create, name='planificar_create'),
    url(r'^jefes/listar/', Jefes_list, name='jefes_list'),
    url(r'^jefes/asig/(?P<id_user_jefe>\d+)/$', Jefes_asig, name='jefes_asig'),
    url(r'^jefes/asig/(?P<id_user_jefe>\d+)/(?P<id_user_fiscal>\d+)/$', Jefes_asig, name='jefes_asig'),
    url(r'^jefes/asigFiscales/(?P<id_user_jefe>\d+)/$', Jefes_asig, name='jefes_asigFiscales'),
    url(r'^jefes/eliminar/(?P<id_user_jefe>\d+)/(?P<id_user_fiscal>\d+)/$', Jefes_delete, name='jefes_del'),
    url(r'^fiscales/asig/(?P<id_user_fiscal>\d+)/$', Fiscales_asig, name='fiscales_asig'),
    url(r'^fiscales/asig/(?P<id_user_fiscal>\d+)/(?P<id_puntoServicio>\d+)/$', Fiscales_asig, name='fiscales_asig'),
    url(r'^fiscales/eliminar/(?P<id_user_fiscal>\d+)/(?P<id_puntoServicio>\d+)/$', Fiscales_delete, name='fiscales_del'),
    url(r'^asignacion/listar/', viewsAsignacion.Asignacion_list, name='asignacion_list'),
    url(r'^asignacion/asignar/(?P<id_puntoServicio>\d+)/$', viewsAsignacion.Asignacion_create, name='asignacion_create'),
]   