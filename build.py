#!/usr/bin/env python3
"""Faragalla Law PPC landing page hub — static site generator.

Zero dependencies (Python 3.8+ stdlib). Reads content/site.json and
content/pages/*.json, writes deploy-ready HTML into public/.

    python3 build.py

Localization: a page JSON may set "lang" (default "en"), override any template
string via "ui": {...} (keys in UI_EN), and override firm-wide copy via
"site_overrides": {...} (shallow-merged over site.json, dicts merged one level).
A page with lang "es" gets the Spanish thank-you page (/gracias.html).
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


def merge_site(site, page):
    """Apply locale defaults (for lang="es") then the page's site_overrides,
    each with one level of dict merge."""
    eff = dict(site)
    layers = []
    if page.get("lang") == "es":
        layers.append(SITE_ES)
    layers.append(page.get("site_overrides", {}))
    for layer in layers:
        for k, v in layer.items():
            if isinstance(v, dict) and isinstance(eff.get(k), dict):
                eff[k] = {**eff[k], **v}
            else:
                eff[k] = v
    return eff


# ---------------------------------------------------------------- UI strings

UI_EN = {
    "thankyou_path": "/thank-you.html",
    "hp_label": "Leave this field empty",
    "full_name": "Full name",
    "email": "Email",
    "phone": "Phone",
    "phone_hint": "Used only to follow up about your inquiry — no marketing calls.",
    "select_one": "Select one…",
    "msg_sending": "Sending your request…",
    "msg_error": "Something went wrong sending the form. Please call us instead — the number is at the top of the page.",
    "see_privacy": "See our",
    "privacy_policy": "Privacy Policy",
    "back_to_top": "back to top",
    "call_firm": "Call",
    "or_call": "or call",
    "avg_google": "average rating on Google",
    "k_problem": "What decides these cases",
    "k_fit": "Qualify yourself in 30 seconds",
    "fit_yes": "This service is likely a fit if…",
    "fit_no": "It's probably not the right fit if…",
    "k_why": "Why {firm}",
    "why_h2": "Counsel that pressure-tests your case before the government does",
    "k_process": "How it works",
    "process_h2": "A defined process — you always know the next step",
    "k_fees": "Costs, addressed head-on",
    "k_reviews": "Client reviews",
    "reviews_h2": "What clients say",
    "google_review_label": "Google review —",
    "reviews_source": "Reviews shown are from the firm's public {gbp_link}, reproduced verbatim with permission. Individual results vary; prior results do not guarantee a similar outcome.",
    "gbp_label": "Google Business Profile",
    "k_attorney": "Your attorney",
    "photo_placeholder": "Attorney headshot goes here<br>(assets/img/sam-faragalla.jpg — see README launch checklist; use a real photograph)",
    "k_faq": "Common questions",
    "faq_h2": "Questions we answer every week",
    "k_final": "Ready when you are",
    "final_call": "Prefer to talk? Call {phone} — tell us you're calling about the {campaign} page.",
    "main_site": "Main website",
    "call_now": "Call Now",
    "quick_actions": "Quick actions",
}

TY_EN = {
    "path": "/thank-you.html",
    "title": "Request Received",
    "h1": "Your request was received.",
    "lead": "{response_promise} — usually sooner. Here's exactly what happens next.",
    "steps": [
        ("We review your submission",
         "An attorney-supervised team member reads your answers and matches your case to the right review track."),
        ("You get a reply within one business day",
         "We email you consultation options, the consultation details, and anything we need from you — check your spam folder just in case."),
        ("Worth gathering meanwhile",
         "Your passport, any prior U.S. visa or immigration paperwork, and — for business cases — basic numbers on your investment or company. Don't worry if something is missing; we'll tell you exactly what matters for your case."),
    ],
    "callout_strong": "Need to talk sooner?",
    "callout_rest": "and mention that you've already submitted the form.",
    "meta_description": "Your request was received. Here's what happens next.",
}

UI_ES = {
    "thankyou_path": "/gracias.html",
    "hp_label": "Deje este campo vacío",
    "full_name": "Nombre completo",
    "email": "Correo electrónico",
    "phone": "Teléfono",
    "phone_hint": "Lo usamos únicamente para responder a su consulta — sin llamadas de mercadeo.",
    "select_one": "Seleccione una opción…",
    "msg_sending": "Enviando su solicitud…",
    "msg_error": "Ocurrió un error al enviar el formulario. Por favor llámenos — el número está en la parte superior de la página.",
    "see_privacy": "Consulte nuestra",
    "privacy_policy": "Política de Privacidad",
    "back_to_top": "volver arriba",
    "call_firm": "Llamar a",
    "or_call": "o llame al",
    "avg_google": "calificación promedio en Google",
    "k_problem": "Lo que decide estos casos",
    "k_fit": "Califíquese en 30 segundos",
    "fit_yes": "Este servicio probablemente es para usted si…",
    "fit_no": "Probablemente no es lo indicado si…",
    "k_why": "Por qué {firm}",
    "why_h2": "Abogados que someten su caso a prueba antes que el gobierno",
    "k_process": "Cómo funciona",
    "process_h2": "Un proceso definido — usted siempre sabe cuál es el siguiente paso",
    "k_fees": "Los costos, de frente",
    "k_reviews": "Reseñas de clientes",
    "reviews_h2": "Lo que dicen nuestros clientes",
    "google_review_label": "Reseña de Google —",
    "reviews_source": "Las reseñas mostradas provienen del {gbp_link} público del despacho, reproducidas textualmente con permiso. Cada caso es distinto; resultados anteriores no garantizan un resultado similar.",
    "gbp_label": "perfil de Google Business",
    "k_attorney": "Su abogado",
    "photo_placeholder": "Fotografía del abogado aquí<br>(assets/img/sam-faragalla.jpg — vea la lista de verificación del README; use una fotografía real)",
    "k_faq": "Preguntas frecuentes",
    "faq_h2": "Preguntas que respondemos cada semana",
    "k_final": "Cuando usted esté listo",
    "final_call": "¿Prefiere hablar? Llame al {phone} — mencione que vio la página «{campaign}».",
    "main_site": "Sitio web principal",
    "call_now": "Llamar Ahora",
    "quick_actions": "Acciones rápidas",
}

# Firm-wide copy defaults applied to every lang="es" page (a page's own
# site_overrides still wins on top of these).
SITE_ES = {
    "firm_tagline": "Abogados de Inmigración",
    "response_promise": "Respondemos dentro de un día hábil",
    "consultation": {
        "line": "Consultas de estrategia con tarifa fija — al responderle confirmamos las opciones de cita y cualquier costo de consulta."
    },
    "form_microcopy_privacy": "Usamos sus datos de contacto únicamente para responder a su consulta. Enviar este formulario no crea una relación abogado-cliente.",
    "offices_line": "Oficinas en Texas y Florida — servimos a clientes en todo el país",
    "disclaimer_footer": "Publicidad de Abogados. Este sitio web es solo informativo y no constituye asesoría legal. Enviar un formulario o llamar al despacho no crea una relación abogado-cliente. Los resultados anteriores no garantizan un resultado similar. No existe una relación abogado-cliente hasta que se firme un acuerdo de representación por escrito.",
    "stats": [
        {"value": "27+", "label": "Años de experiencia migratoria combinada"},
        {"value": "2,000+", "label": "Casos de inmigración manejados"},
        {"value": "4.8★", "label": "Calificación promedio en Google"},
    ],
    "attorney": {
        "title": "Fundador y Abogado Principal de Inmigración",
        "bio_short": "Sam Faragalla se formó en Fragomen, una de las firmas de inmigración corporativa más grandes del mundo, antes de fundar Faragalla Law. El despacho representa a familias, trabajadores, empresarios e inversionistas en asuntos migratorios en todo Estados Unidos.",
        "license_line": "Licenciado para ejercer la abogacía en Nueva York. La ley de inmigración es federal, lo que permite al despacho representar clientes en los 50 estados y en el extranjero.",
    },
    "testimonial_placeholder_lines": [
        "[PEGUE AQUÍ UNA RESEÑA TEXTUAL DE GOOGLE — en español, de un caso similar. Vea el README.]",
        "[PEGUE AQUÍ UNA SEGUNDA RESEÑA TEXTUAL EN ESPAÑOL.]",
    ],
    "languages_line": "Atendemos en español e inglés — todo su caso puede llevarse en su idioma",
}

TY_ES = {
    "path": "/gracias.html",
    "title": "Solicitud Recibida",
    "h1": "Recibimos su solicitud.",
    "lead": "{response_promise} — generalmente antes. Esto es exactamente lo que sigue.",
    "steps": [
        ("Revisamos su información",
         "Un miembro del equipo, supervisado por un abogado, lee sus respuestas y dirige su caso a la vía de evaluación correcta."),
        ("Recibirá respuesta dentro de un día hábil",
         "Le enviaremos por correo las opciones de consulta, los detalles y cualquier cosa que necesitemos de usted — revise su carpeta de spam por si acaso."),
        ("Mientras tanto, vale la pena reunir",
         "Su pasaporte, cualquier documento migratorio anterior y cualquier notificación que haya recibido del gobierno. No se preocupe si le falta algo; le diremos exactamente qué importa en su caso."),
    ],
    "callout_strong": "¿Necesita hablar antes?",
    "callout_rest": "y mencione que ya envió el formulario.",
    "meta_description": "Recibimos su solicitud. Esto es lo que sigue.",
}


def ui_for(page):
    base = {**UI_EN, **UI_ES} if page.get("lang") == "es" else dict(UI_EN)
    return {**base, **page.get("ui", {})}


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

def render_form(site, page, ui, location):
    """One consistent form used in the hero and the final section.

    Backend resolution: form.endpoint wins; else form.formspree_id builds a
    Formspree URL; else Netlify Forms handles the POST. With an endpoint, the
    form's native action targets it too, so leads survive even without JS."""
    slug = page["slug"]
    endpoint = site["form"].get("endpoint", "")
    if not endpoint and site["form"].get("formspree_id"):
        endpoint = f"https://formspree.io/f/{site['form']['formspree_id']}"
    # Netlify attributes only when Netlify is actually the backend — an active
    # endpoint would otherwise leave ghost forms in the Netlify dashboard.
    netlify_attrs = ' data-netlify="true" netlify-honeypot="company_website"' if site["form"].get("netlify") and not endpoint else ""
    action = endpoint if endpoint else ui["thankyou_path"]

    hidden = "\n      ".join(
        f'<input type="hidden" name="{name}" value="">' for name in HIDDEN_TRACKING_FIELDS
    )
    # Baked at build time so the source page is named on every submission,
    # including no-JS posts (JS-filled fields like landing_page need JS).
    hidden += f'\n      <input type="hidden" name="page_name" value="{e(page["campaign"])}">'
    if endpoint:
        # Formspree conveniences (harmless for generic webhooks): per-page email
        # subject, paid-plan no-JS redirect, and the native _gotcha honeypot.
        next_url = f"{site['base_url'].rstrip('/')}{ui['thankyou_path']}?from=/{slug}/"
        hidden += (
            f'\n      <input type="hidden" name="_subject" value="New lead — {e(page["campaign"])} — /{slug}/">'
            f'\n      <input type="hidden" name="_next" value="{e(next_url)}">'
            f'\n      <input class="hp-field" type="text" name="_gotcha" tabindex="-1" autocomplete="off" aria-hidden="true">'
        )

    qualifiers = ""
    for q in page.get("qualifiers", []):
        opts = "".join(f"<option>{e(o)}</option>" for o in q["options"])
        qualifiers += f"""
      <div>
        <label for="{location}-{q['name']}">{e(q['label'])}</label>
        <select id="{location}-{q['name']}" name="{q['name']}" required>
          <option value="" selected disabled>{e(ui['select_one'])}</option>{opts}
        </select>
      </div>"""

    return f"""<form class="lp-form" method="POST" action="{e(action)}" name="lead-{slug}"
      data-form-location="{location}" data-endpoint="{e(endpoint)}" data-thankyou="{ui['thankyou_path']}"
      data-msg-sending="{e(ui['msg_sending'])}" data-msg-error="{e(ui['msg_error'])}"{netlify_attrs}>
      <input type="hidden" name="form-name" value="lead-{slug}">
      <input type="hidden" name="campaign_page" value="{slug}">
      {hidden}
      <p class="hp-field" aria-hidden="true"><label>{e(ui['hp_label'])} <input type="text" name="company_website" tabindex="-1" autocomplete="off"></label></p>
      <div>
        <label for="{location}-name">{e(ui['full_name'])}</label>
        <input id="{location}-name" type="text" name="name" autocomplete="name" required>
      </div>
      <div>
        <label for="{location}-email">{e(ui['email'])}</label>
        <input id="{location}-email" type="email" name="email" autocomplete="email" inputmode="email" required>
      </div>
      <div>
        <label for="{location}-phone">{e(ui['phone'])}</label>
        <input id="{location}-phone" type="tel" name="phone" autocomplete="tel" inputmode="tel" required>
        <div class="field-hint">{e(ui['phone_hint'])}</div>
      </div>{qualifiers}
      <div class="lp-form__status" role="status" aria-live="polite"></div>
      <button class="btn btn--primary btn--block" type="submit">{e(page['cta_label'])}</button>
      <p class="lp-form__microcopy">{e(site['response_promise'])}. {e(site['consultation']['line'])}
      {e(site['form_microcopy_privacy'])} {e(ui['see_privacy'])} <a href="{e(site['privacy_url'])}" target="_blank" rel="noopener">{e(ui['privacy_policy']).replace(' ', '&nbsp;')}</a>.</p>
    </form>"""


