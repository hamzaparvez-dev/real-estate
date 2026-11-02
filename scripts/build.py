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
    fonts = 'family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400;1,600&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700&family=DM+Mono:wght@400;500'
    if l != 'en':
        fonts += '&family=Noto+Sans+Devanagari:wght@300;400;500;600;700&family=Noto+Serif+Devanagari:wght@300;400;500;600'
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
              f'<li class="mnav-projects"><span>{esc(U["nav_projects"])}</span><span class="mnav-subhead">{esc(U["nav_plans"])}</span><a href="/projects/prestige-gold/">Prestige Gold</a></li>'
              f'<li><a href="{h}#pricing">{esc(U["nav_pricing"])}</a></li>'
              f'<li><a href="{h}#services">{esc(U["nav_services"])}</a></li>'
              f'<li><a href="{url(l, "/blog/")}">{esc(U["nav_blog"])}</a></li>'
              f'<li><a href="{h}#contact">{esc(U["nav_contact"])}</a></li>')
    mareas = ''.join(f'<a href="{url(l, "/areas/" + s + "/")}">{esc(city(l, s)["name"])}</a>' for s in CITY_SLUGS)
    return (f'<a class="skip" href="#main">{esc(U["skip"])}</a><div id="prog"></div>\n'
            f'<nav id="nav"{SOLID if solid else ""} aria-label="{attr(U["main_menu"])}">'
            f'<a class="nav-logo" href="{h}" aria-label="{attr(C.BRAND)}"><img src="/img/logo.png" width="160" height="49" alt="{attr(C.BRAND)}"></a>'
            '<div class="nav-r">'
            f'<a class="nav-a" href="{h}#home">{esc(U["home"])}</a>'
            f'<a class="nav-a" href="{h}#about">{esc(U["nav_about"])}</a>'
            f'<div class="nav-dd" id="navProjects"><button class="nav-dd-btn" type="button" aria-expanded="false" aria-controls="ddProjects">{esc(U["nav_projects"])}{I["caret"]}</button>'
            f'<div class="nav-dd-menu nav-projects-menu" id="ddProjects" role="region" aria-label="{attr(U["nav_projects"])}"><div class="nav-projects-group"><span class="nav-projects-label">{esc(U["nav_plans"])}</span><a class="nav-projects-item" href="/projects/prestige-gold/">Prestige Gold</a></div></div></div>'
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
    U, h = UI[l], url(l, '/')
    langs = ''.join(f'<li><a href="{alts[k]}" hreflang="{k}" lang="{k}">{C.LANG_NAME[k]}</a></li>' for k in alts)
    rera = f'<p>{esc(U["rera_label"])}: {esc(C.RERA_NO)}</p>' if C.RERA_NO else ''
    return (f'<footer><div class="foot-grid"><div>'
            f'<a class="foot-logo-link" href="{h}" aria-label="{attr(C.BRAND)}"><img src="/img/logo.png" width="175" height="54" alt="{attr(C.BRAND)}" class="foot-logo"></a>'
            f'<p>{esc(U["foot_tag"])}</p>{rera}</div>'
            f'<div><h4>{esc(U["foot_links"])}</h4><ul><li><a href="{h}">{esc(U["home"])}</a></li><li><a href="{h}#plans">{esc(U["nav_plans"])}</a></li><li><a href="{url(l, "/areas/")}">{esc(U["areas"])}</a></li>'
            f'<li><a href="{url(l, "/blog/")}">{esc(U["blog"])}</a></li><li><a href="{h}#contact">{esc(U["nav_contact"])}</a></li></ul></div>'
            f'<div><h4>{esc(U["foot_contact"])}</h4><p>{esc(C.ADDRESS_LINE)}</p><p><a href="tel:{C.PHONE_TEL}">{C.PHONE_DISPLAY}</a><br>'
            f'<a href="mailto:{C.EMAIL}">{C.EMAIL}</a></p></div>'
            f'<div><h4>{esc(U["foot_lang"])}</h4><ul>{langs}</ul></div></div>'
            f'<div class="foot-legal"><p>{esc(U["disclaimer"])}</p><p>{esc(U["rights"])}</p></div></footer>\n'
            f'<a class="wa" href="{waurl(U["wa_default"])}" target="_blank" rel="noopener" aria-label="{attr(U["wa_btn"])}">{I["chat"]}<span>{esc(U["float_wa"])}</span></a>\n'
            f'<script src="/assets/site.js?v={fver("assets/site.js")}" defer></script>\n</body>\n</html>\n')


def page(l, path, alts, head_html, body):
    """Write one page; alts maps lang -> url path."""
    write((url(l, path)).lstrip('/') + 'index.html', head_html + '<body>\n' + nav(l, alts) + body + footer(l, alts))


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


PAGES = []  # alts dicts (lang -> path); deduplicated when the sitemap is written
SOLID = ' class="solid"'
BLOG_PHOTO_VERSION = '20261101-editorial-photo-set-3'


# ------------------------------------------------------------------ home

def post_card(l, slug):
    p, U = post(l, slug), UI[l]
    return (f'<a class="card" href="{url(l, "/blog/" + slug + "/")}"><img src="/img/blog/{slug}.jpg?v={BLOG_PHOTO_VERSION}" width="800" height="420" loading="lazy" decoding="async" alt="{attr(p["title"] + " — editorial real estate photograph")}">'
            f'<div class="card-b"><span class="card-k">{esc(U["cat_" + p["cat"]])}</span><h3>{esc(p["title"])}</h3><p>{esc(p["desc"])}</p>'
            f'<span class="card-m">{esc(U["min_read"].format(n=p["read"]))}</span></div></a>')


def contact_block(l, h2, p_txt, dark_eye=True, wa_text=None):
    U, H = UI[l], HOME[l]
    rera = f'<li><b>{esc(U["rera_label"])}</b><span>{esc(C.RERA_NO)}</span></li>' if C.RERA_NO else ''
    return ('<section class="sec contact" id="contact"><div class="in contact-grid"><div>'
            f'{eye(esc(H["contact_eye"]))}<h2 class="dh light">{h2}</h2><p class="lead light" style="margin-top:18px">{esc(p_txt)}</p>'
            f'<ul class="contact-list"><li><b>{esc(U["addr_label"])}</b><span>{esc(C.ADDRESS_LINE)}</span></li>'
            f'<li><b>{esc(U["phone_label"])}</b><a href="tel:{C.PHONE_TEL}">{C.PHONE_DISPLAY}</a></li>'
            f'<li><b>WhatsApp</b><a href="{waurl(wa_text or U["wa_default"])}" target="_blank" rel="noopener">{C.PHONE_DISPLAY}</a></li>'
            f'<li><b>{esc(U["email_label"])}</b><a href="mailto:{C.EMAIL}">{C.EMAIL}</a></li>{rera}</ul>'
            f'<div class="cta-row"><a class="btn-wa" href="{waurl(wa_text or U["wa_default"])}" target="_blank" rel="noopener">{I["chat"]}<span>{esc(U["wa_btn"])}</span></a>'
            f'<a class="btn-o" href="tel:{C.PHONE_TEL}">{I["phone"]}<span>{esc(U["call_btn"])}</span></a></div></div>'
            f'<div><iframe class="map" src="{C.MAPS_EMBED}" title="{attr(C.ADDRESS_LINE)}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>'
            f'<p style="margin:12px 0 0"><a class="btn-o" href="{C.MAPS_URL}" target="_blank" rel="noopener">{esc(U["open_maps"])} {I["arrow"]}</a></p></div></div></section>\n')


def build_home(l):
    U, H = UI[l], HOME[l]
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
            f'<div class="hero-dots">{dots}</div></section>\n'
            f'<div class="stats">{"".join(f"<div class=stat><span class=stat-n>{esc(n)}</span><span class=stat-l>{esc(t)}</span></div>" for n, t in H["stats"])}</div>\n')
    about = ('<section class="sec" id="about"><div class="in about-grid"><div>' + eye(esc(H['about_eye'])) + f'<h2 class="dh">{H["about_h"]}</h2>'
             f'<div class="about-body" style="margin-top:30px">{"".join(f"<p>{esc(p)}</p>" for p in H["about"])}</div>'
             f'<div class="tags">{"".join(f"<span class=tag>{esc(t)}</span>" for t in H["tags"])}</div>'
             f'</div>'
             f'<div><div class="about-photo"><img src="/img/about.jpg" width="900" height="1125" loading="lazy" alt="{attr(H["about_alt"])}"></div>'
             f'<div class="about-quote"><p>{esc(H["quote"])}</p><cite>{esc(H["quote_by"])}</cite></div></div></div></section>\n')
    kinds = ['apartments', 'villas', 'plots', 'commercial', 'rentals', 'redevelopment']
    cards = ''.join(f'<a class="type" href="{waurl(U["wa_default"] + " (" + t[2] + ")")}" target="_blank" rel="noopener">'
                    f'<img src="/img/types/{k}.jpg" width="900" height="1200" loading="lazy" alt="{attr(H["types_alt"][i])}">'
                    f'<div class="type-ov"><h3>{esc(t[0])}</h3><p>{esc(t[1])}</p></div></a>' for i, (k, t) in enumerate(zip(kinds, H['types'])))
    types = ('<section class="sec types dark-bg" id="types"><div class="in"><div class="types-hd"><div>' + eye(esc(H['types_eye']))
             + f'<h2 class="dh light">{H["types_h"]}</h2></div><span class="types-hint">{esc(H["types_hint"])}</span></div><div class="types-grid">{cards}</div>'
             f'</div></section>\n')
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
    faq = (f'<section class="sec faq-sec" id="faq"><div class="in faq-center">'
           f'<div class="faq-hd">{eye(esc(H["faq_eye"]))}<h2 class="dh">{H["faq_h"]}</h2></div>'
           f'{faq_html(H["faq"])}'
           f'</div></section>\n')
    contact = contact_block(l, H['contact_h'], H['contact_p'])
    ld = [agent_ld(l), {'@type': 'WebSite', '@id': C.SITE + '/#website', 'url': C.SITE + '/', 'name': C.BRAND, 'inLanguage': ['en-IN', 'hi-IN', 'mr-IN'],
                        'publisher': {'@id': C.SITE + '/#agent'}}, faq_ld(H['faq'])]
    h = head(l, H['title'], H['desc'], alts, '/img/og-default.jpg', C.BRAND, ld, preload='/img/hero-day.jpg')
    page(l, '/', alts, h, hero + about + types + plans + svc + proc + areas + guides + faq + contact + '</main>\n')
    PAGES.append(alts)



