"""
Search-engine helpers: builds schema.org (JSON-LD) data and absolute URLs.

Everything is built as plain Python dicts and serialised with `jsonld()`, which
escapes characters that could close the <script> tag early. Company names or
job titles typed in Admin can therefore never break (or inject into) the page.
"""
import json

from django.conf import settings
from django.templatetags.static import static
from django.utils.safestring import mark_safe

DEFAULT_NAME = 'Highnoon Engineering Solutions Pvt. Ltd.'

EMPLOYMENT_TYPES = {
    'full_time': 'FULL_TIME',
    'part_time': 'PART_TIME',
    'contract': 'CONTRACTOR',
    'internship': 'INTERN',
    'temporary': 'TEMPORARY',
}


# ----------------------------------------------------------------- helpers

def absolute_url(request, url):
    """Turn '/media/x.jpg' into 'https://site/media/x.jpg'. Full URLs pass through."""
    if not url:
        return ''
    if str(url).startswith(('http://', 'https://')):
        return str(url)
    return request.build_absolute_uri(str(url))


def image_url(request, image):
    """Absolute URL for an ImageFieldFile / path, or '' when there is no image."""
    if not image:
        return ''
    try:
        url = image.url if hasattr(image, 'url') else str(image)
    except ValueError:  # field exists but no file is attached
        return ''
    return absolute_url(request, url)


def prune(value):
    """Recursively drop empty values so unset fields never appear in the JSON."""
    if isinstance(value, dict):
        cleaned = {k: prune(v) for k, v in value.items()}
        return {k: v for k, v in cleaned.items() if v not in (None, '', [], {})}
    if isinstance(value, list):
        cleaned = [prune(v) for v in value]
        return [v for v in cleaned if v not in (None, '', [], {})]
    return value


def jsonld(data):
    """Serialise to JSON that is safe inside <script type="application/ld+json">."""
    text = json.dumps(prune(data), ensure_ascii=False, separators=(',', ':'))
    for char, escaped in (
        ('<', '\\u003c'), ('>', '\\u003e'), ('&', '\\u0026'),
        (' ', '\\u2028'), (' ', '\\u2029'),
    ):
        text = text.replace(char, escaped)
    return mark_safe(text)


def _name(profile):
    return (profile.company_name if profile else '') or getattr(
        settings, 'COMPANY_DISPLAY_NAME', '') or DEFAULT_NAME


def logo_url(request, profile):
    if profile and profile.logo:
        return image_url(request, profile.logo)
    return absolute_url(request, static('img/logo.jpg'))


def share_image_url(request, page_image, profile):
    """Picture used for Facebook/WhatsApp/Google previews, most specific first."""
    return (
        image_url(request, page_image)
        or (image_url(request, profile.og_image) if profile else '')
        or logo_url(request, profile)
    )


def _organization(request, profile):
    """Short publisher/provider reference used inside page-level schemas."""
    return {
        '@type': 'Organization',
        'name': _name(profile),
        'url': absolute_url(request, '/'),
        'logo': {'@type': 'ImageObject', 'url': logo_url(request, profile)},
    }


# ----------------------------------------------------------- site-wide data

