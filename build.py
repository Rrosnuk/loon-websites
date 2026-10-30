#!/usr/bin/env python3
"""Build the Loon Softworks websites.

  python3 build.py            -> writes dist/<cloudflare-project>/ for studio, truffe, calendarcorrector
                                 plus dist/lugnutapp-overlay/ (applied to the live Lugnut site at deploy)
Pages live in src/<site>/pages/<id>.<lang>.html with a small front-matter block.
Shared chrome (header, footer, head tags) is generated here so every site matches."""
import json, re, shutil, html, hashlib
from pathlib import Path

ROOT = Path(__file__).parent
SRC, DIST = ROOT / "src", ROOT / "dist"
YEAR = "2026"
EMAIL = "support@loonsoftworks.com"
UPDATED = {"en": "30 October 2026", "fr": "30 octobre 2026", "es": "30 de octubre de 2026", "de": "30. Oktober 2026"}

LANG_NAMES = {"en": "English", "fr": "Français", "es": "Español", "de": "Deutsch"}
HTML_LANG = {"en": "en", "fr": "fr-CA", "es": "es", "de": "de"}
OG_LOCALE = {"en": "en_CA", "fr": "fr_CA", "es": "es_ES", "de": "de_DE"}

STUDIO = "https://loonsoftworks.com"
APPS = {
    "lugnut": {"name": "Lugnut", "url": "https://lugnut.loonsoftworks.com", "icon": "lugnut-icon.svg"},
    "calendar": {"name": "Calendar Corrector", "url": "https://calendarcorrector.loonsoftworks.com", "icon": "calendar-icon.svg"},
    "truffe": {"name": "Truffe", "url": "https://truffe.loonsoftworks.com", "icon": "truffe-icon.svg"},
}

# Strings used in the shared chrome
T = {
    "en": dict(skip="Skip to content", language="Language", legal="Legal", privacy="Privacy", terms="Terms of use",
               access="Accessibility", notice="Legal notice", studio="Loon Softworks", about="About the studio",
               support="Support", press="Press kit", guides="Guides", home="Home", app="The app",
               nocookies="This site uses no cookies, analytics or tracking.",
               madeby="Made by Loon Softworks, an independent app studio in Ontario, Canada.",
               tm="Apple, the Apple logo, iPhone, iPad and Mac are trademarks of Apple Inc., registered in the U.S. and other countries. App Store is a service mark of Apple Inc. Google Play and Android are trademarks of Google LLC.",
               android_app="On Android? {app} is coming to Google Play.", android_cta="Email me when it’s ready",
               android_subject="Android: {app}"),
    "fr": dict(skip="Aller au contenu", language="Langue", legal="Juridique", privacy="Confidentialité", terms="Conditions d’utilisation",
               access="Accessibilité", notice="Mentions légales", studio="Loon Softworks", about="À propos du studio",
               support="Assistance", press="Dossier de presse", guides="Guides", home="Accueil", app="L’app",
               nocookies="Ce site n’utilise ni témoins (cookies), ni outil d’analyse, ni pistage.",
               madeby="Conçu par Loon Softworks, un studio d’applications indépendant en Ontario, au Canada.",
               tm="Apple, le logo Apple, iPhone, iPad et Mac sont des marques d’Apple Inc., déposées aux États-Unis et dans d’autres pays. App Store est une marque de service d’Apple Inc. Google Play et Android sont des marques de Google LLC.",
               android_app="Sur Android? {app} arrive bientôt sur Google Play.", android_cta="M’écrire quand ce sera prêt",
               android_subject="Android : {app}"),
    "es": dict(skip="Ir al contenido", language="Idioma", legal="Legal", privacy="Privacidad", terms="Términos de uso",
               access="Accesibilidad", notice="Aviso legal", studio="Loon Softworks", about="Sobre el estudio",
               support="Soporte", press="Prensa", guides="Guías", home="Inicio", app="La app",
               nocookies="Este sitio no usa cookies, analítica ni rastreo.",
               madeby="Hecho por Loon Softworks, un estudio independiente de apps en Ontario, Canadá.",
               tm="Apple, el logotipo de Apple, iPhone, iPad y Mac son marcas comerciales de Apple Inc., registradas en EE. UU. y otros países. App Store es una marca de servicio de Apple Inc. Google Play y Android son marcas comerciales de Google LLC.",
               android_app="¿Usas Android? {app} llegará pronto a Google Play.", android_cta="Avísame cuando esté lista",
               android_subject="Android: {app}"),
    "de": dict(skip="Zum Inhalt springen", language="Sprache", legal="Rechtliches", privacy="Datenschutz", terms="Nutzungsbedingungen",
               access="Barrierefreiheit", notice="Impressum", studio="Loon Softworks", about="Über das Studio",
               support="Support", press="Presse", guides="Ratgeber", home="Start", app="Die App",
               nocookies="Diese Website verwendet keine Cookies, keine Analyse und kein Tracking.",
               madeby="Entwickelt von Loon Softworks, einem unabhängigen App-Studio in Ontario, Kanada.",
               tm="Apple, das Apple-Logo, iPhone, iPad und Mac sind Marken der Apple Inc., die in den USA und weiteren Ländern eingetragen sind. App Store ist eine Dienstleistungsmarke der Apple Inc. Google Play und Android sind Marken von Google LLC.",
               android_app="Android? {app} kommt bald zu Google Play.", android_cta="Benachrichtigt mich",
               android_subject="Android: {app}"),
}

