from django.urls import path
from .views import (
    EventoListView,
    EventoCreateView,
    EventoUpdateView,
    EventoDeleteView,
    ReservacionListView,
    CrearReservacionView,
    DashboardView,
    UserCreateView
)

urlpatterns = [

    # AUTH (NO DUPLIQUES LOGIN AQUÍ)
    # path('login/', ... ) ❌ eliminar aquí

    # EVENTOS
    path('eventos/', EventoListView.as_view()),
    path('eventos/crear/', EventoCreateView.as_view()),
    path('eventos/editar/<int:pk>/', EventoUpdateView.as_view()),
    path('eventos/eliminar/<int:pk>/', EventoDeleteView.as_view()),

    # RESERVACIONES
    path('reservaciones/', ReservacionListView.as_view()),
    path('reservaciones/crear/', CrearReservacionView.as_view()),

    # USERS
    path('usuarios/crear/', UserCreateView.as_view()),

    # DASHBOARD
    path('dashboard/', DashboardView.as_view()),
]