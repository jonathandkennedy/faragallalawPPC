/* Faragalla Law — PPC landing page runtime (~3KB, no dependencies)
   Handles: UTM/GCLID capture, form submit → thank-you redirect,
   dataLayer events, and focus management for CTA anchor jumps. */
(function () {
  'use strict';

  window.dataLayer = window.dataLayer || [];

  var TRACK_KEYS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'gclid', 'gbraid', 'wbraid', 'msclkid', 'fbclid'];
  var STORE_KEY = 'fl_attribution';

  function safeStorage(fn, fallback) {
    try { return fn(); } catch (e) { return fallback; }
  }

  /* ---- Attribution: capture URL params, persist first-touch + last-touch ---- */
  function getAttribution() {
    var params = new URLSearchParams(window.location.search);
    var current = {};
    TRACK_KEYS.forEach(function (k) {
      var v = params.get(k);
      if (v) current[k] = v.slice(0, 200);
    });

    var stored = safeStorage(function () {
      return JSON.parse(localStorage.getItem(STORE_KEY) || 'null');
    }, null) || { first: null, last: null };

    if (Object.keys(current).length) {
      current._ts = new Date().toISOString();
      current._lp = window.location.pathname;
      if (!stored.first) stored.first = current;
      stored.last = current;
      safeStorage(function () { localStorage.setItem(STORE_KEY, JSON.stringify(stored)); });
    }
    return stored;
  }

  var attribution = getAttribution();

  /* ---- Fill hidden fields in every form ---- */
  function fillHidden(form) {
    var last = attribution.last || {};
    var first = attribution.first || {};
    TRACK_KEYS.forEach(function (k) {
      var el = form.querySelector('[name="' + k + '"]');
      if (el && !el.value) el.value = last[k] || '';
    });
    var setVal = function (name, val) {
      var el = form.querySelector('[name="' + name + '"]');
      if (el) el.value = val || '';
    };
    setVal('landing_page', window.location.pathname);
    setVal('page_url', window.location.href.slice(0, 500));
    setVal('first_touch', first._ts ? (first.utm_source || first.gclid ? JSON.stringify(first).slice(0, 500) : '') : '');
    setVal('referrer', document.referrer.slice(0, 300));
    setVal('device', window.matchMedia('(max-width: 899px)').matches ? 'mobile' : 'desktop');
  }

  /* ---- Form submit: POST, then redirect to thank-you (the real conversion page) ---- */
  function handleForm(form) {
    fillHidden(form);

    form.addEventListener('submit', function (e) {
      e.preventDefault();

      // Honeypot: silently drop bot submissions
      var hp = form.querySelector('[name="company_website"]');
      if (hp && hp.value) return;

      var status = form.querySelector('.lp-form__status');
      var btn = form.querySelector('button[type="submit"]');
      var location_id = form.getAttribute('data-form-location') || 'unknown';

      fillHidden(form); // refresh in case params arrived late

      window.dataLayer.push({
        event: 'lead_form_submit',
        form_location: location_id,
        page_path: window.location.pathname
      });

      if (btn) { btn.disabled = true; btn.setAttribute('data-label', btn.textContent); btn.textContent = 'Sending…'; }
      if (status) { status.className = 'lp-form__status lp-form__status--sending'; status.textContent = 'Sending your request…'; }

      var endpoint = form.getAttribute('data-endpoint');
      var body = new URLSearchParams(new FormData(form)).toString();
      var target = endpoint && endpoint !== '' ? endpoint : '/';

      fetch(target, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: body
      }).then(function (res) {
        if (!res.ok) throw new Error('HTTP ' + res.status);
        var qs = new URLSearchParams();
        qs.set('from', window.location.pathname);
        if (attribution.last && attribution.last.gclid) qs.set('gclid', attribution.last.gclid);
        window.location.assign('/thank-you.html?' + qs.toString());
      }).catch(function () {
        if (btn) { btn.disabled = false; btn.textContent = btn.getAttribute('data-label'); }
        if (status) {
          status.className = 'lp-form__status lp-form__status--error';
          status.textContent = 'Something went wrong sending the form. Please call us instead — the number is at the top of the page.';
        }
        window.dataLayer.push({ event: 'lead_form_error', form_location: location_id });
      });
    });
  }

  /* ---- Phone click tracking ---- */
  function trackCalls() {
    document.querySelectorAll('a[href^="tel:"]').forEach(function (a) {
      a.addEventListener('click', function () {
        window.dataLayer.push({
          event: 'phone_click',
          link_location: a.getAttribute('data-call-location') || 'page',
          page_path: window.location.pathname
        });
      });
    });
  }

  /* ---- CTA anchors: after scrolling to a form, move focus to its first field ---- */
  function focusOnJump() {
    document.querySelectorAll('a[data-jump-form]').forEach(function (a) {
      a.addEventListener('click', function () {
        var id = a.getAttribute('href').slice(1);
        var section = document.getElementById(id);
        if (!section) return;
        var field = section.querySelector('input:not([type="hidden"]), select');
        if (field) setTimeout(function () { field.focus({ preventScroll: true }); }, 450);
      });
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('form.lp-form').forEach(handleForm);
    trackCalls();
    focusOnJump();
  });
})();
