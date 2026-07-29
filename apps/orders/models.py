from django.db import models
from django.core.exceptions import ValidationError
from apps.common.models import TimeStampedModel
from apps.common.validators import validate_phone


class Order(TimeStampedModel):
    STATUS_NEW = 'new'
    STATUS_PROCESSING = 'processing'
    STATUS_DONE = 'done'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_NEW, 'Yangi'),
        (STATUS_PROCESSING, 'Jarayonda'),
        (STATUS_DONE, 'Bajarildi'),
        (STATUS_CANCELLED, 'Bekor qilindi'),
    ]

    # ── Mijoz ma'lumotlari ────────────────────────────────────────────────────
    full_name = models.CharField(max_length=150, verbose_name='Ism-familiya')
    phone = models.CharField(
        max_length=20,
        validators=[validate_phone],
        verbose_name='Telefon'
    )

    # ── Safar ma'lumotlari ────────────────────────────────────────────────────
    route_from = models.CharField(max_length=150, blank=True, verbose_name='Qayerdan')
    route_to = models.CharField(max_length=150, blank=True, verbose_name='Qayerga')

    # car.html da 2 ta sana maydoni bor: "ДАТА НАЧАЛА" va "ДАТА КОНЦА"
    date_start = models.DateField(null=True, blank=True, verbose_name='Boshlanish sanasi')
    date_end = models.DateField(null=True, blank=True, verbose_name='Tugash sanasi')

    # ── Bog'lanishlar ─────────────────────────────────────────────────────────
    vehicle = models.ForeignKey(
        'fleet.Vehicle',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='orders',
        verbose_name='Transport vositasi'
    )
    service = models.ForeignKey(
        'services.ServiceDirection',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='orders',
        verbose_name="Xizmat yo'nalishi"
    )

    comment = models.TextField(blank=True, verbose_name='Izoh')

    # ── Holat ─────────────────────────────────────────────────────────────────
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
        db_index=True,
        verbose_name='Holat'
    )

    class Meta:
        verbose_name = 'Ariza'
        verbose_name_plural = 'Arizalar'
        ordering = ['-created_at']

    def clean(self):
        if self.date_start and self.date_end:
            if self.date_end < self.date_start:
                raise ValidationError('Tugash sanasi boshlanish sanasidan oldin bo\'lishi mumkin emas.')

    def __str__(self):
        return f'#{self.pk} — {self.full_name} ({self.get_status_display()})'

    @property
    def rental_days(self):
        """Ijaraning kunlar soni."""
        if self.date_start and self.date_end:
            return (self.date_end - self.date_start).days + 1
        return None
