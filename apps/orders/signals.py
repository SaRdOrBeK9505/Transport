from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order


@receiver(post_save, sender=Order)
def order_created_notification(sender, instance, created, **kwargs):
    """
    Yangi ariza yaratilganda Celery orqali Telegram xabar yuborish.
    Hozircha placeholder — notifications tayyor bo'lganda yoqiladi.
    """
    if created:
        try:
            from apps.notifications.tasks import send_new_order_notification
            send_new_order_notification.delay(instance.id)
        except ImportError:
            pass