def business_schema(request, profile):
    """Company (LocalBusiness) + WebSite, shown on every page."""
    home = absolute_url(request, '/')
    name = _name(profile)
    phone = (profile.phone if profile else '') or getattr(settings, 'COMPANY_PHONE', '')

    same_as = []
    if profile:
        same_as = [u for u in (
            profile.facebook_url or getattr(settings, 'DEFAULT_FACEBOOK_URL', ''),
            profile.linkedin_url, profile.instagram_url, profile.youtube_url,
            profile.google_business_url,
        ) if u]
    elif getattr(settings, 'DEFAULT_FACEBOOK_URL', ''):
        same_as = [settings.DEFAULT_FACEBOOK_URL]

    geo = None
    if profile and profile.latitude is not None and profile.longitude is not None:
        geo = {
            '@type': 'GeoCoordinates',
            'latitude': float(profile.latitude),
            'longitude': float(profile.longitude),
        }

    hours = []
    if profile and profile.opening_hours:
        hours = [part.strip() for part in profile.opening_hours.split(';') if part.strip()]

    city = profile.city if profile else 'Pokhara'
    country = profile.country if profile else 'Nepal'

    organization = {
        '@type': 'GeneralContractor',
        '@id': home + '#organization',
        'name': name,
        'url': home,
        'logo': logo_url(request, profile),
        'image': share_image_url(request, None, profile),
        'description': (
            (profile.default_seo_description if profile else '')
            or f'{name} is an engineering, construction and metal fabrication company '
               f'based in {city}, {country}.'
        ),
        'telephone': phone,
        'email': profile.email if profile else '',
        'address': {
            '@type': 'PostalAddress',
            'streetAddress': profile.address_line if profile else 'Pokhara-14, BP Marg',
            'addressLocality': city,
            'postalCode': profile.postal_code if profile else '33700',
            'addressCountry': country,
        },
        'geo': geo,
        'areaServed': [
            {'@type': 'City', 'name': city},
            {'@type': 'Country', 'name': country},
        ],
        'openingHours': hours,
        'hasMap': profile.google_business_url if profile else '',
        'sameAs': same_as,
    }
    website = {
        '@type': 'WebSite',
        '@id': home + '#website',
        'url': home,
        'name': name,
        'publisher': {'@id': home + '#organization'},
    }
    return {'@context': 'https://schema.org', '@graph': [organization, website]}


# --------------------------------------------------------------- page-level

def breadcrumb_schema(request, crumbs):
    """crumbs: [('Services', '/services/'), ('Metal Fabrication', '/services/x/')]"""
    trail = [('Home', '/')] + list(crumbs)
    return {
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        'itemListElement': [
            {
                '@type': 'ListItem',
                'position': position,
                'name': label,
                'item': absolute_url(request, url),
            }
            for position, (label, url) in enumerate(trail, start=1)
        ],
    }


def service_schema(request, service, profile):
    city = profile.city if profile else 'Pokhara'
    return {
        '@context': 'https://schema.org',
        '@type': 'Service',
        'name': service.name,
        'serviceType': service.name,
        'description': service.meta_description,
        'url': absolute_url(request, service.get_absolute_url()),
        'image': image_url(request, service.image),
        'areaServed': {'@type': 'City', 'name': city},
        'provider': _organization(request, profile),
    }


def article_schema(request, update, profile):
    url = absolute_url(request, update.get_absolute_url())
    published = update.published_at or update.created_at
    return {
        '@context': 'https://schema.org',
        '@type': 'Article',
        'headline': update.title[:110],
        'description': update.meta_description,
        'image': image_url(request, update.featured_image),
        'datePublished': published.isoformat() if published else '',
        'dateModified': update.updated_at.isoformat() if update.updated_at else '',
        'mainEntityOfPage': url,
        'author': {'@type': 'Organization', 'name': update.author or _name(profile)},
        'publisher': _organization(request, profile),
    }


def job_schema(request, job, profile):
    parts = [job.description]
    if job.responsibility_list:
        parts.append('Responsibilities:\n' + '\n'.join(f'- {i}' for i in job.responsibility_list))
    if job.requirement_list:
        parts.append('Requirements:\n' + '\n'.join(f'- {i}' for i in job.requirement_list))
    return {
        '@context': 'https://schema.org',
        '@type': 'JobPosting',
        'title': job.title,
        'description': '\n\n'.join(p for p in parts if p),
        'datePosted': job.created_at.date().isoformat() if job.created_at else '',
        'validThrough': job.deadline.isoformat() if job.deadline else '',
        'employmentType': EMPLOYMENT_TYPES.get(job.employment_type, 'FULL_TIME'),
        'directApply': True,
        'url': absolute_url(request, job.get_absolute_url()),
        'hiringOrganization': {
            '@type': 'Organization',
            'name': _name(profile),
            'sameAs': absolute_url(request, '/'),
            'logo': logo_url(request, profile),
        },
        'jobLocation': {
            '@type': 'Place',
            'address': {
                '@type': 'PostalAddress',
                'addressLocality': job.location,
                'addressCountry': 'NP',
            },
        },
    }
