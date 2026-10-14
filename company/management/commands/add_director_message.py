from django.core.management.base import BaseCommand

from company.director_defaults import DEFAULT_MESSAGE as MESSAGE, DEFAULT_TITLE as TITLE
from company.models import DirectorMessage

class Command(BaseCommand):
    help = (
        'Adds one starter "Message from the Director" if there are none yet. '
        'Edit the wording in Admin -> Director messages. Use --force to add it anyway.'
    )

    def add_arguments(self, parser):
        parser.add_argument('--force', action='store_true', help='Add even if messages already exist.')

    def handle(self, *args, **options):
        if DirectorMessage.objects.exists() and not options['force']:
            self.stdout.write('Director messages already exist - nothing added. (Use --force to add anyway.)')
            return
        DirectorMessage.objects.create(title=TITLE, message=MESSAGE, display_order=1, active=True)
        self.stdout.write(self.style.SUCCESS('Director message added. Edit it in Admin -> Director messages.'))