def render_header(site, page, ui):
    return f"""<header class="lp-header">
    <div class="container lp-header__inner">
      <a class="lp-header__brand" href="#top" aria-label="{e(site['firm_name'])} — {e(ui['back_to_top'])}">
        <span class="lp-header__name">{e(site['firm_name'])}</span>
        <span class="lp-header__tag">{e(site['firm_tagline'])}</span>
      </a>
      <div class="lp-header__actions">
        <a class="lp-header__phone" href="tel:{e(site['phone_tel'])}" data-call-location="header">
          {ICON_PHONE}<span class="lp-header__phone-num">{e(site['phone_display'])}</span>
          <span class="visually-hidden">{e(ui['call_firm'])} {e(site['firm_name'])}</span>
        </a>
        <a class="btn btn--primary btn--sm lp-header__cta" href="#lead-form" data-jump-form>{e(page['cta_short'])}</a>
      </div>
    </div>
  </header>"""


def render_hero(site, page, ui):
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
          <p class="hero__call">{e(ui['or_call'])} <a href="tel:{e(site['phone_tel'])}" data-call-location="hero">{e(site['phone_display'])}</a></p>
        </div>
        <div class="hero__trust">
          <span><strong>{e(stats[0]['value'])}</strong> {e(stats[0]['label'].lower())}</span>
          <span><strong>{e(stats[1]['value'])}</strong> {e(stats[1]['label'].lower())}</span>
          <span><span class="stars" aria-hidden="true">★★★★★</span>
            <a href="{e(site['google_reviews_url'])}" target="_blank" rel="noopener"><strong>{e(stats[2]['value'].replace('★',''))}</strong> {e(ui['avg_google'])}</a></span>
        </div>
      </div>
      <div class="form-card" id="lead-form">
        <h2>{e(page['form_title'])}</h2>
        <p class="form-card__sub">{e(page['form_sub'])}</p>
        {render_form(site, page, ui, 'hero')}
      </div>
    </div>
  </section>"""


def render_problem(page, ui):
    cards = "\n        ".join(
        f'<div class="card"><h3>{e(c["title"])}</h3><p>{e(c["body"])}</p></div>'
        for c in page["problem_cards"]
    )
    return f"""<section class="section">
    <div class="container">
      <p class="section__kicker">{e(ui['k_problem'])}</p>
      <h2>{e(page['problem_heading'])}</h2>
      <div class="cards">
        {cards}
      </div>
    </div>
  </section>"""


def render_fit(site, page, ui):
    fors = "\n            ".join(
        f"<li>{ICON_CHECK_GREEN}<span>{e(x)}</span></li>" for x in page["who_for"]
    )
    nots = "\n            ".join(
        f"<li>{ICON_X}<span>{e(x)}</span></li>" for x in page["who_not"]
    )
    return f"""<section class="section section--alt">
    <div class="container">
      <p class="section__kicker">{e(ui['k_fit'])}</p>
      <h2>{e(page['who_heading'])}</h2>
      <div class="fit">
        <div class="fit__col">
          <h3>{e(ui['fit_yes'])}</h3>
          <ul>
            {fors}
          </ul>
        </div>
        <div class="fit__col fit__col--no">
          <h3>{e(ui['fit_no'])}</h3>
          <ul>
            {nots}
          </ul>
        </div>
      </div>
    </div>
  </section>"""


def render_why(site, page, ui):
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
      <p class="section__kicker">{e(ui['k_why'].format(firm=site['firm_name']))}</p>
      <h2>{e(ui['why_h2'])}</h2>
      <div class="cards cards--4">
        {cards}
      </div>
    </div>
  </section>
  <section aria-label="{e(site['firm_name'])}">
    <div class="container">
      <div class="stats">
        {stats}
      </div>
    </div>
  </section>"""


