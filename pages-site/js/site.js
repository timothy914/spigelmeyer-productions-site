/* Spigelmeyer Productions: small site script (mobile menu + forms). */
(function () {
  // Mobile menu
  var btn = document.querySelector('.burger');
  var nav = document.getElementById('site-nav');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var open = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', String(!open));
      nav.classList.toggle('open', !open);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('open')) {
        btn.setAttribute('aria-expanded', 'false');
        nav.classList.remove('open');
        btn.focus();
      }
    });
  }

  // Forms. If <meta name="sp-forms-endpoint"> is present, forms POST JSON to the
  // Cloudflare Worker and show the result on the page. Otherwise they fall back to
  // composing an email in the visitor's mail app.
  var meta = document.querySelector('meta[name="sp-forms-endpoint"]');
  var endpoint = meta && meta.content;
  var opened = Date.now();

  function setStatus(form, msg, kind) {
    var s = form.querySelector('.form-status');
    if (!s) return;
    s.textContent = msg;
    s.className = 'fine form-status' + (kind ? ' is-' + kind : '');
  }

  function mailtoFallback(form) {
    var to = form.getAttribute('data-mailto');
    var subject = form.getAttribute('data-subject') || 'Website message';
    var lines = [];
    form.querySelectorAll('input, select, textarea').forEach(function (el) {
      if (!el.name || el.name === 'website' || el.type === 'submit') return;
      lines.push((el.getAttribute('data-label') || el.name) + ': ' + (el.value || '').trim());
    });
    var nameEl = form.querySelector('[name="name"]');
    if (nameEl && nameEl.value.trim()) subject += ' from ' + nameEl.value.trim();
    window.location.href = 'mailto:' + to + '?subject=' + encodeURIComponent(subject) +
      '&body=' + encodeURIComponent(lines.join('\n\n'));
    setStatus(form, 'Your email app should open with your message ready to send. If it does not, write to ' + to + '.');
  }

  document.querySelectorAll('form[data-form]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      form.querySelectorAll('[aria-invalid]').forEach(function (el) { el.removeAttribute('aria-invalid'); });
      if (!form.reportValidity()) return;
      if (!endpoint) return mailtoFallback(form);

      var data = { form: form.getAttribute('data-form'), t: opened, page: location.pathname };
      form.querySelectorAll('input, select, textarea').forEach(function (el) {
        if (el.name) data[el.name] = el.value;
      });
      var submit = form.querySelector('[type="submit"]');
      var label = submit.textContent;
      submit.disabled = true;
      submit.textContent = 'Sending…';
      setStatus(form, 'Sending…');

      fetch(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
        .then(function (r) { return r.json().catch(function () { return { ok: false }; }); })
        .then(function (res) {
          if (res && res.ok) {
            form.reset();
            opened = Date.now();
            setStatus(form, data.form === 'subscribe'
              ? 'Thank you. You are on the signal.'
              : 'Thank you. Your message is on its way, and Timothy will reply by email.', 'ok');
          } else {
            if (res && res.fields) Object.keys(res.fields).forEach(function (k) {
              var el = form.querySelector('[name="' + k + '"]');
              if (el) el.setAttribute('aria-invalid', 'true');
            });
            setStatus(form, (res && res.error) || 'Something went wrong. Please email ' + form.getAttribute('data-mailto') + '.', 'err');
          }
        })
        .catch(function () {
          setStatus(form, 'We could not reach the server. Please try again, or email ' + form.getAttribute('data-mailto') + '.', 'err');
        })
        .then(function () { submit.disabled = false; submit.textContent = label; });
    });
  });
})();
