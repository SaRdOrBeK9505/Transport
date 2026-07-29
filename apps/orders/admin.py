from django.contrib import admin
from django.utils.html import format_html
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'full_name',
        'phone_link',
        'dates_display',
        'route_display',
        'vehicle_display',
        'service_display',
        'status_badge',
        'created_at',
    )
    list_display_links = ('id', 'full_name')
    list_filter = ('status', 'date_start', 'created_at', 'service', 'vehicle__category')
    search_fields = ('full_name', 'phone', 'route_from', 'route_to', 'comment')
    readonly_fields = ('created_at', 'updated_at', 'rental_days_display')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    save_on_top = True

    fieldsets = (
        ("Mijoz ma'lumotlari", {
            'fields': ('full_name', 'phone')
        }),
        ("Safar tafsilotlari", {
            'fields': (
                'route_from', 'route_to',
                'date_start', 'date_end', 'rental_days_display',
                'vehicle', 'service',
                'comment',
            )
        }),
        ('Holat', {
            'fields': ('status',)
        }),
        ('Tizim', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    STATUS_COLORS = {
        'new': '#0d6efd',
        'processing': '#fd7e14',
        'done': '#198754',
        'cancelled': '#dc3545',
    }

    # ── Custom ko'rsatuv usullari ─────────────────────────────────────────────

    def status_badge(self, obj):
        color = self.STATUS_COLORS.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background:{};color:#fff;padding:3px 10px;'
            'border-radius:12px;font-size:11px;white-space:nowrap;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Holat'

    def phone_link(self, obj):
        return format_html(
            '<a href="tel:{}" style="white-space:nowrap;">{}</a>',
            obj.phone, obj.phone
        )
    phone_link.short_description = 'Telefon'

    def dates_display(self, obj):
        if obj.date_start:
            end = f' → {obj.date_end}' if obj.date_end else ''
            days = obj.rental_days
            days_str = format_html(
                ' <small style="color:#28a745;">({} kun)</small>', days
            ) if days else ''
            return format_html(
                '<span style="font-size:12px;white-space:nowrap;">{}{}{}</span>',
                obj.date_start, end, days_str
            )
        return '—'
    dates_display.short_description = 'Sana'

    def route_display(self, obj):
        if obj.route_from or obj.route_to:
            return format_html(
                '<span style="font-size:12px;">{} → {}</span>',
                obj.route_from or '?', obj.route_to or '?'
            )
        return '—'
    route_display.short_description = 'Marshrut'

    def vehicle_display(self, obj):
        if obj.vehicle:
            brand = f'{obj.vehicle.brand} ' if obj.vehicle.brand else ''
            return format_html(
                '<span style="font-size:12px;">{}{}</span>',
                brand, obj.vehicle.name
            )
        return '—'
    vehicle_display.short_description = 'Transport'

    def service_display(self, obj):
        if obj.service:
            return format_html(
                '<span style="font-size:12px;">{}</span>',
                obj.service.title
            )
        return '—'
    service_display.short_description = 'Xizmat'

    def rental_days_display(self, obj):
        days = obj.rental_days
        if days:
            return format_html('<b>{} kun</b>', days)
        return '—'
    rental_days_display.short_description = 'Ijara muddati'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('vehicle', 'service', 'vehicle__category')
