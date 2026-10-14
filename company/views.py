import logging
import os

from django.conf import settings
from django.core.exceptions import SuspiciousFileOperation
from django.db import connection
from django.http import FileResponse, Http404, JsonResponse
from django.views.decorators.http import require_POST, require_safe
from django.shortcuts import render
from django.utils._os import safe_join

from . import i18n_data
from .director_defaults import DEFAULT_DIRECTOR_MESSAGE
from .i18n_scan import normalize
from .models import Statistic, Client, DirectorMessage, ChatFAQ, Translation
from . import chatbot
from services.models import Service
from projects.models import Project
from updates.models import Update

security_logger = logging.getLogger('security')
logger = logging.getLogger('django')


def _director_messages():
    """Active messages from Admin. On a brand-new database (no rows at all) show the
    built-in message so the section is never empty. If messages exist but are all
    unticked 'Active', the section stays hidden - that is a deliberate choice."""
    messages = list(DirectorMessage.objects.filter(active=True)[:4])
    if not messages and not DirectorMessage.objects.exists():
        messages = [DEFAULT_DIRECTOR_MESSAGE]
    return messages


def home(request):
    context = {
        'statistics': Statistic.objects.filter(active=True),
        'clients': Client.objects.filter(active=True),
        'services': Service.objects.filter(active=True)[:6],
        'featured_projects': Project.objects.filter(featured=True)[:6],
        'latest_updates': Update.objects.filter(published=True)[:3],
        'director_messages': _director_messages(),
        'seo_title': (
            'Highnoon Engineering Solutions Pvt. Ltd. | Engineering, Construction '
            '& Metal Fabrication Company in Pokhara, Nepal'
        ),
        'seo_description': (
            'Highnoon Engineering Solutions Pvt. Ltd. is an engineering, construction '
            'and metal fabrication company based in Pokhara, Nepal, offering structural '
            'engineering, building construction, infrastructure and steel fabrication services.'
        ),
    }
    return render(request, 'core/home.html', context)


def about_us(request):
    context = {
        'statistics': Statistic.objects.filter(active=True),
        'clients': Client.objects.filter(active=True),
        'seo_title': 'About Us | Highnoon Engineering Solutions Pvt. Ltd.',
        'seo_description': (
            'Learn about Highnoon Engineering Solutions Pvt. Ltd., an engineering, '
            'construction and metal fabrication company based in Pokhara, Nepal.'
        ),
    }
    return render(request, 'core/about.html', context)


def private_file(request, path):
    """
    Staff-only download of private uploads (CVs, quote attachments).
    Anyone else gets a plain 404, so the URL does not even reveal that a file exists.
    """
    user = request.user
    if not (user.is_authenticated and user.is_staff):
        raise Http404
    if settings.ADMIN_REQUIRE_2FA:
        is_verified = getattr(user, 'is_verified', None)
        if not (callable(is_verified) and is_verified()):
            raise Http404

    try:
        full_path = safe_join(settings.PRIVATE_MEDIA_ROOT, path)
    except (SuspiciousFileOperation, ValueError):
        security_logger.warning('event=private_file_traversal user=%s path=%s', user.pk, request.path)
        raise Http404
    if not os.path.isfile(full_path):
        raise Http404

    security_logger.info('event=private_file_download user=%s file=%s', user.pk, path)
    response = FileResponse(open(full_path, 'rb'), as_attachment=True)
    response['X-Content-Type-Options'] = 'nosniff'
    response['Cache-Control'] = 'private, no-store'
    return response


