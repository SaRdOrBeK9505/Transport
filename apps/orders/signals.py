from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order


@receiver(post_save, sender=Order)
def order_created_notification(sender, instance, created, **kwargs):
    """
    Yangi ariza yaratilganda Telegram xabar yuborish.
    Hozircha o'chirilgan — Celery sozlangandan keyin yoqiladi.
    """
    pass
    # if created:
    #     try:
    #         from apps.notifications.tasks import send_new_order_notification
    #         send_new_order_notification.delay(instance.id)
    #     except Exception:
    #         pass
