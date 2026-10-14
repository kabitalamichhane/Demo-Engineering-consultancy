from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import Update


def update_list(request):
    updates = Update.objects.filter(published=True)
    context = {
        'updates': updates,
        'seo_schemas': [('breadcrumbs', [('Updates', reverse('updates:update_list'))])],
        'seo_title': 'Updates & News | Highnoon Engineering Solutions Pvt. Ltd.',
        'seo_description': (
            'Latest news, project updates and announcements from Highnoon '
            'Engineering Solutions, an engineering and construction company in Pokhara, Nepal.'
        ),
    }
    return render(request, 'updates/update_list.html', context)


def update_detail(request, slug):
    update = get_object_or_404(Update, slug=slug, published=True)
    context = {
        'update': update,
        'seo_title': update.meta_title,
        'seo_description': update.meta_description,
        'seo_image': update.featured_image,
        'seo_image_alt': update.image_alt_text,
        'og_type': 'article',
        'seo_schemas': [
            ('article', update),
            ('breadcrumbs', [
                ('Updates', reverse('updates:update_list')),
                (update.title, update.get_absolute_url()),
            ]),
        ],
    }
    return render(request, 'updates/update_detail.html', context)
