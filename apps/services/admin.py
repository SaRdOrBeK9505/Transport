from django.contrib import admin
from django.utils.html import format_html
from .models import ServiceDirection, ServiceFeature


# ─── ServiceFeature ───────────────────────────────────────────────────────────

@admin.register(ServiceFeature)
class ServiceFeatureAdmin(admin.ModelAdmin):
    """
    Xizmat afzalliklari — services.html sahifasida ko'rsatiladi.
    Masalan: Пунктуальность, 24/7 сервис, Гибкость, Безопасность
    """
    list_display = ('order', 'icon_preview', 'title', 'description', 'icon')
    list_display_links = ('icon_preview', 'title')
    list_editable = ('order',)
    ordering = ('order',)
    save_on_top = True

    def icon_preview(self, obj):
        if obj.icon:
            return format_html(
                '<i class="{}" style="font-size:18px;color:#555;"></i>',
                obj.icon
            )
        return '—'
    icon_preview.short_description = 'Icon'


# ─── ServiceDirection ─────────────────────────────────────────────────────────

class SuitableVehicleInline(admin.TabularInline):
    """Xizmatga mos transport vositalari (ManyToMany)."""
    model = ServiceDirection.suitable_vehicles.through
    verbose_name = 'Mos transport vositasi'
    verbose_name_plural = "Mos transport vositalari"
    extra = 1


@admin.register(ServiceDirection)
class ServiceDirectionAdmin(admin.ModelAdmin):
    list_display = (
        'order', 'image_preview', 'title',
        'short_description', 'suitable_vehicles_count'
    )
    list_display_links = ('image_preview', 'title')
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('order',)
    search_fields = ('title', 'short_description', 'description')
    save_on_top = True
    inlines = [SuitableVehicleInline]

    fieldsets = (
        ("Asosiy", {
            'fields': ('title', 'slug', 'order')
        }),
        ("Kontent", {
            'fields': ('short_description', 'description'),
            'description': (
                '"Qisqa tavsif" — kartochkada ko\'rsatiladi (services.html). '
                '"To\'liq tavsif" — detail sahifada (service.html).'
            )
        }),
        ("Ko'rinish", {
            'fields': ('image', 'icon'),
            'description': (
                'Rasm — xizmat kartochkasidagi asosiy rasm. '
                'Icon — Font Awesome klassi (masalan: fas fa-plane-departure)'
            )
        }),
        ("Что входит в услугу (detail sahifada)", {
            'fields': ('what_is_included',),
            'description': 'Har bir qatorga bir element. Masalan:\nHaydovchi bilan avtomobil\nAeroportga kutib olish'
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:55px;width:80px;object-fit:cover;border-radius:4px;"/>',
                obj.image.url
            )
        return format_html('<span style="color:#aaa;font-size:11px;">Rasm yo\'q</span>')
    image_preview.short_description = 'Rasm'

    def suitable_vehicles_count(self, obj):
        count = obj.suitable_vehicles.count()
        if count:
            return format_html('<span style="color:#28a745;font-weight:bold;">{} ta</span>', count)
        return format_html('<span style="color:#aaa;">—</span>')
    suitable_vehicles_count.short_description = 'Mos mashinalar'
