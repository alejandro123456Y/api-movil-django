from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.db.models import Sum, Count
from django.contrib.auth.models import User

from .models import Evento, Reservacion
from .serializers import EventoSerializer, ReservacionSerializer, UserSerializer


# =========================
# EVENTOS CRUD
# =========================

class EventoListView(generics.ListAPIView):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [IsAuthenticated]


class EventoCreateView(generics.CreateAPIView):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [IsAuthenticated]


class EventoUpdateView(generics.UpdateAPIView):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [IsAuthenticated]


class EventoDeleteView(generics.DestroyAPIView):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [IsAuthenticated]


# =========================
# RESERVACIONES
# =========================

class ReservacionListView(generics.ListAPIView):
    queryset = Reservacion.objects.all()
    serializer_class = ReservacionSerializer
    permission_classes = [IsAuthenticated]


class CrearReservacionView(generics.CreateAPIView):
    queryset = Reservacion.objects.all()
    serializer_class = ReservacionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        evento = serializer.validated_data['evento']
        cantidad = serializer.validated_data['cantidad']

        if evento.cupos_disponibles < cantidad:
            raise Exception("No hay cupos disponibles")

        evento.cupos_disponibles -= cantidad
        evento.save()

        serializer.save(usuario=self.request.user)


# =========================
# USUARIOS (CRUD ADMIN)
# =========================

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


# =========================
# DASHBOARD + GRÁFICAS
# =========================

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        total_eventos = Evento.objects.count()
        total_reservaciones = Reservacion.objects.count()
        total_usuarios = User.objects.count()

        # gráfico 1: reservas por evento
        reservas_por_evento = Reservacion.objects.values(
            'evento__nombre'
        ).annotate(total=Sum('cantidad'))

        # gráfico 2: eventos por fecha
        eventos_por_fecha = Evento.objects.values(
            'fecha'
        ).annotate(total=Count('id'))

        # evento más popular
        evento_top = Reservacion.objects.values(
            'evento__nombre'
        ).annotate(total=Sum('cantidad')).order_by('-total').first()

        return Response({
            "totales": {
                "eventos": total_eventos,
                "reservaciones": total_reservaciones,
                "usuarios": total_usuarios
            },
            "graficas": {
                "reservas_por_evento": reservas_por_evento,
                "eventos_por_fecha": eventos_por_fecha
            },
            "top_evento": evento_top
        })