from django.contrib import admin
from django.utils.html import format_html
from .models import PartnerClient


@admin.register(PartnerClient)
class PartnerClientAdmin(admin.ModelAdmin):
    list_display = ('order', 'logo_preview', 'name', 'website_link', 'is_active')
    list_display_links = ('logo_preview', 'name')
    list_editable = ('order', 'is_active')
    ordering = ('order',)
    search_fields = ('name',)
    list_filter = ('is_active',)
    save_on_top = True

    fieldsets = (
        ('Asosiy', {
            'fields': ('name', 'logo', 'website', 'order', 'is_active')
        }),
    )

    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="height:45px; max-width:100px; object-fit:contain; '
                'background:#f5f5f5; padding:4px; border-radius:4px;"/>',
                obj.logo.url
            )
        return format_html('<span style="color:#aaa;">Logotip yo\'q</span>')
    logo_preview.short_description = 'Logotip'

    def website_link(self, obj):
        if obj.website:
            return format_html('<a href="{}" target="_blank">{}</a>', obj.website, obj.website[:40])
        return '—'
    website_link.short_description = 'Veb-sayt'
