document.addEventListener('DOMContentLoaded', function () {

  /* ---------- Mobile nav toggle ---------- */
  var toggle = document.getElementById('navToggle');
  var nav = document.getElementById('primaryNav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var isOpen = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });
    nav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        nav.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  /* ---------- Fade-in on scroll ---------- */
  var fadeEls = document.querySelectorAll('.fade-in');
  if ('IntersectionObserver' in window && fadeEls.length) {
    var fadeObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in-view');
          fadeObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15 });
    fadeEls.forEach(function (el) { fadeObserver.observe(el); });
  } else {
    fadeEls.forEach(function (el) { el.classList.add('in-view'); });
  }

  /* Safety net: reveal anything already on screen even if the observer never fires
     (new or background tabs, restored pages, translated pages). */
  function revealVisible() {
    var vh = window.innerHeight || document.documentElement.clientHeight;
    document.querySelectorAll('.fade-in:not(.in-view)').forEach(function (el) {
      if (el.getBoundingClientRect().top < vh * 0.95) { el.classList.add('in-view'); }
    });
  }
  window.addEventListener('scroll', revealVisible, { passive: true });
  window.addEventListener('resize', revealVisible);
  window.addEventListener('load', revealVisible);
  window.addEventListener('pageshow', revealVisible);
  document.addEventListener('visibilitychange', revealVisible);
  var revealTries = 0;
  var revealTimer = setInterval(function () {
    revealVisible();
    if (++revealTries >= 10) { clearInterval(revealTimer); }
  }, 500);
  revealVisible();

  /* ---------- Scroll progress bar ---------- */
  var progress = document.createElement('div');
  progress.className = 'scroll-progress';
  document.body.appendChild(progress);
  function updateProgress() {
    var scrollTop = window.scrollY || document.documentElement.scrollTop;
    var docHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    var pct = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
    progress.style.width = pct + '%';
  }
  window.addEventListener('scroll', updateProgress, { passive: true });
  updateProgress();

  /* ---------- Header shadow once scrolled ---------- */
  var header = document.getElementById('site-header');
  function updateHeaderState() {
    if (!header) return;
    if (window.scrollY > 12) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  }
  window.addEventListener('scroll', updateHeaderState, { passive: true });
  updateHeaderState();

  /* ---------- Back-to-top button ---------- */
  var backToTop = document.createElement('button');
  backToTop.className = 'back-to-top';
  backToTop.setAttribute('aria-label', 'Back to top');
  backToTop.innerHTML = '&uarr;';
  document.body.appendChild(backToTop);
  backToTop.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
  window.addEventListener('scroll', function () {
    if (window.scrollY > 480) {
      backToTop.classList.add('visible');
    } else {
      backToTop.classList.remove('visible');
    }
  }, { passive: true });

  /* ---------- Animated stat counters ---------- */
  var statEls = document.querySelectorAll('.stat-value');
  function animateCount(el) {
    var raw = el.textContent.trim();
    var match = raw.match(/^([^\d]*)(\d[\d,]*)(.*)$/);
    if (!match) return; // non-numeric value (e.g. "Pokhara, Nepal") — leave as-is
    var prefix = match[1];
    var target = parseInt(match[2].replace(/,/g, ''), 10);
    var suffix = match[3];
    var current = 0;
    var steps = 40;
    var increment = Math.max(1, Math.ceil(target / steps));
    var interval = setInterval(function () {
      current += increment;
      if (current >= target) {
        current = target;
        clearInterval(interval);
      }
      el.textContent = prefix + current.toLocaleString() + suffix;
    }, 30);
  }
  if ('IntersectionObserver' in window && statEls.length) {
    var statObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          animateCount(entry.target);
          statObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.4 });
    statEls.forEach(function (el) { statObserver.observe(el); });
  }

  /* ---------- Image fallbacks (replaces inline onerror, which the CSP blocks) ---------- */
  function handleImgError(img) {
    var mode = img.getAttribute('data-fallback');
    if (mode === 'hide') {
      img.style.display = 'none';
    } else if (mode === 'show-next' && img.nextElementSibling) {
      img.style.display = 'none';
      img.nextElementSibling.style.display = 'flex';
    }
  }
  document.addEventListener('error', function (e) {
    if (e.target && e.target.tagName === 'IMG' && e.target.hasAttribute('data-fallback')) {
      handleImgError(e.target);
    }
  }, true);
  document.querySelectorAll('img[data-fallback]').forEach(function (img) {
    if (img.complete && img.naturalWidth === 0) handleImgError(img);
  });

  /* ---------- Basic client-side form validation feedback ---------- */
  document.querySelectorAll('form').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      var invalid = form.querySelectorAll(':invalid');
      invalid.forEach(function (field) {
        var existing = field.parentElement.querySelector('.field-error');
        if (!existing) {
          var msg = document.createElement('span');
          msg.className = 'field-error';
          msg.textContent = 'Please complete this field correctly.';
          field.parentElement.appendChild(msg);
        }
      });
    });
  });
});

/* ---------- Hero heading: letters appear one by one, left to right ---------- */
document.addEventListener('DOMContentLoaded', function () {
  var h1 = document.querySelector('.hero-content h1');
  if (!h1 || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  // A headline cut into single letters cannot be translated, so the letter
  // animation is skipped while Nepali / Hindi is selected.
  var chosen = (document.cookie.match(/(?:^|; )hes_lang=([^;]*)/) || [])[1] || 'en';
  if (chosen !== 'en') return;
  var text = h1.textContent.trim();
  h1.setAttribute('aria-label', text);
  h1.textContent = '';
  var i = 0;
  text.split(' ').forEach(function (word, w, words) {
    var wordEl = document.createElement('span');
    wordEl.className = 'hero-word';
    wordEl.setAttribute('aria-hidden', 'true');
    word.split('').forEach(function (ch) {
      var s = document.createElement('span');
      s.className = 'hero-letter';
      s.textContent = ch;
      s.style.animationDelay = (0.2 + i * 0.045) + 's';
      i += 1;
      wordEl.appendChild(s);
    });
    h1.appendChild(wordEl);
    if (w < words.length - 1) h1.appendChild(document.createTextNode(' '));
  });
});
