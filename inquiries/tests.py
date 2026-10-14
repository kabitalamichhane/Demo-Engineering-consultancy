from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import ContactInquiry, QuoteRequest, WorkWithUsInquiry


class CacheClearingTestCase(TestCase):
    """The rate limiter stores counters in the cache; reset it between tests."""

    def setUp(self):
        super().setUp()
        cache.clear()


class ContactFormTests(CacheClearingTestCase):
    def test_contact_form_submission(self):
        response = self.client.post(reverse('inquiries:contact'), {
            'name': 'Test User', 'email': 'test@example.com', 'phone': '9800000000',
            'subject': 'Inquiry', 'inquiry_type': 'general', 'message': 'Hello there.',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ContactInquiry.objects.count(), 1)


class WorkWithUsFormTests(CacheClearingTestCase):
    def test_work_with_us_submission(self):
        response = self.client.post(reverse('inquiries:work_with_us'), {
            'full_name': 'Partner Co', 'company_name': 'Partner Pvt Ltd',
            'email': 'partner@example.com', 'phone': '9811111111',
            'organization_type': 'contractor', 'project_type': 'Industrial',
            'project_location': 'Pokhara', 'message': 'We would like to collaborate.',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(WorkWithUsInquiry.objects.count(), 1)


class SpamProtectionTests(CacheClearingTestCase):
    payload = {
        'name': 'Repeat User', 'email': 'repeat@example.com', 'phone': '9800000000',
        'subject': 'Hi', 'inquiry_type': 'general', 'message': 'Testing.',
    }

    def test_honeypot_blocks_bot_submission(self):
        response = self.client.post(reverse('inquiries:contact'), {
            **self.payload, 'hp_website': 'http://spam.example.com',
        })
        self.assertEqual(response.status_code, 302)  # bot still sees "success"
        self.assertEqual(ContactInquiry.objects.count(), 0)

    def test_rate_limit_blocks_excessive_submissions(self):
        for _ in range(5):
            self.client.post(reverse('inquiries:contact'), self.payload)
        self.assertEqual(ContactInquiry.objects.count(), 5)

        self.client.post(reverse('inquiries:contact'), self.payload)  # 6th: blocked
        self.assertEqual(ContactInquiry.objects.count(), 5)

    def test_spoofed_forwarded_header_does_not_bypass_rate_limit(self):
        """With no trusted proxy, a fake X-Forwarded-For must NOT give a fresh quota."""
        for i in range(8):
            self.client.post(
                reverse('inquiries:contact'), self.payload,
                HTTP_X_FORWARDED_FOR=f'10.0.0.{i}',
            )
        self.assertEqual(ContactInquiry.objects.count(), 5)


class QuoteAPITests(CacheClearingTestCase):
    def setUp(self):
        super().setUp()
        self.api = APIClient()

    def test_quote_post_is_public(self):
        response = self.api.post('/api/quotes/', {
            'name': 'API Test', 'email': 'api@example.com', 'phone': '9800000001',
            'service': 'Metal Fabrication', 'message': 'Need a quote.',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(QuoteRequest.objects.count(), 1)

    def test_quote_list_requires_auth(self):
        response = self.api.get('/api/quotes/')
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))


from django.core import mail
from django.test import TestCase, override_settings


@override_settings(
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    COMPANY_NOTIFY_EMAIL='owner@example.com', DEFAULT_FROM_EMAIL='site@example.com',
    SEND_AUTO_REPLY=True,
)
class NotificationTests(TestCase):
    def _make_quote(self):
        from .models import QuoteRequest
        with self.captureOnCommitCallbacks(execute=True):
            return QuoteRequest.objects.create(
                name='Ram Sharma', email='ram@example.com', phone='9800000000',
                service='Metal Fabrication', message='Need a steel gate.',
            )

    def test_new_quote_sends_alert_and_auto_reply(self):
        self._make_quote()
        self.assertEqual(len(mail.outbox), 2)
        alert, reply = mail.outbox
        self.assertEqual(alert.to, ['owner@example.com'])
        self.assertEqual(alert.reply_to, ['ram@example.com'])
        self.assertIn('Metal Fabrication', alert.body)
        self.assertEqual(reply.to, ['ram@example.com'])

    def test_editing_a_lead_does_not_resend(self):
        quote = self._make_quote()
        mail.outbox.clear()
        with self.captureOnCommitCallbacks(execute=True):
            quote.status = 'won'
            quote.save()
        self.assertEqual(len(mail.outbox), 0)

    @override_settings(SEND_AUTO_REPLY=False)
    def test_auto_reply_can_be_disabled(self):
        self._make_quote()
        self.assertEqual(len(mail.outbox), 1)

    def test_email_failure_never_breaks_submission(self):
        from unittest import mock
        with mock.patch('django.core.mail.EmailMessage.send', side_effect=OSError('smtp down')):
            quote = self._make_quote()
        self.assertTrue(quote.pk)


class LeadTrackingTests(TestCase):
    def test_tracking_fields_not_exposed_publicly(self):
        from api.serializers import QuoteRequestSerializer
        fields = QuoteRequestSerializer().fields
        for private in ('internal_notes', 'assigned_to', 'deal_value', 'follow_up_date'):
            self.assertNotIn(private, fields)

    def test_new_status_choices_exist(self):
        from .models import INQUIRY_STATUS_CHOICES
        values = [v for v, _ in INQUIRY_STATUS_CHOICES]
        for status in ('new', 'in_progress', 'quoted', 'won', 'lost'):
            self.assertIn(status, values)
