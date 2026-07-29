from django.db import models
from django.utils.text import slugify
from apps.common.models import TimeStampedModel, OrderableModel


class ServiceFeature(TimeStampedModel, OrderableModel):
    """
    Xizmat afzalliklari (services.html sahifasida):
    "Пунктуальность — Подача точно в срок"
    "24/7 сервис — Круглосуточно"
    "Гибкость — Индивидуальный подход"
    "Безопасность — Проверенные водители"
    """
    title = models.CharField(max_length=100, verbose_name='Sarlavha')
    description = models.CharField(
        max_length=200, blank=True,
        verbose_name='Qisqa tavsif',
        help_text='Masalan: Podача точно в срок'
    )
    icon = models.CharField(
        max_length=50, blank=True,
        verbose_name='Icon klassi',
        help_text='Masalan: fas fa-clock'
    )

    class Meta(OrderableModel.Meta):
        verbose_name = 'Xizmat afzalligi'
        verbose_name_plural = 'Xizmat afzalliklari'

    def __str__(self):
        return self.title


class ServiceDirection(TimeStampedModel, OrderableModel):
    """
    Xizmat yo'nalishlari (8 ta):
    Обслуживание делегаций, Туристические перевозки, Трансферы,
    VIP обслуживание, Корпоративные поездки, Международные перевозки,
    Обслуживание мероприятий, Долгосрочная аренда
    """
    title = models.CharField(max_length=150, verbose_name='Sarlavha')
    slug = models.SlugField(unique=True, max_length=180, blank=True)
    short_description = models.CharField(
        max_length=255,
        verbose_name='Qisqa tavsif',
        help_text='Kartochkada ko\'rsatiladi'
    )
    description = models.TextField(
        verbose_name="To'liq tavsif",
        help_text='Detail sahifada ko\'rsatiladi'
    )
    icon = models.CharField(max_length=50, blank=True, verbose_name='Icon klassi')
    image = models.ImageField(
        upload_to='services/', blank=True, null=True,
        verbose_name='Rasm'
    )

    # ── "Что входит в услугу" — detail sahifada ───────────────────────────────
    what_is_included = models.TextField(
        blank=True,
        verbose_name='Xizmatga nimalar kiradi (Что входит)',
        help_text='Har bir qatorga bir element yozing. Masalan:\nHaydovchi bilan avtomobil\nAeroportga kutib olish\n24/7 dispetcher'
    )

    # ── "Подходящий транспорт" — detail sahifada ManyToMany ──────────────────
    suitable_vehicles = models.ManyToManyField(
        'fleet.Vehicle',
        blank=True,
        related_name='suitable_services',
        verbose_name='Mos transport vositalari'
    )

    class Meta(OrderableModel.Meta):
        verbose_name = "Xizmat yo'nalishi"
        verbose_name_plural = "Xizmat yo'nalishlari"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def what_is_included_list(self):
        """what_is_included matnini list ga aylantiradi."""
        if not self.what_is_included:
            return []
        return [line.strip() for line in self.what_is_included.splitlines() if line.strip()]
