from django import forms
import logging
import datetime
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
from Operarios.models import Ciudad, Nacionalidad, Especializacion
from Operarios.models import (  PuntoServicio, 
                                Operario, 
                                RelevamientoCab, 
                                RelevamientoDet, 
                                RelevamientoEsp,
                                RelevamientoCupoHoras,
                                RelevamientoMensualeros,
                                PlanificacionCab, 
                                PlanificacionOpe, 
                                PlanificacionEsp,
                                AsignacionCab,
                                AsignacionDet,
                                DiaLibre )

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
            'Coordenadas',
            'NumeroMarcador',
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
            'Coordenadas': 'Coordenadas',
            'NumeroMarcador': 'Numero del Marcador',
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
            'Coordenadas' : forms.TextInput(attrs={'class':'form-control'}),
            'NumeroMarcador' : forms.TextInput(attrs={'class':'form-control'}),
        }

class OperarioForm(forms.ModelForm):

    
    nombre: forms.CharField(max_length=70, required=True, error_messages={'required':'Ingrese un nombre para el Operario'})
    apellido: forms.CharField(max_length=70, required=True, error_messages={'required':'Ingrese un apellido para el Operario'})
    direccion: forms.CharField(max_length=100, required=True, error_messages={'required':'Ingrese la direccion del Operario'})
    numCedula: forms.CharField(max_length=30, required=True, error_messages={'required':'Ingrese un numero de cedula valida', 'max_length': 'La cedula debe tener como maximo 30 caracteres'})
    numPasaporte = forms.CharField(max_length=10, required=False)
    nroLegajo = forms.CharField(max_length=6)
    """
    nacionalidad = forms.IntegerField(required=True)
    ciudad = forms.IntegerField(required=True, error_messages={'required':'Seleccione una ciudad'})
    """
    escolaridad= forms.CharField(max_length=70, required=False, error_messages={'max_length':'Ha superado los 70 caracteres'})
    nombreContacto= forms.CharField(max_length=70)
    telefono=forms.IntegerField(required=True, error_messages={'required':'Ingrese numero de telefono'})
    telefonoContacto=forms.IntegerField(required=True, error_messages={'required':'Ingrese numero de telefono de contacto'})
    """
    profesion=forms.IntegerField(required=True, error_messages={'required':'Seleccione al menos una profesion'})
    """
    banco=forms.CharField(required=True, error_messages={'required':'Ingrese un banco'})
    ctaBanco=forms.IntegerField(required=True, error_messages={'required':'Ingrese un numero de banco'})
    """
    lugarNacimiento=forms.CharField(max_length=30, required=False)
    """
    fechaInicio=forms.DateField(required=True, error_messages={'required':'Ingrese la fecha de ingreso del operario'})
    fechaFin=forms.DateField(required=False)
    email=forms.EmailField(required=False)
    latitud=forms.CharField()
    longitud=forms.CharField()
    direccion=forms.CharField(required=True, error_messages={'required':'Ingrese la direccion del operario'})
    barrios=forms.CharField(required=True, error_messages={'required':'Ingrese el barrio'})
    class Meta:
        model = Operario
        fields=['nombre', 'apellido', 'direccion', 'numCedula', 'numPasaporte', 'nacionalidad', 'escolaridad', 'telefono','ciudad','profesion', 'fechaNacimiento','lugarNacimiento', 'banco', 'ctaBanco', 'nombreContacto', 'telefonoContacto','email', 'nroLegajo', 'fechaFin', 'fechaInicio', 'latitud', 'longitud', 'barrios'   ]

    

