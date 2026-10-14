"""Template tags that print SEO data. Load with {% load seo_tags %}."""
from django import template
from django.utils.safestring import mark_safe

from company import seo

register = template.Library()


def _script(data):
    return mark_safe(
        '<script type="application/ld+json">' + seo.jsonld(data) + '</script>'
    )


@register.simple_tag(takes_context=True)
def site_jsonld(context):
    """Company + website schema (every page)."""
    request = context.get('request')
    if request is None:
        return ''
    return _script(seo.business_schema(request, context.get('company')))


_BUILDERS = {
    'service': seo.service_schema,
    'article': seo.article_schema,
    'job': seo.job_schema,
}


@register.simple_tag(takes_context=True)
def page_jsonld(context):
    """
    Page-specific schemas. A view lists what it wants in `seo_schemas`:
        [('service', service_obj), ('breadcrumbs', [('Services', '/services/')])]
    (a ready-made dict is also accepted).
    """
    request = context.get('request')
    if request is None:
        return ''
    company = context.get('company')
    scripts = []
    for item in context.get('seo_schemas') or []:
        if isinstance(item, tuple):
            kind, payload = item
            if kind == 'breadcrumbs':
                data = seo.breadcrumb_schema(request, payload)
            else:
                data = _BUILDERS[kind](request, payload, company)
        else:
            data = item
        scripts.append(_script(data))
    return mark_safe(''.join(scripts))


@register.simple_tag(takes_context=True)
def share_image_url(context):
    """Absolute URL of the picture used in link previews."""
    request = context.get('request')
    if request is None:
        return ''
    return seo.share_image_url(request, context.get('seo_image'), context.get('company'))