# Studio pages every app links to (legal notice and accessibility live on the studio site)
STUDIO_LINKS = {
    "en": {"about": "/", "privacy": "/privacy/", "access": "/accessibility/", "notice": "/legal/"},
    "fr": {"about": "/fr/", "privacy": "/fr/confidentialite/", "access": "/fr/accessibilite/", "notice": "/fr/mentions-legales/"},
}
def studio_link(lang, key):
    l = lang if lang in STUDIO_LINKS else "en"
    if lang == "de" and key == "notice":
        return STUDIO + "/legal/#impressum"
    return STUDIO + STUDIO_LINKS[l][key]

GLOBE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3z"/></svg>'

SITES = {
    "studio": dict(project="loonsoftworks", domain=STUDIO, key=None, name="Loon Softworks", langs=["en", "fr"],
                   icon="/favicon.svg", theme="#0f2a3a", og="/og.png",
                   nav={"en": [("apps", "Apps", "/#apps"), ("how", "How we build", "/#how"), ("contact", "Contact", "/#contact")],
                        "fr": [("apps", "Apps", "/fr/#apps"), ("how", "Notre façon de faire", "/fr/#how"), ("contact", "Nous joindre", "/fr/#contact")]}),
    "truffe": dict(project="truffe", domain=APPS["truffe"]["url"], key="truffe", name="Truffe", langs=["en", "fr"],
                   icon="/favicon.svg", theme="#6a4cf5", og="/img/og.png",
                   nav={"en": [("home", "Features", "/#features"), ("privacy-h", "Privacy", "/#privacy"), ("support", "Help", "/support/")],
                        "fr": [("home", "Fonctions", "/fr/#features"), ("privacy-h", "Confidentialité", "/fr/#privacy"), ("support", "Aide", "/fr/aide/")]},
                   footer_app={"en": [("Features", "/#features"), ("Help", "/support/"), ("Privacy policy", "/privacy/"), ("Terms of use", "/terms/")],
                               "fr": [("Fonctions", "/fr/#features"), ("Aide", "/fr/aide/"), ("Confidentialité", "/fr/confidentialite/"), ("Conditions d’utilisation", "/fr/conditions/")]}),
    "calendarcorrector": dict(project="calendarcorrector", domain=APPS["calendar"]["url"], key="calendar", name="Calendar Corrector", langs=["en", "fr"],
                   icon="/favicon.svg", theme="#1d4ed8", og="/img/og.png",
                   nav={"en": [("home", "Features", "/#features"), ("pricing", "Pricing", "/#pricing"), ("guides", "Guides", "/guides/"), ("support", "Support", "/support/")],
                        "fr": [("home", "Fonctions", "/fr/#features"), ("pricing", "Prix", "/fr/#pricing"), ("guides", "Guides (EN)", "/guides/"), ("support", "Assistance", "/fr/assistance/")]},
                   footer_app={"en": [("Features", "/#features"), ("Guides", "/guides/"), ("Support", "/support/"), ("Press kit", "/press/"), ("Privacy policy", "/privacy/"), ("Terms of use", "/terms/")],
                               "fr": [("Fonctions", "/fr/#features"), ("Assistance", "/fr/assistance/"), ("Dossier de presse (EN)", "/press/"), ("Confidentialité", "/fr/confidentialite/"), ("Conditions d’utilisation", "/fr/conditions/")]}),
}

def esc(s): return html.escape(s, quote=True)

def parse_page(p: Path):
    raw = p.read_text()
    m = re.match(r"---\n(.*?)\n---\n(.*)", raw, re.S)
    meta = {}
    for line in m.group(1).splitlines():
        k, _, v = line.partition(":")
        meta[k.strip()] = v.strip()
    pid, lang = p.name[:-5].rsplit(".", 1)
    meta.update(id=pid, lang=lang, body=m.group(2))
    return meta

