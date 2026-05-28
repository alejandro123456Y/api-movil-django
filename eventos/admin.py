from django.contrib import admin

from .models import Evento, Reservacion


admin.site.site_header = "Panel de eventos"
admin.site.site_title = "Eventos"
admin.site.index_title = "Administracion"


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
    list_display_links = ('id', 'nombre')
    list_editable = ('capacidad', 'cupos_disponibles', 'precio')
    search_fields = ('nombre', 'ubicacion')
    list_filter = ('fecha',)
    date_hierarchy = 'fecha'
    ordering = ('fecha', 'hora')
    fieldsets = (
        (
            "Informacion principal",
            {
                "fields": (
                    'nombre',
                    'descripcion',
                    ('fecha', 'hora'),
                    'ubicacion',
                )
            },
        ),
        (
            "Disponibilidad y precio",
            {
                "fields": (
                    ('capacidad', 'cupos_disponibles'),
                    'precio',
                )
            },
        ),
    )


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
    list_display_links = ('id', 'usuario')
    list_editable = ('estado',)
    search_fields = ('usuario__username', 'evento__nombre')
    list_filter = ('estado', 'fecha_reservacion')
    date_hierarchy = 'fecha_reservacion'
    ordering = ('-fecha_reservacion',)
