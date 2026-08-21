#!/usr/bin/env python3
"""Faragalla Law PPC landing page hub — static site generator.

Zero dependencies (Python 3.8+ stdlib). Reads content/site.json and
content/pages/*.json, writes deploy-ready HTML into public/.

    python3 build.py
"""
import html
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
CONTENT = ROOT / "content"
PUBLIC = ROOT / "public"


def e(text):
    """Escape text for HTML body/attribute contexts."""
    return html.escape(str(text), quote=True)


def load():
    site = json.loads((CONTENT / "site.json").read_text(encoding="utf-8"))
    pages = []
    for f in sorted((CONTENT / "pages").glob("*.json")):
        pages.append(json.loads(f.read_text(encoding="utf-8")))
    pages.sort(key=lambda p: p.get("priority", 99))
    return site, pages


# ---------------------------------------------------------------- SVG icons

ICON_PHONE = (
    '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
    '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6'
    ' 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81'
    'a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7'
    'A2 2 0 0 1 22 16.92Z" fill="currentColor"/></svg>'
)

ICON_CHECK = (
    '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
    '<circle cx="12" cy="12" r="11" fill="#00bfff"/>'
    '<path d="M7 12.5 10.5 16 17 8.5" stroke="#071d33" stroke-width="2.5" '
    'stroke-linecap="round" stroke-linejoin="round"/></svg>'
)

ICON_CHECK_GREEN = ICON_CHECK.replace("#00bfff", "#d3f2e0").replace("#071d33", "#1e7d43")

ICON_X = (
    '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
    '<circle cx="12" cy="12" r="11" fill="#e8edf2"/>'
    '<path d="M8.5 8.5l7 7M15.5 8.5l-7 7" stroke="#51606f" stroke-width="2.2" '
    'stroke-linecap="round"/></svg>'
)

HIDDEN_TRACKING_FIELDS = [
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "gclid", "gbraid", "wbraid", "msclkid", "fbclid",
    "landing_page", "page_url", "first_touch", "referrer", "device",
]


# ---------------------------------------------------------------- components

def render_form(site, page, location):
    """One consistent form used in the hero and the final section (review fix #16)."""
    slug = page["slug"]
    endpoint = site["form"].get("endpoint", "")
    netlify_attrs = ' data-netlify="true" netlify-honeypot="company_website"' if site["form"].get("netlify") else ""

    hidden = "\n      ".join(
        f'<input type="hidden" name="{name}" value="">' for name in HIDDEN_TRACKING_FIELDS
    )

    qualifiers = ""
    for q in page.get("qualifiers", []):
        opts = "".join(f"<option>{e(o)}</option>" for o in q["options"])
        qualifiers += f"""
      <div>
        <label for="{location}-{q['name']}">{e(q['label'])}</label>
        <select id="{location}-{q['name']}" name="{q['name']}" required>
          <option value="" selected disabled>Select one…</option>{opts}
        </select>
      </div>"""

    return f"""<form class="lp-form" method="POST" action="/thank-you.html" name="lead-{slug}"
      data-form-location="{location}" data-endpoint="{e(endpoint)}"{netlify_attrs}>
      <input type="hidden" name="form-name" value="lead-{slug}">
      <input type="hidden" name="campaign_page" value="{slug}">
      {hidden}
      <p class="hp-field" aria-hidden="true"><label>Leave this field empty <input type="text" name="company_website" tabindex="-1" autocomplete="off"></label></p>
      <div>
        <label for="{location}-name">Full name</label>
        <input id="{location}-name" type="text" name="name" autocomplete="name" required>
      </div>
      <div>
        <label for="{location}-email">Email</label>
        <input id="{location}-email" type="email" name="email" autocomplete="email" inputmode="email" required>
      </div>
      <div>
        <label for="{location}-phone">Phone</label>
        <input id="{location}-phone" type="tel" name="phone" autocomplete="tel" inputmode="tel" required>
        <div class="field-hint">Used only to follow up about your inquiry — no marketing calls.</div>
      </div>{qualifiers}
      <div class="lp-form__status" role="status" aria-live="polite"></div>
      <button class="btn btn--primary btn--block" type="submit">{e(page['cta_label'])}</button>
      <p class="lp-form__microcopy">{e(site['response_promise'])}. {e(site['consultation']['line'])}
      {e(site['form_microcopy_privacy'])} See our <a href="{e(site['privacy_url'])}" target="_blank" rel="noopener">Privacy&nbsp;Policy</a>.</p>
    </form>"""


