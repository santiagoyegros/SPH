import logging
import datetime
from django.utils import timezone
from django.db.models import Q
from Operarios.models import AsignacionDetTemp


def borrar_temporales():
    tolerancia=1440
    print('Procedimiento de borrado de temporales: ' + str(datetime.datetime.now()))
    hoy=datetime.date.today()
    hastaCompleto=(datetime.datetime.now()-datetime.timedelta(minutes=tolerancia))
    asignaciones_temporales= AsignacionDetTemp.objects.filter(fechaCreacion__lte=hastaCompleto)
    for asig in asignaciones_temporales:
        asig.delete()