def header(site, page, alts):
    lang, s = page["lang"], SITES[page["site"]]
    t = T[lang]
    home = "/" if lang == "en" else f"/{lang}/"
    if s["key"]:
        brand = f'<a class="brand" href="{home}"><img src="{s["icon"]}" alt="" width="32" height="32"><span>{esc(s["name"])}</span></a>'
    else:
        brand = f'<a class="brand" href="{home}"><img src="/favicon.svg" alt="" width="32" height="32"><span>Loon Softworks</span></a>'
    items = "".join(
        f'<li><a href="{h}"{" aria-current=\"page\"" if page.get("nav") == k else ""}>{esc(lbl)}</a></li>'
        for k, lbl, h in s["nav"][lang])
    langs = ""
    for l in s["langs"]:
        href = alts.get(l, "/" if l == "en" else f"/{l}/")
        cur = ' aria-current="true"' if l == lang else ""
        langs += f'<li><a href="{href}" hreflang="{l}" lang="{HTML_LANG[l]}"{cur}>{LANG_NAMES[l]}</a></li>'
    lang_menu = (f'<details class="lang"><summary aria-label="{t["language"]}: {LANG_NAMES[lang]}">{GLOBE}<span>{LANG_NAMES[lang]}</span></summary>'
                 f'<ul>{langs}</ul></details>')
    return (f'<a class="skip" href="#main">{t["skip"]}</a>\n'
            f'<header class="site-header"><div class="wrap bar">{brand}'
            f'<nav class="primary" aria-label="{"Main" if lang=="en" else "Principal"}"><ul>{items}</ul></nav>{lang_menu}</div></header>')

def android_note(site, lang):
    s = SITES[site]
    if not s["key"]: return ""
    t = T[lang]; app = s["name"]
    subj = t["android_subject"].format(app=app).replace(" ", "%20").replace(":", "%3A")
    return (f'<div class="android-note" id="android-note" hidden>{esc(t["android_app"].format(app=app))} '
            f'<a href="mailto:{EMAIL}?subject={subj}">{esc(t["android_cta"])}</a></div>')

def footer_html(lang, app_col, studio_self, alts, langs, app_title=None):
    """Shared footer. app_col: list of (label, href) or None (studio)."""
    t = T[lang]
    cols = []
    if app_col:
        cols.append(f'<div><h2>{esc(app_title or t["app"])}</h2><ul>' + "".join(f'<li><a href="{h}">{esc(l)}</a></li>' for l, h in app_col) + "</ul></div>")
    legal = [(t["privacy"], studio_link(lang, "privacy") if not app_col else None), (t["access"], studio_link(lang, "access")), (t["notice"], studio_link(lang, "notice"))]
    if studio_self:
        legal = [(l, h.replace(STUDIO, "")) for l, h in legal if h]
    else:
        legal = [(l, h) for l, h in legal if h]
    cols.append(f'<div><h2>{t["legal"]}</h2><ul>' + "".join(f'<li><a href="{h}">{esc(l)}</a></li>' for l, h in legal) + "</ul></div>")
    studio_items = [(a["name"], a["url"] + ("/" if lang == "en" else f"/{lang}/" if lang in ("fr",) else "/")) for a in APPS.values()]
    about = studio_link(lang, "about")
    if studio_self: about = about.replace(STUDIO, "")
    cols.append(f'<div><h2><a class="studio-mark" href="{about}">Loon Softworks</a></h2><ul>' +
                "".join(f'<li><a href="{h}">{esc(n)}</a></li>' for n, h in studio_items) +
                f'<li><a href="{about}">{esc(t["about"])}</a></li></ul></div>')
    ls = "".join(f'<li><a href="{alts.get(l, "/" if l=="en" else f"/{l}/")}" hreflang="{l}" lang="{HTML_LANG[l]}"{" aria-current=\"true\"" if l==lang else ""}>{LANG_NAMES[l]}</a></li>' for l in langs)
    cols.append(f'<div><h2>{t["language"]}</h2><ul>{ls}</ul></div>')
    return (f'<footer class="site-footer"><div class="wrap cols">{"".join(cols)}</div>'
            f'<div class="wrap fineprint"><p>© {YEAR} Loon Softworks · Ontario, Canada · <a href="mailto:{EMAIL}">{EMAIL}</a></p>'
            f'<p>{esc(t["nocookies"])}</p><p>{esc(t["tm"])}</p></div></footer>')

