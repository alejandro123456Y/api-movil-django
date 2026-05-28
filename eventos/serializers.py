from rest_framework import serializers
from .models import Evento, Reservacion
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'is_staff']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            is_staff=validated_data.get('is_staff', False)
        )
        return user


class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'


class ReservacionSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='usuario.username', read_only=True)
    evento_nombre = serializers.CharField(source='evento.nombre', read_only=True)

    class Meta:
        model = Reservacion
        fields = '__all__'