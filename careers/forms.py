from django import forms
from company.security import HoneypotFormMixin, validate_uploaded_file, ALLOWED_DOCUMENT_EXTENSIONS
from .models import JobApplication


class JobApplicationForm(HoneypotFormMixin, forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['full_name', 'email', 'phone', 'cover_letter', 'resume']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 5}),
        }

    def clean_resume(self):
        return validate_uploaded_file(
            self.cleaned_data.get('resume'),
            allowed_extensions=ALLOWED_DOCUMENT_EXTENSIONS,
        )
