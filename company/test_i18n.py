import json
from pathlib import Path

from django.conf import settings
from django.test import TestCase

from company import i18n_data, i18n_scan
from company.models import CompanyProfile, Translation


class BuiltInTranslationTests(TestCase):
    def test_every_piece_of_template_text_has_a_translation(self):
        found = i18n_scan.template_strings(Path(settings.BASE_DIR) / 'templates')
        missing = sorted(set(found) - set(i18n_data.TABLE))
        self.assertEqual(missing, [], 'Add these to company/i18n_data/: %s' % missing)

    def test_built_in_director_message_is_translated(self):
        from company.director_defaults import DEFAULT_MESSAGE, DEFAULT_TITLE
        self.assertIn(i18n_scan.normalize(DEFAULT_TITLE), i18n_data.TABLE)
        self.assertIn(i18n_scan.normalize(DEFAULT_MESSAGE), i18n_data.TABLE)

    def test_no_translation_is_empty(self):
        empty = [k for k, (ne, hi) in i18n_data.TABLE.items() if not ne.strip() or not hi.strip()]
        self.assertEqual(empty, [])

    def test_nepali_and_hindi_are_written_in_devanagari(self):
        for key, (ne, hi) in i18n_data.TABLE.items():
            if key in ('/ {}',):
                continue
            self.assertRegex(ne, r'[ऀ-ॿ]', key)
            self.assertRegex(hi, r'[ऀ-ॿ]', key)

    def test_patterns_keep_their_placeholders(self):
        for key, (ne, hi) in i18n_data.TABLE.items():
            self.assertEqual(key.count('{}'), ne.count('{}'), key)
            self.assertEqual(key.count('{}'), hi.count('{}'), key)

    def test_normalize_ignores_case_spaces_and_html_entities(self):
        self.assertEqual(i18n_scan.normalize('  View &amp;   Apply &rarr; '), 'view & apply →')


class DictionaryEndpointTests(TestCase):
    def setUp(self):
        CompanyProfile.objects.create()

    def _words(self, lang):
        response = self.client.get('/i18n/%s.json' % lang)
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/json', response['Content-Type'])
        return json.loads(response.content.decode('utf-8'))

    def test_nepali_dictionary(self):
        words = self._words('ne')
        self.assertEqual(words['home'], 'गृहपृष्ठ')
        self.assertEqual(words['get a quote'], 'कोटेशन माग्नुहोस्')

    def test_hindi_dictionary(self):
        self.assertEqual(self._words('hi')['home'], 'होम')

    def test_unknown_language_is_not_found(self):
        self.assertEqual(self.client.get('/i18n/fr.json').status_code, 404)

    def test_text_added_in_admin_is_included_and_overrides_built_in(self):
        Translation.objects.create(english='Steel Gates', nepali='स्टिलका गेटहरू', hindi='')
        Translation.objects.create(english='Home', nepali='मुख्य पृष्ठ', hindi='मुख्य पृष्ठ')
        ne, hi = self._words('ne'), self._words('hi')
        self.assertEqual(ne['steel gates'], 'स्टिलका गेटहरू')
        self.assertNotIn('steel gates', hi)        # no Hindi given: stays English
        self.assertEqual(ne['home'], 'मुख्य पृष्ठ')   # Admin wins over the built-in text

    def test_dictionary_is_read_only(self):
        self.assertEqual(self.client.post('/i18n/ne.json').status_code, 405)


class SwitcherMarkupTests(TestCase):
    def setUp(self):
        CompanyProfile.objects.create()

    def test_switcher_points_to_the_builtin_dictionary_not_google(self):
        html = self.client.get('/').content.decode()
        self.assertIn('data-dict-url="/i18n/xx.json"', html)
        self.assertIn('js/i18n.js', html)
        self.assertNotIn('translate.google', html)
        self.assertNotIn('google_translate_element', html)

    def test_page_language_follows_the_chosen_language(self):
        self.assertIn('<html lang="en">', self.client.get('/').content.decode())
        self.client.cookies['hes_lang'] = 'hi'
        html = self.client.get('/').content.decode()
        self.assertIn('<html lang="hi" class="lang-hi i18n-pending">', html)

    def test_unknown_language_cookie_is_ignored(self):
        self.client.cookies['hes_lang'] = '<script>'
        html = self.client.get('/').content.decode()
        self.assertIn('<html lang="en">', html)

    def test_robots_hides_the_dictionary(self):
        self.assertContains(self.client.get('/robots.txt'), 'Disallow: /i18n/')