class RelevamientoForm(forms.ModelForm):

    class Meta:
        model = RelevamientoCab

        fields = [
            'puntoServicio',
            'cantidad',
            'cantAprendices',
            'cantidadHrTotal',
            'cantidadHrEsp',
            'fechaInicio',
            'tipoSalario',
            'comentario'
        ]

        labels = {
            'puntoServicio': 'Punto de Servicio',
            'cantidad': 'Cantidad de Operarios',
            'cantAprendices': 'Cantidad de Aprendices',
            'cantidadHrTotal': 'Total de Horas semanal',
            'cantidadHrEsp': 'Total de Horas Limp. Profunda Mensual',
            'fechaInicio': 'Fecha de Inicio de Cobertura',
            'tipoSalario': 'Tipo de Salario',
            'comentario': 'Comentarios'
        }

        widgets = {
            'puntoServicio': forms.Select(attrs={'class':'form-control form-control-sm', 'readonly':'readonly'}),
            'cantidad': forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'cantAprendices': forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'cantidadHrTotal': forms.TextInput(attrs={'class':'form-control form-control-sm', 'readonly':'readonly'}),
            'cantidadHrEsp': forms.TextInput(attrs={'class':'form-control form-control-sm', 'readonly':'readonly'}),
            'fechaInicio': DatePickerInput(format='%d/%m/%Y', options={"locale": "es"}),
            'tipoSalario': forms.Select(attrs={'class':'form-control form-control-sm'}), 
            'comentario': forms.Textarea(attrs={'class':'form-control form-control-sm noresize', 'rows':4, 'cols':60}),
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
            'lunEnt': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"useCurrent": False, "showTodayButton": False, "stepping": 5}).start_of('Lunes'),
            'lunSal': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"useCurrent": False, "showTodayButton": False, "stepping": 5}).end_of('Lunes'),
            'marEnt': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"useCurrent": False, "showTodayButton": False, "stepping": 5}).start_of('Martes'),
            'marSal': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"useCurrent": False, "showTodayButton": False, "stepping": 5}).end_of('Martes'),
            'mieEnt': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"useCurrent": False, "showTodayButton": False, "stepping": 5}).start_of('Miercoles'),
            'mieSal': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"useCurrent": False, "showTodayButton": False, "stepping": 5}).end_of('Miercoles'),
            'jueEnt': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"useCurrent": False, "showTodayButton": False, "stepping": 5}).start_of('Jueves'),
            'jueSal': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"useCurrent": False, "showTodayButton": False, "stepping": 5}).end_of('Jueves'),
            'vieEnt': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"useCurrent": False, "showTodayButton": False, "stepping": 5}).start_of('Viernes'),
            'vieSal': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"useCurrent": False, "showTodayButton": False, "stepping": 5}).end_of('Viernes'),
            'sabEnt': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"useCurrent": False, "showTodayButton": False, "stepping": 5}).start_of('Sabado'),
            'sabSal': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"useCurrent": False, "showTodayButton": False, "stepping": 5}).end_of('Sabado'),
            'domEnt': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"useCurrent": False, "showTodayButton": False, "stepping": 5}).start_of('Domingo'),
            'domSal': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"useCurrent": False, "showTodayButton": False, "stepping": 5}).end_of('Domingo')
        }

