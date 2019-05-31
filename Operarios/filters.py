import django_filters
from django.forms.widgets import TextInput
from Operarios.models import EsmeEmMarcaciones, OperariosDisponibles

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

    class Meta:
        model= OperariosDisponibles
        fields={
            'nombres',
            'antiguedad',
            'nroLegajo',
            'ids_puntoServicio',
            'totalHoras',
            'perfil'
        }