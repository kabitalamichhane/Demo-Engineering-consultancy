from django.http import HttpResponse


def robots_txt(request):
    # NOTE: the admin URL is deliberately NOT listed here — listing a secret
    # admin path in robots.txt would advertise it to attackers.
    lines = [
        'User-agent: *',
        'Allow: /',
        'Disallow: /api/',
        'Disallow: /private-files/',
        'Disallow: /health/',
        'Disallow: /chatbot/',
        'Disallow: /i18n/',
        f'Sitemap: {request.scheme}://{request.get_host()}/sitemap.xml',
    ]
    return HttpResponse('\n'.join(lines), content_type='text/plain')
