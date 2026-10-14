from django.contrib import admin
from .models import Update


@admin.register(Update)
class UpdateAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'published', 'published_at')
    list_editable = ('published',)
    list_filter = ('category', 'published')
    search_fields = ('title', 'excerpt', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    ordering = ('-published_at', '-created_at')

    fieldsets = (
        (None, {'fields': ('title', 'slug', 'category', 'author', 'published', 'published_at')}),
        ('Content', {'fields': ('excerpt', 'content', 'featured_image', 'featured_image_alt')}),
        ('SEO', {'fields': ('seo_title', 'seo_description')}),
    )