class RelevamientoEspForm(forms.ModelForm):

    class Meta:
        model = RelevamientoEsp
    
        fields = [
            'tipo',
            'frecuencia',
            #'dia',
            'cantHoras' 
        ]

        labels = {
            'tipo': 'Tipo limpieza especial',
            'frecuencia': 'Frecuencia',
            #'dia': 'Día',
            'cantHoras': 'Cantidad de Horas'
        }

        widgets = {
            'tipo': forms.Select(attrs={'class':'form-control form-control-sm'}),
            'frecuencia': forms.Select(attrs={'class':'form-control form-control-sm'}),
            #'dia': forms.Select(attrs={'class':'form-control form-control-sm'}),
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

    def is_valid(self):
        #Se prueba si es valido
        valid = super(RelevamientoCupoHorasForm, self).is_valid()

        if not valid:
            return valid

        try:
            testCantChoras = self.cleaned_data["cantCHoras"]
            try:
                testfrecuencia = self.cleaned_data["frecuencia"]
                testtipoHora = self.cleaned_data["tipoHora"]
                if testCantChoras is None:
                    self.add_error(None, 'El cupo de hora no esta cargado correctamente')
                    self.add_error('tipoHora', 'El cupo de hora no esta cargado correctamente')
                    self.fields['cantCHoras'].widget.attrs['class'] += " is-invalid"
                    return False
                elif testtipoHora is None:
                    self.add_error(None, 'El cupo de hora no esta cargado correctamente')
                    self.add_error('tipoHora', 'El cupo de hora no esta cargado correctamente')
                    self.fields['tipoHora'].widget.attrs['class'] += " is-invalid"
            except KeyError:
                return False    
        except KeyError:
            print('No pasa nada')
            
        #Si llegamos aca todo esta bien
        return True

class RelevamientoMensualerosForm(forms.ModelForm):
    
    class Meta:
        model = RelevamientoMensualeros
        
        fields = [
            'mensuCantidad',
            'sueldo',
        ]

        labels = {
            'mensuCantidad': 'Mensualeros',
            'sueldo': 'Sueldo Pactado',
        }

        widgets = {
            'mensuCantidad': forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'sueldo': forms.TextInput(attrs={'class':'form-control form-control-sm currency'}),
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

        '''
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

        '''
        #Si llegamos aca todo esta bien
        return True


class PlanificacionOpeForm(forms.ModelForm):

    class Meta:
        model = PlanificacionOpe

        fields = [
            'especialista',
            'cantidad',
            'lun',
            'mar',
            'mie',
            'jue',
            'vie',
            'sab',
            'dom',
            'fer',
            'ent',
            'sal',
            'corte',
            'total'
        ]

        labels = {
            'especialista': 'Especialista',
            'cantidad': 'Cantidad',
            'lun': 'Lunes',
            'mar': 'Martes',
            'mie': 'Miercoles',
            'jue': 'Jueves',
            'vie': 'Viernes',
            'sab': 'Sabado',
            'dom': 'Domingo',
            'fer': 'Feriado',
            'ent': 'Hora Entrada',
            'sal': 'Hora Salida',
            'corte': 'Corte',
            'total': 'Total'
        }

        widgets = {
            'especialista': forms.Select(attrs={'class':'form-row form-control-sm col-sm-6'}),
            'cantidad': forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'lun': forms.CheckboxInput(attrs={'class':'form-check-input p-0'}),
            'mar': forms.CheckboxInput(attrs={'class':'form-check-input p-0'}),
            'mie': forms.CheckboxInput(attrs={'class':'form-check-input p-0'}),
            'jue': forms.CheckboxInput(attrs={'class':'form-check-input p-0'}),
            'vie': forms.CheckboxInput(attrs={'class':'form-check-input p-0'}),
            'sab': forms.CheckboxInput(attrs={'class':'form-check-input p-0'}),
            'dom': forms.CheckboxInput(attrs={'class':'form-check-input p-0'}),
            'fer': forms.CheckboxInput(attrs={'class':'form-check-input p-0'}),
            'ent': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"useCurrent": False, "showTodayButton": False, "stepping": 5}).start_of('Lunes'),
            'sal': TimePickerInput(attrs={'class':'form-control form-control-sm'}, options={"useCurrent": False, "showTodayButton": False, "stepping": 5}).end_of('Lunes'),
            'corte': forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'total': forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            
        }

