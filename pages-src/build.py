#!/usr/bin/env python3
"""Generates the static pages in ../pages-site from shared header/footer templates.
Run: python3 build.py   (pages-site/ is the deployable output; this script is not deployed)"""
from pathlib import Path
OUT = Path(__file__).resolve().parent.parent / 'pages-site'
BASE = 'https://spigiproducts.com'   # assumed production domain, used only for canonical/OG/sitemap
EMAIL = 'timothy@spigiproducts.com'
# Form handler endpoint (Cloudflare Worker in ../forms-worker). Leave '' to keep the mailto fallback.
# Set to e.g. 'https://sp-forms.<subdomain>.workers.dev/submit' once Email Sending is live, then rebuild + redeploy.
FORMS_ENDPOINT = 'https://sp-forms.timothy-876.workers.dev/submit'
LIVE = bool(FORMS_ENDPOINT)
HONEYPOT = '<div class="hp" aria-hidden="true"><label>Leave this empty<input name="website" tabindex="-1" autocomplete="off"></label></div>'
PHONE = '814-537-8014'
TEL = '+18145378014'
KINDLE = 'https://www.amazon.com/dp/B0HFCYQGKM'
KINDLE_FREQ = 'https://www.amazon.com/dp/B0H7NWJTVX'
GUMROAD = 'https://spigimaster.gumroad.com/l/tdipmj'
STORE = 'https://spigelmeyer.com'
SOCIAL = [
    ('X', 'https://x.com/17Timothy21', 'ic-x.svg'),
    ('Instagram', 'https://www.instagram.com/timothyleespigelmeyerjr', 'ic-instagram.svg'),
    ('LinkedIn', 'https://www.linkedin.com/in/timothy-lee-spigelmeyer-jr-781b3437b', 'ic-linkedin.svg'),
    ('Facebook', 'https://www.facebook.com/profile.php?id=61595340982492', 'ic-facebook.svg'),
]
NAV = [('index.html', 'Home'), ('publications.html', 'Publications'), ('design-services.html', 'Design Services'),
       ('merch.html', 'Merch'), ('field-notes.html', 'Field Notes'), ('contact.html', 'Contact')]
import os
# PREVIEW=1 adds unreleased pages (The Inner Thread) and writes to ../pages-site-preview; default build is unchanged production.
PREVIEW = os.environ.get('PREVIEW') == '1'
NAV.insert(5, ('the-inner-thread.html', 'The Inner Thread'))
FOOTER_EXTRA = []   # footer-only Explore links
NAV.insert(3, ('portfolio.html', 'Portfolio'))      # published 2026-10-28
FOOTER_EXTRA.append(('government.html', 'Government &amp; Military'))   # live 2026-10-30
if PREVIEW:
    OUT = OUT.parent / 'pages-site-preview'
# Grouped primary nav (sitewide, both builds). Flat NAV above still drives footer + sitemap.
NAV_GROUPS = [
    ('Work', [('design-services.html', 'Design Services'), ('portfolio.html', 'Portfolio')]),
    ('Publications', [('publications.html', 'All Publications'), ('publications.html#in-the-beginning', 'In The Beginning'),
                      ('publications.html#the-frequency', 'The Frequency'), ('field-notes.html', 'Field Notes'),
                      ('the-inner-thread.html', 'The Inner Thread')]),
    ('Merch', 'merch.html'),
    ('About', 'index.html#about'),
]
NAV_GROUPS.append(('Government', 'government.html'))   # live 2026-10-30
NAV_GROUPS.append(('Start a Project', 'contact.html', 'cta'))
EXT = 'target="_blank" rel="noopener"'
STAR = '<img src="img/star.svg" alt="">'

# Preview-only nav tightening for 7 nav items (desktop >1040px; burger below is unchanged). Move into css/site.css at publish.
NAV_FIX = '''<style>
@media (min-width:1041px){.hdr{gap:28px}.hdr .logo{flex-shrink:0}.site-nav ul{gap:clamp(16px,1.6vw,28px)}.site-nav a{font-size:11px;letter-spacing:.14em;white-space:nowrap}}
@media (min-width:1041px) and (max-width:1219px){.hdr{gap:20px}.hdr .logo img{height:36px}.site-nav ul{gap:14px}.site-nav a{font-size:10.5px;letter-spacing:.08em}}
</style>'''

def head(file, title, desc, og_image='/img/social-share.jpg', og_type='website'):
    path = '/' if file == 'index.html' else '/' + file.replace('.html', '')
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">{(chr(10)+'<meta name="robots" content="noindex, nofollow">') if PREVIEW else ""}
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="veteran-owned creative productions, brand identity design, storytelling design, memoir, iPennedIt Publishing, The Frequency journal">
<meta name="theme-color" content="#0F1E2D">{(chr(10)+'<meta name="sp-forms-endpoint" content="'+FORMS_ENDPOINT+'">') if LIVE else ""}
<link rel="canonical" href="{BASE}{path}">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="512x512" href="img/icon-512.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Spigelmeyer Productions">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{BASE}{path}">
<meta property="og:image" content="{BASE}{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@17Timothy21">
<link rel="stylesheet" href="css/site.css">
<link rel="stylesheet" href="css/nav.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
'''

def _li(h, t, file):
    cur = ' aria-current="page"' if h == file else ''
    return f'<li><a href="{h}"{cur}>{t}</a></li>'

def header(file):
    parts = []
    for i, item in enumerate(NAV_GROUPS):
        label, target = item[0], item[1]
        if isinstance(target, list):
            sid = f'nav-sub-{i}'
            cur = ' is-current' if any(h.split('#')[0] == file for h, _ in target) else ''
            subs = ''.join(_li(h, t, file) for h, t in target)
            parts.append(f'      <li class="has-sub"><button type="button" class="nav-toggle{cur}" aria-expanded="false" aria-controls="{sid}">{label}<span class="caret" aria-hidden="true"></span></button>\n        <ul class="sub" id="{sid}">{subs}</ul></li>')
        else:
            cls = ' class="nav-cta"' if len(item) > 2 else ''
            cur = ' aria-current="page"' if target == file else ''
            parts.append(f'      <li{cls}><a href="{target}"{cur}>{label}</a></li>')
    items = '\n'.join(parts)
    return f'''<header class="site">
  <div class="wrap hdr">
    <a class="logo" href="index.html"><img src="img/SP_horizontal_fullcolor-onlight.svg" alt="Spigelmeyer Productions home" width="250" height="44"></a>
    <button class="burger" type="button" aria-label="Main menu" aria-expanded="false" aria-controls="site-nav"><span></span><span></span><span></span></button>
    <nav class="site-nav" id="site-nav" aria-label="Main"><ul class="nav-top">
{items}
    </ul></nav>
  </div>
</header>
<main id="main" tabindex="-1">
'''

def social(cls='social'):
    return f'<div class="{cls}">' + ''.join(
        f'<a href="{u}" {EXT} aria-label="{n} (opens in a new tab)"><img src="img/{i}" alt=""></a>' for n, u, i in SOCIAL) + '</div>'

def footer():
    links = ''.join(f'<li><a href="{h}">{t}</a></li>' for h, t in NAV + FOOTER_EXTRA)
    return f'''</main>
<footer class="site">
  <div class="wrap">
    <div class="f-grid">
      <div>
        <div class="f-brand"><img src="img/SP_seal_fullcolor-ondark.svg" alt="SP seal"><div class="w">SPIGELMEYER<small>PRODUCTIONS</small></div></div>
        <p class="f-tag">Meaning-making, not decoration.</p>
      </div>
      <div><h2 class="f-h">Explore</h2><ul class="f-nav">{links}</ul></div>
      <div><h2 class="f-h">Contact</h2>
        <div class="f-contact"><a href="mailto:{EMAIL}">{EMAIL}</a><br><a href="tel:{TEL}">{PHONE}</a></div>
        {social()}
      </div>
    </div>
    <div class="f-bot">
      <span class="v">{STAR}Veteran Owned and Operated</span>
      <span>&copy; 2026 Timothy Lee Spigelmeyer Jr and Spigelmeyer Productions. All Rights Reserved.</span>
    </div>
  </div>
</footer>
<script src="js/site.js" defer></script>
<script src="js/nav.js" defer></script>
</body>
</html>
'''

def banner(kicker, title, lede, extra=''):
    return f'''<section class="banner dark">
  <div class="wrap">
    <div class="kicker c">{kicker}</div>
    <h1>{title}</h1>
    <p class="lede">{lede}</p>
    {extra}
  </div>
</section>
'''

SUBSCRIBE = f'''<section class="sub-band dark" aria-labelledby="signal-h">
  <div class="wrap sub-grid">
    <figure class="sub-img"><img src="img/frequency-spread.jpg" alt="Inside The Frequency, Issue 1: Signal" width="1400" height="1076" loading="lazy"><figcaption>Inside Issue 1 &middot; Signal</figcaption></figure>
    <div>
      <div class="kicker">Stay on the Signal</div>
      <h2 id="signal-h">New Issues &amp; Releases</h2>
      <p class="lede">Be the first to know when a new issue of The Frequency, a new book, or a new release is ready.</p>
      <!-- Posts to the forms Worker when FORMS_ENDPOINT is set; otherwise falls back to a pre-filled email. -->
      <form class="form" action="mailto:{EMAIL}?subject=Subscribe%20me%20to%20Stay%20on%20the%20Signal" method="post" enctype="text/plain"
            data-form="subscribe" data-mailto="{EMAIL}" data-subject="Subscribe me to Stay on the Signal">
        {HONEYPOT}
        <div class="row">
          <label class="sr-only" for="sub-name">First name</label>
          <input id="sub-name" type="text" name="name" data-label="First name" placeholder="First name" autocomplete="given-name">
          <label class="sr-only" for="sub-email">Email address</label>
          <input id="sub-email" type="email" name="email" data-label="Email" placeholder="Email address" autocomplete="email" required>
        </div>
        <button class="btn btn-gold" type="submit">Subscribe</button>
        <p class="fine form-status" aria-live="polite"></p>
      </form>
      <p class="fine">{"Unsubscribe anytime. We only write when something new is ready." if LIVE else "Unsubscribe anytime. For now, subscribing opens a pre-filled email to " + EMAIL + "; online sign-up is coming soon."}</p>
    </div>
  </div>
