"""Business details used across the whole site. Edit here, then run: python3 scripts/build.py"""

SITE = 'https://www.prestigeenterprises.in'
BRAND = 'Prestige Projects'

PHONE_DISPLAY = '+91 96895 57788'
PHONE_TEL = '+919689557788'
WA = 'https://wa.me/919689557788'
EMAIL = 'prestigeprojects1956@gmail.com'

STREET = 'Prestige One, Godrej Hill, Khadakpada'
LOCALITY = 'Kalyan'
REGION = 'Maharashtra'
POSTAL = '421301'
COUNTRY = 'IN'
ADDRESS_LINE = f'{STREET}, {LOCALITY}, {REGION} {POSTAL}'
MAPS_URL = 'https://www.google.com/maps/place/PRESTIGE+ONE/@19.262936,73.1425496,17z/data=!3m1!4b1!4m6!3m5!1s0x3be7968ee12f5ffd:0x3b8bf633a3480b65!8m2!3d19.262936!4d73.1425496!16s%2Fg%2F11yjshmnqv'
MAPS_EMBED = 'https://www.google.com/maps?q=19.262936,73.1425496&z=17&output=embed'

# Fill these in when you have them. Empty = not shown anywhere on the site.
RERA_NO = 'P51700052362'
META_PIXEL_ID = ''      # Meta (Facebook) Pixel ID for YOUR ad account. The old client's pixel was removed.
GTM_ID = 'GTM-KH9KRC8Z'  # Google tag / Tag Manager container
SAME_AS = []            # profile URLs, e.g. your Facebook Page and Instagram


def gtm_head():
    """Deferred Google tag — loads after idle so it does not compete with LCP."""
    if not GTM_ID:
        return ''
    return (
        '<script>\n'
        'window.dataLayer=window.dataLayer||[];\n'
        'function gtag(){dataLayer.push(arguments);}\n'
        "gtag('js',new Date());\n"
        '(function(){\n'
        f"var id='{GTM_ID}';\n"
        'function load(){if(window.__peGtm)return;window.__peGtm=1;'
        "var s=document.createElement('script');s.async=true;"
        "s.src='https://www.googletagmanager.com/gtm.js?id='+id;"
        'document.head.appendChild(s);}\n'
        "if('requestIdleCallback' in window)requestIdleCallback(load,{timeout:3500});\n"
        'else window.addEventListener("load",function(){setTimeout(load,1200);});\n'
        '})();\n'
        '</script>\n'
    )

BUILD_DATE = '2026-10-29'
LANGS = ['en', 'hi', 'mr']
LOCALE = {'en': 'en_IN', 'hi': 'hi_IN', 'mr': 'mr_IN'}
HTML_LANG = {'en': 'en-IN', 'hi': 'hi-IN', 'mr': 'mr-IN'}
LANG_NAME = {'en': 'English', 'hi': 'हिन्दी', 'mr': 'मराठी'}
LANG_SHORT = {'en': 'EN', 'hi': 'हिं', 'mr': 'मरा'}
