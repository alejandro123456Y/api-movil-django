from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Evento, Reservacion


def broadcast_change(resource_type, action, instance_id):
    channel_layer = get_channel_layer()
    if channel_layer is None:
        return

    async_to_sync(channel_layer.group_send)(
        "updates",
        {
            "type": "broadcast.update",
            "message": {
                "type": resource_type,
                "action": action,
                "id": instance_id,
                "timestamp": timezone.now().isoformat(),
            },
        },
    )


@receiver(post_save, sender=Evento)
def evento_saved(sender, instance, created, **kwargs):
    broadcast_change("evento", "created" if created else "updated", instance.id)
    broadcast_change("dashboard", "updated", instance.id)


@receiver(post_delete, sender=Evento)
def evento_deleted(sender, instance, **kwargs):
    broadcast_change("evento", "deleted", instance.id)
    broadcast_change("dashboard", "updated", instance.id)


@receiver(post_save, sender=Reservacion)
def reservacion_saved(sender, instance, created, **kwargs):
    broadcast_change("reservacion", "created" if created else "updated", instance.id)
    broadcast_change("evento", "updated", instance.evento_id)
    broadcast_change("dashboard", "updated", instance.id)


@receiver(post_delete, sender=Reservacion)
def reservacion_deleted(sender, instance, **kwargs):
    broadcast_change("reservacion", "deleted", instance.id)
    broadcast_change("dashboard", "updated", instance.id)


@receiver(post_save, sender=User)
def user_saved(sender, instance, created, **kwargs):
    broadcast_change("usuario", "created" if created else "updated", instance.id)
    broadcast_change("dashboard", "updated", instance.id)


@receiver(post_delete, sender=User)
def user_deleted(sender, instance, **kwargs):
    broadcast_change("usuario", "deleted", instance.id)
    broadcast_change("dashboard", "updated", instance.id)