</section>
'''

# Field Notes posts. A post with a slug has its own page at field-notes/<slug>.html; others are placeholders.
POSTS = {
    'home-was-never-behind-the-door': {
        'title': 'Home Was Never Behind the Door', 'iso': '2026-10-23', 'date': 'October 23, 2026',
        'series': 'The Itinerant Creative',
        'excerpt': 'We stand before doors and call them destinies.',
        'desc': 'We stand before doors and call them destinies. A Field Note from Timothy Lee Spigelmeyer Jr, from the series The Itinerant Creative.',
        'image': 'img/field-notes/home-was-never-behind-the-door.jpg', 'image_w': 1600, 'image_h': 1067, 'wide': True,
        'caption': 'A door, and the light beyond it',
        'share': '/img/field-notes/home-was-never-behind-the-door-share.jpg',
        'alt': 'A dark stone passage opening onto a warm-lit doorway and a lattice window beyond',
        'credit': 'Photo by <a href="https://unsplash.com/@prashantbrahmbhatt" target="_blank" rel="noopener" style="color:inherit">Prashant</a> on <a href="https://unsplash.com" target="_blank" rel="noopener" style="color:inherit">Unsplash</a>',
        'body': [
            'We stand before doors and call them destinies.',
            'This one, we say, and we are saved. That one, and we are lost. And so we tremble in the choosing, as though a whole life waited folded up behind a single handle, and every other door led only to exile from it. We call this deciding. We call it discernment. We call it, sometimes, prayer. But beneath the words, it is fear \u2014 the fear that home is a room we have not yet found, and that we might, through some error of judgment, wander past it forever.',
            'I have stood at enough doors now to know this fear personally. I have left. I have crossed water to do it. I have sat in a resort in a country not my own and asked, the way anyone asks, is this the door. And it was only on the far side of that asking \u2014 not in an answer, but in the exhaustion of asking \u2014 that something else arrived.',
            'Home was never behind a door.',
        ],
    },
    'hotel-cyan': {
        'title': 'Hotel Cyan, Late Afternoon', 'iso': '2026-07-13', 'date': 'July 13, 2026',
        'excerpt': 'The light changes color before it changes angle. Cyan turns toward gold ten minutes before the sun visibly moves.',
        'desc': 'The light changes color before it changes angle. A Field Note from Timothy Lee Spigelmeyer Jr on late afternoon by the water and collecting moments of notice.',
        'image': 'img/field-notes/hotel-cyan.jpg', 'image_w': 1199, 'image_h': 1800,
        'share': '/img/field-notes/hotel-cyan-share.jpg',
        'alt': 'Late afternoon light shifting from cyan toward gold by the water, under a palapa on the shore',
        'body': [
            'The light changes color before it changes angle \u2014 that\u2019s the thing nobody tells you about late afternoon by the water. Cyan turns toward gold ten minutes before the sun visibly moves.',
            'I\u2019ve started treating travel less like collecting destinations and more like collecting these small, specific \u201cmoments of notice.\u201d',
            'Not the postcard version of a place. The version only available if you stay still in it long enough for the light to shift while you\u2019re watching.',
            'This is the seed of something larger I\u2019m building \u2014 but for now, it\u2019s just this: gold arriving in cyan, and me, paying attention.',
        ],
    },
    'what-the-lightning-knew': {
        'title': 'What the Lightning Knew', 'iso': '2026-07-12', 'date': 'July 12, 2026',
        'excerpt': 'Some protections outlive their purpose. They stop guarding you and start gathering you into someone smaller than who you actually are.',
        'desc': 'Some protections outlive their purpose. A Field Note from Timothy Lee Spigelmeyer Jr on a dream of lightning, home plate, and taking off the gear.',
        'image': 'img/field-notes/what-the-lightning-knew.jpg', 'image_w': 1600, 'image_h': 778, 'wide': True,
        'caption': 'The storm, closing in',
        'share': '/img/field-notes/what-the-lightning-knew-share.jpg',
        'alt': 'Lightning splitting a dark storm sky above a lamplit house at night',
        'body': [
            'I dreamed once of standing at home plate as an umpire, lightning closing in, the game suspended but not called. The insulation I was wearing \u2014 meant to protect me \u2014 became the very thing keeping me from moving.',
            'Some protections outlive their purpose. They stop guarding you and start gathering you, piece by piece, into someone smaller than who you actually are.',
            'The dream wasn\u2019t telling me to fear the storm. It was telling me to take off the gear built for a danger that had already passed, and walk back onto the field whole.',
        ],
    },
    'confirmation-bias': {
        'title': 'Confirmation Bias and the Limits of a Useful Word', 'iso': '2026-07-11', 'date': 'July 11, 2026',
        'excerpt': 'Some questions sit outside the lab. Not because they\u2019re unrigorous \u2014 because the instrument doing the measuring is the same thing being measured.',
        'desc': 'Confirmation bias is a genuinely useful word. Most of the time. A Field Note from Timothy Lee Spigelmeyer Jr on where it stops applying cleanly.',
        'image': 'img/field-notes/confirmation-bias.jpg', 'image_w': 1664, 'image_h': 852, 'wide': True,
        'caption': 'The instrument and the measured',
        'share': '/img/field-notes/confirmation-bias-share.jpg',
        'alt': 'A hand reaching toward a row of glowing checkboxes, the first one checked, linked by a web of light',
        'body': [
            'Peter Wason coined confirmation bias in 1960 \u2014 our tendency to favor evidence that already agrees with us. It\u2019s a genuinely useful word. Most of the time.',
            'But there\u2019s a place it stops applying cleanly: when the question isn\u2019t \u201cis my data trustworthy\u201d but \u201cis consciousness itself causal.\u201d',
            'You can\u2019t run a controlled experiment on whether awareness shapes reality from the inside of the very awareness you\u2019re testing.',
            'Some questions sit outside the lab. Not because they\u2019re unrigorous \u2014 because the instrument doing the measuring is the same thing being measured.',
        ],
    },
    'pragmatisms-quiet-agreement': {
        'title': 'Pragmatism\u2019s Quiet Agreement', 'iso': '2026-07-10', 'date': 'July 10, 2026',
        'excerpt': 'Pragmatism never said truth was whatever\u2019s convenient. It said truth proves itself in lived consequence, not in abstract argument.',
        'desc': 'Does it work? A Field Note from Timothy Lee Spigelmeyer Jr on William James, pragmatism, and testing the center by living from it.',
        'image': 'img/field-notes/pragmatisms-quiet-agreement.jpg', 'image_w': 996, 'image_h': 676, 'wide': True,
        'caption': 'A current at your back',
        'share': '/img/field-notes/pragmatisms-quiet-agreement-share.jpg',
        'alt': 'Sunlit stream flowing past a moss-covered log in a green forest',
        'body': [
            'William James asked a simple question of any idea: does it work? Does it produce a difference you can feel, live, act on?',
            'It sounds almost too practical for a philosophy of the soul. But look closer \u2014 pragmatism never said truth was whatever\u2019s convenient. It said truth proves itself in lived consequence, not in abstract argument.',
            'Return to Center makes the same claim from a different door. The center isn\u2019t a concept to win a debate about. It\u2019s something you test by living from it \u2014 and you\u2019ll know it\u2019s true the way you know a current at your back: not because someone argued you into it, but because it moves you.',
        ],
    },
    'the-verse-that-waited': {
        'title': 'The Verse That Waited', 'iso': '2026-07-09', 'date': 'July 9, 2026',
        'epigraph': '“The highlights we leave are not records of what we understood; they are appointments with who we are becoming.”',
        'excerpt': 'A verse can arrive years before you have the instruments to decode it, and it will wait, patient as a highlighted line, until you do.',
        'desc': 'The highlights we leave are appointments with who we are becoming. A Field Note from Timothy Lee Spigelmeyer Jr on returning to Romans 1:25.',
        'image': 'img/field-notes/the-verse-that-waited.jpg', 'image_w': 1002, 'image_h': 554, 'wide': True,
        'caption': 'Return to this',
        'share': '/img/field-notes/the-verse-that-waited-share.jpg',
        'alt': 'An open Bible resting on a rock in a field of wildflowers at sunset',
        'body': [
            'This morning I read a verse I had already read. The highlight was mine — ink from a former self, left in the margin like a flag planted on ground he couldn’t yet hold. Romans 1:25: “Who changed the truth of God into a lie, and worshipped and served the creature more than the Creator, who is blessed for ever.”',
            'The first time through, I marked it because something in me recognized it.',
            'This time, I understood why. That gap — between recognition and understanding — is worth sitting with. We tend to treat reading as a one-way transaction: the text delivers, the reader receives, the page is spent. But scripture doesn’t work that way, and neither does any text that carries real signal. The words don’t change. The receiver does. A verse can arrive years before you have the instruments to decode it, and it will wait, patient as a highlighted line, until you do.',
            'What changed in me between the two readings was a framework. I had spent months building a vocabulary of source and transmission — the conviction that everything that exists is emitting, and that the deepest error available to us is attending to the emission while forgetting the emitter. Paul names that error precisely. To worship and serve the creature more than the Creator is not a failure of devotion; it is devotion with its orientation broken. Attention that lost its return address.',
            'And here is where the verse opens further. The creature is not evil. The creature is a mirror — made in an image, reflecting a source. The error Paul describes is not loving the mirror. It is mistaking the mirror for the light. It is severing the reflection from what it reflects, and then bowing to the fragment as though it were the whole. That is [dis]memberment in its oldest form: not violence against the body, but violence against the connection.',
            'Which brings me back to the highlight itself. That mark was a message from a self who was still gathering pieces. Returning to it this morning was an act of [re]membering — not merely remembering that I had read the verse, but re-joining the reader I was to the reader I have become. The text did not unlock because I tried harder. It unlocked because I returned to it carrying something I did not have before, and the verse — blessed for ever, as Paul says — had never stopped transmitting.',
            'This is why I no longer trust the feeling of having finished a text. The books worth reading are not spent on the first pass. They are seeded. The highlights we leave are not records of what we understood; they are appointments with who we are becoming. Maybe that is the quiet instruction hidden in every marked-up Bible, every dog-eared page, every underline we can’t explain: return to this. You are not done here. Neither is it done with you.',
            'Return to Center.',
            'THEY ARE APPOINTMENTS WITH WHO WE ARE BECOMING',
        ],
    },
    'follow-that-dream': {
        'title': 'Follow That Dream', 'iso': '2026-07-08', 'date': 'July 8, 2026',
        'excerpt': 'So if it looks impossible, that’s not a stop sign. That’s just what a dream looks like before you’ve caught up to it.',
        'desc': 'A street sign in the Yucatan that says exactly what it means. A Field Note from Timothy Lee Spigelmeyer Jr on home, return, and following the dream in motion.',
        'image': 'img/field-notes/follow-that-dream.jpg', 'image_w': 1027, 'image_h': 1800,
        'caption': 'Follow that dream',
        'share': '/img/field-notes/follow-that-dream-share.jpg',
        'alt': 'Timothy pointing up at a teal and white street sign that reads Follow That Dream, beside a painted cafe fence in the Yucatan',
        'body': [
            'There is a street sign here in the Yucatan that says exactly what it means. No metaphor required.',
            'FOLLOW THAT DREAM, teal and white, bolted to a plain pole outside a fence painted with tacos and skincare and aphrodisiac hot dogs — the sacred and the absurd sharing the same wall, the way they always do when you’re paying attention.',
            'I stood under it and pointed up, half-joking, half-not. Because that’s the trick of a dream worth following: it rarely announces itself as serious. It looks like a street sign. A stray line in a book. A city you weren’t planning to move to.',
            'We tend to talk about home as a place we’re moving toward — the destination at the end of the dream, the reward for finally arriving. But home was never a location waiting for us down the road.',
            'Home is what happens when we stop outsourcing ourselves to a place, a title, a version of arrival that keeps receding the closer we get. The walking doesn’t end when we get there, because there was never a there. There was only the return — to center, to self, to the person doing the walking.',
            'That’s what makes following the dream feel impossible. We keep looking for the map before we’ll take the step, when the step is the map. The dream doesn’t clarify itself from a safe distance. It clarifies itself in motion — in the leaving, the relocating, the pointing up at a sign you didn’t put there but somehow needed to see.',
            'So if it looks impossible, that’s not a stop sign. That’s just what a dream looks like before you’ve caught up to it.',
            'Maybe the walk is part of the practice.',
        ],
    },
    'the-opposite-of-forgetting': {
        'title': 'The Opposite of Forgetting', 'iso': '2026-07-07', 'date': 'July 7, 2026',
        'excerpt': 'Healing was never about retrieving lost facts. It’s about gathering the scattered members back into one body.',
        'desc': 'We assume the opposite of remembering is forgetting. It isn’t. A Field Note from Timothy Lee Spigelmeyer Jr on [re]membering and becoming whole again.',
        'image': 'img/field-notes/the-opposite-of-forgetting.jpg', 'image_w': 1600, 'image_h': 852, 'wide': True,
        'caption': 'Gathering the scattered members',
        'share': '/img/field-notes/the-opposite-of-forgetting-share.jpg',
        'alt': 'Silhouette of a head made of dark puzzle pieces, with pieces breaking away from the top',
        'body': [
            'We assume the opposite of remembering is forgetting. It isn’t.',
            'The opposite of [re]membering — putting the members, the parts, back together — is [dis]membering: scattering, fragmenting, tearing the self into pieces that no longer recognize each other.',
            'Trauma dismembers. Fear dismembers. Years of believing the wrong story about who you are — that dismembers too, quietly, one small betrayal of self at a time.',
            'Healing was never about retrieving lost facts. It’s about gathering the scattered members back into one body.',
            'Re-membering.',
            'Becoming whole again, on purpose.',
        ],
    },
    'generation-regeneration': {
        'title': 'Generation. [Re]generation', 'iso': '2026-07-06', 'date': 'July 6, 2026',
        'excerpt': 'This is the shape of every real transformation. Not addition. Not invention. Descent, then return.',
        'desc': 'Re-generation is not a second birth from nothing. A Field Note from Timothy Lee Spigelmeyer Jr on the root gen-, descent, and return.',
        'image': 'img/field-notes/generation-regeneration.jpg', 'image_w': 996, 'image_h': 492, 'wide': True,
        'caption': 'Descent, then return',
        'share': '/img/field-notes/generation-regeneration-share.jpg',
        'alt': 'Overlapping silhouettes of people standing in a row, shading from blue to orange light',
        'body': [
            'Generation comes from the Proto-Indo-European root gen- — to give birth, to bring forth. It’s the root behind gene, genesis, genius. Birth, at the root, is creative force.',
            'But re-generation is the more interesting word. It doesn’t mean a second birth from nothing. It means a return passage — descending back into the source-form before rising again, renewed.',
            'This is the shape of every real transformation. Not addition. Not invention. Descent, then return.',
            'You don’t become new.',
            'You go back down to what generated you in the first place, and you come back up [re]membering.',
        ],
    },
}
SIGNOFF = '~ Timothy'   # standing rule: every Field Note ends with this sign-off
NOTES = [  # (iso, display date, title, slug or None)
    ('2026-10-23', 'October 23, 2026', 'Home Was Never Behind the Door', 'home-was-never-behind-the-door'),
    ('2026-07-13', 'July 13, 2026', 'Hotel Cyan, Late Afternoon', 'hotel-cyan'),
    ('2026-07-12', 'July 12, 2026', 'What the Lightning Knew', 'what-the-lightning-knew'),
    ('2026-07-11', 'July 11, 2026', 'Confirmation Bias and the Limits of a Useful Word', 'confirmation-bias'),
    ('2026-07-10', 'July 10, 2026', 'Pragmatism\u2019s Quiet Agreement', 'pragmatisms-quiet-agreement'),
    ('2026-07-09', 'July 9, 2026', 'The Verse That Waited', 'the-verse-that-waited'),
    ('2026-07-08', 'July 8, 2026', 'Follow That Dream', 'follow-that-dream'),
    ('2026-07-07', 'July 7, 2026', 'The Opposite of Forgetting', 'the-opposite-of-forgetting'),
    ('2026-07-06', 'July 6, 2026', 'Generation. [Re]generation', 'generation-regeneration'),
]

def note_cards(link, limit=None):
    out = []
    for iso, d, t, slug in NOTES[:limit]:
        excerpt = ''
        series = ''   # optional per-post series label; posts without 'series' render unchanged
        if slug and POSTS[slug].get('series'):
            series = f'<p class="series" style="font-family:\'Montserrat\';font-weight:500;font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);margin-top:6px">{POSTS[slug]["series"]}</p>'
        if slug:
            excerpt = f'<p class="excerpt" style="font-size:19px;line-height:1.45;margin-top:12px;color:var(--steward)">{POSTS[slug]["excerpt"]}</p>'
            tail = f'<a class="textlink" href="field-notes/{slug}.html">Read the note<span class="sr-only">: {t}</span></a>'
            t = f'<a href="field-notes/{slug}.html">{t}</a>'
        else:
            tail = ('<a class="textlink" href="field-notes.html">Read the note<span class="sr-only">: ' + t + '</span></a>'
                    if link else '<p class="soon-note">Full note coming soon</p>')
        out.append(f'<article class="ncard"><time class="date" datetime="{iso}">{d}</time>{series}<h3>{t}</h3>{excerpt}{tail}'
                   f'<img class="wm" src="img/SP_seal_fullcolor-onlight.svg" alt=""></article>')
    return '\n      '.join(out)

def frame():
    pos = ['tl', 'tr', 'bl', 'br', 'tc', 'bc', 'lc', 'rc']
    stars = ''.join(f'<div class="s {p}">{STAR}</div>' for p in pos)
    return f'<div class="frame" aria-hidden="true"><div class="d t"></div><div class="d b"></div><div class="d l"></div><div class="d r"></div><div class="red"></div>{stars}</div>'

pages = {}

# ---------------- HOME ----------------
pages['index.html'] = ('Spigelmeyer Productions | Books, Brand Design & Merch',
 'Veteran-owned creative productions: books from iPennedIt Publishing, brand identity and storytelling design, and merch designed in-house.',
f'''<section class="hero" aria-label="Introduction">
  <div class="hero-in">
    {frame()}
    <div class="hero-c">
      <img class="hero-logo" src="img/SP_ruled-stack_fullcolor-ondark.svg" alt="Spigelmeyer Productions" width="460" height="184">
      <h1>Meaning-making, <em>not decoration.</em></h1>
      <p class="sub">Books, design, and apparel built on concept, symbolism, and intention. Built by one hand. Made for many.</p>
      <div class="ctas">
        <a class="btn btn-gold" href="#work">Explore the Work</a>
        <a class="btn btn-ghost" href="design-services.html#start">Start a Project</a>
      </div>
      <div class="vet">{STAR}Veteran-owned{STAR}</div>
    </div>
  </div>
