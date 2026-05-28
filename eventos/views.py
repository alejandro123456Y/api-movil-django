from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db.models import Sum
from django.contrib.auth.models import User

from .models import Evento, Reservacion
from .serializers import (
    EventoSerializer,
    ReservacionSerializer
)


# =========================
# EVENTOS
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

        evento.cupos_disponibles -= cantidad

        evento.save()

        serializer.save(usuario=self.request.user)


# =========================
# DASHBOARD ADMIN
# =========================

class DashboardView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        total_eventos = Evento.objects.count()

        total_reservaciones = Reservacion.objects.count()

        total_usuarios = User.objects.count()

        evento_mas_reservado = (
            Reservacion.objects
            .values('evento__nombre')
            .annotate(total=Sum('cantidad'))
            .order_by('-total')
            .first()
        )

        return Response({

            'total_eventos': total_eventos,

            'total_reservaciones': total_reservaciones,

            'total_usuarios': total_usuarios,

            'evento_mas_reservado': evento_mas_reservado

        })