from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import Service


def service_list(request):
    services = Service.objects.filter(active=True)
    context = {
        'services': services,
        'seo_schemas': [('breadcrumbs', [('Services', reverse('services:service_list'))])],
        'seo_title': 'Our Services | Engineering, Construction & Metal Fabrication in Pokhara, Nepal',
        'seo_description': (
            'Explore engineering, construction, infrastructure and metal fabrication '
            'services offered by Highnoon Engineering Solutions Pvt. Ltd. in Pokhara, Nepal.'
        ),
    }
    return render(request, 'services/service_list.html', context)


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, active=True)
    related = Service.objects.filter(active=True).exclude(pk=service.pk)[:3]
    context = {
        'service': service,
        'related_services': related,
        'seo_title': service.meta_title,
        'seo_description': service.meta_description,
        'seo_image': service.image,
        'seo_image_alt': service.image_alt_text,
        'seo_schemas': [
            ('service', service),
            ('breadcrumbs', [
                ('Services', reverse('services:service_list')),
                (service.name, service.get_absolute_url()),
            ]),
        ],
    }
    return render(request, 'services/service_detail.html', context)


def metal_fabrication(request):
    """
    Dedicated Metal Fabrication landing page at /services/metal-fabrication/.
    Falls back to a static template if no matching Service row has been
    created yet, so the page is always available even before an admin adds
    the corresponding Service entry.
    """
    service = Service.objects.filter(slug='metal-fabrication', active=True).first()
    context = {
        'service': service,
        'seo_image': service.image if service else None,
        'seo_schemas': [
            ('breadcrumbs', [
                ('Services', reverse('services:service_list')),
                ('Metal Fabrication', reverse('services:metal_fabrication')),
            ]),
        ],
        'seo_title': 'Metal Fabrication Company in Pokhara, Nepal | Highnoon Engineering Solutions',
        'seo_description': (
            'Highnoon Engineering Solutions Pvt. Ltd. offers custom metal fabrication, '
            'structural steel fabrication and industrial fabrication services in Pokhara, Nepal.'
        ),
    }
    return render(request, 'services/metal_fabrication.html', context)