</section>

<section class="doors" id="work" aria-labelledby="work-h">
  <div class="wrap">
    <div class="sec-head">
      <div class="kicker c">The Work</div>
      <h2 id="work-h">Three Doors, One House</h2>
      <p class="lede">Everything we make starts with an idea worth carrying. Choose where to begin.</p>
    </div>
    <div class="cards">
      <article class="card">
        <div class="media"><img src="img/door-publications.jpg" alt="The memoir In The Beginning and The Frequency, Issue 1" width="1200" height="900" loading="lazy"></div>
        <div class="body">
          <div class="num">01 &middot; iPennedIt Publishing</div>
          <h3>Publications</h3>
          <p>From iPennedIt Publishing: books and journals written to return the reader to center.</p>
          <a class="btn btn-navy" href="publications.html">Browse Publications</a>
        </div>
      </article>
      <article class="card">
        <div class="media"><img src="img/door-design.jpg" alt="The SP seal with gold construction lines" width="1200" height="900" loading="lazy"></div>
        <div class="body">
          <div class="num">02 &middot; Graphic Design</div>
          <h3>Design Services</h3>
          <p>Brand identity and storytelling design, each built from a concept, not a template.</p>
          <a class="btn btn-navy" href="design-services.html">Start a Project</a>
        </div>
      </article>
      <article class="card">
        <div class="media"><img src="img/door-merch.jpg" alt="The SP seal as an embroidered patch" width="1200" height="900" loading="lazy"></div>
        <div class="body">
          <div class="num">03 &middot; Designed In-House</div>
          <h3>Merch</h3>
          <p>Apparel and goods we design ourselves, where every mark carries its meaning.</p>
          <a class="btn btn-navy" href="{STORE}" {EXT}>Shop Merch<span class="sr-only"> (opens spigelmeyer.com in a new tab)</span></a>
        </div>
      </article>
    </div>
  </div>
