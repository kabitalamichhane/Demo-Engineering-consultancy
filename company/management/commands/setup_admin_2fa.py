"""
Create (or reset) two-factor authentication for an admin user.

    python manage.py setup_admin_2fa <username>
    python manage.py setup_admin_2fa <username> --reset

Prints a setup key to add to an authenticator app (Google Authenticator, Microsoft
Authenticator, Authy, 1Password...) plus one-time backup codes. Run this BEFORE
enabling ADMIN_REQUIRE_2FA, otherwise nobody can log in to the admin.
"""
from base64 import b32encode

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django_otp.plugins.otp_static.models import StaticDevice, StaticToken
from django_otp.plugins.otp_totp.models import TOTPDevice


class Command(BaseCommand):
    help = 'Create or reset a TOTP (authenticator app) device and backup codes for a staff user.'

    def add_arguments(self, parser):
        parser.add_argument('username')
        parser.add_argument('--reset', action='store_true',
                            help='Delete existing 2FA devices for this user and create new ones.')

    def handle(self, *args, **options):
        User = get_user_model()
        try:
            user = User.objects.get(**{User.USERNAME_FIELD: options['username']})
        except User.DoesNotExist:
            raise CommandError(f"User '{options['username']}' does not exist.")
        if not user.is_staff:
            raise CommandError('2FA is for staff/admin users only.')

        has_device = TOTPDevice.objects.filter(user=user).exists()
        if has_device and not options['reset']:
            raise CommandError('This user already has 2FA. Use --reset to replace it.')
        if options['reset']:
            TOTPDevice.objects.filter(user=user).delete()
            StaticDevice.objects.filter(user=user).delete()

        device = TOTPDevice.objects.create(user=user, name='authenticator', confirmed=True)
        secret = b32encode(device.bin_key).decode()

        backup = StaticDevice.objects.create(user=user, name='backup-codes', confirmed=True)
        codes = []
        for _ in range(8):
            token = StaticToken.random_token()
            backup.token_set.create(token=token)
            codes.append(token)

        self.stdout.write(self.style.SUCCESS(f'2FA created for {user}.'))
        self.stdout.write('\nIn your authenticator app choose "Enter a setup key" (time-based) and use:')
        self.stdout.write(f'  Account : {user}')
        self.stdout.write(f'  Key     : {secret}')
        self.stdout.write(f'\n(or open this URL in an app that supports it)\n  {device.config_url}')
        self.stdout.write('\nBackup codes (each works ONCE — store them somewhere safe):')
        for code in codes:
            self.stdout.write(f'  {code}')
