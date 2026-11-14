#!/usr/bin/env python3
"""Build the whole Prestige Enterprises site (English at /, Hindi at /hi/, Marathi at /mr/).

    python3 scripts/make_images.py     # only when you want to regenerate the artwork
    python3 scripts/build.py

Content lives in scripts/ui.py (home + interface), cities_*.py and posts_*.py. Business details live in
scripts/config.py. The build asserts that Hindi and Marathi mirror the English structure, so a missing
translation fails loudly instead of shipping a half-translated page.
"""
import hashlib
import html
import json
import os
import shutil
import sys
import urllib.parse
from email.utils import format_datetime
import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import config as C  # noqa: E402
import cities_en, cities_hi, cities_mr, posts_en, posts_hi, posts_mr  # noqa: E402,E401
from ui import HOME, UI  # noqa: E402

LANGS = C.LANGS
CIT = {'en': cities_en.CITIES, 'hi': cities_hi.CITIES, 'mr': cities_mr.CITIES}
PST = {'en': posts_en.POSTS, 'hi': posts_hi.POSTS, 'mr': posts_mr.POSTS}
MENU, NEAR, ORDER, FEATURED = cities_en.MENU, cities_en.NEAR, posts_en.ORDER, posts_en.FEATURED
CITY_SLUGS = [s for _, slugs in MENU for s in slugs]
DATE_FMT = {'en': 'October 29, 2026', 'hi': '29 अक्टूबर 2026', 'mr': '29 ऑक्टोबर 2026'}

# URLs of the old Spanish / Bay Area site: redirected so no inbound link dies.
OLD_BLOG = ['intercambio-1031-california', 'condominio-o-casa', 'comprar-casa-con-itin-california', 'casa-para-rentar-inversion-bay-area',
            'que-hace-un-realtor-cuanto-cobra-california', 'es-buen-momento-para-comprar-casa-2026', 'fix-and-flip-bay-area-regla-70',
            'programas-primera-casa-california', 'rentar-o-comprar-casa-bay-area', 'prestamo-fha-california', 'vender-y-comprar-casa-al-mismo-tiempo',
            'adu-california', 'cuanto-cuesta-vender-casa-california', 'cuanto-ganar-para-comprar-casa-bay-area', 'preaprobacion-hipotecaria',
            'comprar-casa-trabajo-por-cuenta-propia', 'casa-heredada-california', 'costos-de-cierre-comprador-california',
            'cuanto-enganche-para-comprar-casa-california', 'atrasado-en-hipoteca-foreclosure-california', 'vender-casa-rapido-en-efectivo',
            'puntaje-de-credito-para-comprar-casa', 'casas-mas-baratas-bay-area-east-bay', 'seguro-de-casa-california', 'inspeccion-de-casa-california',
            'cuanto-vale-mi-casa-bay-area', 'oferta-ganadora-casa-bay-area', 'impuesto-a-la-propiedad-california', 'como-vender-tu-casa-bay-area',
            'pasos-para-comprar-casa-california']
OLD_AREAS = ['oakland', 'san-francisco', 'pittsburg', 'antioch', 'walnut-creek', 'concord', 'brentwood', 'richmond', 'hayward', 'san-leandro']


# ------------------------------------------------------------------ helpers

def esc(s):
    return html.escape(s, quote=False)


def attr(s):
    return html.escape(s, quote=True)


def pre(l):
    return '' if l == 'en' else '/' + l


def url(l, path):
    return pre(l) + path


def waurl(text):
    return C.WA + '?text=' + urllib.parse.quote(text)


def write(rel, s):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(s)


