from django.db import models
from django.urls import reverse


class Service(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True)
    short_description = models.CharField(
        max_length=300, help_text='Short summary shown on listing/cards.'
    )
    description = models.TextField(help_text='Full detail shown on the service page.')

    features = models.TextField(
        blank=True,
        help_text='One feature per line, e.g. bullet points shown on the service page.',
    )

    image = models.ImageField(upload_to='services/', blank=True, null=True)
    image_alt = models.CharField(
        max_length=150, blank=True,
        help_text="Describe the picture in a few words (helps Google Images and screen readers). Blank = automatic text.",
    )
    icon = models.CharField(
        max_length=50, blank=True, help_text="Icon class or short code, e.g. 'structural'."
    )

    seo_title = models.CharField(max_length=255, blank=True)
    seo_description = models.CharField(max_length=300, blank=True)

    display_order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('services:service_detail', kwargs={'slug': self.slug})

    @property
    def feature_list(self):
        return [line.strip() for line in self.features.splitlines() if line.strip()]

    @property
    def image_alt_text(self):
        return self.image_alt or f'{self.name} — Highnoon Engineering Solutions'

    @property
    def meta_title(self):
        return self.seo_title or f'{self.name} | Highnoon Engineering Solutions'

    @property
    def meta_description(self):
        return self.seo_description or self.short_description