</section>

<section class="books dark" aria-labelledby="shelf-h">
  <div class="wrap">
    <div class="sec-head">
      <div class="kicker c">Publications</div>
      <h2 id="shelf-h">On the Shelf</h2>
    </div>
    <div class="book-grid">
      <article class="book">
        <div class="cover mem"><img src="img/cover-in-the-beginning.jpg" alt="Cover of In The Beginning: A Return to Center by Timothy Lee Spigelmeyer Jr" width="800" height="1230" loading="lazy"></div>
        <div>
          <span class="tag">Now on Kindle</span>
          <h3>In The Beginning</h3>
          <div class="st">A Return to Center</div>
          <div class="by">Timothy Lee Spigelmeyer Jr</div>
          <ul class="facts"><li>A memoir</li><li>Available now in the Kindle Store</li></ul>
          <div class="ctas"><a class="btn btn-gold" href="{KINDLE}" {EXT}>Get it on Kindle</a></div>
        </div>
      </article>
      <article class="book">
        <div class="cover"><img src="img/cover-the-frequency.jpg" alt="Cover of The Frequency, Issue 1: Signal" width="600" height="795" loading="lazy"></div>
        <div>
          <span class="tag">Now on Kindle</span>
          <h3>The Frequency</h3>
          <div class="st">A Quarterly Journal of Depth &amp; Resonance</div>
          <ul class="facts"><li>Issue 1: <b style="font-weight:600">SIGNAL</b></li><li>Available now in the Kindle Store</li><li>ISSN registered with the Library of Congress</li></ul>
          <div class="ctas"><a class="btn btn-gold" href="{KINDLE_FREQ}" {EXT}>Get it on Kindle</a></div>
        </div>
      </article>
    </div>
    <p class="imprint">Published by iPennedIt Publishing &middot; A Spigelmeyer Productions imprint</p>
  </div>
</section>

<section class="notes" aria-labelledby="notes-h">
  <div class="wrap">
    <div class="notes-head">
      <div>
        <div class="kicker">Field Notes</div>
        <h2 id="notes-h">Latest from Field Notes</h2>
        <p class="lede">Philosophy, observation, and the thinking behind the work.</p>
      </div>
      <a class="btn btn-line" href="field-notes.html">All Field Notes</a>
    </div>
    <div class="ncards">
      {note_cards(True, 3)}
    </div>
  </div>
</section>

<section class="about" id="about" aria-labelledby="about-h">
  <div class="wrap about-grid">
    <div class="portrait"><img src="img/headshot.jpg" alt="Timothy Lee Spigelmeyer Jr, founder of Spigelmeyer Productions" width="1000" height="1000" loading="lazy"></div>
    <div>
      <div class="kicker">About</div>
      <h2 id="about-h">Steward of the Mirror</h2>
      <p><span class="name">Spigelmeyer</span> means steward of the mirror. The whole house is built on that idea: every book, garment, and design is made to reflect something true, not just to look good.</p>
      <p>Spigelmeyer Productions is a veteran-owned creative productions company, founded and run by U.S. Navy veteran Timothy Lee Spigelmeyer Jr.</p>
      <p class="motto">Built by one hand <i aria-hidden="true"></i> Made for many</p>
      <a class="btn btn-line" href="field-notes.html">Read Field Notes</a>
    </div>
  </div>
</section>

{SUBSCRIBE}''')

# ---------------- PUBLICATIONS ----------------
pages['publications.html'] = ('Publications | In The Beginning & The Frequency',
 'In The Beginning: A Return to Center, a memoir, and The Frequency, A Quarterly Journal of Depth &amp; Resonance, both on Kindle from iPennedIt Publishing.',
banner('iPennedIt Publishing', 'Publications',
       'Books and journals written to return the reader to center. Published by iPennedIt Publishing, a Spigelmeyer Productions imprint.') + f'''
<section class="section" id="in-the-beginning" aria-labelledby="itb-h">
  <div class="wrap">
    <div class="feature">
      <div class="f-media cover"><img src="img/cover-in-the-beginning.jpg" alt="Cover of In The Beginning: A Return to Center by Timothy Lee Spigelmeyer Jr" width="800" height="1230"></div>
      <div class="prose">
        <span class="tag">Now on Kindle</span>
        <h2 id="itb-h">In The Beginning</h2>
        <p class="st">A Return to Center</p>
        <p class="by">A memoir by Timothy Lee Spigelmeyer Jr</p>
        <p>A memoir by Timothy Lee Spigelmeyer Jr. Available now in the Kindle Store.</p>
        <div class="ctas"><a class="btn btn-navy" href="{KINDLE}" {EXT}>Get it on Kindle<span class="sr-only"> (opens Amazon in a new tab)</span></a></div>
        <p class="small">Published by iPennedIt Publishing.</p>
      </div>
    </div>
  </div>
</section>

<section class="section navy dark" id="the-frequency" aria-labelledby="freq-h">
  <div class="wrap">
    <div class="feature flip">
      <div class="f-media cover"><img src="img/cover-the-frequency.jpg" alt="Cover of The Frequency, Issue 1: Signal" width="600" height="795"></div>
      <div class="prose">
        <span class="tag">Now on Kindle</span>
        <h2 id="freq-h">The Frequency</h2>
        <p class="st">A Quarterly Journal of Depth &amp; Resonance</p>
        <p class="by">Issue 1: SIGNAL</p>
        <p>Issue 1: <em>Signal</em> is available now in the Kindle Store. ISSN registered with the Library of Congress. Published by iPennedIt Publishing.</p>
        <div class="ctas"><a class="btn btn-gold" href="{KINDLE_FREQ}" {EXT}>Get it on Kindle<span class="sr-only"> (opens Amazon in a new tab)</span></a><a class="btn btn-ghost" href="{GUMROAD}" {EXT}>Free Sample Preview<span class="sr-only"> (opens Gumroad in a new tab)</span></a></div>
        <p class="small">The free sample preview is delivered through Gumroad.</p>
      </div>
    </div>
  </div>
</section>

{SUBSCRIBE}''')

# ---------------- DESIGN SERVICES ----------------
pages['design-services.html'] = ('Brand Identity & Storytelling Design | Spigelmeyer',
 'Brand identity and storytelling design from Spigelmeyer Productions, each built from a concept, not a template. Start a project today.',
banner('Graphic Design', 'Design Services',
       'Brand identity and storytelling design, each built from a concept, not a template. Every mark we make is meaning-making, not decoration: grounded in concept, symbolism, and intention.',
       '<a class="btn btn-gold" href="#start">Start a Project</a>' + ' <a class="btn btn-ghost" href="portfolio.html">See the portfolio</a>') + f'''
<section class="section" aria-labelledby="what-h">
  <div class="wrap">
    <div class="sec-head">
      <div class="kicker c">Design Services</div>
      <h2 id="what-h">What We Do</h2>
    </div>
    <div class="svc">
      <article>
        <img src="img/brand-identity.jpg" alt="The Spigelmeyer Productions logo and brand color palette" width="1200" height="900" loading="lazy">
        <div class="body"><h3>Brand Identity</h3><p>Marks and visual identities built from what your name, mission, and story actually mean, so everything you put into the world carries the same intention.</p></div>
      </article>
      <article>
        <img src="img/storytelling-design.jpg" alt="Every symbol chosen on purpose: storytelling design" width="1200" height="900" loading="lazy">
        <div class="body"><h3>Storytelling Design</h3><p>Design that carries a narrative, where every image, symbol, and detail is chosen on purpose so the story reads before a word does.</p></div>
      </article>
    </div>
  </div>
</section>

<section class="section alt" aria-labelledby="how-h">
  <div class="wrap">
    <div class="sec-head">
      <div class="kicker c">Process</div>
      <h2 id="how-h">How We Work</h2>
    </div>
    <ol class="steps">
      <li><h3>Listen</h3><p>It starts with your story, not a style.</p></li>
      <li><h3>Concept</h3><p>We find the idea worth carrying and the symbols that hold it.</p></li>
      <li><h3>Design</h3><p>Every choice is made on purpose and tested for meaning.</p></li>
      <li><h3>Deliver</h3><p>Final files, ready for the places your brand will live.</p></li>
    </ol>
    <div class="brief">
      <div>
        <h3>Creative Brief</h3>
        <p>Want to think it through first? Download the creative brief, fill it in, and attach it to your email.</p>
      </div>
      <a class="btn btn-navy" href="downloads/Creative-Brief_Spigelmeyer-Productions.pdf" download>Download the Brief (PDF)</a>
    </div>
  </div>
</section>

<section class="section" id="start" aria-labelledby="start-h">
  <div class="wrap contact-grid">
    <div>
      <div class="kicker">Design Services Inquiry</div>
      <h2 id="start-h">Start a Project</h2>
      <p class="lede">Tell us about your brand or your story, and what you want it to say. We will reply by email.</p>
      <dl class="c-details">
        <dt>Email</dt><dd><a href="mailto:{EMAIL}?subject=Design%20Services%20Inquiry">{EMAIL}</a></dd>
        <dt>Phone</dt><dd><a href="tel:{TEL}">{PHONE}</a></dd>
      </dl>
    </div>
    <div>
      <!-- Posts to the forms Worker when FORMS_ENDPOINT is set; otherwise falls back to a pre-filled email. -->
      <form class="cform" action="mailto:{EMAIL}?subject=Design%20Services%20Inquiry" method="post" enctype="text/plain"
            data-form="project" data-mailto="{EMAIL}" data-subject="Design Services Inquiry">
        {HONEYPOT}
        <div class="two">
          <div><label for="p-name">Name <span class="req" aria-hidden="true">*</span></label><input id="p-name" name="name" data-label="Name" autocomplete="name" required></div>
          <div><label for="p-email">Email <span class="req" aria-hidden="true">*</span></label><input id="p-email" name="email" data-label="Email" type="email" autocomplete="email" required></div>
        </div>
        <div><label for="p-service">Service you are interested in</label>
          <select id="p-service" name="service" data-label="Service">
            <option>Brand Identity</option><option>Storytelling Design</option><option selected>Not sure yet</option>
          </select></div>
        <div><label for="p-msg">Tell us about your project <span class="req" aria-hidden="true">*</span></label><textarea id="p-msg" name="message" data-label="Project" required></textarea></div>
        <p class="form-note">{("Your inquiry goes straight to Timothy, and the reply comes to the email you enter. Reference files or a completed creative brief? Mention them here and we will tell you where to send them, or email them to " + EMAIL + ".") if LIVE else ("For now this form opens your email app with your message filled in, ready to send to " + EMAIL + ". Reference files or a completed creative brief? Attach them to that email.")}</p>
        <button class="btn btn-navy" type="submit">Send Inquiry</button>
        <p class="fine form-status" aria-live="polite" style="color:var(--muted)"></p>
      </form>
    </div>
  </div>
