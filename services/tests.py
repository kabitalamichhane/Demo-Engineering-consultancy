from django.test import TestCase
from django.urls import reverse
from .models import Service


class ServiceModelTests(TestCase):
    def setUp(self):
        self.service = Service.objects.create(
            name='Metal Fabrication',
            slug='metal-fabrication',
            short_description='Custom metal fabrication in Pokhara, Nepal.',
            description='Full description of metal fabrication services.',
            active=True,
        )

    def test_service_detail_page(self):
        response = self.client.get(self.service.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Metal Fabrication')

    def test_metal_fabrication_landing_page(self):
        response = self.client.get(reverse('services:metal_fabrication'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Metal Fabrication Company in Pokhara, Nepal')

    def test_inactive_service_not_found(self):
        # Note: the slug 'metal-fabrication' has its own landing page that is always
        # available, so a different slug is used to test the 404 behaviour.
        hidden = Service.objects.create(
            name='Hidden Service', slug='hidden-service',
            short_description='Not public.', description='Not public.', active=False,
        )
        response = self.client.get(hidden.get_absolute_url())
        self.assertEqual(response.status_code, 404)
