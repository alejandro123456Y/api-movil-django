from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Evento, Reservacion
from .serializers import (
    CustomTokenObtainPairSerializer,
    EventoSerializer,
    ReservacionSerializer,
    UserSerializer,
)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class EventoListView(generics.ListAPIView):
    queryset = Evento.objects.all().order_by("fecha", "hora", "id")
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

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(
            {"detail": "Evento eliminado correctamente."},
            status=status.HTTP_200_OK,
        )


class ReservacionListView(generics.ListAPIView):
    serializer_class = ReservacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Reservacion.objects.select_related("usuario", "evento").order_by(
            "-fecha_reservacion",
            "-id",
        )

        if self.request.user.is_staff:
            return queryset

        return queryset.filter(usuario=self.request.user)


class CrearReservacionView(generics.CreateAPIView):
    queryset = Reservacion.objects.all()
    serializer_class = ReservacionSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def perform_create(self, serializer):
        evento_id = serializer.validated_data["evento"].id
        cantidad = serializer.validated_data["cantidad"]
        evento = Evento.objects.select_for_update().get(id=evento_id)

        if evento.cupos_disponibles < cantidad:
            raise ValidationError(
                {"detail": "No hay cupos disponibles para esa cantidad."}
            )

        evento.cupos_disponibles -= cantidad
        evento.save(update_fields=["cupos_disponibles"])
        serializer.save(usuario=self.request.user, evento=evento)


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        reservas_por_evento = Reservacion.objects.values("evento__nombre").annotate(
            total=Sum("cantidad")
        )
        reservas_por_fecha = (
            Reservacion.objects.annotate(fecha=TruncDate("fecha_reservacion"))
            .values("fecha")
            .annotate(total=Sum("cantidad"))
            .order_by("fecha")
        )
        evento_top = (
            Reservacion.objects.values("evento__nombre")
            .annotate(total=Sum("cantidad"))
            .order_by("-total")
            .first()
        )
        ocupacion_eventos = {
            item["evento__nombre"]: item["total"] or 0 for item in reservas_por_evento
        }
        reservaciones_por_fecha = {
            item["fecha"].isoformat(): item["total"] or 0 for item in reservas_por_fecha
        }
        total_eventos = Evento.objects.count()
        total_reservaciones = Reservacion.objects.count()
        total_usuarios = User.objects.count()
        evento_mas_reservado = evento_top["evento__nombre"] if evento_top else None

        return Response(
            {
                "total_eventos": total_eventos,
                "total_reservaciones": total_reservaciones,
                "total_usuarios": total_usuarios,
                "evento_mas_reservado": evento_mas_reservado,
                "ocupacion_eventos": ocupacion_eventos,
                "reservaciones_por_fecha": reservaciones_por_fecha,
                "totales": {
                    "eventos": total_eventos,
                    "reservaciones": total_reservaciones,
                    "usuarios": total_usuarios,
                },
                "graficas": {
                    "reservas_por_evento": list(reservas_por_evento),
                    "reservaciones_por_fecha": list(reservas_por_fecha),
                },
                "top_evento": evento_top,
            }
        )