def render_process(site, page, ui):
    steps = "\n        ".join(
        f'<div class="step"><h3>{e(s["title"])}</h3><p>{e(s["body"])}</p></div>'
        for s in page["process"]
    )
    return f"""<section class="section section--alt">
    <div class="container">
      <p class="section__kicker">{e(ui['k_process'])}</p>
      <h2>{e(ui['process_h2'])}</h2>
      <div class="steps">
        {steps}
      </div>
    </div>
  </section>"""


def render_fees(page, ui):
    return f"""<section class="section">
    <div class="container">
      <p class="section__kicker">{e(ui['k_fees'])}</p>
      <h2>{e(page['fees_heading'])}</h2>
      <p class="section__lead" style="margin-bottom:0">{e(page['fees_body'])}</p>
    </div>
  </section>"""


def render_testimonials(site, page, ui):
    quotes = "\n        ".join(
        f"""<figure class="quote">
          <div class="stars" aria-hidden="true">★★★★★</div>
          <blockquote>{e(line)}</blockquote>
          <figcaption>{e(ui['google_review_label'])} {e(page['testimonial_hint'])}</figcaption>
        </figure>"""
        for line in site["testimonial_placeholder_lines"]
    )
    gbp_link = f'<a href="{e(site["google_reviews_url"])}" target="_blank" rel="noopener">{e(ui["gbp_label"])}</a>'
    source = e(ui["reviews_source"]).replace("{gbp_link}", gbp_link)
    return f"""<section class="section section--alt">
    <div class="container">
      <p class="section__kicker">{e(ui['k_reviews'])}</p>
      <h2>{e(ui['reviews_h2'])}</h2>
      <div class="quotes">
        {quotes}
      </div>
      <p class="quotes__source">{source}</p>
    </div>
  </section>"""


