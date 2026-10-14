from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import Project


def project_list(request):
    projects = Project.objects.all()

    category = request.GET.get('category')
    if category:
        projects = projects.filter(category=category)

    status = request.GET.get('status')
    if status:
        projects = projects.filter(status=status)

    context = {
        'projects': projects,
        'categories': Project.CATEGORY_CHOICES,
        'statuses': Project.STATUS_CHOICES,
        'selected_category': category or '',
        'selected_status': status or '',
        'seo_schemas': [('breadcrumbs', [('Projects', reverse('projects:project_list'))])],
        'seo_title': 'Our Projects | Highnoon Engineering Solutions Pvt. Ltd.',
        'seo_description': (
            'Browse engineering, construction, infrastructure and metal fabrication '
            'projects delivered by Highnoon Engineering Solutions in Pokhara, Nepal.'
        ),
    }
    return render(request, 'projects/project_list.html', context)


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    context = {
        'project': project,
        'seo_title': project.meta_title,
        'seo_description': project.meta_description,
        'seo_image': project.featured_image,
        'seo_image_alt': project.image_alt_text,
        # Placeholder/demo projects must never appear in Google.
        'seo_noindex': project.is_demo,
        'seo_schemas': [
            ('breadcrumbs', [
                ('Projects', reverse('projects:project_list')),
                (project.name, project.get_absolute_url()),
            ]),
        ],
    }
    return render(request, 'projects/project_detail.html', context)