</section>''')

# ---------------- MERCH ----------------
pages['merch.html'] = ('Merch | Designed In-House by Spigelmeyer Productions',
 'Apparel and goods designed in-house by Spigelmeyer Productions, where every mark carries its meaning. Shop the store at spigelmeyer.com.',
banner('Designed In-House', 'Merch', 'Apparel and goods we design ourselves, where every mark carries its meaning.') + f'''
<section class="section" aria-labelledby="merch-h">
  <div class="wrap">
    <div class="feature">
      <div class="f-media frame-img"><img src="img/door-merch.jpg" alt="The SP seal as an embroidered patch" width="1200" height="900"></div>
      <div class="prose">
        <div class="kicker">The Store</div>
        <h2 id="merch-h">Every Mark Carries Its Meaning</h2>
        <p>Apparel and goods we design ourselves, where every mark carries its meaning. Nothing here is decoration for its own sake: each piece starts with a concept and a symbol worth wearing.</p>
        <div class="ctas"><a class="btn btn-navy" href="{STORE}" {EXT}>Shop Merch<span class="sr-only"> (opens spigelmeyer.com in a new tab)</span></a></div>
        <p class="small">Our store lives at spigelmeyer.com and opens in a new tab.</p>
      </div>
    </div>
  </div>
</section>
<section class="about" aria-label="Motto">
  <div class="wrap" style="text-align:center">
    <p class="motto" style="justify-content:center;margin-top:0">Built by one hand <i aria-hidden="true"></i> Made for many</p>
  </div>
</section>''')

# ---------------- FIELD NOTES ----------------
pages['field-notes.html'] = ('Field Notes | Spigelmeyer Productions',
 'Philosophy, observation, and the thinking behind the work, from Timothy Lee Spigelmeyer Jr of Spigelmeyer Productions.',
banner('Field Notes', 'Field Notes', 'Philosophy, observation, and the thinking behind the work.') + f'''
<section class="notes" aria-labelledby="recent-h">
  <div class="wrap">
    <div class="notes-head">
      <div>
        <div class="kicker">Recent</div>
        <h2 id="recent-h">Latest Notes</h2>
        <p class="lede">Start with the latest note below, or read back through the series.</p>
      </div>
    </div>
    <!-- Posts live in POSTS in build.py (one page each at field-notes/<slug>.html). Cards without a slug are placeholders until their posts are migrated. -->
    <div class="ncards">
      {note_cards(False)}
    </div>
  </div>
</section>
<section class="about" aria-labelledby="fn-follow-h">
  <div class="wrap" style="text-align:center;max-width:760px">
    <div class="kicker c">Follow Along</div>
    <h2 id="fn-follow-h">Between the Notes</h2>
    <p class="lede" style="margin-left:auto;margin-right:auto">Shorter thoughts and new releases are shared on social.</p>
    <div style="display:flex;justify-content:center">{social('social-light')}</div>
  </div>
</section>''')

# ---------------- CONTACT ----------------
pages['contact.html'] = ('Contact | Spigelmeyer Productions',
 'Contact Spigelmeyer Productions about publishing, brand identity and storytelling design, or merch. Email timothy@spigiproducts.com.',
banner('Get in Touch', 'Contact', 'Questions about a book, a design project, or the merch store? Send a note and we will get back to you.') + f'''
<section class="section" aria-labelledby="contact-h">
  <div class="wrap contact-grid">
    <div>
      <div class="kicker">Spigelmeyer Productions</div>
      <h2 id="contact-h">Send a Note</h2>
      <dl class="c-details">
        <dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd>
        <dt>Phone</dt><dd><a href="tel:{TEL}">{PHONE}</a></dd>
        <dt>Design projects</dt><dd><a href="design-services.html#start">Start a Project</a></dd>
      </dl>
      {social('social-light')}
    </div>
    <div>
      <!-- Posts to the forms Worker when FORMS_ENDPOINT is set; otherwise falls back to a pre-filled email. -->
      <form class="cform" action="mailto:{EMAIL}?subject=General%20Contact" method="post" enctype="text/plain"
            data-form="contact" data-mailto="{EMAIL}" data-subject="General Contact">
        {HONEYPOT}
        <div class="two">
          <div><label for="c-name">Name <span class="req" aria-hidden="true">*</span></label><input id="c-name" name="name" data-label="Name" autocomplete="name" required></div>
          <div><label for="c-email">Email <span class="req" aria-hidden="true">*</span></label><input id="c-email" name="email" data-label="Email" type="email" autocomplete="email" required></div>
        </div>
        <div><label for="c-msg">Message <span class="req" aria-hidden="true">*</span></label><textarea id="c-msg" name="message" data-label="Message" required></textarea></div>
        <p class="form-note">{"Your note goes straight to Timothy, and the reply comes to the email you enter." if LIVE else "For now this form opens your email app with your message filled in, ready to send to " + EMAIL + "."}</p>
        <button class="btn btn-navy" type="submit">Send Message</button>
        <p class="fine form-status" aria-live="polite" style="color:var(--muted)"></p>
      </form>
    </div>
  </div>
</section>''')

# ---------------- 404 ----------------
pages['404.html'] = ('Page Not Found | Spigelmeyer Productions', 'This page could not be found.',
banner('404', 'Page Not Found', 'The page you were looking for is not here. Try one of the doors below.',
       '<a class="btn btn-gold" href="index.html">Return Home</a>'))

import re as _re
POST_STYLE = '''<style>
.post-head{background:var(--midnight) url(../img/page-banner.jpg) center/cover no-repeat;color:var(--ivory);text-align:center}
.post-head .wrap{padding-top:84px;padding-bottom:84px;max-width:860px}
.post-head h1{font-family:'Cinzel';font-weight:500;font-size:46px;letter-spacing:.05em;line-height:1.15;margin-top:18px;color:var(--ivory)}
.post-head time{display:block;margin-top:18px;font-family:'Montserrat';font-weight:500;font-size:12px;letter-spacing:.24em;text-transform:uppercase;color:#C9CFD6}
.post{padding:72px 0 96px}
.post .wrap{max-width:760px}
.post figure{position:relative;padding:12px;margin:0 auto 48px;max-width:560px}
.post figure::before{content:"";position:absolute;inset:0;border:1px solid var(--gold)}
.post figure.wide{max-width:100%}
.post figure img{width:100%}
.post .body p.signoff{font-style:italic;font-size:26px;color:var(--steward);margin-top:32px}
.post figcaption{font-family:'Montserrat';font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);text-align:center;margin-top:14px}
.post .body p{font-size:23px;line-height:1.65;color:var(--midnight);margin-top:24px}
.post .body p:first-child::first-letter{font-family:'Cinzel';float:left;font-size:64px;line-height:.9;padding:6px 10px 0 0;color:var(--gold)}
.post .sign{margin-top:44px;padding-top:28px;border-top:1px solid var(--line);display:flex;justify-content:space-between;align-items:center;gap:20px;flex-wrap:wrap}
.post .sign .motto{margin-top:0;font-size:15px}
@media (max-width:720px){.post-head h1{font-size:32px}.post-head .wrap{padding-top:56px;padding-bottom:56px}.post{padding:48px 0 72px}.post .body p{font-size:20px}.post figure{margin-bottom:36px}}
</style>
'''

def post_page(slug, P):
    paras = '\n        '.join(f'<p>{x}</p>' for x in P['body'])
    epi = (f'<p class="epigraph" style="font-family:\'Cormorant\';font-style:italic;font-size:26px;line-height:1.4;color:var(--midnight);text-align:center;max-width:620px;margin:0 auto 40px">{P["epigraph"]}</p>\n    ') if P.get('epigraph') else ''
    cred = (f'<p class="credit" style="font-family:\'Montserrat\';font-size:11px;letter-spacing:.06em;color:var(--muted);text-align:center;margin-top:8px">{P["credit"]}</p>') if P.get('credit') else ''   # optional photo credit
    ser = (f'\n    <p class="series" style="font-family:\'Montserrat\';font-weight:600;font-size:12px;letter-spacing:.3em;text-transform:uppercase;color:var(--gold-l);margin-top:14px">{P["series"]}</p>') if P.get('series') else ''
    body = f'''<section class="post-head dark" aria-label="Field Note">
  <div class="wrap">
    <div class="kicker c">Field Notes</div>
    <h1>{P["title"]}</h1>
    <time datetime="{P["iso"]}">{P["date"]}</time>{ser}
  </div>
</section>
<article class="post" aria-labelledby="post-title">
  <div class="wrap">
    <h2 id="post-title" class="sr-only">{P["title"]}</h2>
    <figure{' class="wide"' if P.get("wide") else ''}><img src="{P["image"]}" alt="{P["alt"]}" width="{P["image_w"]}" height="{P["image_h"]}"><figcaption>{P.get("caption", "Late afternoon, by the water")}</figcaption>{cred}</figure>
    {epi}<div class="body">
        {paras}
        <p class="signoff">{SIGNOFF}</p>
    </div>
    <div class="sign">
      <p class="motto">Built by one hand <i aria-hidden="true"></i> Made for many</p>
      <a class="btn btn-line" href="field-notes.html">All Field Notes</a>
    </div>
  </div>
