/* Spigelmeyer Productions: disclosure dropdowns for the grouped nav.
   Click/Enter/Space toggles; Escape closes and returns focus; ArrowDown opens and moves in;
   clicking or tabbing outside closes. No hover-only behavior. */
(function () {
  var nav = document.getElementById('site-nav');
  if (!nav) return;
  var toggles = Array.prototype.slice.call(nav.querySelectorAll('.nav-toggle'));
  function sub(t) { return document.getElementById(t.getAttribute('aria-controls')); }
  function setOpen(t, open) { t.setAttribute('aria-expanded', String(open)); }
  function closeAll(except) { toggles.forEach(function (t) { if (t !== except) setOpen(t, false); }); }
  toggles.forEach(function (t) {
    t.addEventListener('click', function () {
      var open = t.getAttribute('aria-expanded') === 'true';
      closeAll(t); setOpen(t, !open);
    });
    t.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown') {
        e.preventDefault(); closeAll(t); setOpen(t, true);
        var first = sub(t).querySelector('a'); if (first) first.focus();
      }
    });
    var s = sub(t);
    s.addEventListener('keydown', function (e) {
      var links = Array.prototype.slice.call(s.querySelectorAll('a'));
      var i = links.indexOf(document.activeElement);
      if (e.key === 'ArrowDown') { e.preventDefault(); links[(i + 1) % links.length].focus(); }
      if (e.key === 'ArrowUp') { e.preventDefault(); if (i <= 0) t.focus(); else links[i - 1].focus(); }
    });
  });
  // Escape: close an open dropdown first (and stop here); otherwise site.js closes the mobile menu.
  nav.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    var open = toggles.filter(function (t) { return t.getAttribute('aria-expanded') === 'true'; })[0];
    if (open) { setOpen(open, false); open.focus(); e.stopPropagation(); }
  });
  document.addEventListener('click', function (e) { if (!nav.contains(e.target)) closeAll(); });
  nav.addEventListener('focusout', function (e) {
    var li = e.target.closest('.has-sub');
    if (li && !li.contains(e.relatedTarget)) { var t = li.querySelector('.nav-toggle'); if (e.relatedTarget) setOpen(t, false); }
  });
  // Same-page anchor links (e.g. About, The Frequency) should close the mobile menu after use.
  nav.addEventListener('click', function (e) {
    var a = e.target.closest('a'); if (!a) return;
    closeAll();
    var btn = document.querySelector('.burger');
    if (btn && btn.getAttribute('aria-expanded') === 'true') { btn.setAttribute('aria-expanded', 'false'); nav.classList.remove('open'); }
  });
})();
