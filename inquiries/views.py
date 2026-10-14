from django.contrib import messages
from django.shortcuts import render, redirect

from company.security import is_rate_limited, log_security_event
from .forms import ContactInquiryForm, QuoteRequestForm, WorkWithUsInquiryForm


def contact_view(request):
    if request.method == 'POST':
        if is_rate_limited(request, scope='contact', limit=5, period_seconds=3600):
            messages.error(request, 'Too many submissions from this address. Please try again later.')
            return redirect('inquiries:contact')

        form = ContactInquiryForm(request.POST)
        if form.is_valid():
            if form.is_spam():
                log_security_event('honeypot_triggered', request, scope='contact')
            else:
                form.save()
            # Spam submissions are silently discarded but still show success,
            # so bots get no signal their submission was rejected.
            messages.success(request, 'Thank you for reaching out. Our team will get back to you soon.')
            return redirect('inquiries:contact')
    else:
        form = ContactInquiryForm()

    context = {
        'form': form,
        'seo_title': 'Contact Us | Highnoon Engineering Solutions Pvt. Ltd.',
        'seo_description': (
            'Contact Highnoon Engineering Solutions Pvt. Ltd. in Pokhara, Nepal for '
            'engineering, construction and metal fabrication inquiries.'
        ),
    }
    return render(request, 'inquiries/contact.html', context)


def get_a_quote_view(request):
    if request.method == 'POST':
        if is_rate_limited(request, scope='quote', limit=5, period_seconds=3600):
            messages.error(request, 'Too many submissions from this address. Please try again later.')
            return redirect('inquiries:get_a_quote')

        form = QuoteRequestForm(request.POST, request.FILES)
        if form.is_valid():
            if form.is_spam():
                log_security_event('honeypot_triggered', request, scope='quote')
            else:
                form.save()
            messages.success(request, 'Your quote request has been received. We will contact you shortly.')
            return redirect('inquiries:get_a_quote')
    else:
        form = QuoteRequestForm()

    context = {
        'form': form,
        'seo_title': 'Get a Quote | Highnoon Engineering Solutions Pvt. Ltd.',
        'seo_description': (
            'Request a quote for engineering, construction or metal fabrication services '
            'from Highnoon Engineering Solutions in Pokhara, Nepal.'
        ),
    }
    return render(request, 'inquiries/get_a_quote.html', context)


def work_with_us_view(request):
    if request.method == 'POST':
        if is_rate_limited(request, scope='work_with_us', limit=5, period_seconds=3600):
            messages.error(request, 'Too many submissions from this address. Please try again later.')
            return redirect('inquiries:work_with_us')

        form = WorkWithUsInquiryForm(request.POST)
        if form.is_valid():
            if form.is_spam():
                log_security_event('honeypot_triggered', request, scope='work_with_us')
            else:
                form.save()
            messages.success(request, 'Thank you for your interest in working with us. We will be in touch.')
            return redirect('inquiries:work_with_us')
    else:
        form = WorkWithUsInquiryForm()

    context = {
        'form': form,
        'seo_title': 'Work With Highnoon Engineering Solutions | Pokhara, Nepal',
        'seo_description': (
            'Partner with Highnoon Engineering Solutions for reliable engineering, '
            'construction and metal fabrication solutions in Pokhara, Nepal.'
        ),
    }
    return render(request, 'inquiries/work_with_us.html', context)
