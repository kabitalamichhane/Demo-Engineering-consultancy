/* Language switcher: English / Nepali / Hindi.
   The translations come from this website itself (/i18n/<lang>.json) - no Google, no outside service.
   The text on the page is swapped for its translation; anything without a translation stays English.
   Kept in an external file because the site's Content-Security-Policy forbids inline scripts. */
(function () {
  'use strict';

  var LANGS = { en: true, ne: true, hi: true };
  var COOKIE = 'hes_lang';
  var SKIP_TAGS = { SCRIPT: 1, STYLE: 1, NOSCRIPT: 1, TEXTAREA: 1, CODE: 1, PRE: 1 };
  var ATTRS = ['placeholder', 'title', 'aria-label', 'alt'];

  var root = document.documentElement;
  var exactWords = {};     // 'english text'  -> translation
  var patterns = [];       // [{re, text}]    for entries that contain {}

  function readLang() {
    var m = document.cookie.match('(?:^|; )' + COOKIE + '=([^;]*)');
    var code = m ? decodeURIComponent(m[1]) : '';
    return LANGS[code] ? code : 'en';
  }

  function setLang(code) {
    document.cookie = COOKIE + '=' + code + '; path=/; max-age=31536000; SameSite=Lax';
    // remove the cookie of the old Google-based switcher, if this browser still has it
    document.cookie = 'googtrans=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/';
    location.reload();
  }

  function markActive(lang) {
    document.querySelectorAll('.lang-btn').forEach(function (btn) {
      var on = btn.getAttribute('data-lang') === lang;
      btn.classList.toggle('active', on);
      btn.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
  }

  // ---- matching -------------------------------------------------------------------
  function normalize(text) { return text.replace(/\s+/g, ' ').trim().toLowerCase(); }
  function escapeRe(text) { return text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }

  function exact(text) {
    var t = exactWords[normalize(text)];
    return typeof t === 'string' ? t : null;
  }

  function byPattern(text) {
    for (var i = 0; i < patterns.length; i++) {
      var m = patterns[i].re.exec(text);
      if (!m) { continue; }
      var groups = m.slice(1);
      var out = patterns[i].text.replace(/\{\}/g, function () {
        var piece = groups.shift() || '';
        var known = exact(piece);
        return known === null ? piece : known;
      });
      return out;
    }
    return null;
  }

  function translateString(raw) {
    var text = raw.replace(/\s+/g, ' ').trim();
    if (!text) { return null; }
    var found = exact(text);
    if (found !== null) { return found; }
    found = byPattern(text);
    if (found !== null) { return found; }
    // "Engineering · Pokhara, Nepal · Full-Time": translate each part on its own
    if (text.indexOf(' · ') !== -1) {
      var changed = false;
      var parts = text.split(' · ').map(function (part) {
        var t = exact(part);
        if (t === null) { t = byPattern(part); }
        if (t === null) { return part; }
        changed = true;
        return t;
      });
      if (changed) { return parts.join(' · '); }
    }
    return null;
  }

  // ---- applying ---------------------------------------------------------------------
  function skipped(el) {
    return !el || SKIP_TAGS[el.tagName] === 1 ||
      (el.closest && el.closest('.notranslate, [translate="no"]'));
  }

  function translateTextNode(node) {
    if (skipped(node.parentElement)) { return; }
    var raw = node.nodeValue;
    var t = translateString(raw);
    if (t === null) { return; }
    node.nodeValue = raw.match(/^\s*/)[0] + t + raw.match(/\s*$/)[0];
  }

  function translateAttributes(el) {
    if (skipped(el)) { return; }
    ATTRS.forEach(function (name) {
      var value = el.getAttribute && el.getAttribute(name);
      if (!value) { return; }
      var t = translateString(value);
      if (t !== null) { el.setAttribute(name, t); }
    });
    if (el.tagName === 'INPUT' && /^(submit|button)$/i.test(el.type || '') && el.value) {
      var tv = translateString(el.value);
      if (tv !== null) { el.value = tv; }
    }
  }

  function translateTree(node) {
    if (node.nodeType === 3) { translateTextNode(node); return; }
    if (node.nodeType !== 1 || skipped(node)) { return; }
    translateAttributes(node);
    node.querySelectorAll('[placeholder],[title],[aria-label],[alt],input[type=submit],input[type=button]')
      .forEach(translateAttributes);
    var walker = document.createTreeWalker(node, NodeFilter.SHOW_TEXT);
    var current;
    var batch = [];
    while ((current = walker.nextNode())) { batch.push(current); }
    batch.forEach(translateTextNode);
  }

  function watchForNewContent() {
    new MutationObserver(function (changes) {
      changes.forEach(function (change) {
        change.addedNodes.forEach(translateTree);
      });
    }).observe(document.body, { childList: true, subtree: true });
  }

  function loadWords(words) {
    Object.keys(words).forEach(function (key) {
      if (key.indexOf('{}') === -1) {
        exactWords[key] = words[key];
      } else {
        var re = new RegExp('^' + key.split('{}').map(escapeRe).join('(.+?)') + '$', 'i');
        patterns.push({ re: re, text: words[key] });
      }
    });
  }

  function ready() { root.classList.remove('i18n-pending'); }

  document.addEventListener('DOMContentLoaded', function () {
    var lang = readLang();
    var switcher = document.querySelector('.lang-switch');
    markActive(lang);
    document.querySelectorAll('.lang-btn').forEach(function (btn) {
      btn.addEventListener('click', function () { setLang(btn.getAttribute('data-lang')); });
    });
    if (lang === 'en' || !switcher) { ready(); return; }

    root.setAttribute('lang', lang);
    root.classList.add('lang-' + lang);
    var url = (switcher.getAttribute('data-dict-url') || '').replace('xx', lang);
    fetch(url, { credentials: 'same-origin', headers: { 'Accept': 'application/json' } })
      .then(function (res) { if (!res.ok) { throw new Error('HTTP ' + res.status); } return res.json(); })
      .then(function (words) {
        loadWords(words);
        translateTree(document.body);
        watchForNewContent();
        ready();
      })
      .catch(function () { ready(); });   // could not load: the page simply stays in English
  });
})();
