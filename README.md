# Faragalla Law — PPC Landing Page Hub

A self-contained hub of 22 campaign landing pages for faragallalaw.com paid
traffic (the `results.goldbergloren.com` pattern: one focused, noindexed page
per campaign, no site navigation, one offer per page) — 15 English pages plus
a 7-page Spanish set (national anchor, arreglar papeles, residencia por
matrimonio, deportación, ciudadanía, Houston, and E-2 para mexicanos), all
sharing the Spanish thank-you page `/gracias.html`.

- **Campaign strategy, keyword data, ad structure:** [STRATEGY.md](STRATEGY.md)
- **Raw keyword research exports:** `research/keywords-us.tsv`, `research/keywords-canada.tsv`

## Build & preview

Zero dependencies — Python 3.8+ only:

```bash
python3 build.py                 # renders everything into public/
cd public && python3 -m http.server 8000   # preview at http://localhost:8000
```

`public/` is committed, so the site is deploy-ready without running anything.

## Structure

```
build.py                  generator (all shared page template logic + i18n strings)
content/site.json         firm-wide config: phone, stats, offer, disclaimers, GTM, form endpoint
content/pages/*.json      one file per campaign: all copy, FAQs, form qualifiers, meta;
                          optional "lang", "ui" (template-string overrides), and
                          "site_overrides" (per-page firm copy, e.g. Spanish stats/attorney bio)
assets/css/lp.css         design system (mobile-first, system fonts, WCAG-checked buttons)
assets/js/lp.js           ~3KB runtime: UTM/gclid capture, form submit, dataLayer events
public/                   generated output — the deployable site
  index.html              internal hub directory (never an ad destination)
  thank-you.html          conversion page (fires generate_lead)
  gracias.html            Spanish conversion page (same event)
  <campaign>/index.html   22 landing pages (15 EN + 7 ES)
research/                 keyword research exports + US-vs-Canada analysis (Aug 2026)
```

To edit copy: change the JSON, run `python3 build.py`, commit both.

## Deploying

Any static host works. Netlify is the zero-config path:

1. New site from this repo, publish directory `public/`, no build command
   (or build command `python3 build.py` if you prefer building on deploy).
2. Forms work immediately — every form has `data-netlify="true"`; submissions
   appear in the Netlify Forms dashboard. Add email notifications there.
3. Point DNS: `results.faragallalaw.com` (or `go.` / `lp.`) → Netlify.

Using a CRM/webhook instead (Zapier, HighLevel, Lawmatics): set
`form.endpoint` in `content/site.json` to the POST URL and rebuild. The JS
posts URL-encoded form data there and redirects to the thank-you page on 2xx.

## 🚨 Launch checklist — do not send paid traffic until every box is checked

**Blockers (legal/trust):**
- [ ] **Testimonials**: replace both placeholder quotes on every page with
  verbatim Google reviews (with client permission), matched to each page's
  practice area. Edit `testimonial_placeholder_lines` handling per page or the
  quotes in `build.py::render_testimonials`. Fabricated/paraphrased reviews
  violate bar advertising rules.
- [ ] **Attorney photo**: add a real professional headshot (no AI images) and
  swap the placeholder block in `build.py::render_attorney`.
- [ ] **Consultation offer** (`site.json → consultation.line`): state plainly
  whether the consultation is free or paid, its length, and what it includes.
- [ ] **Verify all claims** with the firm: 27+ years / 2,000+ cases / 4.8
  rating (`site.json → stats`), Fragomen background, NY bar admission,
  "respond within one business day", flat-fee statements on every page, office
  line. Remove anything the firm can't substantiate.
- [ ] **Office addresses**: several state bars require a physical address on
  attorney advertising. Add street addresses to the footer
  (`site.json → offices_line`).
- [ ] **Privacy policy URL** (`site.json → privacy_url`) resolves. Required for
  Google Ads lead gen.
- [ ] **Attorney-ad review**: have the firm's ethics/advertising counsel review
  the pages (headlines and FAQ answers are written to avoid outcome promises —
  keep it that way).
- [ ] **Google reviews link** (`site.json → google_reviews_url`): replace the
  Maps search with the firm's exact review short-link.

**Plumbing:**
- [x] ~~`site.json → gtm_id`~~ — **SET (2026-08-21): `GTM-T88G9RDN`
  (GTM account 6249382821), rendered on every page (head snippet + noscript
  iframe).** Remaining GTM work happens inside the container: add GA4 + Ads
  conversion triggers on `generate_lead` (thank-you view) and `phone_click`,
  scope hub triggers by hostname if the container also serves the main site,
  and verify with GTM preview mode.
- [ ] Form backend chosen (Netlify Forms or `form.endpoint`) and a **test lead
  submitted end-to-end**: form → thank-you redirect → notification email
  received → hidden fields (gclid/utm) present in the lead payload.
