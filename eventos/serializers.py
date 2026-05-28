from rest_framework import serializers

from .models import Evento, Reservacion


class EventoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Evento
        fields = '__all__'


class ReservacionSerializer(serializers.ModelSerializer):

    usuario_nombre = serializers.CharField(
        source='usuario.username',
        read_only=True
    )

    evento_nombre = serializers.CharField(
        source='evento.nombre',
        read_only=True
    )

    class Meta:
        model = Reservacion
        fields = '__all__'