@require_safe
def health(request):
    """
    Tiny status page for uptime monitors: /health/
    Says only "ok" or "error" - no versions, paths or settings are revealed.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
            cursor.fetchone()
        response = JsonResponse({'status': 'ok'})
    except Exception:
        logger.exception('Health check failed: database unreachable')
        response = JsonResponse({'status': 'error'}, status=503)
    response['Cache-Control'] = 'no-store'
    return response


# ---------------------------------------------------------------------------
# FAQ chatbot endpoints
# ---------------------------------------------------------------------------
def _faq_payload(faq):
    return {
        'found': True,
        'answer': faq.answer,
        'link_text': faq.link_text if faq.safe_link_url else '',
        'link_url': faq.safe_link_url,
    }


@require_safe
def chatbot_faqs(request):
    """Quick-question buttons shown when the chat opens."""
    items = ChatFAQ.objects.filter(active=True, show_as_suggestion=True)[:6]
    return JsonResponse({'suggestions': [{'id': f.pk, 'question': f.question} for f in items]})


@require_safe
def chatbot_ask(request):
    """Answer a question (?q=...) or a suggested question (?id=...). Read-only, nothing is stored."""
    from .security import is_rate_limited

    if is_rate_limited(request, scope='chatbot', limit=60, period_seconds=3600):
        return JsonResponse(
            {'found': False, 'answer': 'You have asked many questions. Please contact our team directly.',
             'link_text': '', 'link_url': ''}, status=429)

    faq_id = request.GET.get('id', '')
    if faq_id.isdigit():
        faq = ChatFAQ.objects.filter(pk=int(faq_id), active=True).first()
        if faq:
            return JsonResponse(_faq_payload(faq))

    message = (request.GET.get('q') or '')[:200]
    if chatbot.is_greeting(message):
        return JsonResponse({
            'found': True,
            'answer': 'Hello! I am the Highnoon virtual assistant. Ask me about our services, location '
                      'or how to get a quote, or tap one of the questions below.',
            'link_text': '', 'link_url': '',
        })

    faq = chatbot.best_faq(message, ChatFAQ.objects.filter(active=True))
    if faq:
        return JsonResponse(_faq_payload(faq))
    return JsonResponse({
        'found': False,
        'answer': "I'm not sure about that one. Our team can help you directly - ask for a call back, "
                  "message us on WhatsApp, or request a quote.",
        'link_text': '', 'link_url': '',
    })


@require_POST
def chatbot_callback(request):
    """Visitor asks the team to call them back. Saved as a Contact Inquiry (shows in Admin + sends email alert)."""
    from django import forms
    from inquiries.models import ContactInquiry
    from .security import HoneypotFormMixin, is_rate_limited, log_security_event

    class CallbackForm(HoneypotFormMixin, forms.Form):
        name = forms.CharField(max_length=150)
        phone = forms.CharField(max_length=30)
        email = forms.EmailField()

    if is_rate_limited(request, scope='chatbot_callback', limit=5, period_seconds=3600):
        return JsonResponse({'ok': False, 'error': 'Too many requests. Please try again later.'}, status=429)

    form = CallbackForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'ok': False, 'error': 'Please enter your name, phone and a valid email.'}, status=400)
    if form.is_spam():
        log_security_event('honeypot_triggered', request, scope='chatbot_callback')
        return JsonResponse({'ok': True})   # bots get no signal

    ContactInquiry.objects.create(
        name=form.cleaned_data['name'],
        phone=form.cleaned_data['phone'],
        email=form.cleaned_data['email'],
        subject='Call-back request from website chatbot',
        inquiry_type='general',
        message='The visitor asked for a call back through the website chatbot.',
    )
    return JsonResponse({'ok': True})


@require_safe
def i18n_dictionary(request, lang):
    """
    Nepali / Hindi text for the language switcher: built-in translations plus anything the
    team added in Admin -> Translations (those win). Public, read-only, no personal data.
    """
    if lang not in i18n_data.LANGUAGES:
        raise Http404('Unknown language')
    words = i18n_data.builtin(lang)
    for row in Translation.objects.all():
        text = (row.nepali if lang == 'ne' else row.hindi).strip()
        if text and row.english.strip():
            words[normalize(row.english)] = text
    response = JsonResponse(words, json_dumps_params={'ensure_ascii': False})
    response['Cache-Control'] = 'public, max-age=300'
    return response