def footer(page, alts):
    s = SITES[page["site"]]; lang = page["lang"]
    return footer_html(lang, s.get("footer_app", {}).get(lang), s["key"] is None, alts, s["langs"], app_title=s["name"] if s["key"] else None)

def head(page, alts):
    s = SITES[page["site"]]; lang = page["lang"]
    url = s["domain"] + page["path"]
    title = page["title"]; desc = page["description"]
    links = ""
    if page["path"] != "/404.html":
        links += f'<link rel="canonical" href="{url}">\n'
        for l, p in alts.items():
            links += f'<link rel="alternate" hreflang="{l}" href="{s["domain"]}{p}">\n'
        if len(alts) > 1 and "en" in alts:
            links += f'<link rel="alternate" hreflang="x-default" href="{s["domain"]}{alts["en"]}">\n'
    og_img = s["domain"] + s["og"]
    ld = page.get("jsonld", "")
    robots = '<meta name="robots" content="noindex">\n' if page["path"] == "/404.html" else ""
    return f"""<!doctype html>
<html lang="{HTML_LANG[lang]}" data-site="{ {'studio':'studio','truffe':'truffe','calendarcorrector':'calendar'}[page['site']] }">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="{s['theme']}">
{robots}{links}<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(s['name'])}">
<meta property="og:title" content="{esc(page.get('ogtitle', title))}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(s['name'])}">
<meta property="og:locale" content="{OG_LOCALE[lang]}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="stylesheet" href="/loon.css?v={CSS_HASH}">
{ld}</head>
<body>
"""

ANDROID_JS = "(function(){try{if(/Android/i.test(navigator.userAgent)){var n=document.getElementById('android-note');if(n)n.hidden=false}}catch(e){}})();\n"

def jsonld_app(site, lang, desc, os_, category, offers):
    s = SITES[site]
    d = {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": s["name"], "description": desc,
         "applicationCategory": category, "operatingSystem": os_, "url": s["domain"] + "/", "inLanguage": s["langs"],
         "offers": offers, "publisher": {"@type": "Organization", "name": "Loon Softworks", "url": STUDIO + "/", "email": EMAIL}}
    return f'<script type="application/ld+json">{json.dumps(d, ensure_ascii=False)}</script>\n'