class PlanificacionEspForm(forms.ModelForm):

    class Meta:
        model = PlanificacionEsp
    
        fields = [
            'especialista',
            'tipo',
            'frecuencia',
            #'dia',
            'cantHoras',
            'fechaLimpProf'
        ]

        labels = {
            'especialista': 'Especialista',
            'tipo': 'Tipo limpieza especial',
            'frecuencia': 'Frecuencia',
            #'dia': 'Día',
            'cantHoras': 'Cantidad de Horas',
            'fechaLimpProf': 'Fecha Inicio'
        }

        widgets = {
            'especialista': forms.Select(attrs={'class':'form-control form-control-sm'}),
            'tipo': forms.Select(attrs={'class':'form-control form-control-sm'}),
            'frecuencia': forms.Select(attrs={'class':'form-control form-control-sm'}),
            #'dia': forms.Select(attrs={'class':'form-control form-control-sm'}),
            'cantHoras': forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'fechaLimpProf': DatePickerInput(format='%d/%m/%Y', options={"locale": "es"})
        }

class AsignacionCabForm(forms.ModelForm):
    
    class Meta:
        model = AsignacionCab

        fields = [
            'puntoServicio',
            'totalasignado',
        ]

        labels = {
            'puntoServicio': 'Punto de Servicio',
            'totalasignado': 'Cantidad Hrs Asignadas',
        }

        widgets = {
            'puntoServicio': forms.TextInput(attrs={'class':'form-control form-control-sm', 'readonly':'readonly'}),
            'totalasignado': forms.TextInput(attrs={'class':'form-control form-control-sm'}),
        }

class AsignacionDetForm(forms.ModelForm):

    class Meta:
        model = AsignacionDet

        fields = [
            'operario',
            'fechaInicio',
            'fechaFin',
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
            'domSal',
            'perfil',
            'supervisor',
            'totalHoras',
        ]

        labels = {
            'operario' : 'Operario',
            'fechaInicio':"Fecha Inicio",
            'fechaFin':"Fecha Fin",
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
            'domSal': 'Domingo Salida',
            'supervisor':'Supervisor',  
            'perfil':'Perfil', 
            'totalHoras':'Total Horas'  
        }

        widgets = { 
            'operario': forms.TextInput(attrs={'class':'form-control form-control-sm d-none', 'readonly':'readonly','style':'height:39px !important'}),
            'fechaInicio': DatePickerInput(format='%d/%m/%Y', options={"locale": "es"},attrs={"placeholder": "Fecha Inicio","class":"form-control examDate"}),
            'fechaFin': DatePickerInput(format='%d/%m/%Y', options={"locale": "es"}, attrs={"placeholder": "Fecha Fin","class":"form-control examDate"}),
            'lunEnt': TimePickerInput(attrs={'class':'form-control form-control-sm examTime'}, options={"useCurrent": False, "showTodayButton": False, "stepping": 5}).start_of('Lunes'),
            'lunSal': TimePickerInput(attrs={'class':'form-control form-control-sm examTime'}, options={"useCurrent": False, "showTodayButton": False, "stepping": 5}).end_of('Lunes'),
            'marEnt': TimePickerInput(attrs={'class':'form-control form-control-sm examTime'}, options={"useCurrent": False, "showTodayButton": False, "stepping": 5}).start_of('Martes'),
            'marSal': TimePickerInput(attrs={'class':'form-control form-control-sm examTime'}, options={"useCurrent": False, "showTodayButton": False, "stepping": 5}).end_of('Martes'),
            'mieEnt': TimePickerInput(attrs={'class':'form-control form-control-sm examTime'}, options={"useCurrent": False, "showTodayButton": False, "stepping": 5}).start_of('Miercoles'),
            'mieSal': TimePickerInput(attrs={'class':'form-control form-control-sm examTime'}, options={"useCurrent": False, "showTodayButton": False, "stepping": 5}).end_of('Miercoles'),
            'jueEnt': TimePickerInput(attrs={'class':'form-control form-control-sm examTime'}, options={"useCurrent": False, "showTodayButton": False, "stepping": 5}).start_of('Jueves'),
            'jueSal': TimePickerInput(attrs={'class':'form-control form-control-sm examTime'}, options={"useCurrent": False, "showTodayButton": False, "stepping": 5}).end_of('Jueves'),
            'vieEnt': TimePickerInput(attrs={'class':'form-control form-control-sm examTime'}, options={"useCurrent": False, "showTodayButton": False, "stepping": 5}).start_of('Viernes'),
            'vieSal': TimePickerInput(attrs={'class':'form-control form-control-sm examTime'}, options={"useCurrent": False, "showTodayButton": False, "stepping": 5}).end_of('Viernes'),
            'sabEnt': TimePickerInput(attrs={'class':'form-control form-control-sm examTime'}, options={"useCurrent": False, "showTodayButton": False, "stepping": 5}).start_of('Sabado'),
            'sabSal': TimePickerInput(attrs={'class':'form-control form-control-sm examTime'}, options={"useCurrent": False, "showTodayButton": False, "stepping": 5}).end_of('Sabado'),
            'domEnt': TimePickerInput(attrs={'class':'form-control form-control-sm examTime'}, options={"useCurrent": False, "showTodayButton": False, "stepping": 5}).start_of('Domingo'),
            'domSal': TimePickerInput(attrs={'class':'form-control form-control-sm examTime'}, options={"useCurrent": False, "showTodayButton": False, "stepping": 5}).end_of('Domingo'),
            'totalHoras': forms.TextInput(attrs={'class':'form-control form-control-sm', 'readonly':'readonly' }),
            'supervisor': forms.CheckboxInput(attrs={'class':'checkbox-supervisor','checked':False,'style':'    display: block;margin: 8px 25px;'}), 
            'perfil': forms.Select(attrs={'class':'form-control form-control-sm perfil-combo'})
        }
        