</article>
'''
    file = f'field-notes/{slug}.html'
    html = head(file, f'{P["title"]} | Field Notes | Spigelmeyer Productions', P['desc'], og_image=P['share'], og_type='article') \
        + header('field-notes.html') + body + '\n' + footer()
    html = html.replace('<link rel="stylesheet" href="css/site.css">', '<link rel="stylesheet" href="css/site.css">\n' + POST_STYLE.rstrip())
    html = html.replace('<meta name="theme-color"', f'<meta property="article:published_time" content="{P["iso"]}">\n<meta name="theme-color"', 1)
    # page lives one folder down: prefix site-relative links and assets with ../
    html = _re.sub(r'((?:href|src)=")(?!https?:|mailto:|tel:|#|/|\.\./)', r'\1../', html)
    return file, html


# ---------------- THE INNER THREAD (preview only) ----------------
IT_STYLE = """<style>
.it-intro{max-width:760px;margin:0 auto}
.it-season h2{text-align:center}.it-ep{margin-top:56px}.it-ep h3{font-family:'Cinzel';font-weight:400;font-size:30px;line-height:1.25;text-align:center;color:var(--midnight)}.it-ep-soon{padding-top:40px;border-top:1px solid var(--line);max-width:760px;margin-left:auto;margin-right:auto}
.it-meta{font-family:'Montserrat';font-size:12px;letter-spacing:.3em;text-transform:uppercase;color:var(--muted);text-align:center;margin-top:10px}
.it-video{position:relative;width:100%;max-width:960px;margin:32px auto 0;aspect-ratio:16/9;background:#0F1E2D;border:1px solid var(--line);overflow:hidden}
.it-video iframe,.it-video button,.it-video img{position:absolute;inset:0;width:100%;height:100%;border:0}
.it-video button{padding:0;cursor:pointer;background:#0F1E2D}
.it-video img{object-fit:cover}
.it-video .play{position:absolute;left:50%;top:50%;width:84px;height:84px;margin:-42px 0 0 -42px;border-radius:50%;background:rgba(15,30,45,.82);border:2px solid var(--gold)}
.it-video .play::after{content:"";position:absolute;left:33px;top:24px;border-style:solid;border-width:18px 0 18px 28px;border-color:transparent transparent transparent var(--gold)}
.it-video .play-low{top:76%}
.it-video .play-side{left:37%;top:58%}
.it-soon-label{position:absolute;left:3%;top:5%;padding:8px 14px;background:rgba(15,30,45,.82);border:1px solid var(--gold);color:var(--gold-l);font-family:'Montserrat';font-weight:600;font-size:11px;letter-spacing:.3em;text-transform:uppercase}
.it-video button:hover .play,.it-video button:focus-visible .play{background:var(--gold)}
.it-video button:hover .play::after,.it-video button:focus-visible .play::after{border-left-color:#0F1E2D}
.it-watch{text-align:center;margin-top:20px}
.it-quote{font-family:'Cormorant';font-style:italic;font-size:30px;line-height:1.4;text-align:center;max-width:760px;margin:0 auto;color:var(--midnight)}
.it-quote footer{font-family:'Montserrat';font-style:normal;font-size:11px;letter-spacing:.3em;text-transform:uppercase;color:var(--muted);margin-top:16px}
.it-next{text-align:center}
@media (max-width:720px){.it-ep h3{font-size:23px}.it-quote{font-size:23px}.it-video .play{width:64px;height:64px;margin:-32px 0 0 -32px}.it-video .play::after{left:25px;top:18px;border-width:14px 0 14px 21px}.it-video .play-side{left:35%;width:50px;height:50px;margin:-25px 0 0 -25px}.it-video .play-side::after{left:19px;top:13px;border-width:12px 0 12px 17px}.it-soon-label{font-size:9px;padding:5px 9px;letter-spacing:.24em}}
</style>
<script>
document.addEventListener('click',function(e){var b=e.target.closest('.it-video button');if(!b)return;var f=document.createElement('iframe');
f.src='https://www.youtube-nocookie.com/embed/'+b.dataset.id+'?autoplay=1&rel=0';f.title=b.dataset.title;
f.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';f.referrerPolicy='strict-origin-when-cross-origin';f.allowFullscreen=true;b.replaceWith(f);f.focus();});
</script>"""
# Season 1 episodes: add one entry per release. youtube = video id or None; status shown when there is no video.
SEASON = 1
SEASON_TOTAL = 8
EPISODES = [
    dict(num=1, title='The Oracle Wasn&rsquo;t the Answer. You Were.', youtube='_fBXroaDga0', runtime='3:55', status=None,
         cover=dict(base='img/inner-thread/ep1-cover-v2', widths=(960, 1920), h=1080, alt='The Inner Thread, Episode 1: The Oracle Wasn&rsquo;t the Answer. You Were.', play='play-side')),
    dict(num=2, title='The Upanishads', youtube='j7n43mCGFv4', runtime='4:46', status=None,
         cover=dict(base='img/inner-thread/ep2-cover-v2', widths=(960, 1920), h=1080, alt='The Inner Thread, Episode 2: The Upanishads', play='play-side')),
]

def it_picture(c):
    ws = c['widths']; b = c['base']; sz = '(max-width: 1000px) 100vw, 960px'
    return (f'<picture><source type="image/webp" srcset="{", ".join(f"{b}-{w}.webp {w}w" for w in ws)}" sizes="{sz}">'
            f'<img src="{b}-{ws[0]}.jpg" srcset="{", ".join(f"{b}-{w}.jpg {w}w" for w in ws)}" sizes="{sz}" alt="{c["alt"]}" width="{ws[-1]}" height="{c["h"]}" loading="lazy"></picture>')

def it_episode(e):
    h = f'<h3 id="ep{e["num"]}-h">Episode {e["num"]} &mdash; {e["title"]}</h3>'
    if not e.get('youtube'):
        if e.get('cover'):
            return f'<article class="it-ep it-ep-soon" aria-labelledby="ep{e["num"]}-h">\n      {h}\n      <p class="it-meta">{e["status"]}</p>\n      <div class="it-video it-soon">{it_picture(e["cover"])}<span class="it-soon-label">{e["status"]}</span></div>\n    </article>'
        return f'<article class="it-ep it-ep-soon" aria-labelledby="ep{e["num"]}-h">\n      {h}\n      <p class="it-meta">{e["status"]}</p>\n    </article>'
    y = e['youtube']; t = f'The Inner Thread: Episode {e["num"]}'
    c = e.get('cover')
    if c:
        poster = it_picture(c)
        play_cls = 'play ' + c.get('play', 'play-low')
    else:
        poster = f'<img src="https://i.ytimg.com/vi/{y}/maxresdefault.jpg" alt="" width="1280" height="720" loading="lazy">'
        play_cls = 'play'
    meta = f'<p class="it-meta">Runtime {e["runtime"]}</p>' if e.get('runtime') else ''
    return f'''<article class="it-ep" aria-labelledby="ep{e["num"]}-h">
      {h}
      {meta}
      <div class="it-video">
        <button type="button" data-id="{y}" data-title="{t}" aria-label="Play {t}">{poster}<span class="{play_cls}" aria-hidden="true"></span></button>
        <noscript><iframe src="https://www.youtube-nocookie.com/embed/{y}" title="{t}" loading="lazy" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></noscript>
      </div>
      <p class="it-watch"><a class="btn btn-line" href="https://youtu.be/{y}" {EXT}>Watch on YouTube<span class="sr-only"> (opens in a new tab)</span></a></p>
    </article>'''

IT_SEASON = f'''<section class="section it-season" aria-labelledby="season-h" style="padding-top:0">
  <div class="wrap">
    <h2 id="season-h">Season {SEASON}</h2>
    <p class="it-meta">Season {SEASON}: {SEASON_TOTAL} episodes. New episodes added as they release.</p>
    ''' + '\n    '.join(it_episode(e) for e in EPISODES) + '''
  </div>
</section>'''
if True:
    pages['the-inner-thread.html'] = ('The Inner Thread | A Cinematic Documentary Series by Spigelmeyer Productions',
 'The Inner Thread is a cinematic documentary series by Spigelmeyer Productions.',
banner('Documentary Series', 'The Inner Thread', 'A cinematic documentary series by Spigelmeyer Productions.') + f'''
<section class="section" aria-label="About the series">
  <div class="wrap prose it-intro">
    <p>The Inner Thread is a cinematic documentary series exploring how people across different cultures and historical periods have investigated the nature of the self, consciousness, knowledge, reality, and the human experience.</p>
    <p>Through historical evidence, primary texts, philosophical inquiry, and contemplative traditions, the series examines ideas that have shaped humanity&rsquo;s understanding of itself. It seeks connections between traditions without erasing their differences.</p>
  </div>
</section>
{IT_SEASON}
<section class="about" aria-label="Guiding principle">
  <div class="wrap">
    <blockquote class="it-quote"><p>Its claims should be verifiable. Its conclusions should invite thought rather than demand belief.</p><footer>Guiding Principle</footer></blockquote>
  </div>
