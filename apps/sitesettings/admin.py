from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import SiteConfig


@admin.register(SiteConfig)
class SiteConfigAdmin(SingletonModelAdmin):
    save_on_top = True
    fieldsets = (
        ('📞 Kontakt ma\'lumotlari', {
            'fields': ('phone_main', 'phone_secondary', 'email', 'address'),
            'description': 'Sayt header, footer va contacts.html da ko\'rsatiladi.'
        }),
        ('💬 Ijtimoiy tarmoqlar va messenjerlar', {
            'fields': (
                'telegram_link', 'whatsapp_link',
                'instagram_link', 'facebook_link', 'youtube_link',
            ),
            'description': 'WhatsApp: https://wa.me/998901234567 formatida. Telegram: https://t.me/username'
        }),
        ('🕐 Ish vaqti', {
            'fields': ('work_days', 'work_hours', 'sunday_schedule', 'dispatch_hours'),
            'description': 'contacts.html da ko\'rsatiladi. Dispetcher — "круглосуточно"'
        }),
        ('⏱ Javob va yetkazib berish vaqti', {
            'fields': ('response_time_minutes', 'delivery_time_minutes'),
            'description': (
                '"Ответ менеджера в течение X минут" va '
                '"Подача: X минут по Ташкенту" uchun.'
            )
        }),
        ('📊 Statistikalar (bosh sahifa)', {
            'fields': (
                'stat_vehicles_count', 'stat_vehicles_label',
                'stat_experience_years', 'stat_categories_count',
                'stat_clients_count', 'stat_support',
            ),
            'description': (
                'Bosh sahifada: "30+ единиц", "8 лет", '
                '"500+ довольных клиентов", "24/7 диспетчер на связи"'
            )
        }),
        ('🔍 SEO', {
            'fields': ('site_title', 'site_description'),
        }),
    )
