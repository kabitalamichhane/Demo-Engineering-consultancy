from django.test import TestCase

from company.models import CompanyProfile, DirectorMessage


class DirectorMessageDisplayTests(TestCase):
    def setUp(self):
        CompanyProfile.objects.create()

    def _section(self, html):
        start = html.index('dmsg-section')
        return html[start:html.index('</section>', start)]

    def test_active_message_is_on_the_home_page(self):
        DirectorMessage.objects.create(title='Our promise', message='We build with care.', active=True)
        html = self.client.get('/').content.decode()
        self.assertIn('Messages from Our Director', html)
        self.assertIn('We build with care.', html)

    def test_director_section_never_uses_the_scroll_fade(self):
        # Content that starts invisible (fade-in) can stay hidden if the scroll
        # detector does not run, so this section must always be visible.
        DirectorMessage.objects.create(title='Our promise', message='We build with care.', active=True)
        section = self._section(self.client.get('/').content.decode())
        self.assertNotIn('fade-in', section)

    def test_built_in_message_shows_on_a_fresh_database(self):
        self.assertEqual(DirectorMessage.objects.count(), 0)
        html = self.client.get('/').content.decode()
        self.assertIn('Messages from Our Director', html)
        self.assertIn('Building with Trust and Quality', html)

    def test_own_message_replaces_the_built_in_one(self):
        DirectorMessage.objects.create(title='Our promise', message='We build with care.', active=True)
        html = self.client.get('/').content.decode()
        self.assertIn('We build with care.', html)
        self.assertNotIn('Building with Trust and Quality', html)

    def test_inactive_message_is_hidden(self):
        DirectorMessage.objects.create(title='Draft', message='Not ready.', active=False)
        self.assertNotContains(self.client.get('/'), 'Messages from Our Director')

    def test_message_is_the_same_on_every_visit(self):
        DirectorMessage.objects.create(title='Our promise', message='We build with care.', active=True)
        for _ in range(3):
            self.assertContains(self.client.get('/'), 'We build with care.')
