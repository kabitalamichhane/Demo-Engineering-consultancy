from django.contrib import admin
from django.utils.html import format_html
from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_preview', 'display_order', 'active', 'updated_at')
    list_editable = ('display_order', 'active')
    list_filter = ('active',)
    search_fields = ('name', 'short_description', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('display_order', 'name')

    fieldsets = (
        (None, {'fields': ('name', 'slug', 'active', 'display_order')}),
        ('Content', {'fields': ('short_description', 'description', 'features', 'image', 'image_alt', 'icon')}),
        ('SEO', {'fields': ('seo_title', 'seo_description')}),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:36px;" />', obj.image.url)
        return '—'
    image_preview.short_description = 'Image'
