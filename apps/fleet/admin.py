from django.contrib import admin
from django.utils.html import format_html, mark_safe
from .models import VehicleCategory, Vehicle, VehicleImage


# ─── Inline ───────────────────────────────────────────────────────────────────

class VehicleImageInline(admin.TabularInline):
    model = VehicleImage
    extra = 1
    fields = ('image', 'image_preview', 'is_main', 'order')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:60px; border-radius:4px;"/>',
                obj.image.url
            )
        return '—'
    image_preview.short_description = "Ko'rinish"


# ─── VehicleCategory ──────────────────────────────────────────────────────────

@admin.register(VehicleCategory)
class VehicleCategoryAdmin(admin.ModelAdmin):
    list_display = ('order', 'name', 'slug', 'icon', 'vehicles_count')
    list_display_links = ('name',)
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order',)

    def vehicles_count(self, obj):
        count = obj.vehicles.filter(is_active=True).count()
        return format_html('<b>{}</b> ta', count)
    vehicles_count.short_description = 'Faol mashinalar'


# ─── Vehicle ──────────────────────────────────────────────────────────────────

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        'main_image_preview',
        'full_name_display',
        'category',
        'seats',
        'year',
        'location',
        'price_display',
        'badges_display',
        'is_active',
    )
    list_display_links = ('main_image_preview', 'full_name_display')
    list_filter = (
        'category', 'is_active',
        'has_driver', 'available_today', 'has_ac',
        'fuel_type', 'transmission', 'year',
    )
    search_fields = ('brand', 'name', 'description', 'location')
    prepopulated_fields = {'slug': ('brand', 'name')}
    list_editable = ('is_active',)
    inlines = [VehicleImageInline]
    ordering = ('category__order', 'brand', 'name')
    save_on_top = True

    fieldsets = (
        ("Asosiy ma'lumotlar", {
            'fields': ('category', 'brand', 'name', 'slug', 'year', 'location', 'is_active')
        }),
        ("Texnik xususiyatlar", {
            'fields': ('seats', 'fuel_type', 'transmission', 'color')
        }),
        ("Narx va ijara shartlari", {
            'fields': (
                'price_per_day', 'price_negotiable',
                'min_rental_days', 'discount_from_days',
                'delivery_time_minutes',
            ),
            'description': (
                '"Narx kelishiladi" belgilansa — "Цена договорная" ko\'rsatiladi. '
                '"Chegirmali ijara" — skidki ot X dney.'
            )
        }),
        ("Kartochka badge'lari (saytda ko'rinadi)", {
            'fields': ('has_driver', 'available_today', 'has_ac', 'has_climate_control'),
        }),
        ("To'liq tavsif", {
            'fields': ('description',),
        }),
        ("Подходит для (detail sahifada)", {
            'fields': ('suitable_for',),
            'description': 'Har bir qatorga bir variant. Masalan:\nDelegatsiyalar\nVIP sayohatlar'
        }),
        ("Ijara shartlari — Условия аренды (detail sahifada)", {
            'fields': ('rental_conditions',),
            'description': 'Har bir qatorga bir shart. Masalan:\nDepolit talab qilinmaydi\nBepul bekor qilish 24 soat oldin'
        }),
    )

    # ── Custom ko'rsatuv usullari ─────────────────────────────────────────────

    def main_image_preview(self, obj):
        img = obj.images.filter(is_main=True).first() or obj.images.first()
        if img:
            return format_html(
                '<img src="{}" style="height:55px;width:80px;object-fit:cover;border-radius:4px;"/>',
                img.image.url
            )
        return mark_safe('<span style="color:#aaa;font-size:11px;">Rasm yo\'q</span>')
    main_image_preview.short_description = 'Rasm'

    def full_name_display(self, obj):
        brand = format_html(
            '<span style="color:#999;font-size:11px;text-transform:uppercase;">{}</span><br>',
            obj.brand
        ) if obj.brand else ''
        return format_html('{}<b>{}</b>', brand, obj.name)
    full_name_display.short_description = 'Nomi'

    def price_display(self, obj):
        if obj.price_negotiable or not obj.price_per_day:
            return mark_safe('<span style="color:#888;font-size:12px;">Kelishiladi</span>')
        return format_html(
            '<span style="font-size:12px;">{:,.0f}<br><small style="color:#999;">so\'m/kun</small></span>',
            obj.price_per_day
        )
    price_display.short_description = 'Narx'

    def badges_display(self, obj):
        badges = []
        if obj.has_driver:
            badges.append(
                '<span style="background:#28a745;color:#fff;padding:2px 6px;'
                'border-radius:3px;font-size:10px;white-space:nowrap;">С водителем</span>'
            )
        if obj.available_today:
            badges.append(
                '<span style="background:#dc3545;color:#fff;padding:2px 6px;'
                'border-radius:3px;font-size:10px;white-space:nowrap;">Сегодня</span>'
            )
        if obj.has_ac:
            badges.append(
                '<span style="background:#17a2b8;color:#fff;padding:2px 6px;'
                'border-radius:3px;font-size:10px;">AC</span>'
            )
        if obj.has_climate_control:
            badges.append(
                '<span style="background:#6f42c1;color:#fff;padding:2px 6px;'
                'border-radius:3px;font-size:10px;">Климат</span>'
            )
        return mark_safe(' '.join(badges)) if badges else '—'
    badges_display.short_description = "Belgilar"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category').prefetch_related('images')
