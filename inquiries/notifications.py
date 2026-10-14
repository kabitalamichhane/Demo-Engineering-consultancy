"""
Email alerts for new website submissions.

* One alert to the company (COMPANY_NOTIFY_EMAIL) with Reply-To set to the customer.
* One short automatic acknowledgement to the customer (can be turned off).

Email problems must NEVER break a form submission, so every send is wrapped
and logged instead of raised.
"""
import logging

from django.conf import settings
from django.core.mail import EmailMessage

logger = logging.getLogger('django')


def _clean(value, limit=200):
    """Single-line, length-limited text for use in email subjects."""
    return ' '.join(str(value or '').split())[:limit]


def _company_name():
    return getattr(settings, 'COMPANY_DISPLAY_NAME', 'Highnoon Engineering Solutions')


def _describe(obj):
    kind = obj.__class__.__name__
    if kind == 'QuoteRequest':
        lines = [
            ('Name', obj.name), ('Company', obj.company), ('Email', obj.email), ('Phone', obj.phone),
            ('Service', obj.service), ('Project type', obj.project_type),
            ('Location', obj.project_location), ('Budget', obj.get_estimated_budget_display() if obj.estimated_budget else ''),
            ('Expected start', obj.expected_start_date or ''), ('Message', obj.message),
            ('Attachment', 'Yes (download in Admin)' if obj.attachment else 'No'),
        ]
        return 'New quote request', obj.name, obj.email, lines
    if kind == 'WorkWithUsInquiry':
        lines = [
            ('Name', obj.full_name), ('Company', obj.company_name), ('Email', obj.email), ('Phone', obj.phone),
            ('Type', obj.get_organization_type_display()), ('Project type', obj.project_type),
            ('Location', obj.project_location), ('Message', obj.message),
        ]
        return 'New "Work With Us" enquiry', obj.full_name, obj.email, lines
    lines = [
        ('Name', obj.name), ('Email', obj.email), ('Phone', obj.phone),
        ('Subject', obj.subject), ('Type', obj.get_inquiry_type_display()), ('Message', obj.message),
    ]
    return 'New contact message', obj.name, obj.email, lines


def send_submission_emails(obj):
    title, name, customer_email, lines = _describe(obj)

    # 1) Alert to the company
    try:
        body = '\n'.join(f'{k}: {v}' for k, v in lines if v) + '\n\nManage this lead in the Admin panel.'
        alert = EmailMessage(
            subject=f'[Website] {title} from {_clean(name, 80)}',
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.COMPANY_NOTIFY_EMAIL],
            reply_to=[customer_email] if customer_email else None,
        )
        alert.send(fail_silently=False)
    except Exception:
        logger.exception('Could not send company alert email')

    # 2) Automatic acknowledgement to the customer
    if getattr(settings, 'SEND_AUTO_REPLY', True) and customer_email:
        try:
            reply = EmailMessage(
                subject=f'We received your message - {_company_name()}',
                body=(
                    f'Dear {_clean(name, 80)},\n\n'
                    f'Thank you for contacting {_company_name()}. We have received your '
                    f'message and a member of our team will get back to you soon.\n\n'
                    f'If your matter is urgent, please call us on {getattr(settings, "COMPANY_PHONE", "9856082231")}.\n\n'
                    f'Kind regards,\n{_company_name()}\nPokhara, Nepal'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[customer_email],
                reply_to=[settings.COMPANY_NOTIFY_EMAIL],
            )
            reply.send(fail_silently=False)
        except Exception:
            logger.exception('Could not send customer acknowledgement email')
