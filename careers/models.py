from django.db import models

from company.private_storage import get_private_storage
from django.urls import reverse


class Job(models.Model):
    EMPLOYMENT_TYPE_CHOICES = [
        ('full_time', 'Full-Time'),
        ('part_time', 'Part-Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('temporary', 'Temporary'),
    ]

    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True)
    department = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=150, default='Pokhara, Nepal')
    employment_type = models.CharField(
        max_length=20, choices=EMPLOYMENT_TYPE_CHOICES, default='full_time'
    )

    description = models.TextField()
    responsibilities = models.TextField(
        blank=True, help_text='One responsibility per line.'
    )
    requirements = models.TextField(
        blank=True, help_text='One requirement per line.'
    )

    deadline = models.DateField(blank=True, null=True)
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-active', '-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('careers:job_detail', kwargs={'slug': self.slug})

    @property
    def responsibility_list(self):
        return [l.strip() for l in self.responsibilities.splitlines() if l.strip()]

    @property
    def requirement_list(self):
        return [l.strip() for l in self.requirements.splitlines() if l.strip()]


class JobApplication(models.Model):
    job = models.ForeignKey(Job, related_name='applications', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    cover_letter = models.TextField(blank=True)
    resume = models.FileField(upload_to='careers/resumes/', storage=get_private_storage)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.full_name} — {self.job.title}'
