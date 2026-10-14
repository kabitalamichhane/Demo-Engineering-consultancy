from django.contrib import admin
from django.utils.html import format_html
from .models import Project, ProjectImage


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ('image', 'caption', 'display_order', 'preview')
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.pk and obj.image:
            return format_html('<img src="{}" style="height:48px;" />', obj.image.url)
        return '—'
    preview.short_description = 'Preview'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category', 'status', 'client', 'location',
        'featured', 'is_demo', 'completion_date',
    )
    list_editable = ('featured', 'is_demo')
    list_filter = ('category', 'status', 'featured', 'is_demo')
    search_fields = ('name', 'client', 'location', 'description')
    prepopulated_fields = {'slug': ('name',)}
    date_hierarchy = 'completion_date'
    ordering = ('-featured', '-completion_date')
    inlines = [ProjectImageInline]

    fieldsets = (
        (None, {'fields': ('name', 'slug', 'category', 'status', 'featured', 'is_demo')}),
        ('Details', {'fields': ('client', 'location', 'start_date', 'completion_date', 'project_value')}),
        ('Content', {'fields': ('description', 'scope', 'featured_image', 'featured_image_alt')}),
        ('SEO', {'fields': ('seo_title', 'seo_description')}),
    )
