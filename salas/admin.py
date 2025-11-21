from django.contrib import admin
from .models import Sala, Reserva
from datetime import timedelta

@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'capacidad_maxima', 'habilitada', 'get_disponibilidad']
    list_filter = ['habilitada']
    search_fields = ['nombre']
    list_editable = ['habilitada']
    
    def get_disponibilidad(self, obj):
        return '✅ Disponible' if obj.disponible else '❌ Reservada'
    get_disponibilidad.short_description = 'Estado'

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ['sala', 'rut', 'fecha_inicio', 'fecha_termino', 'duracion']
    list_filter = ['sala', 'fecha_inicio']
    search_fields = ['rut', 'sala__nombre']
    date_hierarchy = 'fecha_inicio'
    readonly_fields = ['fecha_inicio', 'fecha_termino']
    
    def duracion(self, obj):
        return "2 horas"
    duracion.short_description = 'Duración'
    
    def save_model(self, request, obj, form, change):
        # Forzar recálculo de fecha_termino
        obj.fecha_termino = obj.fecha_inicio + timedelta(hours=2)
        super().save_model(request, obj, form, change)