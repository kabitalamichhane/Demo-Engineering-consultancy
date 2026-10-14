"""
Private file storage for sensitive uploads (CVs, quote attachments).

Files live in settings.PRIVATE_MEDIA_ROOT — OUTSIDE the public MEDIA_ROOT — and
are only downloadable through the staff-only view at /private-files/<path>.
"""
import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage


class PrivateFileStorage(FileSystemStorage):
    @property
    def base_location(self):
        return settings.PRIVATE_MEDIA_ROOT

    @property
    def location(self):
        return os.path.abspath(self.base_location)

    @property
    def base_url(self):
        return '/private-files/'


def get_private_storage():
    return PrivateFileStorage()
