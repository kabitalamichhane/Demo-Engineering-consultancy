from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from projects.models import Project

# Real projects supplied by the company. Names are descriptive placeholders:
# edit name, location, client and description in Admin -> Projects.
MY_PROJECTS = [
    ('Multi-Storey Building with Curved Balconies', 'commercial', 'project-curved-balconies.jpg'),
    ('Resort Building with Garden Courtyard', 'commercial', 'project-wellness-resort.jpg'),
    ('Multi-Storey Commercial Square (Night View)', 'commercial', 'project-square-night.jpg'),
]


class Command(BaseCommand):
    help = "Adds the company's own project photos as real (non-demo), featured projects."

    def handle(self, *args, **options):
        folder = Path(settings.BASE_DIR) / 'static' / 'img' / 'projects'
        for name, category, filename in MY_PROJECTS:
            path = folder / filename
            if not path.exists():
                self.stdout.write(self.style.ERROR(f'Missing image: {path}'))
                continue
            project, created = Project.objects.get_or_create(
                slug=slugify(name),
                defaults=dict(
                    name=name, category=category, status='completed',
                    description='', is_demo=False, featured=True,
                ),
            )
            if created or not project.featured_image:
                with path.open('rb') as fh:
                    project.featured_image.save(filename, File(fh), save=True)
            self.stdout.write(self.style.SUCCESS(
                f"{'Created' if created else 'Already exists'}: {name}"
            ))
        self.stdout.write(self.style.WARNING(
            'Now open Admin -> Projects and set the real name, location and description.'
        ))
