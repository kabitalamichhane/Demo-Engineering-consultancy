from django.contrib.sitemaps import Sitemap
from services.models import Service
from projects.models import Project
from updates.models import Update
from careers.models import Job


class StaticViewSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8

    def items(self):
        return [
            'core:home', 'core:about', 'services:service_list', 'services:metal_fabrication',
            'projects:project_list', 'updates:update_list', 'careers:job_list',
            'inquiries:work_with_us', 'inquiries:contact', 'inquiries:get_a_quote',
        ]

    def location(self, item):
        from django.urls import reverse
        return reverse(item)


class ServiceSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        # The Metal Fabrication landing page is listed once, in the static pages.
        return Service.objects.filter(active=True).exclude(slug='metal-fabrication')

    def lastmod(self, obj):
        return obj.updated_at


class ProjectSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        # Demo/placeholder projects must not be offered to Google.
        return Project.objects.filter(is_demo=False)

    def lastmod(self, obj):
        return obj.updated_at


class UpdateSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        return Update.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.updated_at


class JobSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return Job.objects.filter(active=True)

    def lastmod(self, obj):
        return obj.created_at
