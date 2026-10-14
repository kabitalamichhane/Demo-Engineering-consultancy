from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from company import views as company_views
from .sitemaps import StaticViewSitemap, ServiceSitemap, ProjectSitemap, UpdateSitemap, JobSitemap
from .robots import robots_txt

# Two-factor authentication for the admin: swap the default admin site's class
# BEFORE its URLs are built, so login requires a password AND an authenticator code.
if settings.ADMIN_REQUIRE_2FA:
    from django_otp.admin import OTPAdminSite
    admin.site.__class__ = OTPAdminSite

sitemaps = {
    'static': StaticViewSitemap,
    'services': ServiceSitemap,
    'projects': ProjectSitemap,
    'updates': UpdateSitemap,
    'jobs': JobSitemap,
}

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),

    # Staff-only downloads of private uploads (CVs, quote attachments)
    path('private-files/<path:path>', company_views.private_file, name='private_file'),

    # Public site
    path('', include('company.urls')),
    path('services/', include('services.urls')),
    path('projects/', include('projects.urls')),
    path('updates/', include('updates.urls')),
    path('careers/', include('careers.urls')),
    path('', include('inquiries.urls')),

    # API
    path('api/', include('api.urls')),

    # SEO
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('health/', company_views.health, name='health'),
]

# Swagger / ReDoc — only when ENABLE_API_DOCS is on (default: development only)
if settings.ENABLE_API_DOCS:
    from rest_framework import permissions
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi

    schema_view = get_schema_view(
        openapi.Info(
            title='Highnoon Engineering Solutions API',
            default_version='v1',
            description=(
                'Public and administrative API for Highnoon Engineering Solutions Pvt. Ltd. '
                '— an engineering, construction and metal fabrication company in Pokhara, Nepal.'
            ),
            contact=openapi.Contact(email='info.highnoon2019@gmail.com'),
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )
    urlpatterns += [
        path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