def render_header(site, page):
    return f"""<header class="lp-header">
    <div class="container lp-header__inner">
      <a class="lp-header__brand" href="#top" aria-label="{e(site['firm_name'])} — back to top">
        <span class="lp-header__name">{e(site['firm_name'])}</span>
        <span class="lp-header__tag">{e(site['firm_tagline'])}</span>
      </a>
      <div class="lp-header__actions">
        <a class="lp-header__phone" href="tel:{e(site['phone_tel'])}" data-call-location="header">
          {ICON_PHONE}<span class="lp-header__phone-num">{e(site['phone_display'])}</span>
          <span class="visually-hidden">Call {e(site['firm_name'])}</span>
        </a>
        <a class="btn btn--primary btn--sm lp-header__cta" href="#lead-form" data-jump-form>{e(page['cta_short'])}</a>
      </div>
    </div>
  </header>"""


def render_hero(site, page):
    bullets = "\n          ".join(
        f"<li>{ICON_CHECK}<span>{e(b)}</span></li>" for b in page["bullets"]
    )
    stats = site["stats"]
    return f"""<section class="hero" id="top">
    <div class="container hero__grid">
      <div>
        <p class="hero__eyebrow">{e(page['eyebrow'])}</p>
        <h1>{e(page['h1'])}</h1>
        <p class="hero__sub">{e(page['hero_sub'])}</p>
        <ul class="hero__bullets">
          {bullets}
        </ul>
        <div class="hero__cta-wrap">
          <a class="btn btn--primary" href="#lead-form" data-jump-form>{e(page['cta_label'])}</a>
          <p class="hero__call">or call <a href="tel:{e(site['phone_tel'])}" data-call-location="hero">{e(site['phone_display'])}</a></p>
        </div>
        <div class="hero__trust">
          <span><strong>{e(stats[0]['value'])}</strong> {e(stats[0]['label'].lower())}</span>
          <span><strong>{e(stats[1]['value'])}</strong> {e(stats[1]['label'].lower())}</span>
          <span><span class="stars" aria-hidden="true">★★★★★</span>
            <a href="{e(site['google_reviews_url'])}" target="_blank" rel="noopener"><strong>{e(stats[2]['value'].replace('★',''))}</strong> average rating on Google</a></span>
        </div>
      </div>
      <div class="form-card" id="lead-form">
        <h2>{e(page['form_title'])}</h2>
        <p class="form-card__sub">{e(page['form_sub'])}</p>
        {render_form(site, page, 'hero')}
      </div>
    </div>
  </section>"""


def render_problem(page):
    cards = "\n        ".join(
        f'<div class="card"><h3>{e(c["title"])}</h3><p>{e(c["body"])}</p></div>'
        for c in page["problem_cards"]
    )
    return f"""<section class="section">
    <div class="container">
      <p class="section__kicker">What decides these cases</p>
      <h2>{e(page['problem_heading'])}</h2>
      <div class="cards">
        {cards}
      </div>
    </div>
  </section>"""


def render_fit(site, page):
    fors = "\n            ".join(
        f"<li>{ICON_CHECK_GREEN}<span>{e(x)}</span></li>" for x in page["who_for"]
    )
    nots = "\n            ".join(
        f"<li>{ICON_X}<span>{e(x)}</span></li>" for x in page["who_not"]
    )
    return f"""<section class="section section--alt">
    <div class="container">
      <p class="section__kicker">Qualify yourself in 30 seconds</p>
      <h2>{e(page['who_heading'])}</h2>
      <div class="fit">
        <div class="fit__col">
          <h3>This service is likely a fit if…</h3>
          <ul>
            {fors}
          </ul>
        </div>
        <div class="fit__col fit__col--no">
          <h3>It's probably not the right fit if…</h3>
          <ul>
            {nots}
          </ul>
        </div>
      </div>
    </div>
  </section>"""