def render_attorney(site, ui):
    a = site["attorney"]
    return f"""<section class="section">
    <div class="container attorney">
      <div class="attorney__photo">
        <span>{ui['photo_placeholder']}</span>
      </div>
      <div>
        <p class="section__kicker">{e(ui['k_attorney'])}</p>
        <h3>{e(a['name'])}</h3>
        <p class="attorney__role">{e(a['title'])}</p>
        <p>{e(a['bio_short'])}</p>
        <p class="attorney__license">{e(a['license_line'])}</p>
      </div>
    </div>
  </section>"""


def render_faq(page, ui):
    items = "\n        ".join(
        f"""<details>
          <summary>{e(f['q'])}</summary>
          <div><p>{e(f['a'])}</p></div>
        </details>"""
        for f in page["faq"]
    )
    return f"""<section class="section section--alt">
    <div class="container">
      <p class="section__kicker">{e(ui['k_faq'])}</p>
      <h2>{e(ui['faq_h2'])}</h2>
      <div class="faq">
        {items}
      </div>
    </div>
  </section>"""


def render_final(site, page, ui):
    phone_link = f'<a href="tel:{e(site["phone_tel"])}" data-call-location="final">{e(site["phone_display"])}</a>'
    call_line = e(ui["final_call"]).replace("{phone}", phone_link).replace("{campaign}", e(page["campaign"]))
    return f"""<section class="section section--navy final">
    <div class="container">
      <p class="section__kicker">{e(ui['k_final'])}</p>
      <h2>{e(page['final_heading'])}</h2>
      <p class="section__lead">{e(page['final_sub'])}</p>
      <div class="form-card" id="lead-form-bottom">
        <h3>{e(page['form_title'])}</h3>
        <p class="form-card__sub">{e(page['form_sub'])}</p>
        {render_form(site, page, ui, 'bottom')}
      </div>
      <p class="final__call">{call_line}</p>
    </div>
  </section>"""


