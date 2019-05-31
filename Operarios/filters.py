import django_filters
from django.forms.widgets import TextInput
from Operarios.models import EsmeEmMarcaciones, OperariosAsignacionDet

class MarcacionFilter(django_filters.FilterSet):
    codoperacion=django_filters.CharFilter(lookup_expr='icontains',widget=TextInput(attrs={'placeholder':'codoperacion'}))
    codpersona=django_filters.CharFilter(lookup_expr='icontains',widget=TextInput(attrs={'placeholder':'codpersona'}))
    codubicacion=django_filters.CharFilter(lookup_expr='icontains',widget=TextInput(attrs={'placeholder':'codubicacion'}))
    fechaDesde=django_filters.DateFilter(field_name='fecha',lookup_expr='gt',label='Desde(mm/dd/yyyy)')
    fechaHasta=django_filters.DateFilter(field_name='fecha',lookup_expr='lt',label='Hasta(mm/dd/yyyy)')
    estado=django_filters.CharFilter(lookup_expr='icontains',widget=TextInput(attrs={'placeholder':'estado'}))
    class Meta:
        model= EsmeEmMarcaciones
        fields={
            'codoperacion',
            'codpersona',
            'codubicacion',
            'fecha',
            'estado'
        }

class OperariosFilter(django_filters.FilterSet):
    nombres = django_filters.CharFilter(lookup_expr='icontains',widget=TextInput(attrs={'placeholder':'nombre'}))
    antiguedad = django_filters.CharFilter(lookup_expr='icontains',widget=TextInput(attrs={'placeholder':'antiguedad'}))
    nombreLegajo = django_filters.CharFilter(lookup_expr='icontains',widget=TextInput(attrs={'placeholder':'nro legajo'}))
    id_PuntoServicio = django_filters.CharFilter(lookup_expr='icontains',widget=TextInput(attrs={'placeholder':'puntos de servicio'}))
    totalHoras = django_filters.CharFilter(lookup_expr='icontains',widget=TextInput(attrs={'placeholder':'total horas'}))
    perfil = django_filters.CharFilter(lookup_expr='icontains',widget=TextInput(attrs={'placeholder':'perfil'}))

    class Meta:
        model= OperariosAsignacionDet
        fields={
            'nombres',
            'antiguedad',
            'nombreLegajo',
            'id_PuntoServicio',
            'totalHoras',
            'perfil'
        }