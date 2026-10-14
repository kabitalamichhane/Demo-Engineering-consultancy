from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection
from django.test import RequestFactory

from company.models import CompanyProfile, DirectorMessage


class Command(BaseCommand):
    help = 'Prints what this copy of the site contains, to find why something is not showing.'

    def handle(self, *args, **options):
        out = self.stdout.write
        out('--- Highnoon site status ---')
        out(f'Project folder : {settings.BASE_DIR}')
        out(f'Database file  : {connection.settings_dict["NAME"]}')
        out(f'Debug mode     : {settings.DEBUG}')
        out(f'Admin address  : /{settings.ADMIN_URL}')
        out(f'Language switcher: {settings.ENABLE_LANGUAGE_SWITCHER}')

        out(f'Company profile: {"yes" if CompanyProfile.objects.exists() else "NO (created on first page visit)"}')
        total = DirectorMessage.objects.count()
        active = DirectorMessage.objects.filter(active=True).count()
        out(f'Director messages: {total} saved, {active} active')
        for m in DirectorMessage.objects.all():
            out(f'   - "{m.title}"  active={m.active}')
        if total == 0:
            out('   (none saved: the built-in message should show)')
        elif active == 0:
            out('   (all are unticked "Active": the section is hidden on purpose - tick Active in Admin)')

        out('Rendering the home page ...')
        try:
            from company.views import home
            request = RequestFactory().get('/', HTTP_HOST='127.0.0.1')
            response = home(request)
            html = response.content.decode()
            found = 'Messages from Our Director' in html
            out(f'Home page renders: yes ({len(html)} characters)')
            out(f'Director section in the page: {"YES" if found else "NO"}')
        except Exception as exc:  # show the real error instead of hiding it
            self.stderr.write(self.style.ERROR(f'Home page FAILED: {type(exc).__name__}: {exc}'))
