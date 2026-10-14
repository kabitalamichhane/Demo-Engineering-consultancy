from unittest import mock

from django.test import TestCase


class HealthCheckTests(TestCase):
    def test_health_ok(self):
        resp = self.client.get('/health/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {'status': 'ok'})
        self.assertEqual(resp['Cache-Control'], 'no-store')

    def test_health_allows_head_but_not_post(self):
        self.assertEqual(self.client.head('/health/').status_code, 200)
        self.assertEqual(self.client.post('/health/').status_code, 405)

    def test_health_reports_error_when_database_down(self):
        broken = mock.Mock()
        broken.cursor.side_effect = Exception('db down')
        with mock.patch('company.views.connection', broken):
            resp = self.client.get('/health/')
        self.assertEqual(resp.status_code, 503)
        self.assertEqual(resp.json(), {'status': 'error'})
        self.assertNotIn('db down', resp.content.decode())

    def test_health_does_not_create_company_profile(self):
        from .models import CompanyProfile
        self.client.get('/health/')
        self.assertFalse(CompanyProfile.objects.exists())

    def test_robots_hides_health(self):
        self.assertContains(self.client.get('/robots.txt'), 'Disallow: /health/')
