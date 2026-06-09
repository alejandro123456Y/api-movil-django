from django.urls import path

from .views import (
    CrearReservacionView,
    DashboardView,
    EventoCreateView,
    EventoDeleteView,
    EventoListView,
    EventoUpdateView,
    ReservacionListView,
    RegisterUserView,
    UserCreateView,
    UserDeleteView,
    UserDetailView,
    UserListView,
    UserUpdateView,
)

urlpatterns = [
    path("eventos/", EventoListView.as_view(), name="eventos-list"),
    path("eventos/crear/", EventoCreateView.as_view(), name="eventos-create"),
    path("eventos/editar/<int:pk>/", EventoUpdateView.as_view(), name="eventos-update"),
    path("eventos/eliminar/<int:pk>/", EventoDeleteView.as_view(), name="eventos-delete"),
    path("reservaciones/", ReservacionListView.as_view(), name="reservaciones-list"),
    path("reservaciones/crear/", CrearReservacionView.as_view(), name="reservaciones-create"),
    path("registro/", RegisterUserView.as_view(), name="registro"),
    path("usuarios/", UserListView.as_view(), name="usuarios-list"),
    path("usuarios/<int:pk>/", UserDetailView.as_view(), name="usuarios-detail"),
    path("usuarios/crear/", UserCreateView.as_view(), name="usuarios-create"),
    path("usuarios/editar/<int:pk>/", UserUpdateView.as_view(), name="usuarios-update"),
    path("usuarios/eliminar/<int:pk>/", UserDeleteView.as_view(), name="usuarios-delete"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
]
