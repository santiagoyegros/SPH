import django_filters
from django.forms.widgets import TextInput
from Operarios.models import EsmeEmMarcaciones

class MarcacionFilter(django_filters.FilterSet):
    idpersonaevento=django_filters.CharFilter(lookup_expr='icontains',widget=TextInput(attrs={'placeholder':'idpersonaevento'}))
    codoperacion=django_filters.CharFilter(lookup_expr='icontains',widget=TextInput(attrs={'placeholder':'codoperacion'}))
    codpersona=django_filters.CharFilter(lookup_expr='icontains',widget=TextInput(attrs={'placeholder':'codpersona'}))
    codcategoria=django_filters.CharFilter(lookup_expr='icontains',widget=TextInput(attrs={'placeholder':'codcategoria'}))
    numlinea=django_filters.CharFilter(lookup_expr='icontains',widget=TextInput(attrs={'placeholder':'numlinea'}))
    codubicacion=django_filters.CharFilter(lookup_expr='icontains',widget=TextInput(attrs={'placeholder':'codubicacion'}))
    fechaDesde=django_filters.DateFilter(field_name='fecha',lookup_expr='gt',label='Desde(mm/dd/yyyy)')
    fechaHasta=django_filters.DateFilter(field_name='fecha',lookup_expr='lt',label='Hasta(mm/dd/yyyy)')
    estado=django_filters.CharFilter(lookup_expr='icontains',widget=TextInput(attrs={'placeholder':'estado'}))
    class Meta:
        model= EsmeEmMarcaciones
        fields={
            'idpersonaevento',
            'codoperacion',
            'codpersona',
            'codcategoria',
            'numlinea',
            'codubicacion',
            'fecha',
            'estado'
        }