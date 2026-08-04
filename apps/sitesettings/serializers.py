from rest_framework import serializers
from .models import SiteConfig


class SiteConfigSerializer(serializers.ModelSerializer):
    """
    Public (read-only) serializer — frontend uchun alias fieldlar bilan.
    GET /api/v1/site-settings/
    """
    # Frontend "phone", "telegram", "whatsapp" deb kutayotgani uchun alias fieldlar
    phone = serializers.CharField(source='phone_main', read_only=True)
    telegram = serializers.URLField(source='telegram_link', read_only=True)
    whatsapp = serializers.URLField(source='whatsapp_link', read_only=True)

    class Meta:
        model = SiteConfig
        fields = (
            # Kontakt (asl nomlar)
            'phone_main', 'phone_secondary', 'email', 'address',
            # Alias fieldlar — frontend uchun
            'phone', 'telegram', 'whatsapp',
            # Ijtimoiy tarmoqlar (asl nomlar)
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


class AdminSiteConfigSerializer(serializers.ModelSerializer):
    """
    Admin write serializer — alias fieldlarsiz, to'g'ridan-to'g'ri model maydonlari.
    PUT/PATCH /api/v1/admin/site-settings/
    """
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