def render_footer(site, ui):
    return f"""<footer class="lp-footer">
    <div class="container">
      <div class="lp-footer__firm">{e(site['firm_name'])} — {e(site['firm_tagline'])}</div>
      <div>{e(site['offices_line'])}</div>
      <div>{e(site.get('languages_line', ''))}</div>
      <div class="lp-footer__row">
        <a href="tel:{e(site['phone_tel'])}" data-call-location="footer">{e(site['phone_display'])}</a>
        &nbsp;·&nbsp; <a href="{e(site['privacy_url'])}" target="_blank" rel="noopener">{e(ui['privacy_policy'])}</a>
        &nbsp;·&nbsp; <a href="{e(site['main_site_url'])}" target="_blank" rel="noopener">{e(ui['main_site'])}</a>
      </div>
      <p class="lp-footer__disclaimer">{e(site['disclaimer_footer'])}</p>
    </div>
  </footer>"""


def render_stickybar(site, page, ui):
    return f"""<div class="stickybar" role="navigation" aria-label="{e(ui['quick_actions'])}">
    <a class="btn btn--call" href="tel:{e(site['phone_tel'])}" data-call-location="stickybar">{ICON_PHONE} {e(ui['call_now'])}</a>
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


def gtm_noscript(site):
    """GTM <noscript> iframe — rendered right after <body> when a container is set."""
    if not site.get("gtm_id"):
        return ""
    return (f'<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={site["gtm_id"]}" '
            'height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>')


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


def render_page(site_base, page):
    site = merge_site(site_base, page)
    ui = ui_for(page)
    lang = page.get("lang", "en")
    canonical = f"{site['base_url'].rstrip('/')}/{page['slug']}/"
    jsonld = render_jsonld(site, page, canonical)
    head = render_head(site, page["meta_title"], page["meta_description"], canonical, jsonld)
    return f"""<!doctype html>