def render_why(site, page):
    cards = "\n        ".join(
        f'<div class="card"><h3>{e(c["title"])}</h3><p>{e(c["body"])}</p></div>'
        for c in page["why_points"]
    )
    stats = "\n        ".join(
        f'<div><div class="stats__value">{e(s["value"])}</div><div class="stats__label">{e(s["label"])}</div></div>'
        for s in site["stats"]
    )
    return f"""<section class="section section--navy">
    <div class="container">
      <p class="section__kicker">Why {e(site['firm_name'])}</p>
      <h2>Counsel that pressure-tests your case before the government does</h2>
      <div class="cards cards--4">
        {cards}
      </div>
    </div>
  </section>
  <section aria-label="Firm statistics">
    <div class="container">
      <div class="stats">
        {stats}
      </div>
    </div>
  </section>"""


def render_process(site, page):
    steps = "\n        ".join(
        f'<div class="step"><h3>{e(s["title"])}</h3><p>{e(s["body"])}</p></div>'
        for s in page["process"]
    )
    return f"""<section class="section section--alt">
    <div class="container">
      <p class="section__kicker">How it works</p>
      <h2>A defined process — you always know the next step</h2>
      <div class="steps">
        {steps}
      </div>
    </div>
  </section>"""


def render_fees(page):
    return f"""<section class="section">
    <div class="container">
      <p class="section__kicker">Costs, addressed head-on</p>
      <h2>{e(page['fees_heading'])}</h2>
      <p class="section__lead" style="margin-bottom:0">{e(page['fees_body'])}</p>
    </div>
  </section>"""


def render_testimonials(site, page):
    quotes = "\n        ".join(
        f"""<figure class="quote">
          <div class="stars" aria-hidden="true">★★★★★</div>
          <blockquote>{e(line)}</blockquote>
          <figcaption>Google review — {e(page['testimonial_hint'])}</figcaption>
        </figure>"""
        for line in site["testimonial_placeholder_lines"]
    )
    return f"""<section class="section section--alt">
    <div class="container">
      <p class="section__kicker">Client reviews</p>
      <h2>What clients say</h2>
      <div class="quotes">
        {quotes}
      </div>
      <p class="quotes__source">Reviews shown are from the firm's public
        <a href="{e(site['google_reviews_url'])}" target="_blank" rel="noopener">Google Business Profile</a>,
        reproduced verbatim with permission. Individual results vary; prior results do not guarantee a similar outcome.</p>
    </div>
  </section>"""


def render_attorney(site):
    a = site["attorney"]
    return f"""<section class="section">
    <div class="container attorney">
      <div class="attorney__photo">
        <span>Attorney headshot goes here<br>(assets/img/sam-faragalla.jpg — see README launch checklist; use a real photograph)</span>
      </div>
      <div>
        <p class="section__kicker">Your attorney</p>
        <h3>{e(a['name'])}</h3>
        <p class="attorney__role">{e(a['title'])}</p>
        <p>{e(a['bio_short'])}</p>
        <p class="attorney__license">{e(a['license_line'])}</p>
      </div>
    </div>
  </section>"""


def render_faq(page):
    items = "\n        ".join(
        f"""<details>
          <summary>{e(f['q'])}</summary>
          <div><p>{e(f['a'])}</p></div>
        </details>"""
        for f in page["faq"]
    )
    return f"""<section class="section section--alt">
    <div class="container">
      <p class="section__kicker">Common questions</p>
      <h2>Questions we answer every week</h2>
      <div class="faq">
        {items}
      </div>
    </div>
  </section>"""


def render_final(site, page):
    return f"""<section class="section section--navy final">
    <div class="container">
      <p class="section__kicker">Ready when you are</p>
      <h2>{e(page['final_heading'])}</h2>
      <p class="section__lead">{e(page['final_sub'])}</p>
      <div class="form-card" id="lead-form-bottom">
        <h3>{e(page['form_title'])}</h3>
        <p class="form-card__sub">{e(page['form_sub'])}</p>
        {render_form(site, page, 'bottom')}
      </div>
      <p class="final__call">Prefer to talk? Call
        <a href="tel:{e(site['phone_tel'])}" data-call-location="final">{e(site['phone_display'])}</a>
        — tell us you're calling about the {e(page['campaign'])} page.</p>
    </div>
  </section>"""


