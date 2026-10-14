import json
import re
from datetime import date, timedelta
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from careers.models import Job
from company import seo
from company.models import CompanyProfile
from projects.models import Project
from services.models import Service
from updates.models import Update


def jsonld_blocks(html):
    """All <script type="application/ld+json"> blocks of a page, parsed."""
    raw = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    return [json.loads(block) for block in raw]


def find_type(blocks, type_name):
    for block in blocks:
        for item in block.get('@graph', [block]):
            if item.get('@type') == type_name:
                return item
    return None


class SeoHelperTests(TestCase):
    def test_jsonld_cannot_close_the_script_tag(self):
        text = seo.jsonld({'a': '</script><script>alert(1)</script>', 'b': '', 'c': None, 'd': {'e': ''}})
        self.assertNotIn('<', text)
        self.assertNotIn('>', text)
        # Empty values are dropped, real values survive the round trip.
        self.assertEqual(json.loads(text), {'a': '</script><script>alert(1)</script>'})

    def test_service_alt_text_fallback_and_override(self):
        service = Service(name='Steel Gates', slug='steel-gates')
        self.assertEqual(service.image_alt_text, 'Steel Gates — Highnoon Engineering Solutions')
        service.image_alt = 'Welded steel gate at a house in Pokhara'
        self.assertEqual(service.image_alt_text, 'Welded steel gate at a house in Pokhara')

    def test_project_and_update_alt_text(self):
        self.assertIn('Tower', Project(name='Tower').image_alt_text)
        self.assertEqual(Project(name='Tower', featured_image_alt='Night view').image_alt_text, 'Night view')
        self.assertEqual(Update(title='News').image_alt_text, 'News')
        self.assertEqual(Update(title='News', featured_image_alt='Site visit').image_alt_text, 'Site visit')


class HomePageSEOTests(TestCase):
    def setUp(self):
        self.profile = CompanyProfile.objects.create(
            company_name='Test Fabrication Co',
            phone='9800000000',
            email='hello@example.com',
            facebook_url='https://www.facebook.com/example',
        )

    def test_basic_meta_tags(self):
        html = self.client.get('/').content.decode()
        self.assertIn('<meta name="robots" content="index, follow, max-image-preview:large">', html)
        self.assertIn('rel="canonical" href="http://testserver/"', html)
        self.assertIn('<meta name="twitter:card" content="summary_large_image">', html)
        self.assertIn('<meta property="og:type" content="website">', html)
        # No share image uploaded: falls back to the bundled logo, as a full URL.
        self.assertRegex(html, r'property="og:image" content="http://testserver/[^"]*logo[^"]*"')

    def test_business_schema(self):
        blocks = jsonld_blocks(self.client.get('/').content.decode())
        company = find_type(blocks, 'GeneralContractor')
        self.assertIsNotNone(company)
        self.assertEqual(company['name'], 'Test Fabrication Co')
        self.assertEqual(company['telephone'], '9800000000')
        self.assertEqual(company['address']['addressLocality'], 'Pokhara')
        self.assertIn('https://www.facebook.com/example', company['sameAs'])
        self.assertIsNotNone(find_type(blocks, 'WebSite'))

    def test_unset_optional_fields_are_left_out(self):
        company = find_type(jsonld_blocks(self.client.get('/').content.decode()), 'GeneralContractor')
        self.assertNotIn('geo', company)
        self.assertNotIn('openingHours', company)
        self.assertNotIn('hasMap', company)

    def test_geo_hours_and_map_link(self):
        self.profile.latitude = Decimal('28.2096')
        self.profile.longitude = Decimal('83.9856')
        self.profile.opening_hours = 'Su-Fr 09:00-17:00; Sa 10:00-14:00'
        self.profile.google_business_url = 'https://maps.app.goo.gl/example'
        self.profile.save()
        company = find_type(jsonld_blocks(self.client.get('/').content.decode()), 'GeneralContractor')
        self.assertEqual(company['geo']['latitude'], 28.2096)
        self.assertEqual(company['geo']['longitude'], 83.9856)
        self.assertEqual(company['openingHours'], ['Su-Fr 09:00-17:00', 'Sa 10:00-14:00'])
        self.assertEqual(company['hasMap'], 'https://maps.app.goo.gl/example')
        self.assertIn('https://maps.app.goo.gl/example', company['sameAs'])

    def test_company_name_cannot_break_out_of_the_schema_script(self):
        evil = '</script><script>alert(1)</script>'
        self.profile.company_name = evil
        self.profile.save()
        html = self.client.get('/').content.decode()
        self.assertNotIn('</script><script>alert(1)', html)
        company = find_type(jsonld_blocks(html), 'GeneralContractor')
        self.assertEqual(company['name'], evil)

    def test_verification_tags_only_when_set(self):
        html = self.client.get('/').content.decode()
        self.assertNotIn('google-site-verification', html)
        self.assertNotIn('msvalidate.01', html)

        self.profile.google_site_verification = 'abc123'
        self.profile.bing_site_verification = 'xyz789'
        self.profile.save()
        html = self.client.get('/').content.decode()
        self.assertIn('<meta name="google-site-verification" content="abc123">', html)
        self.assertIn('<meta name="msvalidate.01" content="xyz789">', html)

    def test_pasting_the_whole_meta_tag_keeps_only_the_code(self):
        profile = CompanyProfile(
            google_site_verification='<meta name="google-site-verification" content="CODE_1" />',
            bing_site_verification='  plain-code  ',
        )
        profile.clean()
        self.assertEqual(profile.google_site_verification, 'CODE_1')
        self.assertEqual(profile.bing_site_verification, 'plain-code')

    def test_google_review_link_in_footer(self):
        self.assertNotContains(self.client.get('/'), 'Review us on Google')
        self.profile.google_review_url = 'https://g.page/r/example/review'
        self.profile.save()
        self.assertContains(self.client.get('/'), 'https://g.page/r/example/review')
        self.assertContains(self.client.get('/'), 'Review us on Google')


