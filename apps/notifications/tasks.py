"""
Celery tasks — Telegram orqali yangi ariza haqida xabar yuborish.

Hozircha placeholder. Telegram bot sozlamalari .env ga qo'shilgandan
keyin yoqiladi:
  TELEGRAM_BOT_TOKEN=...
  TELEGRAM_CHAT_ID=...
"""
import logging

logger = logging.getLogger(__name__)


def send_new_order_notification(order_id: int):
    """
    Yangi ariza yaratilganda Telegram guruhiga xabar yuboradi.
    Celery tayyor bo'lganda @shared_task dekoratori qo'shiladi.
    """
    try:
        from apps.orders.models import Order
        order = Order.objects.select_related('vehicle', 'service').get(pk=order_id)

        message = (
            f"📋 *Yangi ariza #{order.pk}*\n\n"
            f"👤 Ism: {order.full_name}\n"
            f"📞 Telefon: {order.phone}\n"
        )
        if order.route_from or order.route_to:
            message += f"🗺 Marshrut: {order.route_from} → {order.route_to}\n"
        if order.date_needed:
            message += f"📅 Sana: {order.date_needed}\n"
        if order.vehicle:
            message += f"🚌 Transport: {order.vehicle.name}\n"
        if order.service:
            message += f"⚙️ Xizmat: {order.service.title}\n"
        if order.comment:
            message += f"💬 Izoh: {order.comment}\n"

        logger.info(f"Order #{order_id} notification (Telegram not configured yet):\n{message}")
        # TODO: bot.send_message(chat_id=settings.TELEGRAM_CHAT_ID, text=message, parse_mode='Markdown')

    except Exception as e:
        logger.error(f"Notification error for order #{order_id}: {e}")
