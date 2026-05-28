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

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

urlpatterns = [
    # AUTH
    path('api/login/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),

    # EVENTOS
    path('api/eventos/', EventoListView.as_view()),
    path('api/eventos/crear/', EventoCreateView.as_view()),
    path('api/eventos/editar/<int:pk>/', EventoUpdateView.as_view()),
    path('api/eventos/eliminar/<int:pk>/', EventoDeleteView.as_view()),

    # RESERVACIONES
    path('api/reservaciones/', ReservacionListView.as_view()),
    path('api/reservaciones/crear/', CrearReservacionView.as_view()),

    # USERS
    path('api/usuarios/crear/', UserCreateView.as_view()),

    # DASHBOARD
    path('api/dashboard/', DashboardView.as_view()),
]