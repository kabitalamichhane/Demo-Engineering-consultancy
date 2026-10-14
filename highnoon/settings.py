"""
Django settings for the Highnoon Engineering Solutions Pvt. Ltd. website.

Security-relevant behaviour is driven by environment variables (see .env.example).
In production the app REFUSES TO START with an insecure configuration.
"""
from datetime import timedelta
from pathlib import Path
import os

from django.core.exceptions import ImproperlyConfigured

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(name, default=False):
    val = os.environ.get(name)
    if val is None:
        return default
    return val.strip().lower() in ('1', 'true', 'yes', 'on')


def env_list(name, default=''):
    val = os.environ.get(name, default)
    return [item.strip() for item in val.split(',') if item.strip()]


def env_int(name, default):
    try:
        return int(os.environ.get(name, default))
    except (TypeError, ValueError):
        return default


# ---------------------------------------------------------------------------
# Core + fail-safe production checks
# ---------------------------------------------------------------------------
_INSECURE_DEFAULT_KEY = 'django-insecure-CHANGE-ME-IN-PRODUCTION-highnoon-engineering-solutions'
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', _INSECURE_DEFAULT_KEY)

# Local-development convenience: DEBUG defaults to True. Production MUST set
# DJANGO_DEBUG=False, and the checks below then enforce a safe configuration.
DEBUG = env_bool('DJANGO_DEBUG', True)

ALLOWED_HOSTS = env_list('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1')

if not DEBUG:
    if SECRET_KEY == _INSECURE_DEFAULT_KEY or SECRET_KEY.startswith('django-insecure') or len(SECRET_KEY) < 50:
        raise ImproperlyConfigured(
            'DJANGO_SECRET_KEY must be set to a long random value (50+ chars) when DJANGO_DEBUG=False.'
        )
    if not os.environ.get('DJANGO_ALLOWED_HOSTS') or '*' in ALLOWED_HOSTS:
        raise ImproperlyConfigured(
            "DJANGO_ALLOWED_HOSTS must list your real domain(s) (no '*') when DJANGO_DEBUG=False."
        )

SITE_URL = os.environ.get('SITE_URL', 'http://127.0.0.1:8000')
SITE_NAME = 'Highnoon Engineering Solutions Pvt. Ltd.'

# Number of reverse proxies (Nginx, Cloudflare...) that sit in front of Django and
# append to X-Forwarded-For. 0 = no proxy: the header is IGNORED (it is spoofable).
TRUSTED_PROXY_COUNT = env_int('TRUSTED_PROXY_COUNT', 0)

# Admin hardening
_admin_path = os.environ.get('ADMIN_URL', 'admin').strip('/') or 'admin'
ADMIN_URL = f'{_admin_path}/'
# Require a TOTP code (authenticator app) for the admin. On by default in production.
ADMIN_REQUIRE_2FA = env_bool('ADMIN_REQUIRE_2FA', not DEBUG)
# Swagger/ReDoc expose a map of the API: off by default in production.
ENABLE_API_DOCS = env_bool('ENABLE_API_DOCS', DEBUG)

# ---------------------------------------------------------------------------
# Applications
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.humanize',

    # Third-party
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'django_filters',
    'corsheaders',
    'drf_yasg',
    'axes',                                  # login lockout
    'django_otp',                            # two-factor auth
    'django_otp.plugins.otp_totp',
    'django_otp.plugins.otp_static',

    # Local apps
    'company',
    'services',
    'projects',
    'updates',
    'careers',
    'inquiries',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'company.security_middleware.SecurityHeadersMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'company.middleware.CompanyProfileMiddleware',
    'axes.middleware.AxesMiddleware',        # keep last
]

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',   # must be first
    'django.contrib.auth.backends.ModelBackend',
]

ROOT_URLCONF = 'highnoon.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'company.context_processors.company_profile',
            ],
        },
    },
]

WSGI_APPLICATION = 'highnoon.wsgi.application'
ASGI_APPLICATION = 'highnoon.asgi.application'

# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('DB_NAME', BASE_DIR / 'db.sqlite3'),
        'USER': os.environ.get('DB_USER', ''),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', ''),
        'PORT': os.environ.get('DB_PORT', ''),
    }
}

# ---------------------------------------------------------------------------
# Passwords
# ---------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     'OPTIONS': {'min_length': 12}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------------------------------------------------------------------------
# Internationalization
# ---------------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kathmandu'
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# Static & media files
# ---------------------------------------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# PUBLIC uploads (service/project/hero images...) — safe to serve from your web server.
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# PRIVATE uploads (CVs, quote attachments). NEVER expose this folder through
# Nginx/Apache. Files are only reachable via the staff-only /private-files/ view.
PRIVATE_MEDIA_ROOT = BASE_DIR / 'private_media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------------------------------------------------------------------
# Django REST Framework
# ---------------------------------------------------------------------------
_api_renderers = ['rest_framework.renderers.JSONRenderer']
if DEBUG:
    _api_renderers.append('rest_framework.renderers.BrowsableAPIRenderer')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_RENDERER_CLASSES': _api_renderers,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 12,
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '60/minute',
        'user': '120/minute',
        # Public POST endpoints (contact, quotes, work-with-us, appointments, applications)
        'form_submit': os.environ.get('FORM_SUBMIT_RATE', '5/hour'),
    },
    # How many proxies to trust for X-Forwarded-For (0 = ignore the header).
    'NUM_PROXIES': TRUSTED_PROXY_COUNT,
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------
CORS_ALLOWED_ORIGINS = env_list('CORS_ALLOWED_ORIGINS', '')
CORS_ALLOW_ALL_ORIGINS = env_bool('CORS_ALLOW_ALL_ORIGINS', False)

