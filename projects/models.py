from django.db import models
from django.urls import reverse


class Project(models.Model):
    CATEGORY_CHOICES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('industrial', 'Industrial'),
        ('infrastructure', 'Infrastructure'),
        ('institutional', 'Institutional'),
        ('metal_fabrication', 'Metal Fabrication'),
        ('structural', 'Structural'),
        ('renovation', 'Renovation'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('ongoing', 'Ongoing'),
        ('upcoming', 'Upcoming'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    client = models.CharField(max_length=150, blank=True)
    location = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='other')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')

    start_date = models.DateField(blank=True, null=True)
    completion_date = models.DateField(blank=True, null=True)

    description = models.TextField(blank=True)
    scope = models.TextField(blank=True, help_text='Scope of work performed.')
    project_value = models.DecimalField(
        max_digits=14, decimal_places=2, blank=True, null=True,
        help_text='Optional. Leave blank if not to be disclosed.',
    )

    featured_image = models.ImageField(upload_to='projects/featured/', blank=True, null=True)
    featured_image_alt = models.CharField(
        max_length=150, blank=True,
        help_text="Describe the picture in a few words (helps Google Images and screen readers). Blank = automatic text.",
    )
    featured = models.BooleanField(default=False)

    is_demo = models.BooleanField(
        default=False,
        help_text='Mark ON for placeholder/demo projects used only during development.',
    )

    seo_title = models.CharField(max_length=255, blank=True)
    seo_description = models.CharField(max_length=300, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-featured', '-completion_date', '-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('projects:project_detail', kwargs={'slug': self.slug})

    @property
    def image_alt_text(self):
        return self.featured_image_alt or f'{self.name} — Highnoon Engineering Solutions project'

    @property
    def meta_title(self):
        return self.seo_title or f'{self.name} | Highnoon Engineering Solutions Projects'

    @property
    def meta_description(self):
        return self.seo_description or (self.description[:280] if self.description else '')


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='gallery_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'id']

    def __str__(self):
        return f'{self.project.name} — image {self.pk}'
