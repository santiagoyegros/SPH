from django import forms
import logging
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput

from Operarios.models import (  PuntoServicio, 
                                Operario, 
                                RelevamientoCab, 
                                RelevamientoDet, 
                                RelevamientoEsp,
                                RelevamientoCupoHoras,
                                PlanificacionCab, 
                                PlanificacionDet, 
                                PlanificacionEsp )

class PuntoServicioForm(forms.ModelForm):
    class Meta:
        model = PuntoServicio

        fields = [
            'Cliente',
            'CodPuntoServicio',
            'NombrePServicio',
            'DireccionContrato',
            'Ciudad',
            'Barrios',
            'Contacto',
            'MailContacto',
            'TelefonoContacto',
            'Coordenadas'
        ]

        labels = {
            'Cliente': 'Cliente',
            'CodPuntoServicio': 'Punto de Servicio',
            'NombrePServicio': 'Nombre de Punto de Servicio',
            'DireccionContrato': 'Direccion del Punto de Servicio',
            'Ciudad': 'Ciudad',
            'Barrios': 'Barrio',
            'Contacto': 'Contacto',
            'MailContacto': 'Mail del Contacto',
            'TelefonoContacto': 'Telefono del Contacto',
            'Coordenadas': 'Coordenadas'
        }

        widgets = {
            'Cliente' : forms.Select(attrs={'class':'form-control'}),
            'CodPuntoServicio' : forms.TextInput(attrs={'class':'form-control'}),
            'NombrePServicio' : forms.TextInput(attrs={'class':'form-control'}),
            'DireccionContrato' : forms.TextInput(attrs={'class':'form-control'}),
            'Ciudad' : forms.Select(attrs={'class':'form-control'}),
            'Barrios' : forms.TextInput(attrs={'class':'form-control'}),
            'Contacto' : forms.TextInput(attrs={'class':'form-control'}),
            'MailContacto' : forms.TextInput(attrs={'class':'form-control'}),
            'TelefonoContacto' : forms.TextInput(attrs={'class':'form-control'}),
            'Coordenadas' : forms.TextInput(attrs={'class':'form-control'})
        }

class OperarioForm(forms.ModelForm):
    
    class Meta:
        model = Operario

        fields = [
            'Nombre',
            'Direccion',
            'Ciudad',
            'Barrios',
            'NroLegajo',
            'Telefono',
            'Email',
            'FechaNacimiento',
            'LugarNacimiento',
            'NumCedula',
            'NumPasaporte',
            'Especialidad',
            'Banco',
            'CtaBanco',
            'Clase',
            'NombreContacto',
            'Profesion',
            'Nacionalidad',
            'FechaInicio',
            'FechaFin'
        ]

        labels = {
            'Nombre':'Nombre',
            'Direccion':'Direccion',
            'Ciudad':'Ciudad',
            'Barrios':'Barrio',
            'NroLegajo':'Numero Legajo',
            'Telefono':'Telefono',
            'Email':'E-mail',
            'FechaNacimiento':'Fecha de Nacimiento',
            'LugarNacimiento':'Lugar de Nacimiento',
            'NumCedula':'N° Cedula',
            'NumPasaporte':'N° Pasaporte',
            'Especialidad': 'Especialidad',
            'Banco':'Banco',
            'CtaBanco':'Numero de Cuenta',
            'Clase':'Clase',
            'NombreContacto':'Nombre de Contacto',
            'Profesion':'Profesión',
            'Nacionalidad':'Nacionalidad',
            'FechaInicio':'Fecha de Inicio',
            'FechaFin':' Fecha de Terminación'
        }

        widgets = {
            'Nombre': forms.TextInput(attrs={'class':'form-control'}),
            'Direccion': forms.TextInput(attrs={'class':'form-control'}),
            'Ciudad': forms.Select(attrs={'class':'form-control'}),
            'Barrios': forms.TextInput(attrs={'class':'form-control'}),
            'NroLegajo': forms.TextInput(attrs={'class':'form-control'}),
            'Telefono': forms.TextInput(attrs={'class':'form-control'}),
            'Email': forms.TextInput(attrs={'class':'form-control'}),
            'FechaNacimiento': DatePickerInput(format='%d/%m/%Y', options={"locale": "es"}),
            'LugarNacimiento': forms.TextInput(attrs={'class':'form-control'}),
            'NumCedula': forms.TextInput(attrs={'class':'form-control'}),
            'NumPasaporte': forms.TextInput(attrs={'class':'form-control'}),
            'Especialidad': forms.Select(attrs={'class':'form-control'}),
            'Banco': forms.TextInput(attrs={'class':'form-control'}),
            'CtaBanco': forms.TextInput(attrs={'class':'form-control'}),
            'Clase': forms.TextInput(attrs={'class':'form-control'}),
            'NombreContacto': forms.TextInput(attrs={'class':'form-control'}),
            'Profesion': forms.TextInput(attrs={'class':'form-control'}),
            'Nacionalidad': forms.Select(attrs={'class':'form-control'}),
            'FechaInicio':  DatePickerInput(format='%d/%m/%Y'),
            'FechaFin':   DatePickerInput(format='%d/%m/%Y')
        }

