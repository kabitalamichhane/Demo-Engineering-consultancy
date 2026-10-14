"""
Built-in Nepali and Hindi translations of the site text.

Add or fix translations in ui.py / pages.py / content.py (format: 'English': ('Nepali', 'Hindi')).
Text typed in Admin (a service name, a news article...) is translated from
Admin -> Translations instead, so no code change is needed for it.
"""
from company.i18n_scan import normalize

from . import content, pages, ui

LANGUAGES = ('ne', 'hi')


def _build():
    table = {}
    for module in (ui, pages, content):
        for english, (nepali, hindi) in module.DATA.items():
            table[normalize(english)] = (nepali, hindi)
    return table


TABLE = _build()


def builtin(lang):
    """{normalized English: translation} for 'ne' or 'hi'."""
    index = LANGUAGES.index(lang)
    return {key: pair[index] for key, pair in TABLE.items()}