- [x] ~~Phone number~~ — **SET (2026-08-21): (866) 655-3729 on every page**
  (header, hero, final CTA, sticky bar, footer, thank-you pages, and
  LegalService schema). Optional later: CallRail pool for keyword-level call
  attribution (see STRATEGY.md).
- [ ] Custom domain + HTTPS live; `curl -I` each page returns 200.
- [ ] Real-device pass: iPhone Safari + Android Chrome — sticky bar doesn't
  cover the form's submit button, tel: links dial, forms submit.

**Spanish pages (all 7) extra blockers:**
- [x] ~~Confirm Spanish-speaking intake~~ — **CONFIRMED (2026-08-21): intake
  operates in both English and Spanish.** Pages and footers now state it
  (`site.json → languages_line`).
- [ ] Native-speaker review of the page copy (written in professional formal
  Spanish; a quick read by a native speaker is cheap insurance).
- [ ] Spanish testimonials: paste verbatim Spanish-language Google reviews.

**Nice-to-have before scale:**
- [ ] Favicon/logo files replacing the inline SVG "F".
- [ ] Speed sanity check (PageSpeed Insights) — pages are ~35KB with system
  fonts and no libraries, so scores should be green out of the box.
- [ ] If the firm has a real NYC or Miami office, clone the Houston page for
  those metros (verify the office claim first — location pages without a real
  presence are a bar-rules and Google Ads policy risk).

## Review fixes implemented

The rebuild bakes in every P0/P1 from the mobile audit of the old E-2 page:

| Audit issue | Where fixed |
|---|---|
| Blank mobile header, no brand | `.lp-header` — wordmark + tagline + tap-to-call always visible |
| `top: 200px` form gap bug | Form card is `position: static`, in normal flow after hero copy |
| Form below the fold, weak first screen | Eyebrow → H1 → 3 bullets → CTA → trust strip → form (the audit's exact prescription); desktop shows the full form above the fold |
| Misleading "Request Consultation" CTA | All CTAs anchor to the actual form and say what you get (e.g. "Request My E-2 Eligibility Review"); sticky-bar/anchor CTAs move focus into the first field |
| Undefined consultation offer | Offer named per page; response time + fee line + next steps in form microcopy and thank-you page (fee line is a launch-checklist item) |
| Generic "Path to Success" headline / guarantee-adjacent copy | Intent-matched H1s; zero outcome-promise language anywhere; "We Handle the Rest" replaced with specific process steps |
| Inconsistent CTA labels everywhere | One offer name + one CTA verb per page, reused in header, hero, sticky bar, form button |
| No pricing expectations | A "What does it cost?" section on every page (structure honesty without publishing fees) |
| No qualification | "Fit / not a fit" section + 2 qualifying dropdowns in every form |
| Generic/duplicated testimonials, fake-looking badge | Two clearly-marked verbatim-review slots + link to the Google profile; no imitation badges |
| ChatGPT-named attorney image | Explicit real-photo placeholder + launch blocker |
| Two different forms | One `render_form()` used in both locations — identical fields |
| `type="text"` phone input | `type="tel"` + `inputmode` + autocomplete everywhere; 16px inputs (no iOS zoom) |
| No phone-privacy microcopy | "Used only to follow up about your inquiry — no marketing calls." |
| No thank-you state | Dedicated `/thank-you.html` with next steps + doc checklist; fires `generate_lead` |
| No privacy/no-attorney-client language | Microcopy under every submit button + full footer disclaimer |
| "Submit" button | Benefit-labeled buttons per campaign |
| Cyan/white contrast failure (2.1:1) | Cyan buttons carry navy-950 text — 7.7:1 (AAA); white text only on navy |
| Text over busy video/imagery | Controlled gradient hero, fully opaque type |
| Sticky CTA: z-index 2147483647, no safe-area, links to /contact-us/ | Bottom bar: z-index 90, `env(safe-area-inset-bottom)`, body padding reserve, links to on-page form + tel:, visible immediately |
| Exit-point navigation | No nav; footer has only privacy + main site |
| No UTM/GCLID capture | 15 hidden tracking fields, localStorage first-touch, auto-filled |
| No conversion architecture | dataLayer events: `lead_form_submit`, `phone_click`, `generate_lead`, `lead_form_error` (see STRATEGY.md) |
| 23 CSS + 29 JS files, GSAP/Lenis | One CSS file + one 3KB JS file; native `<details>` FAQ; CSS-only smooth scroll with `scroll-margin-top` |
| Broken Khyay font 404s | System font stack only — nothing to 404, no layout shift |
| Copied Dallas metadata, trailing-pipe title | Unique per-campaign title/description/OG/canonical |
| Article/BlogPosting schema, wordCount 7 | `LegalService` + `FAQPage` JSON-LD |
| Competing scroll systems | One native mechanism + a focus handler |
| Paid traffic leaking to generic pages | Every CTA resolves on-page (form or tel:); hub index is internal-only |
