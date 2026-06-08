from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Evento, Reservacion


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "is_staff"]
        extra_kwargs = {
            "password": {"write_only": True},
            "is_staff": {"required": False},
        }

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            is_staff=validated_data.get("is_staff", False),
        )


class RegisterUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=4)
    is_staff = serializers.BooleanField(read_only=True)

    def validate_username(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("El usuario es obligatorio.")
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Este usuario ya existe.")
        return value

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            is_staff=False,
        )


class LoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "is_staff"]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = LoginUserSerializer(self.user).data
        return data


class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = "__all__"

    def validate(self, attrs):
        capacidad = attrs.get("capacidad", getattr(self.instance, "capacidad", None))
        cupos = attrs.get("cupos_disponibles", getattr(self.instance, "cupos_disponibles", None))

        if capacidad is not None and capacidad < 0:
            raise serializers.ValidationError({"capacidad": "La capacidad no puede ser negativa."})

        if cupos is not None and cupos < 0:
            raise serializers.ValidationError({"cupos_disponibles": "Los cupos no pueden ser negativos."})

        if capacidad is not None and cupos is not None and cupos > capacidad:
            raise serializers.ValidationError(
                {"cupos_disponibles": "Los cupos disponibles no pueden superar la capacidad."}
            )

        return attrs


class ReservacionSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source="usuario.username", read_only=True)
    evento_nombre = serializers.CharField(source="evento.nombre", read_only=True)

    class Meta:
        model = Reservacion
        fields = [
            "id",
            "usuario",
            "usuario_nombre",
            "evento",
            "evento_nombre",
            "cantidad",
            "fecha_reservacion",
            "estado",
        ]
        read_only_fields = [
            "usuario",
            "usuario_nombre",
            "evento_nombre",
            "fecha_reservacion",
            "estado",
        ]

    def validate_cantidad(self, value):
        if value <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor a cero.")
        return value
