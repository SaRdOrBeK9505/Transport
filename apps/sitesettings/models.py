from django.db import models
from solo.models import SingletonModel


class SiteConfig(SingletonModel):
    """
    Sayt sozlamalari — singleton (faqat bitta qator).
    Admin panelidan boshqariladi.
    Barcha dinamik matnlar, kontaktlar, statistikalar shu yerda.
    """

    # ── Kontakt ma'lumotlari ──────────────────────────────────────────────────
    phone_main = models.CharField(
        max_length=20, blank=True,
        verbose_name='Asosiy telefon',
        help_text='Masalan: +998901234567 — header va footer da ko\'rsatiladi'
    )
    phone_secondary = models.CharField(
        max_length=20, blank=True,
        verbose_name="Qo'shimcha telefon"
    )
    email = models.EmailField(blank=True, verbose_name='Email')
    address = models.CharField(
        max_length=255, blank=True,
        verbose_name='Manzil',
        help_text='Masalan: г. Ташкент, Узбекистан'
    )

    # ── WhatsApp / Telegram ───────────────────────────────────────────────────
    telegram_link = models.URLField(blank=True, verbose_name='Telegram havolasi')
    whatsapp_link = models.URLField(
        blank=True, verbose_name='WhatsApp havolasi',
        help_text='Masalan: https://wa.me/998901234567'
    )
    instagram_link = models.URLField(blank=True, verbose_name='Instagram')
    facebook_link = models.URLField(blank=True, verbose_name='Facebook')
    youtube_link = models.URLField(blank=True, verbose_name='YouTube')

    # ── Ish vaqti ─────────────────────────────────────────────────────────────
    work_days = models.CharField(
        max_length=100, blank=True,
        default='Пн — Сб',
        verbose_name='Ish kunlari'
    )
    work_hours = models.CharField(
        max_length=100, blank=True,
        default='08:00 – 20:00',
        verbose_name='Ish vaqti'
    )
    sunday_schedule = models.CharField(
        max_length=100, blank=True,
        default='по запросу',
        verbose_name='Yakshanba ish tartibi'
    )  # "Вс: по запросу"
    dispatch_hours = models.CharField(
        max_length=100, blank=True,
        default='круглосуточно',
        verbose_name='Dispetcher ish vaqti'
    )  # "Диспетчер: круглосуточно"

    # ── Javob vaqti ───────────────────────────────────────────────────────────
    response_time_minutes = models.PositiveIntegerField(
        default=15,
        verbose_name='Menejer javob vaqti (daqiqada)'
    )  # "Ответ от менеджера — в течение 15 минут"
    delivery_time_minutes = models.PositiveIntegerField(
        default=15,
        verbose_name='Avtomobil yetkazib berish vaqti (daqiqada)'
    )  # "Подача: 15 минут по Ташкенту"

    # ── Statistikalar (bosh sahifa hero bloki) ────────────────────────────────
    stat_vehicles_count = models.PositiveIntegerField(
        default=30,
        verbose_name='Texnika soni'
    )  # "30+ единиц"
    stat_vehicles_label = models.CharField(
        max_length=50, blank=True,
        default='единиц',
        verbose_name='Texnika soni — label'
    )
    stat_experience_years = models.PositiveIntegerField(
        default=8,
        verbose_name='Tajriba yillari'
    )  # "8 лет"
    stat_categories_count = models.PositiveIntegerField(
        default=6,
        verbose_name='Kategoriyalar soni'
    )  # "6 категорий"
    stat_clients_count = models.PositiveIntegerField(
        default=500,
        verbose_name='Mijozlar soni'
    )  # "500+ довольных клиентов"
    stat_support = models.CharField(
        max_length=20, blank=True,
        default='24/7',
        verbose_name="Qo'llab-quvvatlash"
    )  # "24/7 диспетчер на связи"

    # ── SEO ───────────────────────────────────────────────────────────────────
    site_title = models.CharField(
        max_length=100, blank=True,
        default='ARTRANS',
        verbose_name='Sayt nomi'
    )
    site_description = models.CharField(
        max_length=255, blank=True,
        verbose_name='Sayt tavsifi',
        help_text='Masalan: Транспортные услуги для бизнеса, туризма и частных клиентов'
    )

    class Meta:
        verbose_name = 'Sayt sozlamalari'

    def __str__(self):
        return 'Sayt sozlamalari'
