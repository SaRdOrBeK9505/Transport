from django.db import models
from django.utils.text import slugify
from apps.common.models import TimeStampedModel, OrderableModel


class VehicleCategory(TimeStampedModel, OrderableModel):
    name = models.CharField(max_length=100, verbose_name='Nomi')
    slug = models.SlugField(unique=True, max_length=120, blank=True)
    icon = models.CharField(max_length=50, blank=True, verbose_name='Icon klassi')

    class Meta(OrderableModel.Meta):
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Vehicle(TimeStampedModel):
    category = models.ForeignKey(
        VehicleCategory,
        on_delete=models.CASCADE,
        related_name='vehicles',
        verbose_name='Kategoriya'
    )

    # ── Asosiy ma'lumotlar ────────────────────────────────────────────────────
    brand = models.CharField(max_length=100, blank=True, verbose_name='Brend')
    # Masalan: CHEVROLET, BYD, Mercedes-Benz
    name = models.CharField(max_length=150, verbose_name='Model nomi')
    # Masalan: Cobalt, Song Plus, Sprinter
    slug = models.SlugField(unique=True, max_length=180, blank=True)
    seats = models.PositiveIntegerField(verbose_name="O'rindiqlar soni")
    year = models.PositiveIntegerField(null=True, blank=True, verbose_name='Yil')
    location = models.CharField(
        max_length=100, blank=True, default='Tashkent',
        verbose_name='Joylashuv'
    )  # Kartochkada: "Ташкент"
    description = models.TextField(blank=True, verbose_name='Tavsif')

    # ── Narx ─────────────────────────────────────────────────────────────────
    price_per_day = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True,
        verbose_name="Kunlik narx (so'm)"
    )
    price_negotiable = models.BooleanField(
        default=True,
        verbose_name='Narx kelishiladi (Цена договорная)'
    )
    min_rental_days = models.PositiveIntegerField(
        default=1,
        verbose_name='Minimal ijara muddati (kun)'
    )  # "1 день · скидки от 7 дней"
    discount_from_days = models.PositiveIntegerField(
        default=7,
        verbose_name='Chegirmali ijara (kundan)'
    )  # "скидки от 7 дней"

    # ── Kartochkada ko'rsatiladigan badge'lar ─────────────────────────────────
    has_driver = models.BooleanField(
        default=False,
        verbose_name='С водителем (Haydovchi bilan)'
    )
    available_today = models.BooleanField(
        default=False,
        verbose_name='Доступно сегодня (Bugun mavjud)'
    )
    has_ac = models.BooleanField(default=False, verbose_name='Konditsioner')
    has_climate_control = models.BooleanField(default=False, verbose_name='Klimat-kontrol')

    # ── Qo'shimcha xususiyatlar (detail sahifada) ─────────────────────────────
    fuel_type = models.CharField(
        max_length=20, blank=True,
        choices=[
            ('petrol', 'Benzin'),
            ('diesel', 'Dizel'),
            ('gas', 'Gaz'),
            ('hybrid', 'Gibrid'),
            ('electric', 'Elektromobil'),
        ],
        verbose_name="Yoqilg'i turi"
    )
    transmission = models.CharField(
        max_length=20, blank=True,
        choices=[
            ('auto', 'Avtomat'),
            ('manual', 'Mexanik'),
        ],
        verbose_name='Uzatmalar qutisi'
    )
    color = models.CharField(max_length=50, blank=True, verbose_name='Rang')

    # ── "Подходит для" bo'limi — detail sahifada ──────────────────────────────
    suitable_for = models.TextField(
        blank=True,
        verbose_name='Nimaga mos (Подходит для)',
        help_text='Har bir qatorga bir variant yozing. Masalan:\nDelegatsiyalar\nVIP sayohatlar\nHavo maydoni transfer'
    )

    # ── "Условия аренды" — detail sahifada ────────────────────────────────────
    rental_conditions = models.TextField(
        blank=True,
        verbose_name='Ijara shartlari (Условия аренды)',
        help_text='Har bir qatorga bir shart yozing. Masalan:\nDepolit talab qilinmaydi\nBepul bekor qilish 24 soat oldin'
    )

    # ── Подача avtomobil vaqti ────────────────────────────────────────────────
    delivery_time_minutes = models.PositiveIntegerField(
        default=15,
        verbose_name='Yetkazib berish vaqti (daqiqada)'
    )  # "Подача: 15 минут по Ташкенту"

    is_active = models.BooleanField(default=True, verbose_name='Faol')

    class Meta:
        verbose_name = 'Transport vositasi'
        verbose_name_plural = 'Transport vositalari'
        ordering = ['category__order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            base = f'{self.brand}-{self.name}' if self.brand else self.name
            self.slug = slugify(base)
        super().save(*args, **kwargs)

    def __str__(self):
        brand_str = f'{self.brand} ' if self.brand else ''
        return f'{brand_str}{self.name} ({self.seats} o\'rindiq)'

    @property
    def display_price(self):
        if self.price_negotiable or not self.price_per_day:
            return 'Цена договорная'
        return f'{self.price_per_day:,.0f} so\'m/kun'

    @property
    def suitable_for_list(self):
        """suitable_for matnini list ga aylantiradi."""
        if not self.suitable_for:
            return []
        return [line.strip() for line in self.suitable_for.splitlines() if line.strip()]

    @property
    def rental_conditions_list(self):
        """rental_conditions matnini list ga aylantiradi."""
        if not self.rental_conditions:
            return []
        return [line.strip() for line in self.rental_conditions.splitlines() if line.strip()]


class VehicleImage(TimeStampedModel, OrderableModel):
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Transport vositasi'
    )
    image = models.ImageField(upload_to='fleet/', verbose_name='Rasm')
    is_main = models.BooleanField(default=False, verbose_name='Asosiy rasm')

    class Meta(OrderableModel.Meta):
        verbose_name = 'Rasm'
        verbose_name_plural = 'Rasmlar'

    def __str__(self):
        return f'{self.vehicle.name} — rasm #{self.order}'