class RelevamientoForm(forms.ModelForm):

    class Meta:
        model = RelevamientoCab

        fields = [
            'puntoServicio',
            'cantidad',
            'cantidadHrTotal',
            'cantidadHrEsp',
            'fechaInicio',
            'tipoSalario',
            'comentario'
        ]

        labels = {
            'puntoServicio': 'Punto de Servicio',
            'cantidad': 'Cantidad de Operarios',
            'cantidadHrTotal': 'Cantidad Total de Horas',
            'cantidadHrEsp': 'Cantidad Total de horas Especiales',
            'fechaInicio': 'Fecha de Inicio de Cobertura',
            'tipoSalario': 'Tipo de Salario',
            'comentario': 'Comentarios'
        }

        widgets = {
            'puntoServicio': forms.Select(attrs={'class':'form-control form-control-sm', 'readonly':'readonly'}),
            'cantidad': forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'cantidadHrTotal': forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'cantidadHrEsp': forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'fechaInicio': DatePickerInput(format='%d/%m/%Y', options={"locale": "es"}),
            'tipoSalario': forms.Select(attrs={'class':'form-control form-control-sm'}), 
            'comentario': forms.Textarea(attrs={'class':'form-control form-control-sm', 'rows':4, 'cols':60}),
        }

class RelevamientoDetForm(forms.ModelForm):

    class Meta:
        model = RelevamientoDet

        fields = [
            'orden',
            'tipoServPart',
            'lunEnt',
            'lunSal',
            'marEnt',
            'marSal',
            'mieEnt',
            'mieSal',
            'jueEnt',
            'jueSal',
            'vieEnt',
            'vieSal',
            'sabEnt',
            'sabSal',
            'domEnt',
            'domSal'
            
        ]

        labels = {
            'orden': 'Orden',
            'tipoServPart' : 'Tipo de Servicio Particular',
            'lunEnt': 'Lunes Entrada',
            'lunSal': 'Lunes Salida',
            'marEnt': 'Martes Entrada',
            'marSal': 'Martes Salida',
            'mieEnt': 'Miercoles Entrada',
            'mieSal': 'Miercoles Salida',
            'jueEnt': 'Jueves Entrada',
            'jueSal': 'Jueves Salida',
            'vieEnt': 'Viernes Entrada',
            'vieSal': 'Viernes Salida',
            'sabEnt': 'Sabado Entrada',
            'sabSal': 'Sabado Salida',
            'domEnt': 'Domingo Entrada',
            'domSal': 'Domingo Salida'
        }

        widgets = {
            'orden': forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'tipoServPart': forms.Select(attrs={'class':'form-control form-control-sm'}),
            'lunEnt': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"showTodayButton": False, "stepping": 5}).start_of('Lunes'),
            'lunSal': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"showTodayButton": False, "stepping": 5}).end_of('Lunes'),
            'marEnt': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"showTodayButton": False, "stepping": 5}).start_of('Martes'),
            'marSal': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"showTodayButton": False, "stepping": 5}).end_of('Martes'),
            'mieEnt': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"showTodayButton": False, "stepping": 5}).start_of('Miercoles'),
            'mieSal': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"showTodayButton": False, "stepping": 5}).end_of('Miercoles'),
            'jueEnt': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"showTodayButton": False, "stepping": 5}).start_of('Jueves'),
            'jueSal': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"showTodayButton": False, "stepping": 5}).end_of('Jueves'),
            'vieEnt': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"showTodayButton": False, "stepping": 5}).start_of('Viernes'),
            'vieSal': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"showTodayButton": False, "stepping": 5}).end_of('Viernes'),
            'sabEnt': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"showTodayButton": False, "stepping": 5}).start_of('Sabado'),
            'sabSal': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"showTodayButton": False, "stepping": 5}).end_of('Sabado'),
            'domEnt': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"showTodayButton": False, "stepping": 5}).start_of('Domingo'),
            'domSal': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"showTodayButton": False, "stepping": 5}).end_of('Domingo')
        }

