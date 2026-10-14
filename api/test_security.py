import shutil
import tempfile

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from api.throttles import FormSubmitThrottle
from careers.models import Job
from inquiries.models import QuoteRequest

QUOTE = {
    'name': 'API Test', 'email': 'api@example.com', 'phone': '9800000001',
    'service': 'Metal Fabrication', 'message': 'Need a quote.',
}
PDF_BYTES = b'%PDF-1.4\n%fake but correctly-signed pdf\n'


class PrivateUploadTestCase(TestCase):
    """Uploads go to a temporary private folder so tests never touch real files."""

    def setUp(self):
        cache.clear()
        self.api = APIClient()
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        ctx = self.settings(PRIVATE_MEDIA_ROOT=self.tmp)
        ctx.enable()
        self.addCleanup(ctx.disable)


class APIUploadValidationTests(PrivateUploadTestCase):
    def test_executable_attachment_rejected(self):
        bad = SimpleUploadedFile('evil.exe', b'MZ\x90\x00\x03', content_type='application/octet-stream')
        response = self.api.post('/api/quotes/', {**QUOTE, 'attachment': bad}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('attachment', response.data)
        self.assertEqual(QuoteRequest.objects.count(), 0)

    def test_fake_pdf_with_wrong_content_rejected(self):
        bad = SimpleUploadedFile('cv.pdf', b'MZ\x90\x00 this is not a pdf', content_type='application/pdf')
        response = self.api.post('/api/quotes/', {**QUOTE, 'attachment': bad}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_pdf_attachment_accepted_and_stored_privately(self):
        good = SimpleUploadedFile('drawing.pdf', PDF_BYTES, content_type='application/pdf')
        response = self.api.post('/api/quotes/', {**QUOTE, 'attachment': good}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        quote = QuoteRequest.objects.get()
        self.assertTrue(quote.attachment.path.startswith(self.tmp))
        self.assertTrue(quote.attachment.url.startswith('/private-files/'))

    def test_application_to_inactive_job_rejected(self):
        job = Job.objects.create(title='Welder', slug='welder', description='x', active=False)
        resume = SimpleUploadedFile('cv.pdf', PDF_BYTES, content_type='application/pdf')
        response = self.api.post('/api/job-applications/', {
            'job': job.pk, 'full_name': 'A B', 'email': 'a@b.com', 'phone': '9800000000',
            'resume': resume,
        }, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('job', response.data)


class APIThrottleTests(TestCase):
    def setUp(self):
        cache.clear()
        self.api = APIClient()

    def test_form_endpoint_throttled_after_limit(self):
        limit = int(FormSubmitThrottle.THROTTLE_RATES['form_submit'].split('/')[0])
        payload = {'name': 'T', 'email': 't@example.com', 'message': 'hello'}
        codes = [self.api.post('/api/contact/', payload, format='json').status_code
                 for _ in range(limit + 1)]
        self.assertEqual(codes[:limit], [status.HTTP_201_CREATED] * limit)
        self.assertEqual(codes[-1], status.HTTP_429_TOO_MANY_REQUESTS)


class LoginLockoutTests(TestCase):
    def setUp(self):
        cache.clear()
        self.password = 'Str0ng-Unique-Passphrase!'
        get_user_model().objects.create_user('locktest', password=self.password, is_staff=True)
        self.api = APIClient()
        self.url = '/api/auth/token/'

    def test_repeated_bad_logins_block_even_the_correct_password(self):
        # Sanity check: the correct password works before any failures.
        ok = self.api.post(self.url, {'username': 'locktest', 'password': self.password}, format='json')
        self.assertEqual(ok.status_code, status.HTTP_200_OK)
        self.assertIn('access', ok.data)

        for _ in range(8):
            self.api.post(self.url, {'username': 'locktest', 'password': 'wrong'}, format='json')

        # Locked out: no token is issued any more (the status may be 401 or 403).
        blocked = self.api.post(self.url, {'username': 'locktest', 'password': self.password}, format='json')
        self.assertNotEqual(blocked.status_code, status.HTTP_200_OK)
        self.assertNotIn('access', getattr(blocked, 'data', {}) or {})
