from django.contrib import admin
from django.utils.html import format_html
from .models import CompanyProfile, Statistic, Client, DirectorMessage, ChatFAQ, Translation


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    """Only one row should ever exist — edit the company's public details here."""

    fieldsets = (
        ('Identity', {
            'fields': ('company_name', 'short_name', 'tagline', 'description', 'logo', 'favicon')
        }),
        ('Homepage Hero', {
            'fields': (
                'hero_heading', 'hero_subtext', 'hero_image',
                'hero_button_1_text', 'hero_button_1_url',
                'hero_button_2_text', 'hero_button_2_url',
                'hero_button_3_text', 'hero_button_3_url',
            )
        }),
        ('Featured Building Showcase', {
            'fields': ('showcase_image', 'showcase_title', 'showcase_text', 'showcase_caption'),
            'description': 'The large building photo section on the homepage.',
        }),
        ('Team Photo', {
            'fields': ('team_photo', 'team_heading', 'team_text'),
            'description': 'The group photo shown in the "Meet Our Team" section (home and About Us pages).',
        }),
        ("Director's Message", {
            'fields': ('director_name', 'director_designation', 'director_photo', 'director_quote'),
            'description': (
                "Shown on the homepage and About Us page. Leave 'Director Name' blank "
                "to hide this section entirely."
            ),
        }),
        ('Contact Details', {
            'fields': ('address_line', 'city', 'country', 'postal_code', 'phone', 'email', 'map_embed_url')
        }),
        ('Chat Buttons', {
            'fields': ('whatsapp_enabled', 'whatsapp_number', 'viber_number'),
            'description': 'Floating WhatsApp / Viber buttons so customers can message you in one tap.',
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'linkedin_url', 'instagram_url', 'youtube_url'),
            'classes': ('collapse',),
        }),
        ('Default SEO', {
            'fields': ('default_seo_title', 'default_seo_description'),
        }),
        ('Google & Sharing (SEO)', {
            'fields': (
                'og_image', 'google_business_url', 'google_review_url',
                'google_site_verification', 'bing_site_verification',
                'latitude', 'longitude', 'opening_hours',
            ),
            'description': (
                'Helps Google find and show the company. Fill these in after creating the free '
                'Google Business Profile and Google Search Console accounts (see SEO_GUIDE.md).'
            ),
        }),
    )
    readonly_fields = ('updated_at',)

    def has_add_permission(self, request):
        # Enforce singleton: block "Add" once a profile already exists.
        return not CompanyProfile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ('title', 'value', 'display_order', 'active')
    list_editable = ('display_order', 'active')
    list_filter = ('active',)
    search_fields = ('title',)
    ordering = ('display_order',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo_preview', 'website', 'active', 'display_order')
    list_editable = ('active', 'display_order')
    list_filter = ('active',)
    search_fields = ('name',)
    ordering = ('display_order', 'name')

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="height:32px;" />', obj.logo.url)
        return '—'
    logo_preview.short_description = 'Logo'


@admin.register(DirectorMessage)
class DirectorMessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_order', 'active')
    list_editable = ('display_order', 'active')
    list_filter = ('active',)
    search_fields = ('title', 'message')
    ordering = ('display_order',)


@admin.register(ChatFAQ)
class ChatFAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'show_as_suggestion', 'display_order', 'active')
    list_editable = ('show_as_suggestion', 'display_order', 'active')
    list_filter = ('active', 'show_as_suggestion')
    search_fields = ('question', 'keywords', 'answer')
    ordering = ('display_order',)


@admin.register(Translation)
class TranslationAdmin(admin.ModelAdmin):
    """Nepali / Hindi text for anything typed in Admin. Empty box = shown in English."""
    list_display = ('short_english', 'has_nepali', 'has_hindi')
    search_fields = ('english', 'nepali', 'hindi')
    list_filter = ()

    @admin.display(description='English text')
    def short_english(self, obj):
        return obj.english[:90]

    @admin.display(description='Nepali', boolean=True)
    def has_nepali(self, obj):
        return bool(obj.nepali.strip())

    @admin.display(description='Hindi', boolean=True)
    def has_hindi(self, obj):
        return bool(obj.hindi.strip())
