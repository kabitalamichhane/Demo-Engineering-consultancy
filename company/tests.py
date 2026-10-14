from django.test import TestCase, Client as TestClientHTTP
from django.urls import reverse
from .models import CompanyProfile, Statistic, Client


class CompanyProfileTests(TestCase):
    def test_singleton_enforced(self):
        CompanyProfile.objects.create(company_name='Highnoon Engineering Solutions Pvt. Ltd.')
        with self.assertRaises(Exception):
            CompanyProfile.objects.create(company_name='Duplicate')

    def test_full_address(self):
        profile = CompanyProfile.objects.create(
            address_line='Pokhara-14, BP Marg', city='Pokhara', country='Nepal', postal_code='33700'
        )
        self.assertIn('Pokhara-14, BP Marg', profile.full_address)


class HomePageTests(TestCase):
    def setUp(self):
        self.client = TestClientHTTP()

    def test_home_page_loads(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Highnoon')

    def test_about_page_loads(self):
        response = self.client.get(reverse('core:about'))
        self.assertEqual(response.status_code, 200)


class BuildingShowcaseTests(TestCase):
    def test_homepage_shows_building_showcase_with_defaults(self):
        response = self.client.get(reverse('core:home'))
        self.assertContains(response, 'building-section')
        self.assertContains(response, 'Architecture in Metal')
        self.assertContains(response, 'featured-building.png')

    def test_admin_caption_and_title_override_defaults(self):
        CompanyProfile.objects.create(
            showcase_title='Our Signature Facade', showcase_caption='Sample caption',
        )
        response = self.client.get(reverse('core:home'))
        self.assertContains(response, 'Our Signature Facade')
        self.assertContains(response, 'Sample caption')


class HomepageAssetTests(TestCase):
    def test_homepage_references_only_bundled_static_images(self):
        import os
        from django.conf import settings
        body = self.client.get(reverse('core:home')).content.decode()
        for name in ('company-intro.jpg', 'metal-fabrication.jpg'):
            self.assertNotIn(name, body)
        self.assertTrue(os.path.exists(os.path.join(settings.BASE_DIR, 'static', 'img', 'logo.jpg')))
        self.assertTrue(os.path.exists(os.path.join(settings.BASE_DIR, 'static', 'img', 'featured-building.png')))


class TopBarAndHeroTests(TestCase):
    def test_facebook_link_and_icons_in_header(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'facebook.com/profile.php?id=61587978670735')
        self.assertContains(resp, 'tel:')
        self.assertContains(resp, 'mailto:')

    def test_home_is_active_nav_and_hero_background_present(self):
        resp = self.client.get('/')
        self.assertContains(resp, 'class="active"')
        self.assertContains(resp, 'hero-bg')


class DirectorMessagesTests(TestCase):
    def test_messages_and_photo_shown_when_active(self):
        from .models import DirectorMessage
        DirectorMessage.objects.create(title='Our Commitment', message='Quality first.')
        DirectorMessage.objects.create(title='Hidden', message='Nope.', active=False)
        resp = self.client.get('/')
        self.assertContains(resp, 'Our Commitment')
        self.assertNotContains(resp, 'Hidden')
        self.assertContains(resp, 'director.jpg')

    def test_section_hidden_without_messages(self):
        self.assertNotContains(self.client.get('/'), 'dmsg-section')


class EmailLinkTests(TestCase):
    def test_email_links_open_gmail_in_browser(self):
        for url in ['/', '/contact-us/']:
            resp = self.client.get(url)
            self.assertContains(resp, 'mail.google.com/mail/?view=cm')
            self.assertContains(resp, 'target="_blank"')

    def test_contact_page_keeps_mailto_fallback(self):
        self.assertContains(self.client.get('/contact-us/'), 'mailto:info.highnoon2019@gmail.com')


class ChatButtonTests(TestCase):
    def test_whatsapp_button_uses_main_phone_by_default(self):
        resp = self.client.get('/')
        self.assertContains(resp, 'https://wa.me/9779856082231')

    def test_viber_hidden_until_number_set(self):
        self.assertNotContains(self.client.get('/'), 'viber://')
        profile = CompanyProfile.objects.first() or CompanyProfile.objects.create(company_name='HES')
        profile.viber_number = '9779856082231'
        profile.save()
        self.assertContains(self.client.get('/'), 'viber://chat?number=%2B9779856082231')

    def test_whatsapp_can_be_switched_off(self):
        self.client.get('/')  # middleware creates the profile row
        profile = CompanyProfile.objects.first() or CompanyProfile.objects.create(company_name='HES')
        profile.whatsapp_enabled = False
        profile.save()
        self.assertNotContains(self.client.get('/'), 'wa.me')


class TeamSectionTests(TestCase):
    def test_team_section_on_home_and_about(self):
        for url in ['/', '/about-us/']:
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, 200)
            self.assertContains(resp, 'Meet Our Team')
            self.assertContains(resp, 'team.jpg')


class LanguageSwitcherTests(TestCase):
    def test_switcher_shown_with_three_languages(self):
        resp = self.client.get('/')
        self.assertContains(resp, 'data-lang="en"')
        self.assertContains(resp, 'data-lang="ne"')
        self.assertContains(resp, 'data-lang="hi"')
        self.assertContains(resp, 'js/i18n.js')

    def test_switcher_hidden_when_disabled(self):
        from django.test import override_settings
        with override_settings(ENABLE_LANGUAGE_SWITCHER=False):
            resp = self.client.get('/')
        self.assertNotContains(resp, 'data-lang="ne"')