def render_footer(site):
    return f"""<footer class="lp-footer">
    <div class="container">
      <div class="lp-footer__firm">{e(site['firm_name'])} — {e(site['firm_tagline'])}</div>
      <div>{e(site['offices_line'])}</div>
      <div class="lp-footer__row">
        <a href="tel:{e(site['phone_tel'])}" data-call-location="footer">{e(site['phone_display'])}</a>
        &nbsp;·&nbsp; <a href="{e(site['privacy_url'])}" target="_blank" rel="noopener">Privacy Policy</a>
        &nbsp;·&nbsp; <a href="{e(site['main_site_url'])}" target="_blank" rel="noopener">Main website</a>
      </div>
      <p class="lp-footer__disclaimer">{e(site['disclaimer_footer'])}</p>
    </div>
  </footer>"""


def render_stickybar(site, page):
    return f"""<div class="stickybar" role="navigation" aria-label="Quick actions">
    <a class="btn btn--call" href="tel:{e(site['phone_tel'])}" data-call-location="stickybar">{ICON_PHONE} Call Now</a>
    <a class="btn btn--primary" href="#lead-form" data-jump-form>{e(page['cta_short'])}</a>
  </div>"""


def render_jsonld(site, page, canonical):
    service = {
        "@context": "https://schema.org",
        "@type": "LegalService",
        "name": site["firm_name"],
        "url": canonical,
        "telephone": site["phone_tel"],
        "description": page["meta_description"],
        "areaServed": ["US", "CA"],
        "serviceType": page["service_name"],
        "founder": {
            "@type": "Person",
            "name": site["attorney"]["name"],
            "jobTitle": site["attorney"]["title"],
        },
        "parentOrganization": {
            "@type": "Organization",
            "name": site["firm_name"],
            "url": site["main_site_url"],
        },
    }
    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f["q"],
                "acceptedAnswer": {"@type": "Answer", "text": f["a"]},
            }
            for f in page["faq"]
        ],
    }
    return (
        f'<script type="application/ld+json">{json.dumps(service, ensure_ascii=False)}</script>\n'
        f'  <script type="application/ld+json">{json.dumps(faq, ensure_ascii=False)}</script>'
    )


def render_head(site, title, description, canonical, jsonld=""):
    gtm = ""
    if site.get("gtm_id"):
        gtm = f"""<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','{site["gtm_id"]}');</script>"""
    return f"""<meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(description)}">
  <meta name="robots" content="noindex, nofollow">
  <link rel="canonical" href="{e(canonical)}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(description)}">
  <meta property="og:url" content="{e(canonical)}">
  <meta name="theme-color" content="#0b2a4a">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='18' fill='%230b2a4a'/><text x='50' y='68' font-size='52' font-weight='800' font-family='Arial' fill='%2300bfff' text-anchor='middle'>F</text></svg>">
  <link rel="stylesheet" href="/assets/css/lp.css">
  <script>window.dataLayer = window.dataLayer || [];</script>
  {gtm}
  {jsonld}
  <script src="/assets/js/lp.js" defer></script>"""


def render_page(site, page):
    canonical = f"{site['base_url'].rstrip('/')}/{page['slug']}/"
    jsonld = render_jsonld(site, page, canonical)
    head = render_head(site, page["meta_title"], page["meta_description"], canonical, jsonld)
    return f"""<!doctype html>
<html lang="en">
<head>
  {head}
</head>
<body>
  {render_header(site, page)}
  <main>
  {render_hero(site, page)}
  {render_problem(page)}
  {render_fit(site, page)}
  {render_why(site, page)}
  {render_process(site, page)}
  {render_fees(page)}
  {render_testimonials(site, page)}
  {render_attorney(site)}
  {render_faq(page)}
  {render_final(site, page)}
  </main>
  {render_footer(site)}
  {render_stickybar(site, page)}
</body>
</html>
"""


