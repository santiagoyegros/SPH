import django_tables2 as tables
from Operarios.models import EsmeEmMarcaciones
from django_tables2.export.views import ExportMixin
class MarcacionTable(ExportMixin,tables.Table):
    export_formats=['xls']
    class Meta:
        model=EsmeEmMarcaciones
        template_name='marcacion/marcacion_table.html'