# ------------------------------------------------------------------ Prestige Gold project page

def build_prestige_gold():
    path = '/projects/prestige-gold/'
    nav_alts = {k: url(k, '/') for k in LANGS}
    seo_alts = {'en': path}
    title = 'Prestige Gold Kalyan West | 1, 2 & 3 BHK Homes'
    desc = 'Explore Prestige Gold in Kalyan West: 1, 2, 3, 4 and 5 BHK residences, RERA details, indicative pricing, floor plans, amenities and site visit enquiries.'
    wa_text = 'Hello, I would like to know more about Prestige Gold, Kalyan West. Please share current availability, floor plans and the latest cost sheet.'
    wa_link = 'https://wa.me/918446652600?text=' + urllib.parse.quote(wa_text)
    units = [
        ('1 BHK', '₹55,00,000', '404–519 sq. ft.', 'Compact planning with living and dining, bedroom, kitchen provision and balcony.'),
        ('2 BHK', '₹75,00,000', '577–721 sq. ft.', 'Spacious living and dining, two bedrooms, kitchen provision and balcony.'),
        ('3 BHK', '₹1,20,00,000', '873–1,040 sq. ft.', 'Grand living and dining, master bedroom with walk-in wardrobe, two additional bedrooms, three bathrooms, two full-sized balconies and a dedicated pooja room.'),
        ('4 BHK', 'Price on request', 'Area details on request', 'Layout and configuration details available on request. Ask for verified unit-specific information and the latest approved floor plan.'),
        ('5 BHK', 'Price on request', 'Area details on request', 'Layout and configuration details available on request. Ask for verified unit-specific information and the latest approved floor plan.')
    ]
    unit_cards = ''.join(
        f'<article class="pg-unit"><span class="pg-unit-k">RESIDENTIAL CONFIGURATION</span><h3>{esc(name)}</h3>'
        f'<p class="pg-price">{esc(price)}</p><p class="pg-area">RERA area · {esc(area)}</p>'
        f'<p>{esc(summary)}</p><a class="btn-g" href="{wa_link}" target="_blank" rel="noopener">Enquire for {esc(name)}</a></article>'
        for name, price, area, summary in units)
    amenities = [
        ('Rooftop leisure zone', 'Rooftop garden with sit-outs, gazebo and fountain.'),
        ('Security-focused planning', 'Monitored common areas and controlled movement across key entry points.'),
        ('Power backup', 'Backup provision for lifts, lobbies and common areas.'),
        ('Water & utilities', 'KDMC water supply with borewell backup and planned utility infrastructure.'),
        ('Sustainable operations', 'Waste segregation and green-zone planning.'),
        ('Parking convenience', 'Two parking levels with optimized angle-parking design.'),
        ('Sample flat ready', 'Arrange a guided walkthrough to experience the sample flat in person.')
    ]
    amenity_cards = ''.join(f'<article class="pg-amenity"><span>✦</span><div><h3>{esc(a)}</h3><p>{esc(d)}</p></div></article>' for a, d in amenities)
    faq_items = [
        ('Where is Prestige Gold located?', 'Prestige Gold is in Kalyan West, Thane, Maharashtra 421301. Contact the project team for exact directions and a guided site visit.'),
        ('Is Prestige Gold RERA registered?', 'The project website lists MahaRERA registration number P51700052362. Buyers should verify the latest registration details and disclosures on the official MahaRERA portal before booking.'),
        ('Which configurations are listed?', 'The project website lists 1 BHK, 2 BHK, 3 BHK, 4 BHK and 5 BHK configurations. Confirm current inventory and unit-specific areas with the sales team.'),
        ('What are the indicative starting prices?', 'The project website lists indicative starting prices for 1 BHK, 2 BHK and 3 BHK only. Pricing for 4 BHK and 5 BHK is available on request. Confirm all prices and availability in a current written cost sheet.'),
        ('When is possession expected?', 'The project website states June 2027 as the expected possession timeline. Confirm the applicable date against the latest MahaRERA record and your agreement for sale.')
    ]
    hero = (
        '<main id="main"><header class="ph pg-hero"><img src="/img/prestige-tower-day.jpg" width="1920" height="1080" fetchpriority="high" alt="Prestige Gold residential tower, Kalyan West">'
        '<div class="ph-c">' + crumbs([(UI['en']['home'], '/'), ('Projects', None), ('Plans', None), ('Prestige Gold', None)]) +
        eye('KALYAN WEST · RESIDENTIAL + COMMERCIAL') +
        '<h1>Prestige <b>Gold</b></h1>'
        '<p class="ph-lead">A considered address for everyday living and long-term value in Kalyan West. Explore the project, compare configurations and arrange a guided visit.</p>'
        '<div class="pg-hero-facts"><span>1, 2, 3, 4 &amp; 5 BHK</span><span>MahaRERA · P51700052362</span><span>G + 5 floors</span><span>70% completed · Sample flat ready</span></div>'
        f'<div class="section-cta"><a class="cta-enq" href="{wa_link}" target="_blank" rel="noopener">Enquire on WhatsApp</a><a class="cta-wa" href="tel:+918446652600">Call +91 84466 52600</a></div>'
        '</div></header>'
    )
    overview = (
        '<section class="sec pg-overview"><div class="in pg-overview-grid"><div>'
        + eye('THE PROJECT') + '<h2 class="dh">A premium address in <em>Kalyan West</em></h2>'
        '<p class="lead">Prestige Gold is presented as a mixed-use development bringing residential homes and commercial opportunity together. The project website highlights vastu-compliant planning, modern infrastructure and a rooftop leisure zone.</p>'
        '<dl class="pg-facts"><div><dt>Project type</dt><dd>Residential + Commercial</dd></div><div><dt>Configurations</dt><dd>1, 2, 3, 4 &amp; 5 BHK</dd></div><div><dt>MahaRERA</dt><dd>P51700052362</dd></div><div><dt>Expected possession</dt><dd>June 2027*</dd></div><div><dt>Construction status</dt><dd>70% completed*</dd></div><div><dt>Sample flat</dt><dd>Ready to visit</dd></div></dl>'
        '<p class="pg-note">*Construction status and possession timeline are as stated on the project website and may change. Verify the latest MahaRERA disclosures, construction progress and agreement for sale before making a purchase decision.</p>'
        '</div><figure class="pg-overview-image"><img src="/img/prestige-tower-night.jpg" width="1200" height="900" loading="lazy" alt="Prestige Gold tower at night"><figcaption>Prestige Gold · Kalyan West</figcaption></figure></div></section>'
    )
    pricing = (
        '<section class="sec pg-pricing" id="pg-configurations"><div class="in">'
        + eye('CONFIGURATIONS & INDICATIVE PRICING') + '<h2 class="dh">Find a home that <em>fits your plans</em></h2>'
        '<p class="lead">Compare the configurations listed on the project website. Areas and prices are indicative and must be reconfirmed for the selected unit.</p>'
        f'<div class="cards three pg-units">{unit_cards}</div>'
        '<p class="pg-note">Prices are indicative starting figures published on the project website. Final pricing, taxes, statutory charges, parking, inclusions and availability must be confirmed in a current written cost sheet.</p>'
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
    amenities_section = (
        '<section class="sec pg-amenities"><div class="in">'
        + eye('EVERYDAY COMFORT') + '<h2 class="dh">Thoughtful features for <em>daily living</em></h2>'
        f'<div class="pg-amenities-grid">{amenity_cards}</div>'
        '</div></section>'
    )
    progress = (
        '<section class="sec pg-progress"><div class="in"><div class="pg-progress-head">' + eye('CONSTRUCTION UPDATE') + '<h2 class="dh">Built with <em>transparency</em></h2>' +
        '<p class="lead">The project website currently states 70% completion, with the sample flat ready for a guided walkthrough. Confirm the latest on-site status before booking.</p>' +
        '<div class="pg-progress-meter"><div class="pg-progress-copy"><b>70%</b><span>Project status as stated on the project website</span></div><div class="pg-progress-track"><span></span></div></div>' +
        '<div class="pg-milestones"><article><b>01</b><h3>Land, legal &amp; RERA registration</h3><p>Registration and approvals stated as completed on the project website.</p></article><article><b>02</b><h3>Foundation &amp; excavation</h3><p>Foundation and plinth work stated as completed.</p></article><article><b>03</b><h3>RCC structure</h3><p>Structure progress stated on the project website; verify current slab and site status.</p></article><article><b>04</b><h3>Brickwork &amp; internal works</h3><p>Brickwork and internal works are stated as in progress.</p></article><article><b>05</b><h3>Finishes &amp; fittings</h3><p>Plaster, tiling, fittings and painting are listed as upcoming works.</p></article><article><b>06</b><h3>OC, possession &amp; handover</h3><p>Expected possession is stated as June 2027; confirm against the latest RERA record.</p></article></div>' +
        '</div></section>'
    )
    gallery = (
        '<section class="sec pg-gallery"><div class="in">'
        + eye('PROJECT GALLERY') + '<h2 class="dh">A closer look at <em>Prestige Gold</em></h2>'
        '<div class="pg-gallery-grid"><figure><img src="/img/prestige-tower-day.jpg" width="1400" height="900" loading="lazy" alt="Prestige Gold exterior, day view"><figcaption>Day view</figcaption></figure>'
        '<figure><img src="/img/prestige-tower-night.jpg" width="1400" height="900" loading="lazy" alt="Prestige Gold exterior, night view"><figcaption>Night view</figcaption></figure></div>'
        '</div></section>'
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
    contact = (
        '<section class="sec pg-contact" id="pg-enquire"><div class="in pg-contact-inner">'
        + eye('NEXT STEP') + '<h2 class="dh">Experience Prestige <em>Gold</em></h2>'
        '<p class="lead">Ask for current availability, unit-wise pricing, approved floor plans and a guided site visit.</p>'
        '<div class="section-cta"><a class="cta-enq" href="' + wa_link + '" target="_blank" rel="noopener">WhatsApp the project team</a>'
        '<a class="cta-wa" href="tel:+918446652600">Call +91 84466 52600</a></div>'
        '<p class="pg-contact-email">Email: <a href="mailto:shreedurgaenterprise21@gmail.com">shreedurgaenterprise21@gmail.com</a></p>'
        '</div></section>'
    )
    faq = (
        '<section class="sec pg-faq"><div class="in"><div class="faq-hd">' + eye('BUYER INFORMATION') +
        '<h2 class="dh">Frequently asked <em>questions</em></h2></div>' + faq_html(faq_items) + '</div></section></main>'
    )
    body = hero + overview + pricing + floorplans + amenities_section + progress + gallery + location + contact + faq
    ld = [agent_ld('en'), breadcrumb_ld('en', [(UI['en']['home'], url('en', '/')), ('Prestige Gold', path)])]
    html = head('en', title, desc, seo_alts, '/img/prestige-tower-day.jpg', 'Prestige Gold project in Kalyan West', ld)
    write(path.lstrip('/') + 'index.html', html + '<body>\n' + nav('en', nav_alts) + body + footer('en', nav_alts))
    PAGES.append(seo_alts)


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
    body = ('<main id="main"><header class="ph"><img src="/img/hero-day.jpg" width="1920" height="1080" alt=""><div class="ph-c">'
            + crumbs([(U['home'], url(l, '/')), (U['areas'], None)]) + eye(esc(U['hub_eyebrow'])) + f'<h1>{U["hub_h1"]}</h1>'
            f'<p class="ph-lead">{esc(U["hub_lead"])}</p></div></header><section class="sec"><div class="in" style="margin-top:-30px">{out}</div></section>\n'
            + contact_block(l, U['hub_contact_h'], HOME[l]['contact_p']) + '</main>\n')
    ld = [agent_ld(l), breadcrumb_ld(l, [(U['home'], url(l, '/')), (U['areas'], url(l, '/areas/'))])]
    page(l, '/areas/', alts, head(l, U['hub_title'], U['hub_desc'], alts, '/img/og-default.jpg', C.BRAND, ld), body)
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
    body = (f'<main id="main"><header class="ph"><img src="/img/areas/{s}.jpg" width="1200" height="630" alt="{attr(c["alt"])}" fetchpriority="high"><div class="ph-c">'
            + crumbs([(U['home'], url(l, '/')), (U['areas'], url(l, '/areas/')), (n, None)]) + eye(esc(U['city_eyebrow'].format(name=n)))
            + f'<h1>{U["city_h1"].format(name=esc(n))}</h1><p class="ph-lead">{esc(c["lead"])}</p>'
            f'<div class="cta-row"><a class="btn-wa" href="{waurl(wa_t)}" target="_blank" rel="noopener">{I["chat"]}<span>{esc(U["btn_wa"])}</span></a>'
            f'<a class="btn-o" href="#hoods"><span>{esc(U["btn_hoods"])}</span></a></div></div></header>\n'
            f'<section class="sec"><div class="in two-col"><div>{eye(esc(U["intro_eye"].format(name=n)))}<h2 class="dh">{U["intro_h"].format(name=esc(n))}</h2>'
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
    page(l, f'/areas/{s}/', alts, head(l, U['city_title'].format(name=n), c['desc'], alts, f'/img/areas/{s}.jpg', c['alt'], ld), body)
    PAGES.append(alts)


# ------------------------------------------------------------------ blog

def build_blog_index(l):
    U = UI[l]
    alts = {k: url(k, '/blog/') for k in LANGS}
    body = ('<main id="main"><header class="ph" style="min-height:460px"><img src="/img/hero-night.jpg" width="1920" height="1080" alt=""><div class="ph-c">'
            + crumbs([(U['home'], url(l, '/')), (U['blog'], None)]) + eye(esc(U['blog_eyebrow'])) + f'<h1>{U["blog_h1"]}</h1><p class="ph-lead">{esc(U["blog_lead"])}</p></div></header>'
            f'<section class="sec"><div class="in" style="margin-top:-20px"><div class="cards">{"".join(post_card(l, s) for s in ORDER)}</div></div></section>\n'
            + contact_block(l, U['cta_h'], U['cta_p']) + '</main>\n')
    ld = [agent_ld(l), breadcrumb_ld(l, [(U['home'], url(l, '/')), (U['blog'], url(l, '/blog/'))])]
    feed = f'<link rel="alternate" type="application/rss+xml" title="{attr(C.BRAND)}" href="{url(l, "/blog/feed.xml")}">\n'
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
    body = (f'<main id="main"><header class="ph" style="min-height:500px"><img src="/img/blog/{s}.jpg?v={BLOG_PHOTO_VERSION}" width="800" height="420" alt="{attr(p["title"] + " — editorial real estate photograph")}" fetchpriority="high" decoding="async"><div class="ph-c">'
            + crumbs([(U['home'], url(l, '/')), (U['blog'], url(l, '/blog/')), (p['title'], None)]) + eye(esc(U['cat_' + p['cat']]))
            + f'<h1 style="font-size:clamp(34px,5vw,64px)">{esc(p["title"])}</h1><div class="ph-meta"><span>{esc(U["by"])}</span><span>{esc(U["updated"].format(date=DATE_FMT[l]))}</span>'
            f'<span>{esc(U["min_read"].format(n=p["read"]))}</span></div></div></header>\n'
            f'<article class="sec"><div class="post"><div class="answer"><b>{esc(U["quick_answer"])}</b><p>{esc(p["answer"])}</p></div>{secs}'
            f'<h2>{esc(U["post_faq"])}</h2>{faq_html(p["faq"])}'
            f'<div class="cta-box"><h2>{esc(U["cta_h"])}</h2><p>{esc(U["cta_p"])}</p><a class="btn-wa" href="{waurl(wa_t)}" target="_blank" rel="noopener">{I["chat"]}<span>{esc(U["wa_btn"])}</span></a></div>'
            f'</div></article>\n<section class="sec" style="background:#fff"><div class="in"><h2 class="dh" style="font-size:clamp(28px,3.4vw,42px)">{esc(U["related"])}</h2>'
            f'<div class="cards">{"".join(post_card(l, r) for r in rel)}</div></div></section></main>\n')
    ld = [agent_ld(l), breadcrumb_ld(l, [(U['home'], url(l, '/')), (U['blog'], url(l, '/blog/')), (p['title'], url(l, f'/blog/{s}/'))]), faq_ld(p['faq']),
          {'@type': 'Article', 'headline': p['title'], 'description': p['desc'], 'inLanguage': C.HTML_LANG[l], 'datePublished': C.BUILD_DATE, 'dateModified': C.BUILD_DATE,
           'image': f'{C.SITE}/img/blog/{s}.jpg?v={BLOG_PHOTO_VERSION}', 'mainEntityOfPage': C.SITE + alts[l], 'author': {'@id': C.SITE + '/#agent'}, 'publisher': {'@id': C.SITE + '/#agent'}}]
    page(l, f'/blog/{s}/', alts, head(l, (p['title'] + ' | ' + C.BRAND) if len(p['title']) + len(C.BRAND) + 3 <= 70 else p['title'], p['desc'], alts, f'/img/blog/{s}.jpg', p['title'], ld, og_type='article'), body)
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
        build_home(l)
        build_hub(l)
        for s in CITY_SLUGS:
            build_city(l, s)
        build_blog_index(l)
        for s in ORDER:
            build_post(l, s)
        build_feed(l)
    build_prestige_gold()
    build_404()
    build_sitemap()
    build_llms()
    build_vercel()
    print(f'built {len({a["en"] for a in PAGES})} pages x {len(LANGS)} languages = {len(PAGES)} URLs')


if __name__ == '__main__':
    main()