def build_site(site):
    s = SITES[site]
    out = DIST / s["project"]
    if out.exists(): shutil.rmtree(out)
    out.mkdir(parents=True)
    pages = [dict(parse_page(p), site=site) for p in sorted((SRC / site / "pages").glob("*.html"))]
    by_id = {}
    for p in pages: by_id.setdefault(p["id"], {})[p["lang"]] = p["path"]
    for p in pages:
        alts = {} if p["path"] == "/404.html" else by_id[p["id"]]
        body = p["body"].replace("{{UPDATED}}", UPDATED[p["lang"]]).replace("{{EMAIL}}", EMAIL)
        doc = (head(p, alts) + android_note(site, p["lang"]) + "\n" + header(site, p, alts) +
               f'\n<main id="main">\n{body}\n</main>\n' + footer(p, alts) +
               ('\n<script src="/site.js" defer></script>' if s["key"] else "") + "\n</body>\n</html>\n")
        dest = out / (p["path"].lstrip("/") + ("index.html" if p["path"].endswith("/") else ""))
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(doc)
    # static files, shared css, icons
    st = SRC / site / "static"
    if st.exists():
        for f in st.rglob("*"):
            if f.is_file():
                d = out / f.relative_to(st); d.parent.mkdir(parents=True, exist_ok=True); shutil.copy(f, d)
    shutil.copy(SRC / "shared" / "loon.css", out / "loon.css")
    if s["key"]: (out / "site.js").write_text(ANDROID_JS)
    (out / "img").mkdir(exist_ok=True)
    for a in APPS.values():
        shutil.copy(SRC / "shared" / a["icon"], out / "img" / a["icon"])
    # sitemap with alternates
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for pid, alts in by_id.items():
        if pid == "404": continue
        for l, path in alts.items():
            sm.append(f"  <url><loc>{s['domain']}{path}</loc>")
            if len(alts) > 1:
                for l2, p2 in alts.items():
                    sm.append(f'    <xhtml:link rel="alternate" hreflang="{l2}" href="{s["domain"]}{p2}"/>')
                sm.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{s["domain"]}{alts.get("en", path)}"/>')
            sm.append("  </url>")
    sm.append("</urlset>")
    (out / "sitemap.xml").write_text("\n".join(sm) + "\n")
    (out / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {s['domain']}/sitemap.xml\n")
    (out / "_headers").write_text(HEADERS)
    redirects = (SRC / site / "redirects.txt")
    if redirects.exists(): shutil.copy(redirects, out / "_redirects")
    return out

HEADERS = """/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=(), interest-cohort=()
  X-Frame-Options: DENY
  Content-Security-Policy: default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self' 'sha256-JSONLD'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'; form-action 'none'
/loon.css
  Cache-Control: public, max-age=31536000, immutable
/img/*
  Cache-Control: public, max-age=604800
"""

CSS_HASH = hashlib.sha1((SRC / "shared" / "loon.css").read_bytes()).hexdigest()[:8]

def build_lugnut_overlay():
    """Lugnut keeps its pages; at deploy the browser re-skins them with this CSS and chrome."""
    out = DIST / "lugnutapp-overlay"
    if out.exists(): shutil.rmtree(out)
    out.mkdir(parents=True)
    css = (SRC / "shared" / "loon.css").read_text() + (SRC / "lugnut" / "lugnut.css").read_text()
    (out / "site.css").write_text(css)
    (out / "site.js").write_text(ANDROID_JS)
    # Lugnut pages keep a small inline script (copy button), so allow inline but block outside scripts such as analytics beacons.
    (out / "_headers").write_text(HEADERS.replace("script-src 'self'", "script-src 'self' 'unsafe-inline'"))
    shutil.copy(SRC / "shared" / "lugnut-icon.svg", out / "lugnut-icon.svg")
    for a in APPS.values():
        shutil.copy(SRC / "shared" / a["icon"], out / a["icon"])
    chrome = {"cssHash": hashlib.sha1(css.encode()).hexdigest()[:8], "email": EMAIL, "names": LANG_NAMES, "htmlLang": HTML_LANG, "globe": GLOBE, "langs": {}}
    status = {"en": "Coming soon to the App Store and Google Play", "fr": "Bientôt sur l’App Store et Google Play",
              "es": "Muy pronto en App Store y Google Play", "de": "Bald im App Store und bei Google Play"}
    titles = {"en": "Lugnut – Car maintenance log & service reminders", "fr": "Lugnut – Carnet d’entretien auto et rappels",
              "es": "Lugnut – Bitácora de mantenimiento y recordatorios", "de": "Lugnut – Digitales Scheckheft und Wartungserinnerungen"}
    for lang in ["en", "fr", "es", "de"]:
        t = T[lang]
        legal = [(t["access"], studio_link(lang, "access")), (t["notice"], studio_link(lang, "notice"))]
        studio_items = [(a["name"], a["url"] + ("/fr/" if lang == "fr" else "/")) for a in APPS.values()]
        about = studio_link(lang, "about")
        chrome["langs"][lang] = {
            "skip": t["skip"], "language": t["language"], "legalTitle": t["legal"], "app": t["app"],
            "legalLinks": legal, "studioItems": studio_items, "about": [t["about"], about],
            "fineprint": [f'© {YEAR} Loon Softworks · Ontario, Canada · <a href="mailto:{EMAIL}">{EMAIL}</a>', esc(t["nocookies"]), esc(t["tm"])],
            "android": [t["android_app"].format(app="Lugnut"), t["android_cta"], t["android_subject"].format(app="Lugnut")],
            "status": status[lang], "homeTitle": titles[lang], "privacy": t["privacy"], "terms": t["terms"],
        }
    (out / "chrome.json").write_text(json.dumps(chrome, ensure_ascii=False, indent=1))
    return out

def main():
    global HEADERS
    # JSON-LD blocks are data, not scripts, so CSP script-src doesn't apply; drop the placeholder hash.
    HEADERS = HEADERS.replace(" 'sha256-JSONLD'", "")
    DIST.mkdir(exist_ok=True)
    manifest = {}
    for site in SITES:
        out = build_site(site)
        manifest[SITES[site]["project"]] = sorted(str(f.relative_to(out)) for f in out.rglob("*") if f.is_file())
    lo = build_lugnut_overlay()
    manifest["lugnutapp-overlay"] = sorted(str(f.relative_to(lo)) for f in lo.rglob("*") if f.is_file())
    # remote assets fetched by the browser at deploy time (sources the workspace can't reach)
    manifest["_remote"] = json.loads((SRC / "remote-assets.json").read_text())
    (DIST / "manifest.json").write_text(json.dumps(manifest, indent=1))
    print({k: len(v) for k, v in manifest.items()})

if __name__ == "__main__":
    main()
