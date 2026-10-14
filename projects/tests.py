from django.test import TestCase
from django.urls import reverse
from .models import Project


class ProjectModelTests(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name='Demo Project', slug='demo-project', category='residential',
            status='completed', is_demo=True,
        )

    def test_project_list_page(self):
        response = self.client.get(reverse('projects:project_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Demo Project')

    def test_project_detail_page(self):
        response = self.client.get(self.project.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_project_category_filter(self):
        response = self.client.get(reverse('projects:project_list') + '?category=residential')
        self.assertContains(response, 'Demo Project')
        response = self.client.get(reverse('projects:project_list') + '?category=commercial')
        self.assertNotContains(response, 'Demo Project')
