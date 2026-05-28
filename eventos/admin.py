from django.contrib import admin

from .models import Evento, Reservacion


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'nombre',
        'fecha',
        'hora',
        'ubicacion',
        'capacidad',
        'cupos_disponibles',
        'precio'
    )

    search_fields = ('nombre', 'ubicacion')

    list_filter = ('fecha',)


@admin.register(Reservacion)
class ReservacionAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'usuario',
        'evento',
        'cantidad',
        'estado',
        'fecha_reservacion'
    )

    list_filter = ('estado',)