class DetailPageSchemaTests(TestCase):
    def test_service_page_has_service_and_breadcrumbs(self):
        service = Service.objects.create(
            name='Steel Gates', slug='steel-gates',
            short_description='Custom gates.', description='Full description.',
        )
        blocks = jsonld_blocks(self.client.get(service.get_absolute_url()).content.decode())
        self.assertEqual(find_type(blocks, 'Service')['name'], 'Steel Gates')
        crumbs = find_type(blocks, 'BreadcrumbList')['itemListElement']
        self.assertEqual([c['position'] for c in crumbs], [1, 2, 3])
        self.assertEqual([c['name'] for c in crumbs], ['Home', 'Services', 'Steel Gates'])
        self.assertEqual(crumbs[2]['item'], 'http://testserver/services/steel-gates/')

    def test_metal_fabrication_landing_page_has_breadcrumbs(self):
        blocks = jsonld_blocks(self.client.get(reverse('services:metal_fabrication')).content.decode())
        crumbs = find_type(blocks, 'BreadcrumbList')['itemListElement']
        self.assertEqual([c['name'] for c in crumbs], ['Home', 'Services', 'Metal Fabrication'])

    def test_list_pages_have_breadcrumbs(self):
        for url_name, label in (
            ('services:service_list', 'Services'),
            ('projects:project_list', 'Projects'),
            ('updates:update_list', 'Updates'),
            ('careers:job_list', 'Careers'),
        ):
            blocks = jsonld_blocks(self.client.get(reverse(url_name)).content.decode())
            crumbs = find_type(blocks, 'BreadcrumbList')['itemListElement']
            self.assertEqual([c['name'] for c in crumbs], ['Home', label], url_name)

    def test_update_page_is_an_article(self):
        update = Update.objects.create(
            title='New workshop opened', slug='new-workshop', content='We opened a new workshop.',
            excerpt='A new workshop.', published=True,
        )
        html = self.client.get(update.get_absolute_url()).content.decode()
        self.assertIn('<meta property="og:type" content="article">', html)
        article = find_type(jsonld_blocks(html), 'Article')
        self.assertEqual(article['headline'], 'New workshop opened')
        self.assertTrue(article['datePublished'])
        self.assertEqual(article['author']['name'], 'Highnoon Engineering Solutions')

    def test_job_page_is_a_job_posting(self):
        deadline = date.today() + timedelta(days=10)
        job = Job.objects.create(
            title='Welder', slug='welder', description='Welding work in the workshop.',
            requirements='Two years experience', employment_type='contract', deadline=deadline,
        )
        posting = find_type(jsonld_blocks(self.client.get(job.get_absolute_url()).content.decode()), 'JobPosting')
        self.assertEqual(posting['title'], 'Welder')
        self.assertEqual(posting['employmentType'], 'CONTRACTOR')
        self.assertEqual(posting['validThrough'], deadline.isoformat())
        self.assertEqual(posting['jobLocation']['address']['addressLocality'], 'Pokhara, Nepal')
        self.assertIn('Two years experience', posting['description'])

    def test_demo_projects_are_noindex_and_real_ones_are_not(self):
        demo = Project.objects.create(name='Demo', slug='demo-project', is_demo=True)
        real = Project.objects.create(name='Real', slug='real-project', is_demo=False)
        self.assertContains(self.client.get(demo.get_absolute_url()), '<meta name="robots" content="noindex, nofollow">')
        self.assertContains(self.client.get(real.get_absolute_url()), 'content="index, follow')


class SitemapTests(TestCase):
    def setUp(self):
        Service.objects.create(name='Metal Fabrication', slug='metal-fabrication',
                               short_description='x', description='x', active=True)
        Service.objects.create(name='Steel Work', slug='steel-work',
                               short_description='x', description='x', active=True)
        Service.objects.create(name='Hidden', slug='hidden-svc',
                               short_description='x', description='x', active=False)
        Project.objects.create(name='Real', slug='real-proj', is_demo=False)
        Project.objects.create(name='Demo', slug='demo-proj', is_demo=True)
        self.xml = self.client.get('/sitemap.xml').content.decode()

    def test_metal_fabrication_landing_page_is_listed_exactly_once(self):
        self.assertEqual(self.xml.count('/services/metal-fabrication/</loc>'), 1)

    def test_active_services_and_real_projects_are_listed(self):
        self.assertIn('/services/steel-work/', self.xml)
        self.assertIn('/projects/real-proj/', self.xml)

    def test_hidden_and_demo_items_are_not_listed(self):
        self.assertNotIn('hidden-svc', self.xml)
        self.assertNotIn('demo-proj', self.xml)
