from django.conf import settings
from django.db import models

from company.private_storage import get_private_storage


INQUIRY_STATUS_CHOICES = [
    ('new', 'New'),
    ('in_progress', 'Contacted / In Progress'),
    ('quoted', 'Quote Sent'),
    ('won', 'Won'),
    ('lost', 'Lost'),
    ('resolved', 'Closed'),
]


class LeadTrackingMixin(models.Model):
    """Internal sales-tracking fields. Never exposed through the public API."""
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+',
        help_text='Team member responsible for this lead.',
    )
    follow_up_date = models.DateField(null=True, blank=True, help_text='When to follow up next.')
    deal_value = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True,
        help_text='Quoted / won value in NPR (internal only).',
    )
    internal_notes = models.TextField(blank=True, help_text='Private notes - never shown to the customer.')

    class Meta:
        abstract = True


class ContactInquiry(LeadTrackingMixin):
    INQUIRY_TYPE_CHOICES = [
        ('general', 'General Inquiry'),
        ('services', 'Services'),
        ('projects', 'Projects'),
        ('careers', 'Careers'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    subject = models.CharField(max_length=200, blank=True)
    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_TYPE_CHOICES, default='general')
    message = models.TextField()

    status = models.CharField(max_length=20, choices=INQUIRY_STATUS_CHOICES, default='new', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Inquiry'
        verbose_name_plural = 'Contact Inquiries'

    def __str__(self):
        return f'{self.name} — {self.subject or self.inquiry_type}'


class QuoteRequest(LeadTrackingMixin):
    BUDGET_CHOICES = [
        ('under_5_lakh', 'Under NPR 5 Lakh'),
        ('5_20_lakh', 'NPR 5–20 Lakh'),
        ('20_50_lakh', 'NPR 20–50 Lakh'),
        ('50_lakh_1_crore', 'NPR 50 Lakh – 1 Crore'),
        ('above_1_crore', 'Above NPR 1 Crore'),
        ('not_sure', 'Not Sure Yet'),
    ]

    name = models.CharField(max_length=150)
    company = models.CharField(max_length=150, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    service = models.CharField(
        max_length=100,
        help_text="e.g. 'Metal Fabrication', 'Structural Engineering', 'Building Construction'",
    )
    project_type = models.CharField(max_length=150, blank=True)
    project_location = models.CharField(max_length=200, blank=True)
    estimated_budget = models.CharField(max_length=30, choices=BUDGET_CHOICES, blank=True)
    expected_start_date = models.DateField(blank=True, null=True)
    message = models.TextField(blank=True)
    attachment = models.FileField(
        upload_to='quotes/attachments/', storage=get_private_storage, blank=True, null=True
    )

    status = models.CharField(max_length=20, choices=INQUIRY_STATUS_CHOICES, default='new', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Quote Request'
        verbose_name_plural = 'Quote Requests'

    def __str__(self):
        return f'{self.name} — {self.service}'


class WorkWithUsInquiry(LeadTrackingMixin):
    ORGANIZATION_TYPE_CHOICES = [
        ('client', 'Client'),
        ('contractor', 'Contractor'),
        ('consultant', 'Consultant'),
        ('supplier', 'Supplier'),
        ('business_partner', 'Business Partner'),
        ('other', 'Other'),
    ]

    full_name = models.CharField(max_length=150)
    company_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    organization_type = models.CharField(max_length=30, choices=ORGANIZATION_TYPE_CHOICES)
    project_type = models.CharField(max_length=150, blank=True)
    project_location = models.CharField(max_length=200, blank=True)
    message = models.TextField()

    status = models.CharField(max_length=20, choices=INQUIRY_STATUS_CHOICES, default='new', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Work With Us Inquiry'
        verbose_name_plural = 'Work With Us Inquiries'

    def __str__(self):
        return f'{self.full_name} ({self.get_organization_type_display()})'


class Appointment(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    message = models.TextField(blank=True)

    status = models.CharField(max_length=20, choices=INQUIRY_STATUS_CHOICES, default='new', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.preferred_date}'
