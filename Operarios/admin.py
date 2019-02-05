from django.contrib import admin

from .models import Ciudad, Operario, Nacionalidad, Especializacion, TipoServicio, Cargo, CargoAsignado
from .models import GrupoEmpresarial, Cliente, PuntoServicio, RelevamientoCab, RelevamientoDet, RelevamientoEsp

class CiudadAdmin(admin.ModelAdmin):
    list_display = ('NombreCiudad', )

class NacionalidadAdmin(admin.ModelAdmin):
    list_display = ('Pais', )

class EspecializacionAdmin(admin.ModelAdmin):
    list_display = ('especializacion', )

class OperarioAdmin(admin.ModelAdmin):
    list_display = ('NumCedula','NroLegajo' ,'Nombre', 'Email', )

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('Cliente', 'GrupoEmpresarial', )

class PuntoServicioAdmin(admin.ModelAdmin):
    list_display = ('CodPuntoServicio', 'NombrePServicio', )

class RelevamientoDetInline(admin.TabularInline):
    model = RelevamientoDet

class RelevamientoEspInline(admin.TabularInline):
    model = RelevamientoEsp

class RelevaminetoCabAdmin(admin.ModelAdmin):
    inlines = (RelevamientoDetInline, RelevamientoEspInline, )

admin.site.register(Ciudad, CiudadAdmin)
admin.site.register(Nacionalidad, NacionalidadAdmin)
admin.site.register(Especializacion, EspecializacionAdmin)
admin.site.register(Operario, OperarioAdmin)
admin.site.register(GrupoEmpresarial)
admin.site.register(TipoServicio)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(PuntoServicio, PuntoServicioAdmin)
admin.site.register(RelevamientoCab, RelevaminetoCabAdmin)
admin.site.register(Cargo)
admin.site.register(CargoAsignado)
