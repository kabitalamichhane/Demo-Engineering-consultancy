"""
Shared security helpers for the public-facing forms and API:

- File upload validation: size + extension allow-list + real file-content check
- Honeypot mixin to silently trap simple spam bots
- Atomic cache-based IP rate limiter
- Client IP detection that is NOT fooled by a spoofed X-Forwarded-For header
- Security event logging (logs/security.log)

None of this replaces server-level hardening (HTTPS, firewall, updates, backups).
"""
import logging
import os

from django import forms
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ValidationError

security_logger = logging.getLogger('security')

# ---------------------------------------------------------------------------
# File upload validation
# ---------------------------------------------------------------------------
ALLOWED_DOCUMENT_EXTENSIONS = ('.pdf', '.doc', '.docx')
ALLOWED_IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp')
MAX_UPLOAD_SIZE_MB = 5

# Magic bytes at the start of each file type. Stops "malware.exe" renamed to "cv.pdf".
_FILE_SIGNATURES = {
    '.pdf': (b'%PDF-',),
    '.doc': (b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1',),
    '.docx': (b'PK\x03\x04',),
    '.jpg': (b'\xff\xd8\xff',),
    '.jpeg': (b'\xff\xd8\xff',),
    '.png': (b'\x89PNG\r\n\x1a\n',),
}


def _signature_matches(ext, header):
    if ext == '.webp':
        return header[:4] == b'RIFF' and header[8:12] == b'WEBP'
    return any(header.startswith(sig) for sig in _FILE_SIGNATURES.get(ext, ()))


def validate_uploaded_file(uploaded_file, allowed_extensions=None, max_size_mb=MAX_UPLOAD_SIZE_MB):
    """
    Raises ValidationError if the file is too large, has a disallowed extension,
    or its real content does not match its extension. Returns the file otherwise.
    """
    if not uploaded_file:
        return uploaded_file

    allowed_extensions = tuple(
        allowed_extensions or (ALLOWED_DOCUMENT_EXTENSIONS + ALLOWED_IMAGE_EXTENSIONS)
    )

    if uploaded_file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f'File is too large. Maximum allowed size is {max_size_mb} MB.')

    ext = os.path.splitext(uploaded_file.name.lower())[1]
    if ext not in allowed_extensions:
        raise ValidationError(
            f'Unsupported file type. Allowed types: {", ".join(allowed_extensions)}.'
        )

    header = uploaded_file.read(12)
    uploaded_file.seek(0)
    if not _signature_matches(ext, header):
        raise ValidationError('The file content does not match its file type.')

    return uploaded_file


# ---------------------------------------------------------------------------
# Honeypot spam trap
# ---------------------------------------------------------------------------
class HoneypotFormMixin(forms.Form):
    """
    Adds an invisible field ('hp_website') that real users never see or fill in.
    Bots that fill it in have their submission silently discarded by the view.
    """
    hp_website = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'hp-field',
            'tabindex': '-1',
            'autocomplete': 'off',
        }),
        label='',
    )

    def is_spam(self):
        return bool(self.cleaned_data.get('hp_website'))


# ---------------------------------------------------------------------------
# Client IP + rate limiting
# ---------------------------------------------------------------------------
def get_client_ip(request):
    """
    Returns the real client IP.

    X-Forwarded-For is trusted ONLY when settings.TRUSTED_PROXY_COUNT > 0 (i.e. the
    site really is behind that many proxies). With N trusted proxies the genuine
    client address is the N-th entry from the RIGHT; anything an attacker puts to
    the left of it is ignored. With no proxy, the header is ignored entirely.
    """
    remote = request.META.get('REMOTE_ADDR', 'unknown')
    count = getattr(settings, 'TRUSTED_PROXY_COUNT', 0)
    if count > 0:
        forwarded = request.META.get('HTTP_X_FORWARDED_FOR', '')
        ips = [ip.strip() for ip in forwarded.split(',') if ip.strip()]
        if len(ips) >= count:
            return ips[-count]
    return remote


def log_security_event(event, request=None, **details):
    ip = get_client_ip(request) if request is not None else 'n/a'
    path = getattr(request, 'path', '-')
    extra = ' '.join(f'{key}={value}' for key, value in details.items())
    security_logger.warning('event=%s ip=%s path=%s %s', event, ip, path, extra)


def is_rate_limited(request, scope, limit=5, period_seconds=3600):
    """
    True once this IP has made more than `limit` requests to `scope` within
    `period_seconds`. Uses atomic cache operations (no read-then-write race).
    """
    key = f'ratelimit:{scope}:{get_client_ip(request)}'
    if cache.add(key, 1, timeout=period_seconds):
        return False
    try:
        count = cache.incr(key)
    except ValueError:  # key expired between add() and incr()
        cache.set(key, 1, timeout=period_seconds)
        return False
    if count > limit:
        log_security_event('rate_limited', request, scope=scope)
        return True
    return False
