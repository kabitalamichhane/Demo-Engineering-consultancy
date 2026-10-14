from django.core.cache import cache
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from services.models import Service


class PublicAPITests(TestCase):
    def setUp(self):
        cache.clear()
        self.api = APIClient()
        Service.objects.create(
            name='Structural Engineering', slug='structural-engineering',
            short_description='Structural engineering services.',
            description='Full description.', active=True,
        )

    def test_services_list_public(self):
        response = self.api.get('/api/services/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_services_write_requires_auth(self):
        response = self.api.post('/api/services/', {'name': 'New Service'})
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))