class RelevamientoEspForm(forms.ModelForm):

    class Meta:
        model = RelevamientoEsp
    
        fields = [
            'tipo',
            'frecuencia',
            'dia',
            'cantHoras' 
        ]

        labels = {
            'tipo': 'Tipo limpieza especial',
            'frecuencia': 'Frecuencia',
            'dia': 'Día',
            'cantHoras': 'Cantidad de Horas'
        }

        widgets = {
            'tipo': forms.Select(attrs={'class':'form-control form-control-sm'}),
            'frecuencia': forms.Select(attrs={'class':'form-control form-control-sm'}),
            'dia': forms.Select(attrs={'class':'form-control form-control-sm'}),
            'cantHoras': forms.TextInput(attrs={'class':'form-control form-control-sm'})
        }

class RelevamientoCupoHorasForm(forms.ModelForm):

    class Meta:
        model = RelevamientoCupoHoras
    
        fields = [
            'cantCHoras',
            'frecuencia',
            'tipoHora'
        ]

        labels = {
            'cantCHoras': 'Cantidad Hrs',
            'frecuencia': 'Frecuencia',
            'tipoHora': 'Tipo de Hora',
        }

        widgets = {
            'cantCHoras': forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'frecuencia': forms.Select(attrs={'class':'form-control form-control-sm'}),
            'tipoHora': forms.Select(attrs={'class':'form-control form-control-sm'})
        }


class PlanificacionForm(forms.ModelForm):

    class Meta:
        model = PlanificacionCab

        fields = [
            'puntoServicio',
            'cantidad',
            'cantHoras',
            'cantHorasNoc',
            'cantHorasEsp',
        ]

        labels = {
            'puntoServicio': 'Punto de Servicio',
            'cantidad': 'Cantidad de Operarios',
            'cantHoras': 'Cantidad de Horas',
            'cantHorasNoc': 'Cantidad de Horas Nocturnas',
            'cantHorasEsp': 'Cantidad de Horas Especiales',
        }

        widgets = {
            'puntoServicio': forms.Select(attrs={'class':'form-control form-control-sm', 'readonly':'readonly'}),
            'cantidad': forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'cantHoras': forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'cantHorasNoc': forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'cantHorasEsp': forms.TextInput(attrs={'class':'form-control form-control-sm'})
        }


    def is_valid(self, cantidad, cantidadHrTotal, cantidadHrEsp):
        #Se prueba si es valido
        valid = super(PlanificacionForm, self).is_valid()

        if not valid:
            return valid

        if (cantidadHrTotal is not None) and (self.cleaned_data['cantHoras'] is not None):
            logging.getLogger("error_logger").error('cantidadHrTotal/cantHoras no son None')

            if timeInHours(self.cleaned_data['cantHoras']) > timeInHours(cantidadHrTotal):
                self.add_error(None, 'Cantidad de Horas Normales que sobrepasan la cantidad estimada')
                self.add_error('cantHoras', 'La Cantidad no puede superar las horas planificadas')
                self.fields['cantHoras'].widget.attrs['class'] += " is-invalid"
                return False

        if (cantidad is not None) and (self.cleaned_data['cantidad'] is not None):
            logging.getLogger("error_logger").error('cantidad/cantidad no son None')

            if self.cleaned_data['cantidad'] < cantidad:
                self.add_error(None, 'Cantidad de Operarios minima no se cumple')
                self.add_error('cantidad', 'La Cantidad no puede superar las horas planificadas')
                self.fields['cantidad'].widget.attrs['class'] += " is-invalid"
                return False

        if (cantidadHrEsp is not None) and (self.cleaned_data['cantHorasEsp'] is not None):
            logging.getLogger("error_logger").error('cantidadHrEsp no son None')
            if timeInHours(self.cleaned_data['cantHorasEsp']) > timeInHours(cantidadHrEsp):
                self.add_error(None, 'Cantidad de Horas Especiales que sobrepasan la cantidad estimada')
                self.add_error('cantHorasEsp', 'La Cantidad no puede superar las horas planificadas')
                self.fields['cantHorasEsp'].widget.attrs['class'] += " is-invalid"
                return False

        #Si llegamos aca todo esta bien
        return True


