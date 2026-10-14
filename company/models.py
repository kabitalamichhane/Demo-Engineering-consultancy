import re

from django.db import models
from django.core.exceptions import ValidationError


class CompanyProfile(models.Model):
    """
    Singleton-style model holding editable company-wide information.
    Administrators edit this from Django Admin instead of changing code.
    """
    company_name = models.CharField(
        max_length=255, default='Highnoon Engineering Solutions Pvt. Ltd.'
    )
    short_name = models.CharField(max_length=50, default='HES')
    tagline = models.CharField(
        max_length=255,
        default='Engineering, Construction & Metal Fabrication Solutions in Pokhara, Nepal.',
    )
    description = models.TextField(
        blank=True,
        help_text='Used on the About / Company Introduction section of the homepage.',
    )

    # Hero section (homepage) — fully editable
    hero_heading = models.CharField(
        max_length=255, default='Engineering Solutions Built for Tomorrow'
    )
    hero_subtext = models.TextField(
        default=(
            'Engineering, construction and metal fabrication solutions '
            'delivered with a commitment to quality, safety and reliability.'
        )
    )
    hero_image = models.ImageField(upload_to='company/hero/', blank=True, null=True)
    hero_button_1_text = models.CharField(max_length=50, default='Explore Our Services')
    hero_button_1_url = models.CharField(max_length=255, default='/services/')
    hero_button_2_text = models.CharField(max_length=50, default='Work With Us')
    hero_button_2_url = models.CharField(max_length=255, default='/work-with-us/')
    hero_button_3_text = models.CharField(max_length=50, default='Get a Quote')
    hero_button_3_url = models.CharField(max_length=255, default='/get-a-quote/')

    # Director's Message — shown on the homepage and About Us page
    director_name = models.CharField(
        max_length=150, blank=True,
        help_text="e.g. 'Ram Bahadur Thapa'. Leave blank to hide this section.",
    )
    director_designation = models.CharField(
        max_length=150, blank=True, default='Managing Director',
    )
    director_photo = models.ImageField(
        upload_to='company/director/', blank=True, null=True,
        help_text='Square or portrait photo recommended.',
    )
    director_quote = models.TextField(
        blank=True,
        help_text=(
            "The director's personal message — e.g. what inspired starting the "
            "company or the motivation behind the services offered."
        ),
    )

    # Featured building showcase (homepage). Leave image blank to use the bundled photo.
    showcase_image = models.ImageField(
        upload_to='company/showcase/', blank=True, null=True,
        help_text='Photo of a standout building/structure. Higher resolution is better (1200px+ tall).',
    )
    showcase_title = models.CharField(
        max_length=150, blank=True,
        help_text="Heading, e.g. 'Architecture in Metal'. Blank = default heading.",
    )
    showcase_text = models.TextField(
        blank=True,
        help_text='Short paragraph next to the photo. Blank = default text.',
    )
    showcase_caption = models.CharField(
        max_length=200, blank=True,
        help_text="Optional caption, e.g. the building/project name. Only add facts you can stand behind.",
    )

    # Address / contact
    address_line = models.CharField(max_length=255, default='Pokhara-14, BP Marg')
    city = models.CharField(max_length=100, default='Pokhara')
    country = models.CharField(max_length=100, default='Nepal')
    postal_code = models.CharField(max_length=20, default='33700')
    phone = models.CharField(max_length=30, default='9856082231')
    email = models.EmailField(default='info.highnoon2019@gmail.com')

    map_embed_url = models.URLField(
        blank=True,
        help_text='Optional Google Maps embed URL for the address above.',
    )

    team_photo = models.ImageField(
        upload_to='company/team/', blank=True, null=True,
        help_text='Group photo of your team. If empty, the built-in team photo is used.',
    )
    team_heading = models.CharField(max_length=120, blank=True, default='Meet Our Team')
    team_text = models.CharField(
        max_length=300, blank=True,
        default='The people behind Highnoon Engineering Solutions, working together to deliver quality engineering, construction and metal fabrication.',
    )

    whatsapp_enabled = models.BooleanField(
        default=True,
        help_text='Show the floating WhatsApp chat button on every page.',
    )
    whatsapp_number = models.CharField(
        max_length=20, blank=True,
        help_text="Digits with country code, e.g. 9779856082231. Leave blank to use the main phone number.",
    )
    viber_number = models.CharField(
        max_length=20, blank=True,
        help_text='Digits with country code. Leave blank to hide the Viber button.',
    )

    facebook_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)

    logo = models.ImageField(upload_to='company/branding/', blank=True, null=True)
    favicon = models.ImageField(upload_to='company/branding/', blank=True, null=True)

    # Global SEO defaults
    default_seo_title = models.CharField(
        max_length=255,
        default='Highnoon Engineering Solutions Pvt. Ltd. | Engineering, Construction & Metal Fabrication in Pokhara, Nepal',
        blank=True,
    )
    default_seo_description = models.CharField(
        max_length=300,
        default=(
            'Highnoon Engineering Solutions Pvt. Ltd. is an engineering, '
            'construction and metal fabrication company based in Pokhara, Nepal.'
        ),
        blank=True,
    )

    # Search & sharing (SEO)
    og_image = models.ImageField(
        upload_to='company/branding/', blank=True, null=True,
        verbose_name='Share image',
        help_text=(
            'Picture shown when a page link is shared on Facebook / WhatsApp / Google. '
            'Best size 1200 x 630 px. If empty, the logo is used.'
        ),
    )
    google_business_url = models.URLField(
        blank=True, verbose_name='Google Business Profile / Maps link',
        help_text='Link to the company on Google Maps (from your free Google Business Profile).',
    )
    google_review_url = models.URLField(
        blank=True, verbose_name='Google review link',
        help_text="The 'Ask for reviews' link from Google Business Profile. Adds a 'Review us on Google' link in the footer.",
    )
    google_site_verification = models.CharField(
        max_length=120, blank=True,
        help_text='Google Search Console verification code (only the code, not the whole tag).',
    )
    bing_site_verification = models.CharField(
        max_length=120, blank=True,
        help_text='Bing Webmaster Tools verification code (optional).',
    )
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True,
        help_text='Optional. Office latitude, e.g. 28.209600 (right-click the place in Google Maps to copy).',
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True,
        help_text='Optional. Office longitude, e.g. 83.985600.',
    )
    opening_hours = models.CharField(
        max_length=200, blank=True,
        help_text="Optional. Example: Su-Fr 09:00-17:00. Separate several rules with a semicolon.",
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Company Profile'
        verbose_name_plural = 'Company Profile'

    def __str__(self):
        return self.company_name

    def clean(self):
        super().clean()
        # People often paste the whole <meta ...> tag. Keep only the code.
        for field in ('google_site_verification', 'bing_site_verification'):
            value = (getattr(self, field) or '').strip()
            match = re.search(r'content\s*=\s*["\']([^"\']+)["\']', value)
            if match:
                value = match.group(1)
            setattr(self, field, value.strip('"\' '))

    def save(self, *args, **kwargs):
        if not self.pk and CompanyProfile.objects.exists():
            raise ValidationError(
                'Only one Company Profile instance is allowed. Edit the existing one.'
            )
        super().save(*args, **kwargs)

    @staticmethod
    def _intl_digits(raw):
        digits = ''.join(ch for ch in (raw or '') if ch.isdigit())
        if len(digits) == 10:          # Nepali local number, add country code
            digits = '977' + digits
        return digits

    @property
    def whatsapp_link(self):
        if not self.whatsapp_enabled:
            return ''
        from django.conf import settings
        digits = self._intl_digits(
            self.whatsapp_number or self.phone or getattr(settings, 'COMPANY_PHONE', '')
        )
        return f'https://wa.me/{digits}' if digits else ''

    @property
    def viber_link(self):
        digits = self._intl_digits(self.viber_number)
        return f'viber://chat?number=%2B{digits}' if digits else ''

    @property
    def full_address(self):
        return f'{self.address_line}, {self.city}, {self.country}, {self.postal_code}'

    @property
    def has_director_message(self):
        return bool(self.director_name and self.director_quote)


class Translation(models.Model):
    """
    A Nepali / Hindi translation of any text on the site. Use it for text typed in Admin
    (a service name, a news article, a project description...). The built-in translations
    for the standard site text live in company/i18n_data/.
    The English text must match what is shown on the page (capital letters do not matter).
    """
    english = models.TextField(
        help_text='The English text exactly as it appears on the page. Copy and paste it.',
    )
    nepali = models.TextField('Nepali', blank=True)
    hindi = models.TextField('Hindi', blank=True)

    class Meta:
        ordering = ['english']
        verbose_name = 'Translation'
        verbose_name_plural = 'Translations'

    def __str__(self):
        return self.english[:60]


class Statistic(models.Model):
    """Editable homepage statistics/counters (e.g. 'Services Offered: 11')."""
    title = models.CharField(max_length=100)
    value = models.CharField(max_length=50, help_text="e.g. '10+', '250', '100%'")
    icon = models.CharField(
        max_length=50, blank=True, help_text='Optional icon class name or short code.'
    )
    display_order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order', 'id']

    def __str__(self):
        return f'{self.title}: {self.value}'


class Client(models.Model):
    """Clients / partners shown in a logo strip. Add only real, confirmed clients."""
    name = models.CharField(max_length=150)
    logo = models.ImageField(upload_to='clients/', blank=True, null=True)
    website = models.URLField(blank=True)
    description = models.CharField(max_length=255, blank=True)
    active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name


class DirectorMessage(models.Model):
    """Short messages from the director, shown with the director's photo at the end of the homepage."""
    title = models.CharField(max_length=120, help_text="Short heading, e.g. 'Our Commitment'.")
    message = models.TextField(max_length=800)
    display_order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order', 'id']

    def __str__(self):
        return self.title


class ChatFAQ(models.Model):
    """Question & answer used by the website chatbot. The client edits these in Admin."""
    question = models.CharField(max_length=200, help_text="e.g. 'Where are you located?'")
    keywords = models.TextField(
        blank=True,
        help_text='Words or phrases that should trigger this answer, one per line or comma-separated. '
                  'Add Nepali/Hindi words too, e.g. "location, address, where, कहाँ".',
    )
    answer = models.TextField(max_length=800, help_text='Plain text only.')
    link_text = models.CharField(max_length=60, blank=True, help_text="Optional button text, e.g. 'Get a Quote'.")
    link_url = models.CharField(
        max_length=200, blank=True,
        help_text="Optional button link: a page on this site like /get-a-quote/ or a full https:// address.",
    )
    display_order = models.PositiveIntegerField(default=0)
    show_as_suggestion = models.BooleanField(default=True, help_text='Show as a quick-question button.')
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order', 'id']
        verbose_name = 'Chatbot question'
        verbose_name_plural = 'Chatbot questions'

    def __str__(self):
        return self.question

    @property
    def keyword_list(self):
        raw = self.keywords.replace(',', '\n')
        return [k.strip().lower() for k in raw.splitlines() if k.strip()]

    @property
    def safe_link_url(self):
        """Only same-site paths or https links are ever sent to the browser."""
        url = (self.link_url or '').strip()
        if url.startswith('/') and not url.startswith('//'):
            return url
        if url.startswith('https://'):
            return url
        return ''
