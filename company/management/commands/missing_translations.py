from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from company import i18n_data, i18n_scan


class Command(BaseCommand):
    help = (
        'Lists text in the templates that has no built-in Nepali/Hindi translation yet. '
        'Add the missing text to company/i18n_data/ (or to Admin -> Translations).'
    )

    def handle(self, *args, **options):
        found = i18n_scan.template_strings(Path(settings.BASE_DIR) / 'templates')
        missing = sorted(set(found) - set(i18n_data.TABLE))
        self.stdout.write(f'{len(found)} pieces of text on the site, {len(missing)} without a translation.')
        for key in missing:
            self.stdout.write(f'  - {key}   ({", ".join(sorted(found[key]))})')
        if not missing:
            self.stdout.write(self.style.SUCCESS('Every piece of template text is translated.'))
