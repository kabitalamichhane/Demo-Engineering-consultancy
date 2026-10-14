"""
Simple, safe FAQ matching for the website chatbot.

No outside service is used: answers come only from questions the company wrote
in Admin, so the bot can never invent prices, promises or facts.
"""
import re

STOP_WORDS = {
    'the', 'and', 'for', 'you', 'your', 'are', 'is', 'do', 'does', 'can', 'what', 'how', 'where',
    'when', 'who', 'why', 'will', 'with', 'have', 'has', 'any', 'about', 'please', 'tell', 'me',
    'our', 'this', 'that', 'there', 'want', 'need', 'get', 'know', 'from', 'into', 'its',
}
GREETINGS = {'hi', 'hii', 'hello', 'hey', 'namaste', 'namaskar', 'नमस्ते', 'नमस्कार'}
WORD_RE = re.compile(r'[a-z0-9\u0900-\u097f]+')
MIN_SCORE = 2


def _tokens(text):
    return {w for w in WORD_RE.findall((text or '').lower()) if len(w) > 2 and w not in STOP_WORDS}


def is_greeting(message):
    words = set(WORD_RE.findall((message or '').lower()))
    return bool(words) and words <= (GREETINGS | {'there', 'dear', 'sir', 'madam'})


def best_faq(message, faqs):
    """Return the best-matching FAQ for `message`, or None if nothing matches well enough."""
    text = (message or '').lower().strip()
    if not text:
        return None
    msg_tokens = _tokens(text)
    best, best_score = None, 0
    for faq in faqs:
        score = 0
        for kw in faq.keyword_list:
            if kw and kw in text:
                score += 3
        score += len(msg_tokens & _tokens(faq.question))
        if score > best_score:
            best, best_score = faq, score
    return best if best_score >= MIN_SCORE else None