# ---------------------------------------------------------------------------
# Email
# ---------------------------------------------------------------------------
EMAIL_BACKEND = os.environ.get(
    'EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend'
)
EMAIL_HOST = os.environ.get('EMAIL_HOST', '')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = env_bool('EMAIL_USE_TLS', True)
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'info.highnoon2019@gmail.com')
COMPANY_NOTIFY_EMAIL = os.environ.get('COMPANY_NOTIFY_EMAIL', 'info.highnoon2019@gmail.com')
# Send the customer a short "we received your message" email after a form is submitted.
# Email the site owner whenever the live site hits a server error (500). Only active when DEBUG=False.
SERVER_EMAIL = os.environ.get('SERVER_EMAIL', DEFAULT_FROM_EMAIL)
if env_bool('SEND_ERROR_EMAILS', True):
    ADMINS = [('Site owner', os.environ.get('ERROR_EMAIL_TO', COMPANY_NOTIFY_EMAIL))]
EMAIL_SUBJECT_PREFIX = '[Highnoon site error] '
SEND_AUTO_REPLY = env_bool('SEND_AUTO_REPLY', True)
COMPANY_DISPLAY_NAME = os.environ.get('COMPANY_DISPLAY_NAME', 'Highnoon Engineering Solutions')
COMPANY_PHONE = os.environ.get('COMPANY_PHONE', '9856082231')

# ---------------------------------------------------------------------------
# Cache (rate limiting). LocMemCache is per-process: use Redis/Memcached in
# production if you run several workers so counts are shared.
# ---------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': os.environ.get(
            'DJANGO_CACHE_BACKEND', 'django.core.cache.backends.locmem.LocMemCache'
        ),
        'LOCATION': os.environ.get('DJANGO_CACHE_LOCATION', 'highnoon-locmem'),
    }
}

# ---------------------------------------------------------------------------
# Login lockout (django-axes) — covers the admin login AND /api/auth/token/
# ---------------------------------------------------------------------------
AXES_ENABLED = env_bool('AXES_ENABLED', True)
AXES_FAILURE_LIMIT = env_int('AXES_FAILURE_LIMIT', 5)
AXES_COOLOFF_TIME = timedelta(minutes=env_int('AXES_COOLOFF_MINUTES', 60))
AXES_LOCKOUT_PARAMETERS = ['ip_address']
AXES_RESET_ON_SUCCESS = True
# Only trust X-Forwarded-For when we really sit behind proxies (otherwise spoofable).
_axes_ip_headers = ['HTTP_X_FORWARDED_FOR', 'REMOTE_ADDR'] if TRUSTED_PROXY_COUNT > 0 else ['REMOTE_ADDR']
AXES_IPWARE_META_PRECEDENCE_ORDER = _axes_ip_headers   # django-axes >= 7
AXES_IPWARE_PROXY_COUNT = TRUSTED_PROXY_COUNT or None

# ---------------------------------------------------------------------------
# Security headers, cookies, uploads
# ---------------------------------------------------------------------------
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
CSRF_TRUSTED_ORIGINS = env_list('CSRF_TRUSTED_ORIGINS', '')

SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_AGE = 60 * 60 * 8          # staff sessions expire after 8 hours
CSRF_COOKIE_HTTPONLY = True               # no JavaScript on this site reads the CSRF cookie
CSRF_COOKIE_SAMESITE = 'Lax'

DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
DATA_UPLOAD_MAX_NUMBER_FIELDS = 200

if env_bool('DJANGO_BEHIND_PROXY_SSL', False):
    # Set ONLY when Nginx/Cloudflare terminates HTTPS and sets X-Forwarded-Proto.
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

if not DEBUG:
    SECURE_SSL_REDIRECT = env_bool('DJANGO_SECURE_SSL_REDIRECT', True)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    # Enable only once HTTPS works end-to-end (e.g. 31536000 = 1 year).
    SECURE_HSTS_SECONDS = env_int('DJANGO_HSTS_SECONDS', 0)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool('DJANGO_HSTS_INCLUDE_SUBDOMAINS', False)
    SECURE_HSTS_PRELOAD = env_bool('DJANGO_HSTS_PRELOAD', False)

LOGIN_URL = f'/{ADMIN_URL}login/'

# ---------------------------------------------------------------------------
# Security logging -> logs/security.log (+ console)
# ---------------------------------------------------------------------------
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {'format': '{asctime} {levelname} {name} {message}', 'style': '{'},
    },
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'formatter': 'verbose'},
        'security_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(LOG_DIR / 'security.log'),
            'maxBytes': 5 * 1024 * 1024,
            'backupCount': 5,
            'formatter': 'verbose',
            'delay': True,
        },
    },
    'loggers': {
        'security': {'handlers': ['console', 'security_file'], 'level': 'INFO', 'propagate': False},
        'axes': {'handlers': ['console', 'security_file'], 'level': 'INFO', 'propagate': False},
        'django.security': {'handlers': ['console', 'security_file'], 'level': 'WARNING', 'propagate': False},
    },
}


# Used when no Facebook URL has been entered in Admin -> Company Profile -> Social Media.
DEFAULT_FACEBOOK_URL = os.environ.get(
    'DEFAULT_FACEBOOK_URL', 'https://www.facebook.com/profile.php?id=61587978670735'
)

# English / Nepali / Hindi language switcher. The translations are built into the site
# (company/i18n_data) plus anything added in Admin -> Translations. No outside service is used.
# The old name ENABLE_GOOGLE_TRANSLATE is still read, so existing .env files keep working.
ENABLE_LANGUAGE_SWITCHER = env_bool('ENABLE_LANGUAGE_SWITCHER', env_bool('ENABLE_GOOGLE_TRANSLATE', True))
