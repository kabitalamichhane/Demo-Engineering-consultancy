from django.core.cache import cache
from django.test import TestCase

from inquiries.models import ContactInquiry
from .chatbot import best_faq, is_greeting
from .models import ChatFAQ


class ChatbotMatchingTests(TestCase):
    def setUp(self):
        self.loc = ChatFAQ.objects.create(
            question='Where are you located?', keywords='location, address, ठेगाना', answer='Pokhara-14.')
        self.quote = ChatFAQ.objects.create(
            question='How can I get a quote?', keywords='quote, price, cost', answer='Use the quote form.')

    def test_keyword_match(self):
        self.assertEqual(best_faq('what is your office address', ChatFAQ.objects.all()), self.loc)
        self.assertEqual(best_faq('price for a steel gate?', ChatFAQ.objects.all()), self.quote)

    def test_devanagari_keyword_match(self):
        self.assertEqual(best_faq('तपाईंको ठेगाना के हो', ChatFAQ.objects.all()), self.loc)

    def test_no_match_returns_none(self):
        self.assertIsNone(best_faq('banana pancakes recipe', ChatFAQ.objects.all()))
        self.assertIsNone(best_faq('', ChatFAQ.objects.all()))

    def test_greeting_detection(self):
        self.assertTrue(is_greeting('Hello'))
        self.assertTrue(is_greeting('namaste'))
        self.assertFalse(is_greeting('hello what is the price'))

    def test_unsafe_link_is_dropped(self):
        faq = ChatFAQ(question='x', answer='y', link_url='javascript:alert(1)')
        self.assertEqual(faq.safe_link_url, '')
        self.assertEqual(ChatFAQ(question='x', answer='y', link_url='//evil.com').safe_link_url, '')
        self.assertEqual(ChatFAQ(question='x', answer='y', link_url='/get-a-quote/').safe_link_url, '/get-a-quote/')
        self.assertEqual(ChatFAQ(question='x', answer='y', link_url='https://example.com').safe_link_url, 'https://example.com')


class ChatbotEndpointTests(TestCase):
    def setUp(self):
        cache.clear()
        self.faq = ChatFAQ.objects.create(
            question='Where are you located?', keywords='location, address', answer='Pokhara-14.',
            link_text='Contact us', link_url='/contact-us/')
        ChatFAQ.objects.create(question='Hidden', keywords='secret', answer='no', active=False)

    def test_suggestions_list_only_active(self):
        data = self.client.get('/chatbot/faqs/').json()
        self.assertEqual([s['question'] for s in data['suggestions']], ['Where are you located?'])

    def test_ask_by_id_and_by_text(self):
        by_id = self.client.get('/chatbot/ask/', {'id': self.faq.pk}).json()
        self.assertTrue(by_id['found'])
        self.assertEqual(by_id['answer'], 'Pokhara-14.')
        self.assertEqual(by_id['link_url'], '/contact-us/')
        by_text = self.client.get('/chatbot/ask/', {'q': 'your address please'}).json()
        self.assertTrue(by_text['found'])

    def test_inactive_faq_not_answered(self):
        hidden = ChatFAQ.objects.get(question='Hidden')
        data = self.client.get('/chatbot/ask/', {'id': hidden.pk}).json()
        self.assertFalse(data['found'])

    def test_unknown_question_offers_fallback(self):
        data = self.client.get('/chatbot/ask/', {'q': 'zzz qqq'}).json()
        self.assertFalse(data['found'])
        self.assertIn('call back', data['answer'])

    def test_greeting(self):
        self.assertTrue(self.client.get('/chatbot/ask/', {'q': 'hello'}).json()['found'])

    def test_post_not_allowed_on_ask(self):
        self.assertEqual(self.client.post('/chatbot/ask/').status_code, 405)

    def test_ask_is_rate_limited(self):
        for _ in range(60):
            self.client.get('/chatbot/ask/', {'q': 'hi'})
        self.assertEqual(self.client.get('/chatbot/ask/', {'q': 'hi'}).status_code, 429)

    def test_widget_on_home_page(self):
        resp = self.client.get('/')
        self.assertContains(resp, 'id="chatbot"')
        self.assertContains(resp, 'js/chatbot.js')


class ChatbotCallbackTests(TestCase):
    def setUp(self):
        cache.clear()

    def _post(self, **extra):
        data = {'name': 'Sita', 'phone': '9800000001', 'email': 'sita@example.com'}
        data.update(extra)
        return self.client.post('/chatbot/callback/', data)

    def test_callback_creates_contact_inquiry(self):
        resp = self._post()
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json()['ok'])
        inquiry = ContactInquiry.objects.get()
        self.assertEqual(inquiry.name, 'Sita')
        self.assertIn('chatbot', inquiry.subject.lower())

    def test_invalid_email_rejected(self):
        resp = self._post(email='not-an-email')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(ContactInquiry.objects.count(), 0)

    def test_honeypot_discards_silently(self):
        resp = self._post(hp_website='http://spam.example')
        self.assertTrue(resp.json()['ok'])
        self.assertEqual(ContactInquiry.objects.count(), 0)

    def test_get_not_allowed(self):
        self.assertEqual(self.client.get('/chatbot/callback/').status_code, 405)

    def test_callback_rate_limited(self):
        for _ in range(5):
            self._post()
        self.assertEqual(self._post().status_code, 429)
