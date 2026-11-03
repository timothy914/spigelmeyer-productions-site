// Spigelmeyer Productions: website form handler (Cloudflare Worker, ES module).
// Accepts POST JSON from the Contact, Start a Project and Stay on the Signal forms,
// validates it, and emails timothy@spigiproducts.com via the Email Sending binding (env.EMAIL).
// From: forms@spigiproducts.com · Reply-To: the visitor.

const TO = 'timothy@spigiproducts.com';
const FROM = { email: 'forms@spigiproducts.com', name: 'Spigelmeyer Productions Website' };
const ALLOWED_ORIGINS = new Set([
  'https://spigiproducts.com',
  'https://www.spigiproducts.com',
  'https://spigelmeyer-productions.pages.dev',
]);
const PREVIEW_ORIGIN = /^https:\/\/[a-z0-9-]+\.spigelmeyer-productions\.pages\.dev$/;
const FORMS = {
  contact:   { subject: 'General Contact',          required: ['name', 'email', 'message'] },
  project:   { subject: 'Design Services Inquiry',  required: ['name', 'email', 'message'] },
  subscribe: { subject: 'Stay on the Signal signup', required: ['email'] },
};
const MAX = { name: 120, email: 200, service: 60, message: 5000 };
const SERVICES = new Set(['Brand Identity', 'Storytelling Design', 'Not sure yet', '']);
const EMAIL_RE = /^[^\s@<>"',;]+@[^\s@<>"',;]+\.[a-z]{2,}$/i;

function cors(origin) {
  const ok = origin && (ALLOWED_ORIGINS.has(origin) || PREVIEW_ORIGIN.test(origin));
  return ok ? {
    'Access-Control-Allow-Origin': origin,
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '86400',
    'Vary': 'Origin',
  } : { 'Vary': 'Origin' };
}
const json = (status, body, origin) =>
  new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json; charset=utf-8', ...cors(origin) } });
const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const clean = s => (typeof s === 'string' ? s : '').replace(/\r\n?/g, '\n').trim();
const oneLine = s => clean(s).replace(/[\n\t]+/g, ' ');

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const origin = request.headers.get('Origin') || '';
    const originOk = ALLOWED_ORIGINS.has(origin) || PREVIEW_ORIGIN.test(origin);

    if (url.pathname === '/health') return json(200, { ok: true }, origin);
    if (url.pathname !== '/submit') return json(404, { ok: false, error: 'Not found.' }, origin);
    if (request.method === 'OPTIONS') return new Response(null, { status: originOk ? 204 : 403, headers: cors(origin) });
    if (request.method !== 'POST') return json(405, { ok: false, error: 'Method not allowed.' }, origin);
    if (!originOk) return json(403, { ok: false, error: 'Origin not allowed.' }, origin);
    if (!(request.headers.get('Content-Type') || '').includes('application/json'))
      return json(415, { ok: false, error: 'Send JSON.' }, origin);
    if (Number(request.headers.get('Content-Length') || 0) > 20000)
      return json(413, { ok: false, error: 'Message too long.' }, origin);

    let d;
    try { d = await request.json(); } catch { return json(400, { ok: false, error: 'Invalid request.' }, origin); }
    if (!d || typeof d !== 'object') return json(400, { ok: false, error: 'Invalid request.' }, origin);

    const form = FORMS[d.form];
    if (!form) return json(400, { ok: false, error: 'Unknown form.' }, origin);

    // Spam checks: honeypot field must be empty; form must have been open at least 3 seconds.
    // Bots get a fake success so they don't retry.
    const elapsed = Date.now() - Number(d.t || 0);
    if (clean(d.website) || !(elapsed > 3000 && elapsed < 86400000)) return json(200, { ok: true }, origin);

    const f = {
      name: oneLine(d.name), email: oneLine(d.email).toLowerCase(),
      service: oneLine(d.service), message: clean(d.message),
    };
    const errors = {};
    for (const k of form.required) if (!f[k]) errors[k] = 'Required.';
    for (const k of Object.keys(MAX)) if (f[k].length > MAX[k]) errors[k] = 'Too long.';
    if (f.email && !EMAIL_RE.test(f.email)) errors.email = 'Enter a valid email address.';
    if (d.form === 'project' && !SERVICES.has(f.service)) errors.service = 'Choose a listed service.';
    if (Object.keys(errors).length) return json(422, { ok: false, error: 'Please check the highlighted fields.', fields: errors }, origin);

    const rows = [['Form', form.subject], ['Name', f.name], ['Email', f.email]];
    if (d.form === 'project') rows.push(['Service', f.service || 'Not specified']);
    if (f.message) rows.push(['Message', f.message]);
    rows.push(['Page', oneLine(d.page).slice(0, 300) || origin]);

    const subject = `[Website] ${form.subject}${f.name ? ' from ' + f.name : ''}`.slice(0, 200);
    const text = rows.map(([k, v]) => `${k}: ${v}`).join('\n\n') + '\n\nReply to this email to answer the visitor directly.';
    const html = `<div style="font-family:Georgia,serif;color:#1C3A5C;max-width:640px">
<p style="font:600 11px/1.4 Arial,sans-serif;letter-spacing:.2em;text-transform:uppercase;color:#AC9150;margin:0 0 12px">Spigelmeyer Productions · ${esc(form.subject)}</p>
<table cellpadding="8" style="border-collapse:collapse;width:100%">${rows.map(([k, v]) =>
  `<tr><td style="vertical-align:top;font:600 12px Arial,sans-serif;color:#5A6573;width:90px;border-bottom:1px solid #D8CFB8">${esc(k)}</td><td style="font-size:16px;line-height:1.5;border-bottom:1px solid #D8CFB8;white-space:pre-wrap">${esc(v)}</td></tr>`).join('')}</table>
<p style="font:12px Arial,sans-serif;color:#5A6573">Reply to this email to answer the visitor directly.</p></div>`;

    try {
      await env.EMAIL.send({ to: TO, from: FROM, replyTo: f.name ? { email: f.email, name: f.name } : f.email, subject, text, html });
    } catch (e) {
      console.log('send failed', e && e.code, e && e.message);
      return json(502, { ok: false, error: 'We could not send your message just now. Please email timothy@spigiproducts.com.' }, origin);
    }
    return json(200, { ok: true }, origin);
  },
};
