from django.urls import path

from .views import (
    CrearReservacionView,
    DashboardView,
    EventoCreateView,
    EventoDeleteView,
    EventoListView,
    EventoUpdateView,
    ReservacionListView,
    UserCreateView,
)

urlpatterns = [
    path("eventos/", EventoListView.as_view(), name="eventos-list"),
    path("eventos/crear/", EventoCreateView.as_view(), name="eventos-create"),
    path("eventos/editar/<int:pk>/", EventoUpdateView.as_view(), name="eventos-update"),
    path("eventos/eliminar/<int:pk>/", EventoDeleteView.as_view(), name="eventos-delete"),
    path("reservaciones/", ReservacionListView.as_view(), name="reservaciones-list"),
    path("reservaciones/crear/", CrearReservacionView.as_view(), name="reservaciones-create"),
    path("usuarios/crear/", UserCreateView.as_view(), name="usuarios-create"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
]
