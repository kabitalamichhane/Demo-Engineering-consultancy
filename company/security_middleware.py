"""
Adds browser-side security headers to every response:

- Content-Security-Policy: the browser only runs scripts from this site, so an
  injected <script> (XSS) cannot execute. Skipped for the admin and API docs,
  which ship their own inline scripts.
- Permissions-Policy: disables camera/microphone/geolocation etc.
- Cross-Origin-Opener-Policy: isolates the page from other windows.
"""
from django.conf import settings


class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        directives = [
            "default-src 'self'",
            "script-src 'self'",
            # inline style="" attributes are used by templates; Google Fonts CSS
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
            "font-src 'self' https://fonts.gstatic.com",
            "img-src 'self' data:",
            "frame-src https://www.google.com https://maps.google.com https://www.openstreetmap.org",
            "connect-src 'self'",
            "object-src 'none'",
            "base-uri 'self'",
            "form-action 'self'",
            "frame-ancestors 'none'",
        ]
        if not settings.DEBUG:
            directives.append('upgrade-insecure-requests')
        self.csp = '; '.join(directives)

        self.skip_prefixes = (
            '/' + settings.ADMIN_URL,
            '/api/docs/',
            '/api/redoc/',
        )

    def __call__(self, request):
        response = self.get_response(request)
        if not request.path.startswith(self.skip_prefixes):
            response.setdefault('Content-Security-Policy', self.csp)
        response.setdefault(
            'Permissions-Policy',
            'camera=(), microphone=(), geolocation=(), payment=(), usb=()',
        )
        response.setdefault('Cross-Origin-Opener-Policy', 'same-origin')
        return response