<html lang="{lang}">
<head>
  {head}
</head>
<body>
  {gtm_noscript(site)}
  {render_header(site, page, ui)}
  <main>
  {render_hero(site, page, ui)}
  {render_problem(page, ui)}
  {render_fit(site, page, ui)}
  {render_why(site, page, ui)}
  {render_process(site, page, ui)}
  {render_fees(page, ui)}
  {render_testimonials(site, page, ui)}
  {render_attorney(site, ui)}
  {render_faq(page, ui)}
  {render_final(site, page, ui)}
  </main>
  {render_footer(site, ui)}
  {render_stickybar(site, page, ui)}
</body>
</html>
"""


def render_thank_you(site, ty, lang):
    head = render_head(
        site,
        f"{ty['title']} | {site['firm_name']}",
        ty["meta_description"],
        f"{site['base_url'].rstrip('/')}{ty['path']}",
    )
    steps = "\n      ".join(
        f'<div class="card"><h3><span>{i}.</span> {e(t)}</h3><p>{e(b)}</p></div>'
        for i, (t, b) in enumerate(ty["steps"], 1)
    )
    lead = e(ty["lead"].format(response_promise=site["response_promise"]))
    return f"""<!doctype html>
<html lang="{lang}">
<head>
  {head}
  <script>
    window.dataLayer.push({{
      event: 'generate_lead',
      page_path: '{ty['path']}',
      from_page: new URLSearchParams(location.search).get('from') || 'direct'
    }});
  </script>
</head>
<body>
  {gtm_noscript(site)}
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
    <h1>{e(ty['h1'])}</h1>
    <p class="ty-lead">{lead}</p>
    <div class="ty-steps">
      {steps}
    </div>
    <div class="ty-callout">
      <strong>{e(ty['callout_strong'])}</strong>
      <a href="tel:{e(site['phone_tel'])}" data-call-location="thankyou">{e(site['phone_display'])}</a>
      {e(ty['callout_rest'])}
    </div>
    <p class="lp-form__microcopy">{e(site['form_microcopy_privacy'])}</p>
  </main>
  {render_footer(site, {**UI_EN} if lang == 'en' else {**UI_EN, 'privacy_policy': 'Política de Privacidad', 'main_site': 'Sitio web principal'})}
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
  {gtm_noscript(site)}
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
      <p class="section__lead" style="font-size:14px">Conversion pages: <a href="/thank-you.html">/thank-you.html</a> · <a href="/gracias.html">/gracias.html</a> (ES) · Strategy &amp; launch checklist: see README.md and STRATEGY.md in the repository.</p>
    </div>
  </main>
  {render_footer(site, UI_EN)}
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
        print(f"  built /{page['slug']}/  [{page.get('lang', 'en')}]")

    (PUBLIC / "thank-you.html").write_text(render_thank_you(site, TY_EN, "en"), encoding="utf-8")
    print("  built /thank-you.html")

    # Spanish thank-you whenever any page is Spanish
    es_pages = [p for p in pages if p.get("lang") == "es"]
    if es_pages:
        site_es = merge_site(site, es_pages[0])
        (PUBLIC / "gracias.html").write_text(render_thank_you(site_es, TY_ES, "es"), encoding="utf-8")
        print("  built /gracias.html")

    (PUBLIC / "index.html").write_text(render_index(site, pages), encoding="utf-8")
    print("  built /index.html (hub directory)")

    # robots: allow crawling (AdsBot must reach pages for Quality Score);
    # organic exclusion is handled by the per-page meta noindex.
    (PUBLIC / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")
    print("  built /robots.txt")

    print(f"\nDone — {len(pages)} campaign pages + thank-you pages + index in public/")


if __name__ == "__main__":
    main()
