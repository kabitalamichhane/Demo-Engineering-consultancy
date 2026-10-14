from django import forms
from company.security import HoneypotFormMixin, validate_uploaded_file, ALLOWED_DOCUMENT_EXTENSIONS
from .models import ContactInquiry, QuoteRequest, WorkWithUsInquiry, Appointment


class ContactInquiryForm(HoneypotFormMixin, forms.ModelForm):
    class Meta:
        model = ContactInquiry
        fields = ['name', 'email', 'phone', 'subject', 'inquiry_type', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }


class QuoteRequestForm(HoneypotFormMixin, forms.ModelForm):
    class Meta:
        model = QuoteRequest
        fields = [
            'name', 'company', 'email', 'phone', 'service', 'project_type',
            'project_location', 'estimated_budget', 'expected_start_date',
            'message', 'attachment',
        ]
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
            'expected_start_date': forms.DateInput(attrs={'type': 'date'}),
        }

    SERVICE_CHOICES = [
        ('Engineering Consultancy', 'Engineering Consultancy'),
        ('Structural Engineering', 'Structural Engineering'),
        ('Building Construction', 'Building Construction'),
        ('Infrastructure Development', 'Infrastructure Development'),
        ('Project Management', 'Project Management'),
        ('Quantity Surveying & Estimation', 'Quantity Surveying & Estimation'),
        ('Metal Fabrication', 'Metal Fabrication'),
        ('Steel Fabrication', 'Steel Fabrication'),
        ('Custom Metal Works', 'Custom Metal Works'),
        ('Renovation & Retrofitting', 'Renovation & Retrofitting'),
        ('Maintenance Services', 'Maintenance Services'),
        ('Other', 'Other'),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'] = forms.ChoiceField(choices=self.SERVICE_CHOICES)

    def clean_attachment(self):
        return validate_uploaded_file(
            self.cleaned_data.get('attachment'),
            allowed_extensions=ALLOWED_DOCUMENT_EXTENSIONS + ('.jpg', '.jpeg', '.png'),
        )


class WorkWithUsInquiryForm(HoneypotFormMixin, forms.ModelForm):
    class Meta:
        model = WorkWithUsInquiry
        fields = [
            'full_name', 'company_name', 'email', 'phone', 'organization_type',
            'project_type', 'project_location', 'message',
        ]
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }


class AppointmentForm(HoneypotFormMixin, forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['name', 'email', 'phone', 'preferred_date', 'preferred_time', 'message']
        widgets = {
            'preferred_date': forms.DateInput(attrs={'type': 'date'}),
            'preferred_time': forms.TimeInput(attrs={'type': 'time'}),
            'message': forms.Textarea(attrs={'rows': 4}),
        }