def fver(rel):
    with open(os.path.join(ROOT, rel), 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()[:8]


def post(l, slug):
    d = dict(PST['en'][slug])
    d.update(PST[l][slug])
    return d


def city(l, slug):
    return CIT[l][slug]


def jd(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')


# ------------------------------------------------------------------ validation

def shape(x):
    if isinstance(x, dict):
        return {k: shape(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [len(x)] + [shape(i) for i in x] if x and isinstance(x[0], (list, tuple, dict)) else [len(x)]
    return None


def validate():
    errs = []

    def same(a, b, what):
        if shape(a) != shape(b):
            errs.append(f'structure mismatch: {what}')

    for l in ('hi', 'mr'):
        if set(UI[l]) != set(UI['en']):
            errs.append(f'UI keys differ for {l}: {set(UI["en"]) ^ set(UI[l])}')
        if set(HOME[l]) != set(HOME['en']):
            errs.append(f'HOME keys differ for {l}')
        for k in HOME['en']:
            if k in HOME[l]:
                same(HOME['en'][k], HOME[l][k], f'HOME[{l}][{k}]')
        for k in UI['en']:
            if k in UI[l]:
                same(UI['en'][k], UI[l][k], f'UI[{l}][{k}]')
        if set(CIT[l]) != set(CIT['en']):
            errs.append(f'city slugs differ for {l}')
        for s in CIT['en']:
            same(CIT['en'][s], CIT[l][s], f'city {s} [{l}]')
        if set(PST[l]) != set(PST['en']):
            errs.append(f'post slugs differ for {l}')
        for s in PST['en']:
            a, b = PST['en'][s], PST[l][s]
            for k in ('title', 'desc', 'answer', 'sections', 'faq'):
                if k not in b:
                    errs.append(f'post {s} [{l}] missing {k}')
            if 'sections' in b:
                if len(a['sections']) != len(b['sections']):
                    errs.append(f'post {s} [{l}] section count')
                else:
                    for i, (x, y) in enumerate(zip(a['sections'], b['sections'])):
                        if len(x[1]) != len(y[1]) or len(x[2]) != len(y[2]):
                            errs.append(f'post {s} [{l}] section {i} paragraphs/bullets')
            if len(a['faq']) != len(b['faq']):
                errs.append(f'post {s} [{l}] faq count')
    if set(ORDER) != set(PST['en']):
        errs.append('ORDER does not match posts')
    for s, near in NEAR.items():
        for n in near:
            if n not in CIT['en']:
                errs.append(f'NEAR {s} -> unknown {n}')
    for l in LANGS:
        for s in CITY_SLUGS:
            if not os.path.exists(os.path.join(ROOT, f'img/areas/{s}.jpg')):
                errs.append(f'missing image img/areas/{s}.jpg')
        for s in ORDER:
            if not os.path.exists(os.path.join(ROOT, f'img/blog/{s}.jpg')):
                errs.append(f'missing image img/blog/{s}.jpg')
        if len(CIT[l]['kalyan']['desc']) > 175:
            errs.append(f'long city desc {l}')
    if errs:
        sys.exit('BUILD FAILED:\n  ' + '\n  '.join(errs))


# ------------------------------------------------------------------ svg bits

def svg(inner, cls='', vb='0 0 24 24'):
    return f'<svg class="{cls}" viewBox="{vb}" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{inner}</svg>'


I = {
    'chat': svg('<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>'),
    'caret': svg('<path d="M6 9l6 6 6-6"/>', 'nav-dd-caret'),
    'arrow': svg('<path d="M5 12h14M13 6l6 6-6 6"/>'),
    'phone': svg('<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>'),
    'zoom': svg('<circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35M11 8v6M8 11h6"/>'),
}
SVC_ICONS = [
    svg('<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/>'),
    svg('<path d="M20.6 13.4l-7.2 7.2a2 2 0 0 1-2.8 0L2 12V2h10l8.6 8.6a2 2 0 0 1 0 2.8z"/><path d="M7 7h.01"/>'),
    svg('<path d="M21 2l-2 2m-7.6 7.6a5.5 5.5 0 1 1-7.8 7.8 5.5 5.5 0 0 1 7.8-7.8zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4"/>'),
    svg('<path d="M23 6l-9.5 9.5-5-5L1 18"/><path d="M17 6h6v6"/>'),
    svg('<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/>'),
    svg('<path d="M19 5L5 19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/>'),
]


# ------------------------------------------------------------------ shell

def agent_ld(l):
    return {
        '@type': 'RealEstateAgent', '@id': C.SITE + '/#agent', 'name': C.BRAND, 'url': C.SITE + '/',
        'image': C.SITE + '/img/logo.png', 'logo': C.SITE + '/img/logo.png', 'telephone': C.PHONE_TEL, 'email': C.EMAIL,
        'description': HOME[l]['jsonld_desc'],
        'address': {'@type': 'PostalAddress', 'streetAddress': C.STREET, 'addressLocality': C.LOCALITY,
                    'addressRegion': C.REGION, 'postalCode': C.POSTAL, 'addressCountry': C.COUNTRY},
        'hasMap': C.MAPS_URL,
        'areaServed': [{'@type': 'City', 'name': f"{cities_en.CITIES[s]['name']}, Maharashtra"} for s in CITY_SLUGS]
                      + [{'@type': 'AdministrativeArea', 'name': 'Mumbai Metropolitan Region'}],
        'knowsLanguage': ['en', 'hi', 'mr'],
        **({'sameAs': C.SAME_AS} if C.SAME_AS else {}),
    }


def head(l, title, desc, alts, img, img_alt, ld, preload=None, og_type='website', extra=''):
    canon = C.SITE + alts[l]
    hl = ''.join(f'<link rel="alternate" hreflang="{k}" href="{C.SITE}{alts[k]}">' for k in alts)
    hl += f'<link rel="alternate" hreflang="x-default" href="{C.SITE}{alts["en"]}">'
    og_alt = ''.join(f'<meta property="og:locale:alternate" content="{C.LOCALE[k]}">' for k in alts if k != l)
    fonts = 'family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400;1,600&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700'
    if l != 'en':
        fonts += '&family=DM+Mono:wght@400;500&family=Noto+Sans+Devanagari:wght@300;400;500;600;700&family=Noto+Serif+Devanagari:wght@300;400;500;600'
    pix = ''
    if C.META_PIXEL_ID:
        pix = ("<script>!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};"
               "if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];"
               f"s.parentNode.insertBefore(t,s)}}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');fbq('init','{C.META_PIXEL_ID}');fbq('track','PageView');</script>")
    return (f'<!doctype html>\n<html lang="{C.HTML_LANG[l]}">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            f'<title>{esc(title)}</title>\n<meta name="description" content="{attr(desc)}">\n'
            '<meta name="robots" content="index, follow, max-image-preview:large">\n'
            f'<link rel="canonical" href="{canon}">\n{hl}\n<meta name="theme-color" content="#0A1525">\n'
            f'<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="{C.BRAND}">'
            f'<meta property="og:locale" content="{C.LOCALE[l]}">{og_alt}<meta property="og:url" content="{canon}">'
            f'<meta property="og:title" content="{attr(title)}"><meta property="og:description" content="{attr(desc)}">'
            f'<meta property="og:image" content="{C.SITE}{img}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
            f'<meta property="og:image:alt" content="{attr(img_alt)}"><meta name="twitter:card" content="summary_large_image">\n'
            '<link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" type="image/png" sizes="192x192" href="/icon-192.png">'
            '<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n'
            + (f'<link rel="preload" as="image" href="{preload}" fetchpriority="high">\n' if preload else '')
            + '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            f'<link href="https://fonts.googleapis.com/css2?{fonts}&display=swap" rel="stylesheet">\n'
            f'<link rel="stylesheet" href="/assets/site.css?v={fver("assets/site.css")}">\n{extra}'
            f'<script type="application/ld+json">{jd({"@context": "https://schema.org", "@graph": ld})}</script>\n{pix}</head>\n')


def nav(l, alts, solid=True):
    U, h = UI[l], url(l, '/')
    sol = SOLID if solid else ''
    cols = []
    for g, slugs in MENU:
        cols.append(f'<div class="nav-dd-col"><span class="nav-dd-h">{esc(U["grp_" + g])}</span>'
                    + ''.join(f'<a href="{url(l, "/areas/" + s + "/")}">{esc(city(l, s)["name"])}</a>' for s in slugs) + '</div>')
    langs = ''.join(f'<a href="{alts[k]}" hreflang="{k}" lang="{k}" aria-label="{attr(C.LANG_NAME[k])}"' + (' aria-current="true"' if k == l else '')
                    + f'>{C.LANG_SHORT[k]}</a>' for k in alts)
    mlinks = (f'<li><a href="{h}#home">{esc(U["home"])}</a></li>'
              f'<li><a href="{h}#about">{esc(U["nav_about"])}</a></li>'
              f'<li class="mnav-projects"><span>{esc(U["nav_projects"])}</span><span class="mnav-subhead">{esc(U["nav_plans"])}</span>'
              f'<a href="/projects/prestige-gold/">Prestige Gold</a><a href="/projects/prestige-gold/#commercial">Commercial</a>'
              f'<a href="/projects/prestige-gold/#shri-durga">Shri Durga Enterprises</a>'
              f'<a href="/projects/prestige-one/">Prestige One</a></li>'
              f'<li><a href="{h}#pricing">{esc(U["nav_pricing"])}</a></li>'
              f'<li><a href="{h}#services">{esc(U["nav_services"])}</a></li>'
              f'<li><a href="{url(l, "/blog/")}">{esc(U["nav_blog"])}</a></li>'
              f'<li><a href="{h}#contact">{esc(U["nav_contact"])}</a></li>')
    mareas = ''.join(f'<a href="{url(l, "/areas/" + s + "/")}">{esc(city(l, s)["name"])}</a>' for s in CITY_SLUGS)
    return (f'<a class="skip" href="#main">{esc(U["skip"])}</a><div id="prog"></div>\n'
            f'<nav id="nav"{SOLID if solid else ""} aria-label="{attr(U["main_menu"])}">'
            f'<a class="nav-logo" href="{h}" aria-label="{attr(C.BRAND)}"><img src="/img/new-logo.png" width="160" height="49" alt="{attr(C.BRAND)}"></a>'
            '<div class="nav-r">'
            f'<a class="nav-a" href="{h}#home">{esc(U["home"])}</a>'
            f'<a class="nav-a" href="{h}#about">{esc(U["nav_about"])}</a>'
            f'<div class="nav-dd" id="navProjects"><button class="nav-dd-btn" type="button" aria-expanded="false" aria-controls="ddProjects">{esc(U["nav_projects"])}{I["caret"]}</button>'
            f'<div class="nav-dd-menu nav-projects-menu" id="ddProjects" role="region" aria-label="{attr(U["nav_projects"])}"><div class="nav-projects-group"><span class="nav-projects-label">{esc(U["nav_plans"])}</span>'
            f'<a class="nav-projects-item" href="/projects/prestige-gold/">Prestige Gold</a>'
            f'<a class="nav-projects-item" href="/projects/prestige-gold/#commercial">Commercial</a>'
            f'<a class="nav-projects-item" href="/projects/prestige-gold/#shri-durga">Shri Durga Enterprises</a>'
            f'<a class="nav-projects-item" href="/projects/prestige-one/">Prestige One</a></div></div></div>'
            f'<a class="nav-a" href="{h}#pricing">{esc(U["nav_pricing"])}</a>'
            f'<a class="nav-a" href="{h}#services">{esc(U["nav_services"])}</a>'
            f'<div class="nav-dd" id="navAreas"><button class="nav-dd-btn" type="button" aria-expanded="false" aria-controls="ddAreas">{esc(U["nav_areas"])}{I["caret"]}</button>'
            f'<div class="nav-dd-menu" id="ddAreas" role="region" aria-label="{attr(U["menu_label"])}">{"".join(cols)}'
            f'<a class="nav-dd-all" href="{url(l, "/areas/")}">{esc(U["all_areas"])} &rarr;</a></div></div>'
            f'<a class="nav-a" href="{url(l, "/blog/")}">{esc(U["nav_blog"])}</a>'
            f'<div class="lang" role="group" aria-label="{attr(U["lang_label"])}">{langs}</div>'
            f'<a class="nav-cta" href="{h}#contact">{I["chat"]}{esc(U["nav_contact"])}</a>'
            f'<button class="nav-ham" id="navHam" type="button" aria-label="{attr(U["main_menu"])}" aria-expanded="false" aria-controls="mnav"><span></span><span></span><span></span></button>'
            '</div></nav>\n'
            f'<div class="mnav" id="mnav" hidden><ul>{mlinks}</ul><p class="mnav-h">{esc(U["nav_areas"])}</p><div class="mnav-areas">{mareas}</div>'
            f'<a class="mnav-all" href="{url(l, "/areas/")}">{esc(U["all_areas"])} &rarr;</a><br><div class="lang" role="group" aria-label="{attr(U["lang_label"])}">{langs}</div><br>'
            f'<a class="btn-wa" href="{waurl(U["wa_default"])}" target="_blank" rel="noopener" style="width:100%">{I["chat"]}<span>{esc(U["wa_btn"])}</span></a></div>\n')


def footer(l, alts):
    """Sitewide footer — same structure/copy as the homepage home-footer."""
    U, h = UI[l], url(l, '/')
    lang_keys = [k for k in ('en', 'hi', 'mr') if k in alts] or list(alts)
    langs = ''.join(
        f'<a href="{alts[k]}" hreflang="{k}" lang="{k}"'
        + (' aria-current="true"' if k == l else '')
        + f'>{C.LANG_NAME[k]}</a>'
        for k in lang_keys
    )
    rera = f'<p class="foot-rera"><strong>{esc(U["rera_label"])}:</strong> {esc(C.RERA_NO)}</p>' if C.RERA_NO else ''
    js_ver = fver('assets/site.js')
    return (
        f'<footer class="home-footer"><div class="foot-grid"><div>'
        f'<a class="foot-logo-link" href="{h}" aria-label="{attr(C.BRAND)}">'
        f'<img src="/img/logo-on-dark.png" width="210" height="70" alt="{attr(C.BRAND)}" class="foot-logo"></a>'
        f'<p>{esc(U["foot_tag"])}</p><div class="foot-langs">{langs}</div></div>'
        f'<div><h4>{esc(U["foot_links"])}</h4><ul>'
        f'<li><a href="{h}#about">{esc(U["nav_about"])}</a></li>'
        f'<li><a href="{h}#amenities">{esc(U["foot_amenities"])}</a></li>'
        f'<li><a href="{h}#plans">{esc(U["foot_plans"])}</a></li>'
        f'<li><a href="{h}#location">{esc(U["foot_location"])}</a></li>'
        f'<li><a href="{url(l, "/blog/")}">{esc(U["blog"])}</a></li>'
        f'<li><a href="{h}#contact">{esc(U["nav_contact"])}</a></li></ul></div>'
        f'<div><h4>{esc(U["foot_projects"])}</h4><ul>'
        f'<li><a href="/projects/prestige-gold/">Prestige Gold</a></li>'
        f'<li><a href="/projects/prestige-gold/#shri-durga">Shri Durga Enterprises</a></li>'
        f'<li><a href="/projects/prestige-one/">Prestige One</a></li></ul></div>'
        f'<div><h4>{esc(U["foot_contact"])}</h4><p>{esc(C.ADDRESS_LINE)}</p>'
        f'<p><a href="tel:{C.PHONE_TEL}">{C.PHONE_DISPLAY}</a><br>'
        f'<a href="mailto:{C.EMAIL}">{C.EMAIL}</a></p></div></div>'
        f'<div class="foot-legal">{rera}'
        f'<p><a href="/privacy/">{esc(U["privacy"])}</a></p>'
        f'<p>{esc(U["disclaimer"])}</p><p>{esc(U["rights"])}</p></div></footer>\n'
        f'<a class="wa" href="{waurl(U["wa_default"])}" target="_blank" rel="noopener" aria-label="{attr(U["wa_btn"])}">{I["chat"]}<span>{esc(U["float_wa"])}</span></a>\n'
        f'<script src="/assets/site.js?v={js_ver}" defer></script>\n</body>\n</html>\n'
    )


def page(l, path, alts, head_html, body):
    """Write one page; alts maps lang -> url path."""
    write((url(l, path)).lstrip('/') + 'index.html',
          head_html + '<body class="has-video-hero">\n' + nav(l, alts) + body + footer(l, alts))


def breadcrumb_ld(l, trail):
    return {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': C.SITE + u} for i, (n, u) in enumerate(trail)]}


def faq_ld(items):
    return {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in items]}


def faq_html(items, dark=False):
    return f'<div class="faq-list{" faq-dark" if dark else ""}">' + ''.join(
        f'<details class="q"><summary>{esc(q)}</summary><div class="ans">{esc(a)}</div></details>' for q, a in items) + '</div>'


def eye(txt):
    return f'<div class="eye"><span class="eye-line"></span><span class="eye-txt">{txt}</span></div>'


def crumbs(items):
    return '<ol class="crumbs">' + ''.join(f'<li>{"<a href=" + chr(34) + u + chr(34) + ">" + esc(n) + "</a>" if u else esc(n)}</li>' for n, u in items) + '</ol>'


HERO_VIDEO_BLOB = 'https://bjoj2azd7axubq1h.public.blob.vercel-storage.com/Prestige_One_Kalyan_Sales_Video_1080p%20%281%29.mp4'
HERO_VIDEO_HOST = 'https://bjoj2azd7axubq1h.public.blob.vercel-storage.com'


def video_hero(label='Prestige Enterprises residences in Kalyan West'):
    """Same homepage video hero used on every public page."""
    return (
        f'<main id="main"><section id="home" class="hero hero-video-hero site-video-hero" aria-label="{attr(label)}">'
        f'<video class="hero-video" id="heroVideo" src="{HERO_VIDEO_BLOB}" autoplay muted loop playsinline webkit-playsinline '
        'preload="auto" disablepictureinpicture disableremoteplayback x-webkit-airplay="deny" aria-hidden="true" tabindex="-1"></video>'
        '<div class="hero-video-shade" aria-hidden="true"></div></section>'
    )


def page_intro(inner):
    """Page title band under the shared video hero (former ph-c content)."""
    return f'<section class="page-intro"><div class="in page-intro-inner">{inner}</div></section>'


def video_preconnect():
    return (f'<link rel="preconnect" href="{HERO_VIDEO_HOST}" crossorigin>\n'
            f'<link rel="dns-prefetch" href="{HERO_VIDEO_HOST}">\n')


PAGES = []  # alts dicts (lang -> path); deduplicated when the sitemap is written
SOLID = ' class="solid"'
BLOG_PHOTO_VERSION = '20261114-blog-insight-photos-2'


# ------------------------------------------------------------------ home

def post_card(l, slug):
    p, U = post(l, slug), UI[l]
    return (f'<a class="card" href="{url(l, "/blog/" + slug + "/")}"><img src="/img/blog/{slug}.jpg?v={BLOG_PHOTO_VERSION}" width="800" height="420" loading="lazy" decoding="async" alt="{attr(p["title"] + " — editorial real estate photograph")}">'
            f'<div class="card-b"><span class="card-k">{esc(U["cat_" + p["cat"]])}</span><h3>{esc(p["title"])}</h3><p>{esc(p["desc"])}</p>'
            f'<span class="card-m">{esc(U["min_read"].format(n=p["read"]))}</span></div></a>')


def contact_block(l, h2, p_txt, dark_eye=True, wa_text=None):
    U, H = UI[l], HOME[l]
    brochure_wa = wa_text or (U['wa_default'] + ' Please share the Prestige Gold / Prestige One brochure.')
    return ('<section class="sec contact" id="contact"><div class="in contact-grid"><div>'
            f'{eye(esc(H["contact_eye"]))}<h2 class="dh light">{h2}</h2><p class="lead light" style="margin-top:18px">{esc(p_txt)}</p>'
            f'<ul class="contact-list"><li><b>{esc(U["addr_label"])}</b><span>{esc(C.ADDRESS_LINE)}</span></li>'
            f'<li><b>{esc(U["phone_label"])}</b><a href="tel:{C.PHONE_TEL}">{C.PHONE_DISPLAY}</a></li>'
            f'<li><b>WhatsApp</b><a href="{waurl(wa_text or U["wa_default"])}" target="_blank" rel="noopener">{C.PHONE_DISPLAY}</a></li>'
            f'<li><b>{esc(U["email_label"])}</b><a href="mailto:{C.EMAIL}">{C.EMAIL}</a></li></ul>'
            f'<div class="cta-row"><a class="btn-g" href="{waurl(brochure_wa)}" target="_blank" rel="noopener"><span>{esc(U["brochure_btn"])}</span></a>'
            f'<a class="btn-wa" href="{waurl(wa_text or U["wa_default"])}" target="_blank" rel="noopener">{I["chat"]}<span>{esc(U["wa_btn"])}</span></a>'
            f'<a class="btn-o" href="tel:{C.PHONE_TEL}">{I["phone"]}<span>{esc(U["call_btn"])}</span></a></div></div>'
            f'<div><iframe class="map" src="{C.MAPS_EMBED}" title="{attr(C.ADDRESS_LINE)}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>'
            f'<p style="margin:12px 0 0"><a class="btn-o" href="{C.MAPS_URL}" target="_blank" rel="noopener">{esc(U["open_maps"])} {I["arrow"]}</a></p></div></div></section>\n')


def build_home(l):
    U, H = UI[l], HOME[l]
    stat_class = lambda label: 'stat stat-services' if label in ('Residential & Commercial', 'रेज़िडेंशियल और कमर्शियल', 'रेसिडेन्शियल आणि कमर्शियल') else 'stat'
    alts = {k: url(k, '/') for k in LANGS}
    hero_imgs = [
        ('hero-day.jpg', 'Prestige Gold Kalyan - Modern Architecture Tower (Day View)'),
        ('hero-night.jpg', 'Prestige Gold Kalyan - Evening Ambiance (Night View)'),
        ('hero-iso-2bhk.jpg', 'Prestige Gold - 2 BHK 3D Isometric View'),
        ('hero-iso-1bhk.jpg', 'Prestige Gold - 1 BHK 3D Isometric View'),
        ('hero-plan-1bhk.jpg', 'Prestige Gold - 1 BHK Architectural Floor Plan'),
    ]
    slides = ''.join(f'<div class="hero-slide{" active" if i == 0 else ""}"><img src="/img/{n}" width="1920" height="1080" alt="{attr(alt)}"'
                     + (' fetchpriority="high"' if i == 0 else ' loading="lazy"') + '></div>' for i, (n, alt) in enumerate(hero_imgs))
    dots = ''.join(f'<button class="hc-dot{" on" if i == 0 else ""}" type="button" aria-label="{i + 1}"></button>' for i in range(len(hero_imgs)))
    hero = ('<main id="main"><section id="home" class="hero"><div class="hero-slides">' + slides + '</div><div class="hero-veil"></div><div class="hero-c">'
            f'<div class="hero-tag"><span class="hero-dot"></span>{esc(H["tag"])}</div>'
            '<h1 class="hero-name">Prestige<b>Enterprises</b></h1>'
            f'<div class="hero-tagline-wrap"><div class="hero-tagline">{"".join(f"<span>{esc(t)}</span>" for t in H["taglines"])}</div></div>'
            f'<div class="hero-pills">{"".join(f"<span class=hero-pill>{esc(p)}</span>" for p in H["pills"])}</div>'
            f'<div class="hero-btns"><a class="btn-g" href="{waurl(U["wa_default"])}" target="_blank" rel="noopener">{I["chat"]}<span>{esc(H["btn1"])}</span></a>'
            f'<a class="btn-o" href="{url(l, "/areas/")}"><span>{esc(H["btn2"])}</span>{I["arrow"]}</a></div></div>'
            f'<div class="hero-dots">{dots}</div></section>\n')
    about = ('<section class="sec" id="about"><div class="in about-grid"><div>' + eye(esc(H['about_eye'])) + f'<h2 class="dh">{H["about_h"]}</h2>'
             f'<div class="about-body" style="margin-top:30px">{"".join(f"<p>{esc(p)}</p>" for p in H["about"])}</div>'
             f'<div class="tags">{"".join(f"<span class=tag>{esc(t)}</span>" for t in H["tags"])}</div>'
             f'</div>'
             f'<div><div class="about-photo"><img src="/img/about.jpg" width="900" height="1125" loading="lazy" alt="{attr(H["about_alt"])}"></div>'
             f'<div class="about-quote"><p>{esc(H["quote"])}</p><cite>{esc(H["quote_by"])}</cite></div></div></div></section>\n')
    projects = (
        '<section class="sec project-showcase" id="projects"><div class="in project-showcase-grid">'
        '<div class="project-showcase-media"><img src="/img/prestige-tower-day.jpg" width="1200" height="900" loading="lazy" alt="Prestige Gold tower, Kalyan West"></div>'
        '<div class="project-showcase-copy"><div class="eye"><span class="eye-line"></span><span class="eye-txt">Prestige Gold</span></div>'
        '<h2 class="dh">Prime location · <em>1, 2 & 3 BHK</em></h2>'
        '<p class="lead">Residential and commercial. Luxury amenities, modern security, 3 BHK across the complete site from ₹1.40 Cr (140 L).</p>'
        '<a class="btn-o dark" href="/projects/prestige-gold/">Prestige Gold</a></div></div>'
        '<div class="in project-showcase-grid" style="margin-top:48px"><div class="project-showcase-media">'
        '<img src="/img/Prestige%20One%20Tower%20in%20Daylight.png" width="991" height="1536" loading="lazy" alt="Prestige One tower"></div>'
        '<div class="project-showcase-copy"><div class="eye"><span class="eye-line"></span><span class="eye-txt">Prestige One</span></div>'
        '<h2 class="dh">Elite <em>5 BHK</em> residences</h2>'
        '<p class="lead">Spacious layouts. Configuration on request — pricing shared privately with serious buyers.</p>'
        '<a class="btn-o dark" href="/projects/prestige-one/">Prestige One</a></div></div></section>\n'
    )
    def plan_card(p):
        if p[3]:
            visual = (f'<div class="plan-img-wrap" data-full="{p[3]}" data-title="{attr(p[1])}">'
                      f'<img src="{p[3]}" width="666" height="375" loading="lazy" alt="{attr(p[1])}">'
                      f'<span class="plan-zoom-hint">{I["zoom"]}<span>{esc(H["plans_zoom"])}</span></span></div>')
        else:
            visual = (f'<div class="plan-img-wrap plan-request-wrap" role="img" aria-label="{attr(H["plans_request"])}">'
                      f'<div class="plan-request-box"><span>{esc(H["plans_request"])}</span></div></div>')
        return (f'<div class="plan-card">'
                f'<div class="plan-card-hd"><span class="plan-badge">{esc(p[0])}</span><h3>{esc(p[1])}</h3><p>{esc(p[2])}</p></div>'
                f'{visual}'
                f'<div class="plan-card-ft">'
                f'<a class="btn-wa-sm" href="{waurl(U["wa_default"] + " (" + p[0] + ")")}" target="_blank" rel="noopener">'
                f'{I["chat"]}<span>{esc(H["plans_enquire"])}</span></a></div></div>')
    p_cards = ''.join(plan_card(p) for p in H['plans'])
    plans = (f'<section class="sec plans dark-bg" id="plans"><div class="in">'
             f'<div class="plans-hd"><div>{eye(esc(H["plans_eye"]))}<h2 class="dh light">{H["plans_h"]}</h2></div>'
             f'<p class="lead light" style="margin-top:16px;max-width:680px">{esc(H["plans_p"])}</p></div>'
             f'<div class="plans-grid">{p_cards}</div>'
             f'</div></section>\n')
    svc = ('<section class="sec services" id="services"><div class="in">' + eye(esc(H['svc_eye'])) + f'<h2 class="dh">{H["svc_h"]}</h2><div class="svc-grid">'
           + ''.join(f'<div class="svc"><div class="svc-ic">{SVC_ICONS[i]}</div><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for i, (t, d) in enumerate(H['svc']))
           + f'</div></div></section>\n')
    proc = ('<section class="sec dark-bg" id="process"><div class="in">' + eye(esc(H['proc_eye'])) + f'<h2 class="dh light">{H["proc_h"]}</h2><div class="proc">'
            + ''.join(f'<div class="proc-step"><span class="proc-n">{i + 1:02d}</span><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for i, (t, d) in enumerate(H['proc']))
            + f'</div></div></section>\n')
    pins = ''.join(f'<a class="area-pin" href="{url(l, "/areas/" + s + "/")}"><i></i>{esc(city(l, s)["name"])}</a>' for s in CITY_SLUGS)
    areas = ('<section class="sec" id="areas"><div class="in">' + eye(esc(H['areas_eye'])) + f'<h2 class="dh">{H["areas_h"]}</h2>'
             f'<p class="lead" style="margin-top:20px">{esc(H["areas_p"])}</p><div class="area-pins">{pins}</div>'
             f'</div></section>\n')
    guides = ('<section class="sec" id="guides" style="background:#fff"><div class="in">' + eye(esc(H['guides_eye'])) + f'<h2 class="dh">{H["guides_h"]}</h2>'
              f'<div class="cards">{"".join(post_card(l, s) for s in FEATURED)}</div>'
              f'<p style="margin-top:36px"><a class="btn-o dark" href="{url(l, "/blog/")}"><span>{esc(H["guides_btn"])}</span>{I["arrow"]}</a></p></div></section>\n')
    contact = contact_block(l, H['contact_h'], H['contact_p'])
    ld = [agent_ld(l), {'@type': 'WebSite', '@id': C.SITE + '/#website', 'url': C.SITE + '/', 'name': C.BRAND, 'inLanguage': ['en-IN', 'hi-IN', 'mr-IN'],
                        'publisher': {'@id': C.SITE + '/#agent'}}]
    h = head(l, H['title'], H['desc'], alts, '/img/og-default.jpg', C.BRAND, ld, preload='/img/hero-day.jpg')
    page(l, '/', alts, h, hero + about + projects + plans + svc + areas + guides + contact + '</main>\n')
    PAGES.append(alts)



# ------------------------------------------------------------------ Prestige Gold project page

GOLD_WA = '918446652600'


def build_prestige_gold():
    path = '/projects/prestige-gold/'
    nav_alts = {k: url(k, '/') for k in LANGS}
    seo_alts = {'en': path}
    title = 'Prestige Gold | 1, 2 & 3 BHK + Commercial | Kalyan West'
    desc = 'Prestige Gold — prime Kalyan West address. 1, 2 & 3 BHK from ₹55 Lakh; 3 BHK complete site from ₹1.40 Cr (140 L). RERA area 999.4–1,001.4 sq. ft. Commercial space. Site visits open.'
    wa_text = 'Hello, I would like the Prestige Gold brochure, floor plans and current 3 BHK availability in Kalyan West.'
    wa_link = 'https://wa.me/' + GOLD_WA + '?text=' + urllib.parse.quote(wa_text)
    commercial_wa = ('https://wa.me/' + GOLD_WA + '?text=' +
                     urllib.parse.quote('Hello, I would like the Prestige Gold commercial brochure for retail and office space in Kalyan West. Please share availability, sizes and pricing.'))
    units = [
        ('1 BHK', '₹55,00,000', '404–519 sq. ft.', 'Compact elite layout — living, bedroom, kitchen provision, balcony.'),
        ('2 BHK', '₹75,00,000', '577–721 sq. ft.', 'Spacious living and dining, two bedrooms, balcony, modern finishes.'),
        ('3 BHK', '₹1,40,00,000', '999.4–1,001.4 sq. ft.', 'Available across the complete site. Grand living, master suite, balconies, pooja room.'),
    ]
    commercial = (
        '<article class="pg-unit" id="commercial"><span class="pg-unit-k">COMMERCIAL</span><h3>Retail &amp; office</h3>'
        '<p class="pg-price">On request</p><p class="pg-area">Ground &amp; podium levels</p>'
        '<p>Prime frontage at Prestige Gold. High footfall Kalyan West corridor. Request the commercial brochure.</p>'
        f'<a class="btn-g" href="{commercial_wa}" target="_blank" rel="noopener">Request commercial brochure</a></article>'
    )
    unit_cards = ''.join(
        f'<article class="pg-unit"><span class="pg-unit-k">RESIDENTIAL CONFIGURATION</span><h3>{esc(name)}</h3>'
        f'<p class="pg-price">{esc(price)}</p><p class="pg-area">RERA area · {esc(area)}</p>'
        f'<p>{esc(summary)}</p><a class="btn-g" href="https://wa.me/{GOLD_WA}?text={urllib.parse.quote("Hello, I would like details for Prestige Gold " + name + " in Kalyan West. Please share brochure, floor plans, availability and pricing.")}" target="_blank" rel="noopener">Enquire for {esc(name)}</a></article>'
        for name, price, area, summary in units)
    amenity_tiles = [
        ('swimming-pool', 'Swimming pool'),
        ('cricket', 'Cricket practice pitch'),
        ('games-lounge', 'Games lounge'),
        ('library', 'Reading library'),
        ('mini-theatre', 'Mini theatre'),
        ('pickleball', 'Pickleball court'),
        ('residents-lounge', 'Residents’ lounge'),
        ('fitness-centre', 'Fitness centre'),
    ]
    amenity_cards = ''.join(
        f'<figure class="amen-tile"><img src="/img/amenities/{slug}.webp" width="456" height="384" loading="lazy" alt="{esc(name)}">'
        f'<figcaption>{esc(name)}</figcaption></figure>'
        for slug, name in amenity_tiles
    )
    gallery_items = [
        ('/img/prestige-tower-day.jpg', 1400, 900, 'Prestige Gold exterior, day view', 'Day view'),
        ('/img/prestige-tower-night.jpg', 1400, 900, 'Prestige Gold exterior, night view', 'Night view'),
        ('/img/hero-day.jpg', 1920, 1080, 'Prestige Gold residential tower in Kalyan West', 'Tower view'),
        ('/img/amenities/rooftop-garden.webp', 1200, 800, 'Rooftop garden amenity at Prestige Gold', 'Rooftop garden'),
        ('/img/amenities/swimming-pool.webp', 912, 768, 'Swimming pool at Prestige Gold', 'Swimming pool'),
        ('/img/amenities/fitness-centre.webp', 912, 768, 'Fitness centre at Prestige Gold', 'Fitness centre'),
    ]
    gallery_figures = ''.join(
        f'<figure><img src="{src}" width="{w}" height="{h}" loading="lazy" alt="{esc(alt)}"><figcaption>{esc(cap)}</figcaption></figure>'
        for src, w, h, alt, cap in gallery_items
    )
    hero = video_hero('Prestige Gold — prime Kalyan West') + page_intro(
        crumbs([(UI['en']['home'], '/'), ('Projects', None), ('Plans', None), ('Prestige Gold', None)]) +
        eye('PRIME KALYAN WEST · RESIDENTIAL + COMMERCIAL') +
        '<h1>Prestige <b>Gold</b></h1>'
        '<p class="ph-lead">Elite living in a full residential project — luxury amenities, modern security, 1, 2 &amp; 3 BHK homes and commercial space.</p>'
        '<div class="pg-hero-facts"><span>1, 2 &amp; 3 BHK</span><span>Commercial</span><span>Shri Durga Enterprises</span><span>G + 5 floors</span><span>Expected possession June 2027</span></div>'
        f'<div class="section-cta"><a class="cta-enq" href="{wa_link}" target="_blank" rel="noopener">Request brochure</a><a class="cta-wa" href="tel:+' + GOLD_WA + '">Call +91 84466 52600</a></div>'
    )
    overview = (
        '<section class="sec pg-overview"><div class="in pg-overview-grid"><div>'
        + eye('THE PROJECT') + '<h2 class="dh">Full residential · <em>prime location</em></h2>'
        '<p class="lead">A landmark mixed-use address: vastu-friendly homes, rooftop leisure, power backup and smart security — built for elite everyday living.</p>'
        '<dl class="pg-facts"><div><dt>Project type</dt><dd>Residential + Commercial</dd></div><div><dt>Configurations</dt><dd>1, 2 &amp; 3 BHK + Commercial</dd></div>'
        '<div><dt>Expected possession</dt><dd>June 2027</dd></div><div><dt>Construction</dt><dd>Brickwork &amp; internal works complete</dd></div>'
        '<div><dt>Sample flat</dt><dd>Ready for visits</dd></div></dl>'
        '<p class="pg-note"><strong>Nearby:</strong> Khadakpada, Godrej Hill, KDMC services, Kalyan West station, schools and daily retail.</p>'
        '</div><figure class="pg-overview-image"><img src="/img/prestige-tower-night.jpg" width="1200" height="900" loading="lazy" alt="Prestige Gold tower at night"><figcaption>Prestige Gold · Kalyan West</figcaption></figure></div></section>'
    )
    pricing = (
        '<section class="sec pg-pricing" id="pg-configurations"><div class="in">'
        + eye('CONFIGURATIONS') + '<h2 class="dh">1, 2 &amp; 3 BHK · <em>plus commercial</em></h2>'
        '<p class="lead">3 BHK available across the complete site from ₹1.40 Cr (140 L). RERA area 999.4–1,001.4 sq. ft. Commercial is the fourth option — ground &amp; podium retail and office.</p>'
        f'<div class="cards four pg-units">{unit_cards}{commercial}</div>'
        '<p class="pg-note">Indicative starting prices. Taxes, parking and final agreement values confirmed in writing at booking.</p>'
        '</div></section>'
    )
    floorplans = (
        '<section class="sec pg-floorplans"><div class="in">'
        + eye('LAYOUT PREVIEW') + '<h2 class="dh">Explore the <em>floor plans</em></h2>'
        '<p class="lead">Indicative visual references. Request the latest approved, unit-specific floor plan and RERA carpet-area statement before booking.</p>'
        '<div class="pg-plan-grid"><figure><img src="/img/prestige-plan-1bhk.png" width="1000" height="760" loading="lazy" alt="Prestige Gold 1 BHK floor plan"><figcaption><b>1 BHK</b><span>Indicative layout</span></figcaption></figure>'
        '<figure><img src="/img/prestige-iso-2bhk.png" width="1000" height="760" loading="lazy" alt="Prestige Gold 2 BHK isometric layout"><figcaption><b>2 BHK</b><span>Isometric layout reference</span></figcaption></figure>'
        '<figure><img src="/img/prestige-iso-1bhk.png" width="1000" height="760" loading="lazy" alt="Prestige Gold 1 BHK isometric layout"><figcaption><b>1 BHK</b><span>Isometric layout reference</span></figcaption></figure></div>'
        '<p class="pg-note">3, 4 and 5 BHK drawings and additional unit-specific plans can be requested from the project sales team.</p>'
        '</div></section>'
    )
    gallery = (
        '<section class="sec pg-gallery" id="gallery"><div class="in">'
        + eye('PROJECT GALLERY') + '<h2 class="dh">A closer look at <em>Prestige Gold</em></h2>'
        '<p class="lead">Tower views, leisure spaces and everyday amenities from the Prestige Gold community.</p>'
        f'<div class="pg-gallery-grid pg-gallery-grid-rich">{gallery_figures}</div>'
        '</div></section>'
    )
    amenities_section = (
        '<section class="sec home-amenities pg-amenities-visual" id="amenities"><div class="in">'
        + eye('AMENITIES') + '<h2 class="dh">Leisure, wellness and play, <em>right at home</em></h2>'
        '<p class="lead">Spaces designed for unhurried mornings, active evenings and weekends with family, all within the community.</p>'
        f'<div class="amen-grid" style="margin-top:36px">{amenity_cards}</div>'
        '</div></section>'
    )
    progress = (
        '<section class="sec pg-progress" id="construction"><div class="in pg-progress-layout">'
        '<div class="pg-progress-left">'
        + eye('CONSTRUCTION UPDATE') + '<h2 class="dh">Built with <em>transparency</em></h2>'
        '<article class="pg-status-card">'
        '<p class="pg-status-kicker">Current site status</p>'
        '<p class="pg-status-pct">70% <span>Completed</span></p>'
        '<p class="pg-status-copy">G + 5 floor development is advancing on schedule. Sample flat is ready for live walkthrough and quality checks.</p>'
        '</article>'
        '<article class="pg-status-card pg-status-meter-card">'
        '<div class="pg-status-meter-top"><div><p class="pg-status-kicker">Project completion</p>'
        '<p class="pg-status-sub">Brickwork complete · finishes underway</p></div>'
        '<div class="pg-ring" role="img" aria-label="70 percent complete" style="--pct:70">'
        '<svg viewBox="0 0 36 36" aria-hidden="true"><path class="pg-ring-bg" d="M18 2.5a15.5 15.5 0 1 1 0 31 15.5 15.5 0 1 1 0-31"/><path class="pg-ring-fg" pathLength="100" d="M18 2.5a15.5 15.5 0 1 1 0 31 15.5 15.5 0 1 1 0-31"/></svg>'
        '<span>70%</span></div></div>'
        '<div class="pg-seg-track" aria-hidden="true"><i class="done"></i><i class="done"></i><i class="done"></i><i class="live"></i><i></i><i></i></div>'
        '<ul class="pg-seg-legend"><li><span class="dot done"></span>Completed</li><li><span class="dot live"></span>In progress</li><li><span class="dot"></span>Upcoming</li></ul>'
        '</article></div>'
        '<div class="pg-progress-right" role="list">'
        '<details class="pg-stage is-done" open><summary><span class="pg-stage-mark" aria-hidden="true">✓</span>'
        '<span class="pg-stage-body"><b>01</b><strong>Land, legal &amp; RERA registration</strong></span>'
        '<span class="pg-stage-tag done">Completed</span></summary>'
        '<p>Approvals and registration formalities for Prestige Gold are complete.</p></details>'
        '<details class="pg-stage is-done" open><summary><span class="pg-stage-mark" aria-hidden="true">✓</span>'
        '<span class="pg-stage-body"><b>02</b><strong>Foundation &amp; excavation</strong></span>'
        '<span class="pg-stage-tag done">Completed</span></summary>'
        '<p>Foundation and excavation works are finished on site.</p></details>'
        '<details class="pg-stage is-done" open><summary><span class="pg-stage-mark" aria-hidden="true">✓</span>'
        '<span class="pg-stage-body"><b>03</b><strong>RCC structure progress</strong></span>'
        '<span class="pg-stage-tag done">Completed</span></summary>'
        '<p>Structural RCC for the G + 5 development is complete.</p></details>'
        '<details class="pg-stage is-done" open><summary><span class="pg-stage-mark" aria-hidden="true">✓</span>'
        '<span class="pg-stage-body"><b>04</b><strong>Brickwork &amp; internal works</strong></span>'
        '<span class="pg-stage-tag done">Completed</span></summary>'
        '<p>Walls, ducts and internal masonry are done across the towers.</p></details>'
        '<details class="pg-stage is-live" open><summary><span class="pg-stage-mark" aria-hidden="true"></span>'
        '<span class="pg-stage-body"><b>05</b><strong>Finishes &amp; fittings</strong></span>'
        '<span class="pg-stage-tag live">In progress</span></summary>'
        '<p>Plaster, tiling, MEP and fittings are underway toward handover.</p></details>'
        '<details class="pg-stage is-next"><summary><span class="pg-stage-mark" aria-hidden="true"></span>'
        '<span class="pg-stage-body"><b>06</b><strong>OC, possession &amp; handover</strong></span>'
        '<span class="pg-stage-tag">Expected June 2027</span></summary>'
        '<p>Possession targeted for June 2027, subject to final approvals.</p></details>'
        '</div></div></section>'
    )
    location = (
        '<section class="sec pg-location"><div class="in pg-location-grid"><div>'
        + eye('LOCATION ADVANTAGE') + '<h2 class="dh">Connected to <em>Kalyan West</em></h2>'
        '<p class="lead">The project is located in Kalyan West, Thane, Maharashtra – 421301. Contact the sales team for the exact site pin, route guidance and a scheduled walkthrough.</p>'
        '<p class="pg-address"><b>Prestige Gold</b><br>Kalyan West, Thane<br>Maharashtra – 421301</p>'
        '<a class="btn-o" href="https://www.google.com/maps/search/?api=1&amp;query=Prestige+Gold+Kalyan+West+Thane+421301" target="_blank" rel="noopener">Open location in Google Maps ↗</a>'
        '</div><div class="pg-map-card"><span>VISIT THE PROJECT</span><h3>See the location and experience the sample flat.</h3><p>Site visits are arranged through the project sales team.</p>'
        f'<a class="btn-g" href="{wa_link}" target="_blank" rel="noopener">Arrange a site visit</a></div></div></section>'
    )
    shri_wa = ('https://wa.me/' + GOLD_WA + '?text=' +
               urllib.parse.quote('Hello, I am interested in Shri Durga Enterprises at Prestige Gold. Please share project details, floor plans, availability and cost sheet.'))
    shri_durga = (
        '<section class="sec pg-overview" id="shri-durga"><div class="in pg-overview-grid"><div>'
        + eye('PART OF PRESTIGE GOLD') + '<h2 class="dh">Shri Durga <em>Enterprises</em></h2>'
        '<p class="lead">Shri Durga Enterprises is offered as part of Prestige Gold — the same Kalyan West address, sales team and enquiry flow for verified layouts, pricing and site visits.</p>'
        '<p>Request the latest approved floor plans, unit configurations, carpet-area details and a dated cost sheet. Confirm MahaRERA registration and project documents independently before booking or payment.</p>'
        '<div class="cards pg-units" style="margin-top:28px;grid-template-columns:1fr">'
        '<article class="pg-unit"><span class="pg-unit-k">SHRI DURGA · PRESTIGE GOLD</span><h3>Enquire here</h3>'
        '<p>Floor plans, cost sheet and visit coordination for Shri Durga are handled with Prestige Gold.</p>'
        f'<a class="btn-g" href="{shri_wa}" target="_blank" rel="noopener">Enquire about Shri Durga</a></article></div>'
        '</div><figure class="pg-overview-image pg-image-full"><img src="/img/shri%20durga.png" width="992" height="1536" loading="lazy" alt="Shri Durga Enterprises tower, part of Prestige Gold">'
        '<figcaption>Shri Durga Enterprises · Prestige Gold</figcaption></figure></div></section>'
    )
    contact = (
        '<section class="sec pg-contact" id="pg-enquire"><div class="in pg-contact-inner">'
        + eye('NEXT STEP') + '<h2 class="dh">Experience Prestige <em>Gold</em></h2>'
        '<p class="lead">Ask for current availability, unit-wise pricing, approved floor plans and a guided site visit — including Shri Durga Enterprises.</p>'
        '<div class="section-cta"><a class="cta-enq" href="' + wa_link + '" target="_blank" rel="noopener">Request brochure</a>'
        '<a class="cta-wa" href="tel:+' + GOLD_WA + '">Call +91 84466 52600</a></div>'
        '<p class="pg-contact-email">Our team is ready to assist.</p>'
        '</div></section></main>'
    )
    body = hero + overview + pricing + floorplans + gallery + amenities_section + progress + location + shri_durga + contact
    ld = [agent_ld('en'), breadcrumb_ld('en', [(UI['en']['home'], url('en', '/')), ('Prestige Gold', path)])]
    html = head('en', title, desc, seo_alts, '/img/prestige-tower-day.jpg', 'Prestige Gold project in Kalyan West', ld, extra=video_preconnect())
    write(path.lstrip('/') + 'index.html', html + '<body class="has-video-hero">\n' + nav('en', nav_alts) + body + footer('en', nav_alts))
    PAGES.append(seo_alts)


def build_prestige_one():
    path = '/projects/prestige-one/'
    nav_alts = {k: url(k, '/') for k in LANGS}
    seo_alts = {'en': path}
    title = 'Prestige One | 5 BHK Elite Residences | Kalyan'
    desc = 'Prestige One — 5 BHK luxury homes in Kalyan. Spacious layouts from 999.4 & 1001.4 sq. ft. No public price list. Request brochure and site visit.'
    wa_text = 'Hello, I am interested in Prestige One 5 BHK in Kalyan. Please share the brochure and floor plans.'
    wa_link = waurl(wa_text)
    hero = video_hero('Prestige One tower') + page_intro(
        crumbs([(UI['en']['home'], '/'), ('Projects', None), ('Plans', None), ('Prestige One', None)]) +
        eye('KALYAN · PRESTIGE ONE') +
        '<h1>Prestige <b>One</b></h1>'
        '<p class="ph-lead">Elite 5 BHK living — prime location, modern amenities, luxury finishes and integrated security.</p>'
        '<div class="pg-hero-facts"><span>5 BHK</span><span>999.4 &amp; 1001.4 sq. ft.</span><span>Pricing on request</span><span>Our team is ready to assist</span></div>'
        f'<div class="section-cta"><a class="cta-enq" href="{wa_link}" target="_blank" rel="noopener">Request brochure</a>'
        f'<a class="cta-wa" href="tel:{C.PHONE_TEL}">Call {C.PHONE_DISPLAY}</a></div>'
    )
    overview = (
        '<section class="sec pg-overview"><div class="in pg-overview-grid"><div>'
        + eye('PRESTIGE ONE') + '<h2 class="dh">Full residential · <em>elite 5 BHK</em></h2>'
        '<p class="lead">A striking tower for families who want space, privacy and a prime Kalyan address — without compromise on security or amenities.</p>'
        '<dl class="pg-facts"><div><dt>Configuration</dt><dd>5 BHK</dd></div><div><dt>Areas</dt><dd>999.4 &amp; 1001.4 sq. ft.</dd></div>'
        '<div><dt>Starting price</dt><dd>Shared on request</dd></div><div><dt>Office</dt><dd>Prestige One, Godrej Hill, Khadakpada</dd></div></dl>'
        '</div><figure class="pg-overview-image pg-image-full"><img src="/img/Prestige%20One%20Tower%20in%20Daylight.png" loading="lazy" alt="Prestige One tower"><figcaption>Prestige One</figcaption></figure></div></section>'
    )
    pricing = (
        '<section class="sec pg-pricing" id="pg-configurations"><div class="in">'
        + eye('5 BHK') + '<h2 class="dh">Spacious layouts · <em>on request</em></h2>'
        '<p class="lead">Floor plans, views and pricing are shared privately with serious buyers.</p>'
        '<div class="cards pg-units"><article class="pg-unit"><span class="pg-unit-k">5 BHK</span><h3>Layout A</h3>'
        '<p class="pg-price">Price on request</p><p class="pg-area">999.4 sq. ft.</p>'
        f'<a class="btn-g" href="{wa_link}" target="_blank" rel="noopener">Request brochure</a></article>'
        '<article class="pg-unit"><span class="pg-unit-k">5 BHK</span><h3>Layout B</h3>'
        '<p class="pg-price">Price on request</p><p class="pg-area">1001.4 sq. ft.</p>'
        f'<a class="btn-g" href="{wa_link}" target="_blank" rel="noopener">Request brochure</a></article></div></div></section>'
    )
    contact = (
        '<section class="sec pg-contact" id="contact"><div class="in pg-contact-inner">'
        + eye('CONTACT') + '<h2 class="dh">Our team is <em>ready to assist</em></h2>'
        '<p class="lead">Book a visit or request the Prestige One brochure.</p>'
        f'<div class="section-cta"><a class="cta-enq" href="{wa_link}" target="_blank" rel="noopener">Request brochure</a>'
        f'<a class="cta-wa" href="tel:{C.PHONE_TEL}">Call {C.PHONE_DISPLAY}</a></div></div></section></main>'
    )
    body = hero + overview + pricing + contact
    ld = [{'@type': 'WebPage', 'name': 'Prestige One', 'url': C.SITE + path, 'description': desc, 'inLanguage': 'en-IN'}]
    html = head('en', title, desc, seo_alts, '/img/Prestige%20One%20Tower%20in%20Daylight.png', 'Prestige One Kalyan', ld, extra=video_preconnect())
    write(path.lstrip('/') + 'index.html', html + '<body class="has-video-hero">\n' + nav('en', nav_alts) + body + footer('en', nav_alts))
    PAGES.append(seo_alts)


def build_home_en_video():
    """English home: standard nav + video hero (not Sobha overlay nav)."""
    U, H = UI['en'], HOME['en']
    alts = {k: url(k, '/') for k in LANGS}
    css_ver = fver('assets/site.css')
    hero = (
        '<main id="main"><section id="home" class="hero hero-video-hero hero-under-nav" aria-label="Prestige projects in Kalyan">'
        f'<video class="hero-video" id="heroVideo" src="{HERO_VIDEO_BLOB}" autoplay muted loop playsinline webkit-playsinline preload="auto" aria-hidden="true" tabindex="-1"></video>'
        '<div class="hero-video-shade" aria-hidden="true"></div>'
        '<div class="hero-c hero-c-video">'
        f'<div class="hero-tag"><span class="hero-dot"></span>{esc(H["tag"])}</div>'
        '<h1 class="hero-name">Elite living in <b>Kalyan</b></h1>'
        f'<p class="hero-video-lead">{esc(H["taglines"][0])}</p>'
        f'<div class="hero-btns"><a class="btn-g" href="/projects/prestige-gold/"><span>Prestige Gold</span></a>'
        f'<a class="btn-o" href="{waurl(U["wa_default"])}" target="_blank" rel="noopener"><span>{esc(H["btn1"])}</span></a></div></div></section>\n'
        '<section class="home-seo-intro home-passion"><div class="in home-passion-in">'
        '<p class="home-passion-title">Prime location · Luxury · Security</p>'
        '<div class="home-passion-copy"><p>Prestige Gold — 1, 2 &amp; 3 BHK and commercial. Prestige One — elite 5 BHK.</p>'
        f'<p>{esc(U["team_ready"])}</p></div></div></section>\n'
    )
    about = ('<section class="sec" id="about"><div class="in about-grid"><div>' + eye(esc(H['about_eye'])) + f'<h2 class="dh">{H["about_h"]}</h2>'
             f'<div class="about-body" style="margin-top:24px">{"".join(f"<p>{esc(p)}</p>" for p in H["about"])}</div>'
             f'<div class="tags">{"".join(f"<span class=tag>{esc(t)}</span>" for t in H["tags"])}</div></div>'
             f'<div class="about-photo"><img src="/img/prestige-tower-day.jpg" width="900" height="1125" loading="lazy" alt="{attr(H["about_alt"])}"></div></div></section>\n')
    projects = (
        '<section class="sec project-showcase" id="pricing"><div class="in project-showcase-grid">'
        '<div class="project-showcase-media"><img src="/img/prestige-tower-night.jpg" width="1200" height="900" loading="lazy" alt="Prestige Gold"></div>'
        '<div class="project-showcase-copy"><div class="eye"><span class="eye-line"></span><span class="eye-txt">Prestige Gold</span></div>'
        '<h2 class="dh">1, 2 &amp; 3 BHK · <em>from ₹55 Lakh</em></h2>'
        '<p class="lead">3 BHK complete site ₹1.40 Cr (140 L) · 999.4–1,001.4 sq. ft. Commercial space available.</p>'
        '<a class="btn-o dark" href="/projects/prestige-gold/">View Prestige Gold</a></div></div></section>\n'
    )
    plans = (f'<section class="sec plans dark-bg" id="plans"><div class="in"><div class="plans-hd"><div>{eye(esc(H["plans_eye"]))}'
             f'<h2 class="dh light">{H["plans_h"]}</h2><p class="lead light" style="margin-top:14px;max-width:640px">{esc(H["plans_p"])}</p></div></div>'
             f'<p style="margin-top:28px"><a class="btn-o" href="/projects/prestige-gold/"><span>Request brochure</span></a></p></div></section>\n')
    assist = (
        '<section class="sec" id="services"><div class="in" style="text-align:center;padding:40px 0">'
        f'<p class="lead" style="max-width:560px;margin:0 auto">{esc(U["team_ready"])} '
        '<a href="/projects/prestige-one/">Prestige One</a> · <a href="/projects/prestige-gold/#commercial">Commercial</a></p></div></section>\n'
    )
    contact = contact_block('en', H['contact_h'], H['contact_p'])
    ld = [agent_ld('en'), {'@type': 'WebSite', '@id': C.SITE + '/#website', 'url': C.SITE + '/', 'name': C.BRAND, 'inLanguage': ['en-IN', 'hi-IN', 'mr-IN'],
                           'publisher': {'@id': C.SITE + '/#agent'}}]
    extra = ('<link rel="preconnect" href="https://bjoj2azd7axubq1h.public.blob.vercel-storage.com" crossorigin>\n'
             '<link rel="dns-prefetch" href="https://bjoj2azd7axubq1h.public.blob.vercel-storage.com">\n')
    h = head('en', H['title'], H['desc'], alts, '/img/og-default.jpg', C.BRAND, ld, extra=extra)
    h = h.replace(f'/assets/site.css?v={fver("assets/site.css")}', f'/assets/site.css?v={css_ver}')
    body_main = hero + about + projects + plans + assist + contact + '</main>\n'
    write('index.html', h + '<body class="home-premium">\n' + nav('en', alts) + body_main + footer('en', alts))


# ------------------------------------------------------------------ areas

def build_hub(l):
    U = UI[l]
    alts = {k: url(k, '/areas/') for k in LANGS}
    out = ''
    for g, slugs in MENU:
        out += f'<p class="grp-h">{esc(U["grp_" + g])}</p><div class="cards four" style="margin-top:20px">' + ''.join(
            f'<a class="card" href="{url(l, "/areas/" + s + "/")}"><img src="/img/areas/{s}.jpg" width="1200" height="630" loading="lazy" alt="{attr(city(l, s)["alt"])}">'
            f'<div class="card-b"><h3>{esc(city(l, s)["name"])}</h3><p>{esc(city(l, s)["card"])}</p><span class="card-m">{esc(U["hub_more"].format(name=city(l, s)["name"]))} →</span></div></a>'
            for s in slugs) + '</div>'
    body = (video_hero(U['hub_eyebrow']) + page_intro(
            crumbs([(U['home'], url(l, '/')), (U['areas'], None)]) + eye(esc(U['hub_eyebrow'])) + f'<h1>{U["hub_h1"]}</h1>'
            f'<p class="ph-lead">{esc(U["hub_lead"])}</p>')
            + f'<section class="sec"><div class="in">{out}</div></section>\n'
            + contact_block(l, U['hub_contact_h'], HOME[l]['contact_p']) + '</main>\n')
    ld = [agent_ld(l), breadcrumb_ld(l, [(U['home'], url(l, '/')), (U['areas'], url(l, '/areas/'))])]
    page(l, '/areas/', alts, head(l, U['hub_title'], U['hub_desc'], alts, '/img/og-default.jpg', C.BRAND, ld, extra=video_preconnect()), body)
    PAGES.append(alts)


def build_city(l, s):
    U, c = UI[l], city(l, s)
    n = c['name']
    alts = {k: url(k, f'/areas/{s}/') for k in LANGS}
    wa_t = U['city_wa'].format(name=n)
    facts = ''.join(f'<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k, v in c['facts'])
    hoods = ''.join(f'<div class="hood"><h3>{esc(a)}</h3><p>{esc(b)}</p></div>' for a, b in c['hoods'])
    why = ''.join(f'<div><h3>{esc(a)}</h3><p>{esc(b)}</p></div>' for a, b in c['why'])
    pills = ''.join(f'<a class="svc-pill" href="{waurl(wa_t + " (" + t + ")")}" target="_blank" rel="noopener">{esc(t)}</a>' for t in U['city_svc'])
    near = ''.join(f'<a class="card" href="{url(l, "/areas/" + x + "/")}"><img src="/img/areas/{x}.jpg" width="1200" height="630" loading="lazy" alt="{attr(city(l, x)["alt"])}">'
                   f'<div class="card-b"><h3>{esc(city(l, x)["name"])}</h3><p>{esc(city(l, x)["card"])}</p></div></a>' for x in NEAR[s])
    near_section = (f'<section class="sec"><div class="in"><h2 class="dh" style="font-size:clamp(28px,3.4vw,42px)">{esc(U["near_h"])}</h2><div class="cards">{near}</div></div></section>\n' if near else '')
    body = (video_hero(c['alt']) + page_intro(
            crumbs([(U['home'], url(l, '/')), (U['areas'], url(l, '/areas/')), (n, None)]) + eye(esc(U['city_eyebrow'].format(name=n)))
            + f'<h1>{U["city_h1"].format(name=esc(n))}</h1><p class="ph-lead">{esc(c["lead"])}</p>'
            f'<div class="cta-row"><a class="btn-wa" href="{waurl(wa_t)}" target="_blank" rel="noopener">{I["chat"]}<span>{esc(U["btn_wa"])}</span></a>'
            f'<a class="btn-o dark" href="#hoods"><span>{esc(U["btn_hoods"])}</span></a></div>')
            + f'\n<section class="sec"><div class="in two-col"><div>{eye(esc(U["intro_eye"].format(name=n)))}<h2 class="dh">{U["intro_h"].format(name=esc(n))}</h2>'
            f'<div class="prose" style="margin-top:28px">{"".join(f"<p>{esc(p)}</p>" for p in c["intro"])}</div></div>'
            f'<aside class="facts"><h3>{esc(U["facts_h"])}</h3><dl>{facts}</dl></aside></div></section>\n'
            f'<section class="sec" id="hoods" style="background:#fff"><div class="in">{eye(esc(U["hoods_eye"]))}<h2 class="dh">{U["hoods_h"].format(name=esc(n))}</h2><div class="hoods">{hoods}</div></div></section>\n'
            f'<section class="sec dark-bg"><div class="in">{eye(esc(U["why_eye"].format(name=n)))}<h2 class="dh light">{U["why_h"].format(name=esc(n))}</h2><div class="why">{why}</div></div></section>\n'
            f'<section class="sec"><div class="in"><h2 class="dh">{U["svc_h"].format(name=esc(n))}</h2><div class="svc-pills">{pills}</div></div></section>\n'
            f'<section class="sec" style="background:#fff;padding-top:60px"><div class="in">{eye(esc(U["faq_eye"]))}<h2 class="dh">{U["faq_h"].format(name=esc(n))}</h2>{faq_html(c["faq"])}</div></section>\n'
            f'{near_section}'
            + contact_block(l, U['contact_h'].format(name=esc(n)), HOME[l]['contact_p'], wa_text=wa_t) + '</main>\n')
    trail = [(U['home'], url(l, '/')), (U['areas'], url(l, '/areas/')), (n, url(l, f'/areas/{s}/'))]
    ld = [agent_ld(l), breadcrumb_ld(l, trail), faq_ld(c['faq'])]
    page(l, f'/areas/{s}/', alts, head(l, U['city_title'].format(name=n), c['desc'], alts, f'/img/areas/{s}.jpg', c['alt'], ld, extra=video_preconnect()), body)
    PAGES.append(alts)


# ------------------------------------------------------------------ blog

def build_blog_index(l):
    U = UI[l]
    alts = {k: url(k, '/blog/') for k in LANGS}
    body = (video_hero(U['blog_eyebrow']) + page_intro(
            crumbs([(U['home'], url(l, '/')), (U['blog'], None)]) + eye(esc(U['blog_eyebrow'])) + f'<h1>{U["blog_h1"]}</h1><p class="ph-lead">{esc(U["blog_lead"])}</p>')
            + f'<section class="sec"><div class="in"><div class="cards">{"".join(post_card(l, s) for s in ORDER)}</div></div></section>\n'
            + contact_block(l, U['cta_h'], U['cta_p']) + '</main>\n')
    ld = [agent_ld(l), breadcrumb_ld(l, [(U['home'], url(l, '/')), (U['blog'], url(l, '/blog/'))])]
    feed = video_preconnect() + f'<link rel="alternate" type="application/rss+xml" title="{attr(C.BRAND)}" href="{url(l, "/blog/feed.xml")}">\n'
    page(l, '/blog/', alts, head(l, U['blog_title'], U['blog_desc'], alts, '/img/og-default.jpg', C.BRAND, ld, extra=feed), body)
    PAGES.append(alts)


def build_post(l, s):
    U, p = UI[l], post(l, s)
    alts = {k: url(k, f'/blog/{s}/') for k in LANGS}
    secs = ''
    for hd, paras, bullets in p['sections']:
        secs += f'<h2>{esc(hd)}</h2>' + ''.join(f'<p>{esc(x)}</p>' for x in paras)
        if bullets:
            secs += '<ul>' + ''.join(f'<li>{esc(b)}</li>' for b in bullets) + '</ul>'
    idx = ORDER.index(s)
    rel = [ORDER[(idx + k) % len(ORDER)] for k in (1, 2, 3)]
    wa_t = U['post_wa'].format(title=p['title'])
    body = (video_hero(p['title']) + page_intro(
            crumbs([(U['home'], url(l, '/')), (U['blog'], url(l, '/blog/')), (p['title'], None)]) + eye(esc(U['cat_' + p['cat']]))
            + f'<h1>{esc(p["title"])}</h1><div class="ph-meta"><span>{esc(U["by"])}</span><span>{esc(U["updated"].format(date=DATE_FMT[l]))}</span>'
            f'<span>{esc(U["min_read"].format(n=p["read"]))}</span></div>')
            + f'\n<article class="sec"><div class="post"><div class="answer"><b>{esc(U["quick_answer"])}</b><p>{esc(p["answer"])}</p></div>{secs}'
            f'<h2>{esc(U["post_faq"])}</h2>{faq_html(p["faq"])}'
            f'<div class="cta-box"><h2>{esc(U["cta_h"])}</h2><p>{esc(U["cta_p"])}</p><a class="btn-wa" href="{waurl(wa_t)}" target="_blank" rel="noopener">{I["chat"]}<span>{esc(U["wa_btn"])}</span></a></div>'
            f'</div></article>\n<section class="sec" style="background:#fff"><div class="in"><h2 class="dh" style="font-size:clamp(28px,3.4vw,42px)">{esc(U["related"])}</h2>'
            f'<div class="cards">{"".join(post_card(l, r) for r in rel)}</div></div></section></main>\n')
    ld = [agent_ld(l), breadcrumb_ld(l, [(U['home'], url(l, '/')), (U['blog'], url(l, '/blog/')), (p['title'], url(l, f'/blog/{s}/'))]), faq_ld(p['faq']),
          {'@type': 'Article', 'headline': p['title'], 'description': p['desc'], 'inLanguage': C.HTML_LANG[l], 'datePublished': C.BUILD_DATE, 'dateModified': C.BUILD_DATE,
           'image': f'{C.SITE}/img/blog/{s}.jpg?v={BLOG_PHOTO_VERSION}', 'mainEntityOfPage': C.SITE + alts[l], 'author': {'@id': C.SITE + '/#agent'}, 'publisher': {'@id': C.SITE + '/#agent'}}]
    page(l, f'/blog/{s}/', alts, head(l, (p['title'] + ' | ' + C.BRAND) if len(p['title']) + len(C.BRAND) + 3 <= 70 else p['title'], p['desc'], alts, f'/img/blog/{s}.jpg', p['title'], ld, og_type='article', extra=video_preconnect()), body)
    PAGES.append(alts)


def build_feed(l):
    U = UI[l]
    dt = format_datetime(datetime.datetime(2026, 10, 29, 9, 0, tzinfo=datetime.timezone.utc))
    items = ''.join(f'<item><title>{esc(post(l, s)["title"])}</title><link>{C.SITE}{url(l, "/blog/" + s + "/")}</link><guid>{C.SITE}{url(l, "/blog/" + s + "/")}</guid>'
                    f'<pubDate>{dt}</pubDate><description>{esc(post(l, s)["answer"])}</description></item>' for s in ORDER)
    write(url(l, '/blog/feed.xml').lstrip('/'), f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>{esc(C.BRAND)}: {esc(U["blog"])}</title>'
          f'<link>{C.SITE}{url(l, "/blog/")}</link><description>{esc(U["blog_desc"])}</description><language>{C.HTML_LANG[l]}</language>{items}</channel></rss>\n')


# ------------------------------------------------------------------ site files

def build_404():
    l = 'en'
    U = UI[l]
    alts = {'en': '/'}
    body = (f'<main id="main" class="sec" style="padding-top:170px;min-height:70vh"><div class="in"><h1 class="dh">{esc(U["notfound_h"])}</h1><p class="lead" style="margin:20px 0 28px">{esc(U["notfound_p"])}</p>'
            f'<a class="btn-g" href="/">{esc(U["home"])}</a> <a class="btn-o dark" href="/blog/">{esc(U["blog"])}</a></div></main>\n')
    h = head(l, f'{U["notfound_h"]} | {C.BRAND}', U['notfound_p'], {'en': '/404.html'}, '/img/og-default.jpg', C.BRAND, [], extra='').replace('content="index, follow', 'content="noindex, follow')
    write('404.html', h + '<body>\n' + nav(l, {'en': '/', 'hi': '/hi/', 'mr': '/mr/'}) + body + footer(l, {'en': '/', 'hi': '/hi/', 'mr': '/mr/'}))


def build_login_page():
    """Copy the private enquiry CRM template to /login/."""
    template = os.path.join(ROOT, 'admin', 'dashboard.html')
    with open(template, 'r', encoding='utf-8') as f:
        write('login/index.html', f.read())


def build_sitemap():
    rows, seen = '', set()
    for alts in PAGES:
        if alts['en'] in seen:
            continue
        seen.add(alts['en'])
        for l in alts:
            links = ''.join(f'<xhtml:link rel="alternate" hreflang="{k}" href="{C.SITE}{alts[k]}"/>' for k in alts)
            links += f'<xhtml:link rel="alternate" hreflang="x-default" href="{C.SITE}{alts["en"]}"/>'
            rows += f'<url><loc>{C.SITE}{alts[l]}</loc><lastmod>{C.BUILD_DATE}</lastmod>{links}</url>\n'
    write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + rows + '</urlset>\n')
    write('robots.txt', f'User-agent: *\nAllow: /\n\nSitemap: {C.SITE}/sitemap.xml\n')


def build_llms():
    lines = [f'# {C.BRAND}', '', f'> Property consultants in Kalyan, Maharashtra, helping buyers, sellers, tenants and investors across the Mumbai Metropolitan Region. '
             'Site available in English (/), Hindi (/hi/) and Marathi (/mr/).', '', '## Contact', f'- Office: {C.ADDRESS_LINE}', f'- Phone / WhatsApp: {C.PHONE_DISPLAY}',
             f'- Email: {C.EMAIL}', '', '## Areas served']
    lines += [f'- [{CIT["en"][s]["name"]}]({C.SITE}/areas/{s}/): {CIT["en"][s]["card"]}' for s in CITY_SLUGS]
    lines += ['', '## Guides']
    lines += [f'- [{PST["en"][s]["title"]}]({C.SITE}/blog/{s}/): {PST["en"][s]["answer"]}' for s in ORDER]
    lines += ['', '## Notes', 'Information is general guidance, not legal, tax or financial advice. Confirm rates and rules with official sources.', '']
    write('llms.txt', '\n'.join(lines))


def build_vercel():
    red = [{'source': '/en', 'destination': '/', 'permanent': True}, {'source': '/en/', 'destination': '/', 'permanent': True}]
    for s in OLD_BLOG:
        red += [{'source': f'/blog/{s}', 'destination': '/blog/', 'permanent': True}, {'source': f'/blog/{s}/', 'destination': '/blog/', 'permanent': True},
                {'source': f'/en/blog/{s}/', 'destination': '/blog/', 'permanent': True}]
    for s in OLD_AREAS:
        red += [{'source': f'/areas/{s}', 'destination': '/areas/', 'permanent': True}, {'source': f'/areas/{s}/', 'destination': '/areas/', 'permanent': True},
                {'source': f'/en/areas/{s}/', 'destination': '/areas/', 'permanent': True}]
    red += [{'source': '/en/areas/', 'destination': '/areas/', 'permanent': True}, {'source': '/img/prestige_enterprises.in.png', 'destination': '/img/logo.png', 'permanent': False}]
    cfg = {'trailingSlash': True, 'redirects': red, 'headers': [
        {'source': '/(.*)', 'headers': [{'key': 'X-Content-Type-Options', 'value': 'nosniff'}, {'key': 'X-Frame-Options', 'value': 'SAMEORIGIN'},
                                         {'key': 'Referrer-Policy', 'value': 'strict-origin-when-cross-origin'}, {'key': 'Permissions-Policy', 'value': 'camera=(), microphone=(), geolocation=()'}]},
        {'source': '/img/(.*)', 'headers': [{'key': 'Cache-Control', 'value': 'public, max-age=2592000'}]},
        {'source': '/assets/(.*)', 'headers': [{'key': 'Cache-Control', 'value': 'public, max-age=31536000, immutable'}]}]}
    write('vercel.json', json.dumps(cfg, indent=2) + '\n')


# ------------------------------------------------------------------ main

def main():
    validate()
    for d in ('en', 'hi', 'mr', 'areas', 'blog'):  # generated trees (old Spanish site included)
        shutil.rmtree(os.path.join(ROOT, d), ignore_errors=True)
    for l in LANGS:
        if l == 'en':
            build_home_en_video()
        else:
            build_home(l)
        build_hub(l)
        for s in CITY_SLUGS:
            build_city(l, s)
        build_blog_index(l)
        for s in ORDER:
            build_post(l, s)
        build_feed(l)
    build_prestige_gold()
    build_prestige_one()
    build_login_page()
    build_404()
    build_sitemap()
    build_llms()
    build_vercel()
    print(f'built {len({a["en"] for a in PAGES})} pages x {len(LANGS)} languages = {len(PAGES)} URLs')


if __name__ == '__main__':
    main()
