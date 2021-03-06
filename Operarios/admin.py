from django.contrib import admin

from .models import Ciudad, Operario, Nacionalidad, Especializacion, TipoServicio, Cargo, CargoAsignado
from .models import AsigJefeFiscal, AsigFiscalPuntoServicio, TipoHorario, TipoSalario, TipoServicioParticular
from .models import GrupoEmpresarial, Cliente, PuntoServicio, RelevamientoCab, RelevamientoDet, RelevamientoEsp, RelevamientoCupoHoras
from .models import AsignacionCab, AsignacionDet

class CiudadAdmin(admin.ModelAdmin):
    list_display = ('NombreCiudad', )

class NacionalidadAdmin(admin.ModelAdmin):
    list_display = ('Pais', )

class EspecializacionAdmin(admin.ModelAdmin):
    list_display = ('especializacion', )

class OperarioAdmin(admin.ModelAdmin):
    list_display = ('numCedula','nroLegajo' ,'nombre', 'email', )

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('Cliente', 'GrupoEmpresarial', )

class PuntoServicioAdmin(admin.ModelAdmin):
    list_display = ('CodPuntoServicio', 'NombrePServicio', )

class TipoHorarioAdmin(admin.ModelAdmin):
    list_display = ('tipoHorario', )

class TipoSalarioAdmin(admin.ModelAdmin):
    list_display = ('tipoSalario', )

class TipoServicioParticularAdmin(admin.ModelAdmin):
    list_display = ('tipoServicioParticular', )

class RelevamientoDetInline(admin.TabularInline):
    model = RelevamientoDet

class RelevamientoEspInline(admin.TabularInline):
    model = RelevamientoEsp

class RelevamientoCupoHorasInline(admin.TabularInline):
    model = RelevamientoCupoHoras

class RelevamientoCabAdmin(admin.ModelAdmin):
    inlines = (RelevamientoCupoHorasInline, RelevamientoDetInline, RelevamientoEspInline, )

class AsignacionDetInline(admin.TabularInline):
    model = AsignacionDet

class AsignacionCabAdmin(admin.ModelAdmin):
    inlines = (AsignacionDetInline, )

class CargoAsignadoAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_name', 'get_last_name', 'cargo', )
    
    def get_name(self, obj):
        return obj.user.first_name
    
    def get_last_name(self, obj):
        return obj.user.last_name

    get_name.short_description = 'Nombre'
    get_last_name.short_description = 'Apellido'

    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'cargo__cargo')


class AsigJefeFiscalAdmin(admin.ModelAdmin):
    list_display = ('get_jefe_name', 'get_fiscal_name', )
    
    def get_jefe_name(self, obj):
        return obj.userJefe.last_name + ' ' + obj.userJefe.first_name

    def get_fiscal_name(self, obj):
        return obj.userFiscal.last_name + ' ' + obj.userFiscal.first_name

    get_jefe_name.short_description = 'Jefe'
    get_fiscal_name.short_description = 'Fiscal'
    
    search_fields = ('userJefe__first_name', 'userJefe__last_name', 'userFiscal__first_name', 'userFiscal__last_name', )


admin.site.register(Ciudad, CiudadAdmin)
admin.site.register(Nacionalidad, NacionalidadAdmin)
admin.site.register(Especializacion, EspecializacionAdmin)
admin.site.register(Operario, OperarioAdmin)
admin.site.register(GrupoEmpresarial)
admin.site.register(TipoServicio)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(PuntoServicio, PuntoServicioAdmin)
admin.site.register(TipoHorario, TipoHorarioAdmin)
admin.site.register(TipoSalario, TipoSalarioAdmin)
admin.site.register(TipoServicioParticular, TipoServicioParticularAdmin)
admin.site.register(RelevamientoCab, RelevamientoCabAdmin)
admin.site.register(Cargo)
admin.site.register(CargoAsignado, CargoAsignadoAdmin)
admin.site.register(AsigJefeFiscal, AsigJefeFiscalAdmin)
admin.site.register(AsigFiscalPuntoServicio)
admin.site.register(AsignacionCab, AsignacionCabAdmin)