def timeInHours(str):
    tokens = str.split(':')

    return int(tokens[0]) + float(tokens[1])/60.0



"""class DiaLibreForm(forms.ModelForm):

    class Meta:
        model = DiaLibre

        fields = [
            'diaInicio',
            'horaInicio',
            'diaFin',
            'horaFin'
        ]

        labels = {
            'diaInicio' : 'Fecha inicio',
            'horaInicio' : 'Hora inicio',
            'diaFin':'Fecha Fin',
            'horaFin':'Hora Fin'
        }
        choices = (('Lunes','Lunes'),('Martes','Martes'),('Miercoles','Miercoles'),('Jueves','Jueves'),('Viernes','Viernes'),('Sabado','Sabado'),('Domingo','Domingo'))
        widgets = {
            'diaInicio': forms.Select(attrs={'class':'form-control form-control-sm select-form'},choices=choices),
            'horaInicio':TimePickerInput(attrs={'class':'form-control form-control-sm',"placeholder": "Hora Inicio"}, options={"useCurrent": False, "showTodayButton": False, "stepping": 5}).end_of('Jueves'),
            'diaFin': forms.Select(attrs={'class':'form-control form-control-sm select-form'},choices=choices),
            'horaFin': TimePickerInput(attrs={'class':'form-control form-control-sm',"placeholder": "Hora Fin"}, options={"useCurrent": False, "showTodayButton": False, "stepping": 5}).end_of('Jueves'),
 
        }
        
"""
# class AccionesAlertasFrom(forms.ModelForm):
#     accion:
#     horaEntrada:
#     horaAprox:
#     motivo:forms.CharField(max_length=100, required=False)
#     fechaRetorno:
#     horaRetorno:
#     comentario:forms.CharField(max_length=100, required=False)
#     escalar:
#     class Meta:
#         model = Operario
#         fields=['nombre', 'apellido', 'direccion', 'numCedula', 'numPasaporte', 'nacionalidad', 'escolaridad', 'telefono','ciudad','profesion', 'fechaNacimiento','lugarNacimiento', 'banco', 'ctaBanco', 'nombreContacto', 'telefonoContacto','email', 'nroLegajo', 'fechaFin', 'fechaInicio', 'latitud', 'longitud', 'barrios'   ]
