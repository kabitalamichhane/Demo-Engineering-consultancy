/* FAQ chatbot widget. External file because the site's CSP blocks inline scripts.
   All text from the server is inserted with textContent (never innerHTML). */
(function () {
  'use strict';
  var root = document.getElementById('chatbot');
  if (!root) return;

  var launcher = document.getElementById('cbLauncher');
  var panel = document.getElementById('cbPanel');
  var closeBtn = document.getElementById('cbClose');
  var messages = document.getElementById('cbMessages');
  var suggestions = document.getElementById('cbSuggestions');
  var form = document.getElementById('cbForm');
  var text = document.getElementById('cbText');
  var callback = document.getElementById('cbCallback');
  var started = false;

  function safeUrl(url) {
    if (!url) return '';
    if (url.charAt(0) === '/' && url.charAt(1) !== '/') return url;
    if (url.indexOf('https://') === 0) return url;
    return '';
  }

  function scrollDown() { messages.scrollTop = messages.scrollHeight; }

  function addMessage(who, content, extra) {
    var bubble = document.createElement('div');
    bubble.className = 'cb-msg cb-' + who;
    var p = document.createElement('p');
    p.textContent = content;
    bubble.appendChild(p);
    if (extra) bubble.appendChild(extra);
    messages.appendChild(bubble);
    scrollDown();
    return bubble;
  }

  function actionButton(label, href, external) {
    var a = document.createElement('a');
    a.className = 'cb-action';
    a.textContent = label;
    a.href = href;
    if (external) { a.target = '_blank'; a.rel = 'noopener noreferrer'; }
    return a;
  }

  function actionsFor(data) {
    var wrap = document.createElement('div');
    wrap.className = 'cb-actions';
    var link = safeUrl(data.link_url);
    if (link && data.link_text) wrap.appendChild(actionButton(data.link_text, link, link.indexOf('https://') === 0));
    if (!data.found) {
      var cb = document.createElement('button');
      cb.type = 'button'; cb.className = 'cb-action'; cb.textContent = 'Request a call back';
      cb.addEventListener('click', showCallback);
      wrap.appendChild(cb);
      if (root.dataset.whatsapp) wrap.appendChild(actionButton('WhatsApp us', root.dataset.whatsapp, true));
      wrap.appendChild(actionButton('Get a quote', root.dataset.quoteUrl, false));
    }
    return wrap.childNodes.length ? wrap : null;
  }

  function reply(data) {
    addMessage('bot', data.answer || 'Sorry, something went wrong.', actionsFor(data));
  }

  function ask(params, shownText) {
    if (shownText) addMessage('user', shownText);
    fetch(root.dataset.askUrl + '?' + params, { headers: { 'Accept': 'application/json' }, credentials: 'same-origin' })
      .then(function (r) { return r.json(); })
      .then(reply)
      .catch(function () {
        reply({ found: false, answer: 'Sorry, I could not answer just now. Please contact our team.' });
      });
  }

  function loadSuggestions() {
    fetch(root.dataset.faqsUrl, { headers: { 'Accept': 'application/json' }, credentials: 'same-origin' })
      .then(function (r) { return r.json(); })
      .then(function (data) {
        suggestions.textContent = '';
        (data.suggestions || []).forEach(function (s) {
          var b = document.createElement('button');
          b.type = 'button'; b.className = 'cb-chip'; b.textContent = s.question;
          b.addEventListener('click', function () { ask('id=' + encodeURIComponent(s.id), s.question); });
          suggestions.appendChild(b);
        });
      })
      .catch(function () {});
  }

  function open() {
    panel.hidden = false;
    launcher.setAttribute('aria-expanded', 'true');
    launcher.classList.add('open');
    if (!started) {
      started = true;
      addMessage('bot', 'Hi! I am the Highnoon virtual assistant (automated). Ask me about our services, location or quotes, or tap a question below.');
      loadSuggestions();
    }
    setTimeout(function () { text.focus(); }, 50);
  }

  function close() {
    panel.hidden = true;
    launcher.setAttribute('aria-expanded', 'false');
    launcher.classList.remove('open');
  }

  function showCallback() { callback.hidden = false; form.hidden = true; scrollDown(); }
  function hideCallback() { callback.hidden = true; form.hidden = false; }

  launcher.addEventListener('click', function () { panel.hidden ? open() : close(); });
  closeBtn.addEventListener('click', close);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !panel.hidden) close(); });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var q = text.value.trim();
    if (!q) return;
    text.value = '';
    ask('q=' + encodeURIComponent(q), q);
  });

  document.getElementById('cbCallbackCancel').addEventListener('click', hideCallback);
  callback.addEventListener('submit', function (e) {
    e.preventDefault();
    fetch(root.dataset.callbackUrl, { method: 'POST', body: new FormData(callback), credentials: 'same-origin' })
      .then(function (r) { return r.json().then(function (d) { return { ok: r.ok, data: d }; }); })
      .then(function (res) {
        if (res.ok && res.data.ok) {
          callback.reset(); hideCallback();
          addMessage('bot', 'Thank you! Our team will call you back soon.');
        } else {
          addMessage('bot', (res.data && res.data.error) || 'Please check your details and try again.');
        }
      })
      .catch(function () { addMessage('bot', 'Sorry, we could not send that. Please call or WhatsApp us.'); });
  });
})();
