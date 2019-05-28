import django_tables2 as tables
from Operarios.models import EsmeEmMarcaciones

class MarcacionTable(tables.Table):
    class Meta:
        model=EsmeEmMarcaciones
        template_name='marcacion/marcacion_table.html'
