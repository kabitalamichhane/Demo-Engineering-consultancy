from django.conf import settings
from .models import CompanyProfile


def company_profile(request):
    """
    Makes the (singleton) CompanyProfile available in every template as
    `company`, so header/footer/contact details stay editable from Admin
    without touching any template code.
    """
    profile = CompanyProfile.objects.first()
    facebook = (profile.facebook_url if profile and profile.facebook_url
                else getattr(settings, 'DEFAULT_FACEBOOK_URL', ''))
    switcher = getattr(settings, 'ENABLE_LANGUAGE_SWITCHER', False)
    chosen = request.COOKIES.get('hes_lang', '')
    return {
        'ui_lang': chosen if switcher and chosen in ('ne', 'hi') else 'en',
        'company': profile,
        'facebook_url': facebook,
        'enable_translate': switcher,
    }
