"""
Finds the visible English text in the site's templates, so we can check that every piece
has a Nepali and Hindi translation (see company/i18n_data/ and `manage.py missing_translations`).

Only the Python standard library is used, so it also runs outside Django.
"""
import html
import re
from pathlib import Path

# Text that is not language (icons, abbreviations, codes) and never needs translating.
NOT_TRANSLATED = {'en', 'fb', 'ig', 'in', 'yt', 'npr', 'hes', 'website', 'pokhara', 'nepal', 'pokhara-14, bp marg', 'facebook', 'instagram', 'linkedin', 'youtube'}

# Pieces that sit next to a variable in a template (e.g. "The {{ name }} team"). The browser sees
# the finished sentence, so these are translated by the {} patterns in i18n_data/ui.py instead.
COVERED_BY_PATTERNS = {'the', 'team', '. all rights reserved.', '· apply by'}

_DEFAULT_RE = re.compile(r'''\|default:(?:"([^"]+)"|'([^']+)')''')
_ATTR_RE = re.compile(r'(?:placeholder|aria-label|title|alt)="([^"{}]+)"')
_EMAIL_OR_NUMBER = re.compile(r'^[\w.+-]+@[\w.-]+$|^[\d\s+()-]+$')


def normalize(text):
    """Same rule as static/js/i18n.js: unescape, collapse spaces, lower-case."""
    return re.sub(r'\s+', ' ', html.unescape(text or '')).strip().lower()


def _keep(text):
    key = normalize(text)
    if len(key) < 2 or not re.search(r'[a-z]', key):
        return None
    if key in NOT_TRANSLATED or _EMAIL_OR_NUMBER.match(key):
        return None
    if key.startswith(('/', 'http')) or key in COVERED_BY_PATTERNS:      # links / pattern-covered
        return None
    return key


def template_strings(templates_dir):
    """{normalized text: [files where it appears]} for every template under templates_dir."""
    found = {}

    def add(raw, source):
        key = _keep(raw)
        if key:
            found.setdefault(key, set()).add(source)

    for path in sorted(Path(templates_dir).rglob('*.html')):
        text = path.read_text(encoding='utf-8')
        source = path.name
        text = re.sub(r'(?s)<script.*?</script>', ' ', text)
        text = re.sub(r'(?s)<style.*?</style>', ' ', text)
        text = re.sub(r'{#.*?#}', ' ', text)
        for match in _ATTR_RE.finditer(text):
            add(match.group(1), source)
        for match in _DEFAULT_RE.finditer(text):
            add(match.group(1) or match.group(2), source)
        text = re.sub(r'(?s)<[^>]+>', '\x00', text)
        text = re.sub(r'{%.*?%}', '\x00', text)
        text = re.sub(r'{{.*?}}', '\x01', text)
        for segment in text.split('\x00'):
            for part in segment.split('\x01'):
                add(part, source)
    return found