class PlanificacionDetForm(forms.ModelForm):

    class Meta:
        model = PlanificacionDet

        fields = [
            'especialista',
            'orden',
            'lunEnt',
            'lunSal',
            'marEnt',
            'marSal',
            'mieEnt',
            'mieSal',
            'jueEnt',
            'jueSal',
            'vieEnt',
            'vieSal',
            'sabEnt',
            'sabSal',
            'domEnt',
            'domSal'
        ]

        labels = {
            'especialista': 'Especialista',
            'orden': 'Orden',
            'lunEnt': 'Lunes Entrada',
            'lunSal': 'Lunes Salida',
            'marEnt': 'Martes Entrada',
            'marSal': 'Martes Salida',
            'mieEnt': 'Miercoles Entrada',
            'mieSal': 'Miercoles Salida',
            'jueEnt': 'Jueves Entrada',
            'jueSal': 'Jueves Salida',
            'vieEnt': 'Viernes Entrada',
            'vieSal': 'Viernes Salida',
            'sabEnt': 'Sabado Entrada',
            'sabSal': 'Sabado Salida',
            'domEnt': 'Domingo Entrada',
            'domSal': 'Domingo Salida'
        }

        widgets = {
            'especialista': forms.Select(attrs={'class':'form-row form-control-sm col-sm-6'}),
            'orden': forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'lunEnt': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"showTodayButton": False, "stepping": 5}).start_of('Lunes'),
            'lunSal': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"showTodayButton": False, "stepping": 5}).end_of('Lunes'),
            'marEnt': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"showTodayButton": False, "stepping": 5}).start_of('Martes'),
            'marSal': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"showTodayButton": False, "stepping": 5}).end_of('Martes'),
            'mieEnt': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"showTodayButton": False, "stepping": 5}).start_of('Miercoles'),
            'mieSal': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"showTodayButton": False, "stepping": 5}).end_of('Miercoles'),
            'jueEnt': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"showTodayButton": False, "stepping": 5}).start_of('Jueves'),
            'jueSal': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"showTodayButton": False, "stepping": 5}).end_of('Jueves'),
            'vieEnt': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"showTodayButton": False, "stepping": 5}).start_of('Viernes'),
            'vieSal': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"showTodayButton": False, "stepping": 5}).end_of('Viernes'),
            'sabEnt': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"showTodayButton": False, "stepping": 5}).start_of('Sabado'),
            'sabSal': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"showTodayButton": False, "stepping": 5}).end_of('Sabado'),
            'domEnt': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"showTodayButton": False, "stepping": 5}).start_of('Domingo'),
            'domSal': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"showTodayButton": False, "stepping": 5}).end_of('Domingo')
        }

class PlanificacionEspForm(forms.ModelForm):

    class Meta:
        model = PlanificacionEsp
    
        fields = [
            'especialista',
            'tipo',
            'frecuencia',
            'dia',
            'cantHoras' 
        ]

        labels = {
            'especialista': 'Especialista',
            'tipo': 'Tipo limpieza especial',
            'frecuencia': 'Frecuencia',
            'dia': 'Día',
            'cantHoras': 'Cantidad de Horas'
        }

        widgets = {
            'especialista': forms.Select(attrs={'class':'form-control form-control-sm'}),
            'tipo': forms.Select(attrs={'class':'form-control form-control-sm'}),
            'frecuencia': forms.Select(attrs={'class':'form-control form-control-sm'}),
            'dia': forms.Select(attrs={'class':'form-control form-control-sm'}),
            'cantHoras': forms.TextInput(attrs={'class':'form-control form-control-sm'})
        }

def timeInHours(str):
    tokens = str.split(':')

    return int(tokens[0]) + float(tokens[1])/60.0