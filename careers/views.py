from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from company.security import is_rate_limited, log_security_event
from .models import Job
from .forms import JobApplicationForm


def job_list(request):
    jobs = Job.objects.filter(active=True)
    context = {
        'jobs': jobs,
        'seo_schemas': [('breadcrumbs', [('Careers', reverse('careers:job_list'))])],
        'seo_title': 'Careers at Highnoon Engineering Solutions Pvt. Ltd.',
        'seo_description': (
            'View current job openings at Highnoon Engineering Solutions, an '
            'engineering, construction and metal fabrication company in Pokhara, Nepal.'
        ),
    }
    return render(request, 'careers/job_list.html', context)


def job_detail(request, slug):
    job = get_object_or_404(Job, slug=slug, active=True)
    if request.method == 'POST':
        if is_rate_limited(request, scope='job_application', limit=5, period_seconds=3600):
            messages.error(request, 'Too many submissions from this address. Please try again later.')
            return redirect('careers:job_detail', slug=job.slug)

        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            if form.is_spam():
                log_security_event('honeypot_triggered', request, scope='job_application')
            else:
                application = form.save(commit=False)
                application.job = job
                application.save()
            messages.success(request, 'Your application has been submitted. Thank you for your interest.')
            return redirect('careers:job_detail', slug=job.slug)
    else:
        form = JobApplicationForm()

    context = {
        'job': job,
        'form': form,
        'seo_title': f'{job.title} | Careers at Highnoon Engineering Solutions',
        'seo_description': job.description[:280] if job.description else '',
        'seo_schemas': [
            ('job', job),
            ('breadcrumbs', [
                ('Careers', reverse('careers:job_list')),
                (job.title, job.get_absolute_url()),
            ]),
        ],
    }
    return render(request, 'careers/job_detail.html', context)