def render_thank_you(site):
    head = render_head(
        site,
        f"Request Received | {site['firm_name']}",
        "Your request was received. Here's what happens next.",
        f"{site['base_url'].rstrip('/')}/thank-you.html",
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  {head}
  <script>
    window.dataLayer.push({{
      event: 'generate_lead',
      page_path: '/thank-you.html',
      from_page: new URLSearchParams(location.search).get('from') || 'direct'
    }});
  </script>
</head>
<body>
  <header class="lp-header">
    <div class="container lp-header__inner">
      <span class="lp-header__brand">
        <span class="lp-header__name">{e(site['firm_name'])}</span>
        <span class="lp-header__tag">{e(site['firm_tagline'])}</span>
      </span>
      <div class="lp-header__actions">
        <a class="lp-header__phone" href="tel:{e(site['phone_tel'])}" data-call-location="header">
          {ICON_PHONE}<span class="lp-header__phone-num">{e(site['phone_display'])}</span>
        </a>
      </div>
    </div>
  </header>
  <main class="ty-wrap">
    <div class="ty-check" aria-hidden="true">
      <svg width="32" height="32" viewBox="0 0 24 24" fill="none"><path d="M4 12.5 9.5 18 20 6.5" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>
    </div>
    <h1>Your request was received.</h1>
    <p class="ty-lead">{e(site['response_promise'])} — usually sooner. Here's exactly what happens next.</p>
    <div class="ty-steps">
      <div class="card"><h3><span>1.</span> We review your submission</h3><p>An attorney-supervised team member reads your answers and matches your case to the right review track.</p></div>
      <div class="card"><h3><span>2.</span> You get a reply within one business day</h3><p>We email you consultation options, the consultation details, and anything we need from you — check your spam folder just in case.</p></div>
      <div class="card"><h3><span>3.</span> Worth gathering meanwhile</h3><p>Your passport, any prior U.S. visa or immigration paperwork, and — for business cases — basic numbers on your investment or company. Don't worry if something is missing; we'll tell you exactly what matters for your case.</p></div>
    </div>
    <div class="ty-callout">
      <strong>Need to talk sooner?</strong> Call
      <a href="tel:{e(site['phone_tel'])}" data-call-location="thankyou">{e(site['phone_display'])}</a>
      and mention that you've already submitted the form.
    </div>
    <p class="lp-form__microcopy">{e(site['form_microcopy_privacy'])}</p>
  </main>
  {render_footer(site)}
</body>
</html>
"""


def render_index(site, pages):
    head = render_head(
        site,
        f"PPC Landing Page Hub | {site['firm_name']}",
        "Internal directory of campaign landing pages.",
        f"{site['base_url'].rstrip('/')}/",
    )
    cards = "\n      ".join(
        f"""<a class="hub-card" href="/{p['slug']}/">
        <span class="hub-card__slug">/{p['slug']}/</span>
        <h3>{e(p['campaign'])}</h3>
        <p>{e(p['h1'])}</p>
      </a>"""
        for p in pages
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  {head}
</head>
<body>
  <header class="lp-header">
    <div class="container lp-header__inner">
      <span class="lp-header__brand">
        <span class="lp-header__name">{e(site['firm_name'])}</span>
        <span class="lp-header__tag">PPC Landing Page Hub</span>
      </span>
    </div>
  </header>
  <main class="section">
    <div class="container">
      <p class="section__kicker">Internal directory — not an ad destination</p>
      <h2>Campaign landing pages</h2>
      <p class="section__lead">Each page below is a self-contained ad destination for one campaign.
      Point ads at the page URLs directly — never at this index. All pages are noindexed.</p>
      <div class="hub-list">
      {cards}
      </div>
      <p class="section__lead" style="font-size:14px">Conversion page: <a href="/thank-you.html">/thank-you.html</a> · Strategy &amp; launch checklist: see README.md and STRATEGY.md in the repository.</p>
    </div>
  </main>
  {render_footer(site)}
</body>
</html>
"""


def main():
    site, pages = load()

    if PUBLIC.exists():
        shutil.rmtree(PUBLIC)
    PUBLIC.mkdir(parents=True)

    # assets
    shutil.copytree(ROOT / "assets", PUBLIC / "assets")

    # campaign pages
    for page in pages:
        out = PUBLIC / page["slug"]
        out.mkdir(parents=True)
        (out / "index.html").write_text(render_page(site, page), encoding="utf-8")
        print(f"  built /{page['slug']}/")

    (PUBLIC / "thank-you.html").write_text(render_thank_you(site), encoding="utf-8")
    print("  built /thank-you.html")

    (PUBLIC / "index.html").write_text(render_index(site, pages), encoding="utf-8")
    print("  built /index.html (hub directory)")

    # robots: allow crawling (AdsBot must reach pages for Quality Score);
    # organic exclusion is handled by the per-page meta noindex.
    (PUBLIC / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")
    print("  built /robots.txt")

    print(f"\nDone — {len(pages)} campaign pages + thank-you + index in public/")


if __name__ == "__main__":
    main()
