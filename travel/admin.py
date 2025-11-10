from django.contrib import admin
from .models import Viaje

# Register your models here.

class ViajeAdmin(admin.ModelAdmin):
    # Qué columnas mostrar en la lista
    list_display = ('id', 'pasajero', 'conductor', 'estado', 'precio_final', 'created_at')
    # Añadir un filtro por estado
    list_filter = ('estado',)
    # Añadir una barra de búsqueda
    search_fields = ('pasajero__full_name', 'conductor__full_name', 'id')
    # No dejar editar todo en la lista
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Viaje, ViajeAdmin)