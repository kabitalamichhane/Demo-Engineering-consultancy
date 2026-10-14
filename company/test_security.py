import os
import shutil
import tempfile

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import Http404
from django.test import RequestFactory, TestCase, override_settings
from django.conf import settings

from company.security import get_client_ip, validate_uploaded_file, ALLOWED_DOCUMENT_EXTENSIONS
from company.views import private_file


class ClientIPTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def _request(self, xff):
        return self.factory.get('/', REMOTE_ADDR='203.0.113.9', HTTP_X_FORWARDED_FOR=xff)

    @override_settings(TRUSTED_PROXY_COUNT=0)
    def test_header_ignored_without_trusted_proxy(self):
        self.assertEqual(get_client_ip(self._request('1.2.3.4')), '203.0.113.9')

    @override_settings(TRUSTED_PROXY_COUNT=1)
    def test_last_entry_used_with_one_proxy_and_spoof_ignored(self):
        # attacker sent "6.6.6.6"; our proxy appended the real client "198.51.100.7"
        self.assertEqual(get_client_ip(self._request('6.6.6.6, 198.51.100.7')), '198.51.100.7')

    @override_settings(TRUSTED_PROXY_COUNT=2)
    def test_two_proxies(self):
        self.assertEqual(
            get_client_ip(self._request('6.6.6.6, 198.51.100.7, 172.16.0.1')), '198.51.100.7'
        )


class FileValidationTests(TestCase):
    def _file(self, name, content):
        return SimpleUploadedFile(name, content)

    def test_valid_pdf_passes(self):
        f = self._file('cv.pdf', b'%PDF-1.7 data')
        self.assertIs(validate_uploaded_file(f, ALLOWED_DOCUMENT_EXTENSIONS), f)

    def test_valid_docx_signature_passes(self):
        validate_uploaded_file(self._file('cv.docx', b'PK\x03\x04rest'), ALLOWED_DOCUMENT_EXTENSIONS)

    def test_wrong_extension_rejected(self):
        with self.assertRaises(ValidationError):
            validate_uploaded_file(self._file('run.exe', b'MZ..'), ALLOWED_DOCUMENT_EXTENSIONS)

    def test_extension_content_mismatch_rejected(self):
        with self.assertRaises(ValidationError):
            validate_uploaded_file(self._file('cv.pdf', b'MZ\x90\x00'), ALLOWED_DOCUMENT_EXTENSIONS)

    def test_oversize_rejected(self):
        big = self._file('cv.pdf', b'%PDF-' + b'0' * (6 * 1024 * 1024))
        with self.assertRaises(ValidationError):
            validate_uploaded_file(big, ALLOWED_DOCUMENT_EXTENSIONS)

    def test_empty_value_allowed(self):
        self.assertIsNone(validate_uploaded_file(None))


class SecurityHeaderTests(TestCase):
    def test_public_page_has_csp_and_hardening_headers(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        csp = response['Content-Security-Policy']
        self.assertIn("script-src 'self'", csp)
        self.assertIn("frame-ancestors 'none'", csp)
        self.assertIn('Permissions-Policy', response)
        self.assertEqual(response['X-Frame-Options'], 'DENY')

    def test_admin_login_exempt_from_csp(self):
        response = self.client.get('/' + settings.ADMIN_URL + 'login/')
        self.assertNotIn('Content-Security-Policy', response)

    def test_no_inline_event_handlers_in_pages(self):
        body = self.client.get('/').content.decode()
        self.assertNotIn('onerror=', body)
        self.assertNotIn('onclick=', body)

    def test_robots_does_not_reveal_admin_path(self):
        body = self.client.get('/robots.txt').content.decode()
        self.assertNotIn(settings.ADMIN_URL, body)


class PrivateFileTests(TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        os.makedirs(os.path.join(self.tmp, 'quotes', 'attachments'))
        with open(os.path.join(self.tmp, 'quotes', 'attachments', 'a.pdf'), 'wb') as fh:
            fh.write(b'%PDF-1.4 secret')
        with open(os.path.join(os.path.dirname(self.tmp), 'outside_secret.txt'), 'w') as fh:
            fh.write('top secret')
        self.addCleanup(os.remove, os.path.join(os.path.dirname(self.tmp), 'outside_secret.txt'))
        ctx = self.settings(PRIVATE_MEDIA_ROOT=self.tmp, ADMIN_REQUIRE_2FA=False)
        ctx.enable()
        self.addCleanup(ctx.disable)
        User = get_user_model()
        self.staff = User.objects.create_user('staffer', password='Str0ng-Unique-Passphrase!', is_staff=True)
        self.visitor = User.objects.create_user('visitor', password='Str0ng-Unique-Passphrase!')
        self.url = '/private-files/quotes/attachments/a.pdf'

    def test_anonymous_gets_404(self):
        self.assertEqual(self.client.get(self.url).status_code, 404)

    def test_non_staff_gets_404(self):
        self.client.force_login(self.visitor, backend='django.contrib.auth.backends.ModelBackend')
        self.assertEqual(self.client.get(self.url).status_code, 404)

    def test_staff_can_download_as_attachment(self):
        self.client.force_login(self.staff, backend='django.contrib.auth.backends.ModelBackend')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('attachment', response['Content-Disposition'])
        self.assertEqual(response['X-Content-Type-Options'], 'nosniff')
        self.assertEqual(b''.join(response.streaming_content), b'%PDF-1.4 secret')
        response.close()

    def test_path_traversal_blocked(self):
        request = RequestFactory().get('/private-files/x')
        request.user = self.staff
        with self.assertRaises(Http404):
            private_file(request, '../outside_secret.txt')

    def test_missing_file_404(self):
        self.client.force_login(self.staff, backend='django.contrib.auth.backends.ModelBackend')
        self.assertEqual(self.client.get('/private-files/nope.pdf').status_code, 404)


class LanguageSwitcherCSPTests(TestCase):
    """The language switcher is built in, so the security policy must stay strict:
    no Google addresses and no inline scripts."""

    def _csp(self):
        from django.http import HttpResponse
        from django.test import RequestFactory
        from company.security_middleware import SecurityHeadersMiddleware
        mw = SecurityHeadersMiddleware(lambda r: HttpResponse('x'))
        return mw(RequestFactory().get('/'))['Content-Security-Policy']

    def test_no_google_translate_addresses_are_allowed(self):
        csp = self._csp()
        self.assertNotIn('translate.google.com', csp)
        self.assertNotIn('translate.googleapis.com', csp)
        self.assertNotIn('translate-pa.googleapis.com', csp)

    def test_script_src_never_allows_inline_scripts(self):
        script_src = [d for d in self._csp().split('; ') if d.startswith('script-src')][0]
        self.assertNotIn('unsafe-inline', script_src)
        self.assertNotIn('unsafe-eval', script_src)
        self.assertEqual(script_src, "script-src 'self'")

    def test_dictionary_requests_are_same_origin(self):
        connect_src = [d for d in self._csp().split('; ') if d.startswith('connect-src')][0]
        self.assertEqual(connect_src, "connect-src 'self'")