</section>''')


# ---------------- PORTFOLIO + GOVERNMENT (preview only) ----------------
# One entry per project. section: 'client' or 'studio'. images: list of (src, alt). placeholder=True renders a 'Project coming soon' tile.
PROJECTS = [
    dict(section='client', title='Guardian Angel Ride', label='Logo &amp; Brand Identity',
         desc='Logo and brand identity for a transportation business in the State College, PA area.',
         pic=dict(base='img/portfolio/guardian-angel-ride', w=4000, h=4000, bg='#ffffff', pad='6%'),
         images=[('img/portfolio/guardian-angel-ride-960.jpg', 'Guardian Angel Ride logo with the tagline Protecting What Matters, Every Mile')]),
    dict(section='client', title='Mad Max Custom Knife Handles', label='Website Design &amp; Mockup',
         desc='Website design and mockup for a York, Pennsylvania custom knife handle maker, covering the home, work, contact and mobile pages.',
         pic=dict(base='img/portfolio/mad-max-knife-handles', w=2400, h=1152, bg='#0e0e0e', pad='0'),
         images=[('img/portfolio/mad-max-knife-handles-960.jpg', 'Mad Max Custom Knife Handles website mockup showing home, work, contact and mobile pages')]),
] + [dict(section='studio', title=t, label=l, desc=d, bg=bg, gallery=g, soon=(x[0] if x else None)) for t, l, d, bg, g, *x in [
    ('[Au]thentic', 'Apparel &middot; T-Shirt Design', 'T-shirt design built around a gold &ldquo;[Au] 79&rdquo; element mark and the line &ldquo;no one can do you like you can.&rdquo;', '#eef0f2',
     [('authentic-tee-mockup', 2662, 1854, 'Navy [Au]thentic T-shirt mockup, front and back'), ('authentic-artwork', 2880, 1864, '[Au]thentic artwork in gold on navy with the line no one can do you like you can')]),
    ('Captain', 'Logo', 'Logo pairing an engraved anchor with script lettering and the line &ldquo;Smooth seas never made a good captain.&rdquo;', '#ffffff',
     [('captain-logo', 1840, 1376, 'Captain logo: an anchor with script lettering and the line Smooth seas never made a good captain')]),
    ('Whimworks &amp; The Fifth Flower', 'Game Brand Identity &amp; Marketing', 'Identity and marketing for a concept gaming company, Whimworks (&ldquo;History Replayed&rdquo;), and its concept board game reviving Patolli.', '#14110d',
     [('fifth-flower-box', 3825, 2550, 'The Fifth Flower board game box mockup in a jungle setting'), ('fifth-flower-answer-the-call', 4575, 5700, 'Whimworks poster: Answer the Call, become the Guardian of the Fifth Flower'),
      ('fifth-flower-roll-the-beans', 4575, 5700, 'Whimworks poster: Roll the Beans, The Fifth Flower board game'), ('fifth-flower-logo', 4000, 4000, 'The Fifth Flower logo: A Revival of Patolli'),
      ('whimworks-logo', 4000, 4000, 'Whimworks Gaming Company logo with the line History Replayed')]),
    ("Crackling&rsquo;s Wood Fired Smokehouse", 'Poster &amp; Marketing', 'Concept restaurant poster, &ldquo;Hear it before you taste it,&rdquo; shown flat and on a street kiosk.', '#1a1512',
     [('cracklings-kiosk', 3500, 2454, 'Crackling&rsquo;s Wood Fired Smokehouse poster on a street kiosk mockup'), ('cracklings-poster', 3290, 4602, 'Crackling&rsquo;s Wood Fired Smokehouse poster: Hear it before you taste it')]),
    ('Breezy Productions', 'Logo', 'Logo with a speaker-inspired &ldquo;B&rdquo; mark and the tagline &ldquo;Music for the Masses.&rdquo;', '#191932',
     [('breezy-logo', 2400, 1135, 'Breezy Productions logo with the tagline Music for the Masses')]),
    ('[RE]MEMBERing', 'Event Poster', 'Event poster for &ldquo;A Still Small Voice,&rdquo; an evening of sound, silence, and Return, shown on a kiosk and flat.', '#15130f',
     [('remembering-kiosk', 3500, 2454, '[RE]MEMBERing event poster on a street kiosk mockup'), ('remembering-poster', 3300, 5100, '[RE]MEMBERing poster: A Still Small Voice, an evening of sound, silence, and Return')]),
    ('Black Sea Chocolate', 'Packaging &amp; Brand Identity', 'A concept chocolate and coffee brand with packaging for a bar, pouch, tin, gift box and tote, with hand-drawn cacao details.', '#f1ece2',
     [('black-sea-group', 1920, 1280, 'Black Sea Chocolate packaging group: a gold tin, a teal box and a canvas tote, each with the red oval Black Sea Chocolate logo'),
      ('black-sea-bar', 1920, 1280, 'Black Sea Chocolate bar in red and gold packaging with a hand-drawn cacao pod, unwrapped to show dark chocolate squares'),
      ('black-sea-gift-box', 1776, 1360, 'Open teal and gold Black Sea Chocolate gift box with a tray of gold-wrapped chocolates'),
      ('black-sea-coffee-pouch', 1120, 2240, 'Teal Black Sea Salt Coffee pouch with the red oval logo and hand-drawn cacao leaves, surrounded by coffee beans and sea salt'),
      ('black-sea-tote', 1776, 1360, 'Canvas Black Sea Chocolate tote bag with the red oval logo and a blue patterned border')], 'Coming soon!'),
]]
PF_SECTIONS = [('client', 'Client Work', None), ('studio', 'SP Studio &amp; Concept Work', 'Concept brands, posters and mockups designed in-house by Timothy Lee Spigelmeyer Jr. Not client work.')]
PF_STYLE = """<style>
.pf-sec{margin-top:8px}
.pf-sec h2{text-align:center}
.pf-note{font-family:'Montserrat';font-size:12px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);text-align:center;margin-top:10px}
.pf-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:28px;margin-top:36px}
.pf-card{border:1px solid var(--line);background:#fff}
.pf-card img{display:block;width:100%;aspect-ratio:4/3;object-fit:cover}
.pf-media{aspect-ratio:4/3;display:flex;align-items:center;justify-content:center;border-bottom:1px solid var(--line);box-sizing:border-box}
.pf-media picture{display:contents}
.pf-card .pf-media img{width:100%;height:100%;aspect-ratio:auto;object-fit:contain}
.pf-card .pf-body{padding:18px 20px 22px}
.pf-card h3{font-family:'Cinzel';font-weight:400;font-size:21px;color:var(--midnight)}
.pf-card .pf-label{font-family:'Montserrat';font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--steward);margin-top:6px}
.pf-card p{font-size:18px;line-height:1.45;margin-top:8px}
.pf-ph{aspect-ratio:4/3;display:flex;align-items:center;justify-content:center;background:var(--steward);color:var(--gold-l);font-family:'Montserrat';font-weight:600;font-size:12px;letter-spacing:.3em;text-transform:uppercase;border:1px solid var(--line);text-align:center;padding:20px}
#pf-client .pf-grid{grid-template-columns:repeat(2,minmax(0,380px));justify-content:center}
.pf-open{all:unset;box-sizing:border-box;display:block;width:100%;cursor:zoom-in;text-align:left;font:inherit}
.pf-open:focus-visible{outline:3px solid var(--gold);outline-offset:3px}
.pf-open:hover .pf-media img{transform:scale(1.02)}
.pf-media img{transition:transform .3s}
.pf-soon{display:inline-block;font-family:'Montserrat';font-weight:600;font-size:10.5px;letter-spacing:.2em;text-transform:uppercase;background:var(--midnight);color:var(--ivory);border-left:3px solid var(--gold);padding:5px 10px;margin-bottom:10px}
.pf-count{font-family:'Montserrat';font-size:10.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--muted);margin-top:10px}
.lb{position:fixed;inset:0;z-index:1000;background:rgba(8,10,16,.95);display:none;flex-direction:column;color:#fff}
.lb[open],.lb.on{display:flex}
.lb-top{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:12px 16px;font-family:'Montserrat';font-size:12px;letter-spacing:.12em;text-transform:uppercase}
.lb-stage{flex:1;min-height:0;display:flex;align-items:center;justify-content:center;padding:0 64px;touch-action:pan-y}
.lb-stage picture{display:contents}
.lb-stage img{max-width:100%;max-height:100%;width:auto;height:auto;object-fit:contain}
.lb-cap{padding:10px 16px 16px;text-align:center;font-size:16px;min-height:2.6em;color:#ddd}
.lb button{background:rgba(255,255,255,.1);color:#fff;border:1px solid rgba(255,255,255,.3);border-radius:50%;width:46px;height:46px;font-size:24px;line-height:1;cursor:pointer;display:flex;align-items:center;justify-content:center}
.lb button:focus-visible{outline:3px solid var(--gold);outline-offset:2px}
.lb-nav{position:absolute;top:50%;transform:translateY(-50%)}
.lb-prev{left:10px}.lb-next{right:10px}
.lb.single .lb-nav{display:none}
@media (max-width:900px){.pf-grid{grid-template-columns:repeat(2,1fr)}}
@media (max-width:560px){.pf-grid,#pf-client .pf-grid{grid-template-columns:1fr;gap:20px}.lb-stage{padding:0 8px}.lb-nav{top:auto;bottom:58px;transform:none}}
</style>"""
def pf_card(pj):
    if pj.get('placeholder'):
        return '<div class="pf-ph" role="img" aria-label="Project coming soon">Project coming soon</div>'
    img = ''.join(f'<img src="{a}" alt="{b}" loading="lazy">' for a, b in pj.get('images', [])[:1])
    pc = pj.get('pic')
    if pc:
        a, b = pj['images'][0]
        ss = lambda ext: ', '.join(f"{pc['base']}-{w}.{ext} {w}w" for w in (960, 1920))
        sz = '(max-width:560px) 92vw, (max-width:900px) 46vw, 380px'
        img = (f'<div class="pf-media" style="background:{pc["bg"]};padding:{pc["pad"]}"><picture>'
               f'<source type="image/webp" srcset="{ss("webp")}" sizes="{sz}">'
               f'<img src="{a}" srcset="{ss("jpg")}" sizes="{sz}" width="{pc["w"]}" height="{pc["h"]}" alt="{b}" loading="lazy" decoding="async">'
               f'</picture></div>')
    lab = f'<div class="pf-label">{pj["label"]}</div>' if pj.get('label') else ''
    g = pj.get('gallery')
    if g:
        import json, html as H
        sz = '(max-width:560px) 92vw, (max-width:900px) 46vw, 380px'
        src = lambda n, w, ext: f'img/portfolio/{n}-{min(w, 960) if False else 960}.{ext}'
        def ss(n, w, ext): return f'img/portfolio/{n}-960.{ext} 960w, img/portfolio/{n}-1920.{ext} {min(w,1920)}w'
        n, w, h, alt = g[0]
        data = H.escape(json.dumps([dict(w=f'img/portfolio/{a}-1920.webp', j=f'img/portfolio/{a}-1920.jpg', s=f'img/portfolio/{a}-960.webp', W=min(b,1920), H=round(c*min(b,1920)/b), a=H.unescape(d)) for a, b, c, d in g]))
        soon = f'<div class="pf-soon">{pj["soon"]}</div>' if pj.get('soon') else ''
        cnt = f'<div class="pf-count">{len(g)} image{"s" if len(g)>1 else ""} &middot; view gallery</div>'
        return (f'<article class="pf-card"><button type="button" class="pf-open" data-title="{H.escape(H.unescape(pj["title"]))}" data-g="{data}" aria-haspopup="dialog">'
                f'<div class="pf-media" style="background:{pj["bg"]};padding:4%"><picture><source type="image/webp" srcset="{ss(n,w,"webp")}" sizes="{sz}">'
                f'<img src="img/portfolio/{n}-960.jpg" srcset="{ss(n,w,"jpg")}" sizes="{sz}" width="{w}" height="{h}" alt="{alt}" loading="lazy" decoding="async"></picture></div>'
                f'<div class="pf-body">{soon}<h3>{pj["title"]}</h3>{lab}<p>{pj["desc"]}</p>{cnt}</div></button></article>')
    return f'<article class="pf-card">{img}<div class="pf-body"><h3>{pj["title"]}</h3>{lab}<p>{pj.get("desc","")}</p></div></article>'
def pf_section(key, name, note):
    cards = '\n      '.join(pf_card(p) for p in PROJECTS if p['section'] == key)
    nt = f'<p class="pf-note">{note}</p>' if note else ''
    return f"""<section class="section pf-sec" id="pf-{key}" aria-labelledby="pf-{key}-h">
  <div class="wrap">
    <h2 id="pf-{key}-h">{name}</h2>
    {nt}
    <div class="pf-grid">
      {cards}
    </div>
  </div>
</section>"""
PF_LIGHTBOX = """
<div class="lb" id="pf-lb" role="dialog" aria-modal="true" aria-labelledby="lb-title" hidden>
  <div class="lb-top"><span><span id="lb-title"></span> &middot; <span id="lb-pos" aria-live="polite"></span></span><button type="button" class="lb-close" aria-label="Close gallery">&times;</button></div>
  <div class="lb-stage"><picture><source id="lb-src" type="image/webp"><img id="lb-img" alt=""></picture></div>
  <button type="button" class="lb-nav lb-prev" aria-label="Previous image">&#8249;</button>
  <button type="button" class="lb-nav lb-next" aria-label="Next image">&#8250;</button>
  <p class="lb-cap" id="lb-cap"></p>
</div>
<script>
(function(){var lb=document.getElementById('pf-lb'),img=document.getElementById('lb-img'),src=document.getElementById('lb-src'),cap=document.getElementById('lb-cap'),pos=document.getElementById('lb-pos'),ttl=document.getElementById('lb-title'),G=[],i=0,opener=null;
function show(){var g=G[i];src.srcset=g.s+' 960w, '+g.w+' '+g.W+'w';src.sizes='100vw';img.src=g.j;img.width=g.W;img.height=g.H;img.alt=g.a;cap.textContent=g.a;pos.textContent=(i+1)+' of '+G.length;}
function open(b){G=JSON.parse(b.dataset.g);i=0;opener=b;ttl.textContent=b.dataset.title;lb.classList.toggle('single',G.length<2);show();lb.hidden=false;lb.classList.add('on');document.body.style.overflow='hidden';lb.querySelector('.lb-close').focus();}
function close(){lb.classList.remove('on');lb.hidden=true;document.body.style.overflow='';if(opener)opener.focus();}
function go(d){if(G.length<2)return;i=(i+d+G.length)%G.length;show();}
document.querySelectorAll('.pf-open').forEach(function(b){b.addEventListener('click',function(){open(b)})});
lb.querySelector('.lb-close').onclick=close;lb.querySelector('.lb-prev').onclick=function(){go(-1)};lb.querySelector('.lb-next').onclick=function(){go(1)};
lb.addEventListener('click',function(e){if(e.target===lb||e.target.classList.contains('lb-stage'))close();});
document.addEventListener('keydown',function(e){if(lb.hidden)return;if(e.key==='Escape')close();else if(e.key==='ArrowRight')go(1);else if(e.key==='ArrowLeft')go(-1);else if(e.key==='Tab'){var f=[].slice.call(lb.querySelectorAll('button')).filter(function(x){return x.offsetParent});var a=f.indexOf(document.activeElement);if(e.shiftKey&&a<=0){e.preventDefault();f[f.length-1].focus();}else if(!e.shiftKey&&a===f.length-1){e.preventDefault();f[0].focus();}}});
var x0=null,y0=null;lb.addEventListener('touchstart',function(e){x0=e.touches[0].clientX;y0=e.touches[0].clientY},{passive:true});
lb.addEventListener('touchend',function(e){if(x0===null)return;var dx=e.changedTouches[0].clientX-x0,dy=e.changedTouches[0].clientY-y0;if(Math.abs(dx)>40&&Math.abs(dx)>Math.abs(dy))go(dx<0?1:-1);x0=null;},{passive:true});})();
</script>"""
GOV_STYLE = """<style>
.gov-grid{display:grid;grid-template-columns:1.3fr 1fr;gap:56px;align-items:start}
.gov-list{list-style:none;margin-top:18px}
.gov-list li{font-size:21px;padding:12px 0;border-bottom:1px solid var(--line)}
.gov-list li::before{content:"\\2726";color:var(--gold);margin-right:12px}
.gov-data{border:1px solid var(--gold);padding:28px 30px;background:#fff;position:relative}
.gov-data h2{font-size:24px}
.gov-draft{position:absolute;top:-12px;right:20px;background:var(--gold);color:var(--midnight);font-family:'Montserrat';font-weight:700;font-size:10.5px;letter-spacing:.3em;padding:4px 10px}
.gov-data dl{margin-top:14px}
.gov-data dt{font-family:'Montserrat';font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--muted);margin-top:14px}
.gov-data dd{font-size:20px;color:var(--midnight);font-weight:600;margin:4px 0 0}
.gov-data dd a{color:var(--steward);text-decoration:underline;text-underline-offset:3px}
.gov-cta{margin-top:28px;display:flex;gap:14px;flex-wrap:wrap}
@media (max-width:900px){.gov-grid{grid-template-columns:1fr;gap:40px}}
</style>"""
pages['portfolio.html'] = ('Portfolio | Spigelmeyer Productions',
 'Selected brand identity and design work by Spigelmeyer Productions.',
banner('Design Work', 'Portfolio', 'Selected brand identity and design work by Spigelmeyer Productions.') + '\n'.join(pf_section(*x) for x in PF_SECTIONS) + PF_LIGHTBOX)
if True:   # Government page live 2026-10-30
    pages['government.html'] = ('Government &amp; Military | Spigelmeyer Productions',
 'Spigelmeyer Productions is a veteran-owned creative company founded by Timothy Lee Spigelmeyer Jr, a veteran of the U.S. Navy and Pennsylvania Army National Guard.',
banner('Federal Work', 'Government &amp; Military', 'Spigelmeyer Productions is a veteran-owned creative company founded by Timothy Lee Spigelmeyer Jr, a veteran of the U.S. Navy and Pennsylvania Army National Guard.') + f"""
<section class="section" aria-labelledby="gov-svc-h">
  <div class="wrap gov-grid">
    <div class="prose">
      <div class="kicker">Services</div>
      <h2 id="gov-svc-h">What We Provide</h2>
      <ul class="gov-list">
        <li>Brand identity and design</li>
        <li>Publishing (iPennedIt Publishing)</li>
        <li>Documentary and video production</li>
      </ul>
      <div class="gov-cta">
        <a class="btn btn-navy" href="downloads/SP-Capability-Statement.pdf" download>Download Capability Statement (PDF)</a>
        <a class="btn btn-line" href="mailto:{EMAIL}">{EMAIL}</a>
      </div>
    </div>
    <aside class="gov-data" aria-labelledby="gov-data-h">
      <h2 id="gov-data-h">Company Data</h2>
      <dl>
        <dt>Entity</dt><dd>Spigelmeyer Productions, LLC</dd>
        <dt>UEI</dt><dd>G8KWZL6GBLK8</dd>
        <dt>CAGE Code</dt><dd>10JQ3</dd>
        <dt>SAM.gov Status</dt><dd>Active</dd>
        <dt>Ownership</dt><dd>Veteran-owned (U.S. Navy veteran)</dd>
        <dt>Certifications</dt><dd>VOSB certification in progress (SBA)</dd>
        <dt>NAICS Codes</dt><dd>541430 (primary)<br>323111<br>513130<br>541921<br>711510</dd>
        <dt>Location</dt><dd>Erie, PA</dd>
        <dt>Contact</dt><dd><a href="tel:{TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></dd>
      </dl>
    </aside>
  </div>
</section>""")

for f, (title, desc, body) in pages.items():
    hdr_file = f if f != '404.html' else ''
    html = head(f, title, desc) + header(hdr_file) + body + '\n' + footer()
    if f == '404.html' and not PREVIEW:
        html = html.replace('<meta name="description"', '<meta name="robots" content="noindex">\n<meta name="description"')
    if f == 'portfolio.html':
        html = html.replace('<link rel="stylesheet" href="css/site.css">', '<link rel="stylesheet" href="css/site.css">\n' + PF_STYLE)
    if f == 'government.html':
        html = html.replace('<link rel="stylesheet" href="css/site.css">', '<link rel="stylesheet" href="css/site.css">\n' + GOV_STYLE)
    if f == 'the-inner-thread.html':
        html = html.replace('<link rel="stylesheet" href="css/site.css">', '<link rel="stylesheet" href="css/site.css">\n' + IT_STYLE)
    (OUT / f).write_text(html)
    print('wrote', f)

(OUT / 'field-notes').mkdir(exist_ok=True)
# Portfolio images live in pages-src/img/portfolio and are copied into both outputs.
import shutil
shutil.copytree(Path(__file__).resolve().parent / 'img' / 'portfolio', OUT / 'img' / 'portfolio', dirs_exist_ok=True)
# Grouped nav assets (sitewide)
SRC = Path(__file__).resolve().parent
(OUT / 'css').mkdir(exist_ok=True); (OUT / 'js').mkdir(exist_ok=True)
shutil.copy2(SRC / 'nav' / 'nav.css', OUT / 'css' / 'nav.css')
shutil.copy2(SRC / 'nav' / 'nav.js', OUT / 'js' / 'nav.js')
# Capability statement PDF (ships with both builds)
if True:
    (OUT / 'downloads').mkdir(exist_ok=True)
    shutil.copy2(Path(__file__).resolve().parent / 'assets' / 'SP-Capability-Statement.pdf', OUT / 'downloads' / 'SP-Capability-Statement.pdf')
for slug, P in POSTS.items():
    pf, phtml = post_page(slug, P)
    (OUT / pf).write_text(phtml)
    print('wrote', pf)

urls = ''.join(f'  <url><loc>{BASE}{"/" if h=="index.html" else "/"+h[:-5]}</loc></url>\n' for h, _ in NAV + FOOTER_EXTRA)
urls += ''.join(f'  <url><loc>{BASE}/field-notes/{slug}</loc></url>\n' for slug in POSTS)
(OUT / 'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
(OUT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n')
(OUT / '_headers').write_text('''/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: SAMEORIGIN

/fonts/*
  Cache-Control: public, max-age=31536000, immutable

/img/*
  Cache-Control: public, max-age=604800
''')
