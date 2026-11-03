# sp-forms: Spigelmeyer Productions website form handler

Cloudflare Worker that receives the Contact, Start a Project and Stay on the Signal forms
and emails them to timothy@spigiproducts.com from forms@spigiproducts.com (Reply-To = visitor).

Status: DEPLOYED as sp-forms -> https://sp-forms.timothy-876.workers.dev/submit (Oct 9, 2026). Email Sending onboarded for spigiproducts.com.

## Endpoint contract
POST /submit, JSON: { form: "contact"|"project"|"subscribe", name, email, service, message, website (honeypot), t (ms timestamp form opened), page }
- 200 {ok:true} on success (also returned silently for honeypot/too-fast bot submissions)
- 422 {ok:false, error, fields:{name:"Required."...}} on validation errors
- 403 bad Origin, 404/405/413/415 as usual, 502 if Email Sending fails
- CORS: https://spigiproducts.com, https://www.spigiproducts.com, https://spigelmeyer-productions.pages.dev, https://*.spigelmeyer-productions.pages.dev
- GET /health -> {ok:true}

## Prerequisites (not done yet)
1. Workers Paid plan on the account (Email Sending to arbitrary recipients is not available on Workers Free).
2. Onboard spigiproducts.com in Dashboard > Compute > Email Service > Email Sending (or API POST /zones/{zone}/email/sending/subdomains {"name":"spigiproducts.com"}).
   Run the preview first: POST /zones/{zone}/email/sending/subdomains/preview. Records go on cf-bounce.spigiproducts.com
   (MX, SPF, DKIM) so the apex SPF used by Microsoft 365 does not need to change. The existing _dmarc record must stay the only DMARC record.
3. A workers.dev subdomain for the account (opening Workers & Pages in the dashboard creates one), or a route.

## Deploy
npx wrangler deploy        (from this folder; wrangler.toml has the send_email binding restricted to forms@ -> timothy@)
Then set FORMS_ENDPOINT in ../pages-src/build.py to https://sp-forms.<subdomain>.workers.dev/submit, run build.py, redeploy pages-site.
With FORMS_ENDPOINT empty, the site keeps the mailto fallback.
