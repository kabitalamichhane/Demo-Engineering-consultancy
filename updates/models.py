from django.db import models
from django.urls import reverse
from django.utils import timezone


class Update(models.Model):
    CATEGORY_CHOICES = [
        ('company_news', 'Company News'),
        ('project_update', 'Project Update'),
        ('industry_insight', 'Industry Insight'),
        ('announcement', 'Announcement'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    featured_image = models.ImageField(upload_to='updates/', blank=True, null=True)
    featured_image_alt = models.CharField(
        max_length=150, blank=True,
        help_text="Describe the picture in a few words (helps Google Images and screen readers). Blank = automatic text.",
    )
    excerpt = models.CharField(max_length=300, blank=True)
    content = models.TextField()
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='company_news')
    author = models.CharField(max_length=100, blank=True, default='Highnoon Engineering Solutions')

    published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)

    seo_title = models.CharField(max_length=255, blank=True)
    seo_description = models.CharField(max_length=300, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.published and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('updates:update_detail', kwargs={'slug': self.slug})

    @property
    def image_alt_text(self):
        return self.featured_image_alt or self.title

    @property
    def meta_title(self):
        return self.seo_title or f'{self.title} | Highnoon Engineering Solutions'

    @property
    def meta_description(self):
        return self.seo_description or self.excerpt
