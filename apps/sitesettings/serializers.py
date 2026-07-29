from rest_framework import serializers
from .models import SiteConfig


class SiteConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteConfig
        fields = (
            # Kontakt
            'phone_main', 'phone_secondary', 'email', 'address',
            # Ijtimoiy tarmoqlar
            'telegram_link', 'whatsapp_link',
            'instagram_link', 'facebook_link', 'youtube_link',
            # Ish vaqti
            'work_days', 'work_hours', 'sunday_schedule', 'dispatch_hours',
            # Javob vaqti
            'response_time_minutes', 'delivery_time_minutes',
            # Statistikalar
            'stat_vehicles_count', 'stat_vehicles_label',
            'stat_experience_years', 'stat_categories_count',
            'stat_clients_count', 'stat_support',
            # SEO
            'site_title', 'site_description',
        )
