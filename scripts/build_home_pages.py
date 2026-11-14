"""Generate the English, Hindi and Marathi home pages from one shared template.

Run from the repo root:  python3 scripts/build_home_pages.py
Writes index.html, hi/index.html and mr/index.html.
"""
import html
import json
import os
import sys
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import posts_en
import posts_hi
import posts_mr

SITE = 'https://www.prestigeenterprises.in'
ASSET_VER = 'prestige-home-revamp-20261114-v29'
BLOG_PHOTO_VERSION = '20261101-editorial-photo-set-3'
FEATURED_GUIDES = posts_en.FEATURED
POSTS = {'en': posts_en.POSTS, 'hi': posts_hi.POSTS, 'mr': posts_mr.POSTS}
VIDEO = 'https://bjoj2azd7axubq1h.public.blob.vercel-storage.com/Prestige_One_Kalyan_Sales_Video_1080p%20%281%29.mp4'
VIDEO_HOST = 'https://bjoj2azd7axubq1h.public.blob.vercel-storage.com'
PHONE_TEL = '+919689557788'
PHONE = '+91 96895 57788'
WA = 'https://wa.me/919689557788'
EMAIL = 'prestigeprojects1956@gmail.com'
ADDRESS = 'Prestige One, Godrej Hill, Khadakpada, Kalyan, Maharashtra 421301'
MAPS_EMBED = 'https://www.google.com/maps?q=Prestige+One,+Godrej+Hill,+Khadakpada,+Kalyan,+Maharashtra+421301&output=embed'
MAPS_URL = 'https://maps.app.goo.gl/VFL4kqKsmQ6XdHS69'
RERA = 'P51700052362'
LANGS = ('en', 'hi', 'mr')
PREFIX = {'en': '', 'hi': '/hi', 'mr': '/mr'}
LOCALE = {'en': 'en_IN', 'hi': 'hi_IN', 'mr': 'mr_IN'}
HTML_LANG = {'en': 'en-IN', 'hi': 'hi-IN', 'mr': 'mr-IN'}

e = html.escape


def a(s):
    return html.escape(s, quote=True)


def wa(text):
    return WA + '?text=' + urllib.parse.quote(text)


SVG = {
    'chat': '<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>',
    'phone': '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
    'arrow': '<path d="M5 12h14M13 6l6 6-6 6"/>',
    'zoom': '<circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35M11 8v6M8 11h6"/>',
    'pin': '<path d="M12 22s7-6.5 7-12a7 7 0 1 0-14 0c0 5.5 7 12 7 12z"/><circle cx="12" cy="10" r="2.6"/>',
    'crown': '<path d="M3 18h18M4 18l-1-10 5 4 4-7 4 7 5-4-1 10"/>',
    'leaf': '<path d="M5 19c0-8 6-14 15-14 0 9-6 15-14 15"/><path d="M5 19l8-8"/>',
    'shield': '<path d="M12 22s8-4 8-11V5l-8-3-8 3v6c0 7 8 11 8 11z"/><path d="M9 12l2 2 4-4"/>',
}


def icon(name, cls=''):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{SVG[name]}</svg>')


# Large line illustrations for the location cards (64px, Mohan-style outline icons).
LOC_ICON = {
    'health': ('<svg class="loc-icon" viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true">'
               '<path d="M6 58h52M10 58V22h44v36"/><path d="M22 22V8h20v14"/><path d="M32 11v8M28 15h8"/>'
               '<path d="M16 30h8v6h-8zM40 30h8v6h-8zM16 42h8v6h-8zM40 42h8v6h-8z"/><path d="M28 58V44h8v14"/></svg>'),
    'shop': ('<svg class="loc-icon" viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true">'
             '<path d="M4 58h56M8 58V26h48v32"/><path d="M4 26l8-14h40l8 14z"/><rect x="18" y="16" width="28" height="8"/>'
             '<path d="M14 34h14v24H14zM36 34h14v12H36z"/><path d="M21 34v24"/></svg>'),
    'school': ('<svg class="loc-icon" viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true">'
               '<path d="M4 58h56M8 58V30h48v28"/><path d="M4 30l28-16 28 16"/><path d="M32 14V4l8 3-8 3"/>'
               '<circle cx="32" cy="27" r="5"/><path d="M32 24v3h2"/><path d="M14 36h8v6h-8zM42 36h8v6h-8zM14 46h8v6h-8zM42 46h8v6h-8z"/>'
               '<path d="M27 58V44h10v14"/></svg>'),
}

AMENITY_IMGS = ['swimming-pool', 'cricket', 'games-lounge', 'library', 'mini-theatre', 'pickleball', 'residents-lounge', 'fitness-centre']

# Distances are approximate drive times from Khadakpada, Kalyan West.
LOCATIONS = {
    'health': [('Aayush Hospital', 2, 5), ('Fortis Hospital', 4, 8), ('Shwaas Multispeciality Hospital', 5, 9)],
    'shop': [('Patel Mart / DMart', 1, 2), ('Metro Junction Mall', 5, 9), ('Mukta A2 Cinemas', 5, 9), ('Xperia Mall', 10, 13), ('Viviana Mall', 20, 25)],
    'school': [('Podar International School', 1, 2), ('Agrawal College', 1, 2), ('Vibgyor Roots & Rise', 2, 3), ('Birla College', 2, 5)],
}

T = {}

T['en'] = dict(
    title='Luxury Homes in Kalyan West | Prestige Enterprises',
    desc='Residences in Khadakpada, Kalyan West: prime location, luxury living, modern amenities and round-the-clock security. 1, 2 & 3 BHK from ₹55 Lakh. Book a private site visit.',
    nav_label='Main menu', menu_open='Open menu', hero_label='Prestige Enterprises residences in Kalyan West',
    intro_h='A home that feels worth the wait',
    intro=['Sunlit rooms. Branded finishes. Amenities that feel like a private club. Prestige Enterprises creates residences for families who expect more than another flat on the market.',
           'Homes are limited and pricing is clear. The fastest way to know if this one is yours is a private viewing with our team.'],
    intro_cta='Book a private viewing',
    pillars=[('pin', 'Prime location', 'Khadakpada, Kalyan West. Leading schools, hospitals and shopping within a short drive.'),
             ('crown', 'Luxury living', 'Designer lobbies, branded fittings, vitrified flooring and aluminium French windows.'),
             ('leaf', 'Modern amenities', 'A landscaped rooftop garden, open gym, pool, mini theatre and courts for every age.'),
             ('shield', 'Security systems', 'CCTV across common areas, a secured entrance gate and lifts with power backup.')],
    about_eye='Who we are', about_h='Homes built around <em>how you live</em>',
    about=['Prestige Enterprises creates and represents residences in Kalyan West for families who expect more from the place they call home: better light, better planning and better neighbours.',
           'Our office sits within Prestige One at Godrej Hill, Khadakpada. We know these streets, these buildings and these documents first-hand, so every visit is guided by someone who has walked the site.',
           'Every home is offered with transparent pricing, MahaRERA-registered paperwork and a written cost sheet, so the only surprise is how quickly it feels like yours.'],
    about_alt='Prestige Gold residential tower in Kalyan West',
    quote='A home is the biggest decision most families make. Our role is to make it a confident one.',
    one_view_alt='Prestige One living room opening onto a balcony with riverside sunset views',
    one_poster_alt='Prestige One: One Life. One Home.',
    projects_eye='Our residences', projects_h='Two addresses, <em>one standard</em>',
    projects=[('/projects/prestige-gold/', '/img/prestige-tower-day.jpg', 1920, 1080, 'Prestige Gold residential tower in Kalyan West',
               'Prestige Gold', 'Contemporary <em>1, 2 &amp; 3 BHK</em> residences',
               'Efficient, light-filled homes with modular kitchens, city-view balconies and premium vitrified flooring. Residential and commercial spaces in Kalyan West.',
               'Explore Prestige Gold'),
              ('/projects/prestige-one/', '/img/Prestige%20One%20Tower%20in%20Daylight.png', 1011, 1555, 'Prestige One residential tower in daylight, Kalyan',
               'Prestige One', 'A landmark at <em>Godrej Hill</em>',
               'A striking tower with sculpted balconies and a commanding presence over Khadakpada. Elite 5 BHK residences, shared privately with serious buyers.',
               'Explore Prestige One')],
    amen_eye='Amenities', amen_h='Leisure, wellness and play, <em>right at home</em>',
    amen_lead='Spaces designed for unhurried mornings, active evenings and weekends with family, all within the community.',
    amen_names=['Swimming pool', 'Cricket practice pitch', 'Games lounge', 'Reading library', 'Mini theatre', 'Pickleball court', 'Residents\u2019 lounge', 'Fitness centre'],
    roof_eye='Signature amenity', roof_h='A rooftop garden of <em>298 sq. m.</em>',
    roof_p='Spanning both wings across 45.85 metres, the terrace is landscaped into a private retreat above the city, with water, shade, greenery and space to move.',
    roof_feats=[('Water body with waterfall feature', '3.00 × 4.50 m'), ('Two seating gazebos', '3.00 × 3.00 m each'),
                ('Open-air gym', '4.50 × 5.00 m'), ('Planting area with pathways', '4.50 × 6.00 m'),
                ('Central stone and wooden-deck walkway', '2.00 m wide'), ('Direct lift and staircase access', 'Wings A & B')],
    roof_note='Dimensions are approximate, as per plan.',
    roof_cta='Download RERA area plan',
    roof_alt='Rooftop garden with water body, gazebos, open gym and landscaped walkway',
    spec_eye='Specifications & security', spec_h='Finished with care, <em>protected around the clock</em>',
    spec_h1='Specifications',
    specs=['Decorative entrance gate and designer lobby', 'Branded vitrified flooring throughout',
           'Powder-coated aluminium French windows', 'Designer bathrooms with branded fittings',
           'Wooden doors for bedrooms, main door and bathrooms', 'Ample parking space'],
    spec_h2='Security systems',
    security=['CCTV surveillance across common areas', 'Secured, gated entrance', 'Branded lifts with power backup',
              'Well-lit lobbies, corridors and parking'],
    spec_alt='Specifications and amenities: entrance gate, lifts, parking, lobby, flooring, CCTV and bathrooms',
    price_eye='Residences & pricing', price_h='Choose your home <em>with clarity</em>',
    price_p='Starting prices and RERA carpet areas for each configuration. Our team will share live availability and a detailed cost sheet on request.',
    area_label='RERA area', details='Home details', starting='Starting price', onwards='Onwards · premium and corner units on request',
    enquire='Enquire', tap='Tap to view', sqft='sq. ft.',
    units=[('1 BHK', '404–519', '₹55,00,000', '/img/plans/1bhk-3d.webp', '1 BHK 3D floor plan',
            ['Living and dining room', 'Bedroom with attached bath', 'Modular kitchen provision', 'Balcony with city view', 'Utility / dry balcony', 'Premium vitrified flooring']),
           ('2 BHK', '577–721', '₹75,00,000', '/img/plans/2bhk-layout.webp', '2 BHK floor plan',
            ['Spacious living and dining', 'Master bedroom with attached bath', 'Second bedroom with common bath', 'Modular kitchen and dry balcony', 'Twin balconies', 'UPVC sliding windows']),
           ('3 BHK', '999.4–1,001.4', '₹1,40,00,000', '', '3 BHK floor plan',
            ['Available across the complete site', 'Grand living and dining', 'Master bedroom with walk-in wardrobe', 'Two additional bedrooms', 'Three bathrooms (two attached)', 'Two full-size balconies', 'Dedicated pooja room'])],
    plan_req='Layout shared on request',
    more_eye='Also available',
    more_h='Commercial, 4 BHK &amp; 5 BHK',
    more_p='Separate options beyond the published 1, 2 and 3 BHK homes. Details are shared privately with serious buyers.',
    more_units=[
        ('Commercial', 'CO', 'Ground & podium levels', 'On request',
         ['Retail and office frontage', 'High-footfall Kalyan West corridor', 'Brochure and sizes on request', 'Pricing shared in writing'],
         'Hello Prestige Enterprises, I would like the Prestige Gold commercial brochure for retail and office space in Kalyan West.'),
        ('4 BHK', '4B', 'Layout shared on request', 'On request',
         ['Larger family layouts', 'Multiple balconies', 'Premium finishes', 'Availability confirmed privately'],
         'Hello Prestige Enterprises, I would like details for 4 BHK residences in Kalyan West. Please share layouts, availability and pricing.'),
        ('5 BHK', '5B', '', 'On request',
         ['Elite Prestige One residences', 'Spacious private layouts', 'Shared privately with serious buyers', 'Site visit on request'],
         'Hello Prestige Enterprises, I would like details for Prestige One 5 BHK residences. Please share layouts, carpet areas and pricing.'),
    ],
    more_enquire='Request details',
    price_note='Prices and areas are indicative. Final pricing, availability, taxes, statutory charges and parking are confirmed in a current written cost sheet before booking.',
    plans_eye='Floor plans', plans_h='Layouts planned <em>for everyday life</em>',
    plans_p='Explore 3D and top-view layouts. Tap any plan to view it full size.',
    plans=[('/img/plans/1bhk-3d.webp', '1 BHK · 3D view', '1 BHK residence', 'Bedroom, living, dining and kitchen arranged in one bright, efficient line, with balconies at both ends.'),
           ('/img/plans/1bhk-layout.webp', '1 BHK · Top view', '1 BHK layout', 'Separate bath and powder room, a utility balcony and a lounge balcony beside the living area.'),
           ('/img/plans/2bhk-layout.webp', '2 BHK · Top view', '2 BHK layout', 'Two bedrooms, two baths and three balconies around a generous living and dining space.')],
    plans_btn='View Prestige Gold details',
    loc_eye='Prime location', loc_h='Everything you need, <em>minutes away</em>',
    loc_p='Khadakpada is among Kalyan West\u2019s most established residential neighbourhoods: tree-lined, well connected and surrounded by trusted schools, hospitals and shopping.',
    loc_titles={'health': 'Hospitals & Healthcare', 'shop': 'Malls & Entertainment', 'school': 'Schools & Colleges'},
    km='km', mins='min', loc_note='Distances and drive times are approximate and vary with traffic.',
    faq_eye='FAQ', faq_h='Common <em>questions</em>',
    faq=[('Where are the residences located?', 'In Kalyan West, around Khadakpada and Godrej Hill. Our office is at Prestige One, Godrej Hill, Khadakpada, Kalyan 421301.'),
         ('Which configurations are available?', '1, 2 and 3 BHK residences with published starting prices from ₹55 Lakh at Prestige Gold, plus commercial space. 4 BHK and elite 5 BHK residences are offered privately on request.'),
         ('What amenities do residents enjoy?', 'A 298 sq. m. landscaped rooftop garden with a water body, gazebos and open gym, along with a swimming pool, fitness centre, mini theatre, games lounge, library and sports courts.'),
         ('What security systems are in place?', 'CCTV surveillance across common areas, a secured gated entrance, well-lit common spaces and branded lifts with power backup.'),
         ('Is the project RERA registered?', f'Yes. MahaRERA registration number {RERA}. We share the registration details and documents before you book.'),
         ('How do I book a site visit?', 'Message us on WhatsApp or call +91 96895 57788. We will confirm a time that suits you and share the latest availability.')],
    guides_eye='Guides', guides_h='Straight answers on <em>buying property in Kalyan</em>',
    guides_btn='View all guides', guides_min='{n} min read',
    guide_cats={'buying': 'Buying', 'costs': 'Costs', 'legal': 'Legal checks', 'finance': 'Finance', 'tax': 'Tax', 'investing': 'Investing'},
    contact_eye='Contact', contact_h='Arrange a <em>private site visit</em>',
    contact_p='Tell us the home you have in mind. Our Khadakpada team will share live availability, floor plans and a written cost sheet, and arrange a visit at your convenience.',
    addr='Office', phone='Phone', email='Email', wa_btn='Chat on WhatsApp', call='Call us', maps='Open in Google Maps',
    wa_text='Hello Prestige Enterprises, I would like to arrange a site visit and receive current availability in Kalyan West.',
    foot_tag='Thoughtfully planned residences in Kalyan West, Maharashtra.',
    foot_explore='Explore', foot_projects='Projects', foot_contact='Contact',
    foot_links=[('#about', 'About'), ('#amenities', 'Amenities'), ('#plans', 'Floor plans'), ('#location', 'Location'), ('/blog/', 'Guides'), ('#contact', 'Contact')],
    privacy='Privacy Policy', rera_verified='Verified & Registered',
    disclaimer='Images are artistic impressions for representation only. Amenities, specifications, prices and distances are indicative and may change; confirm current details in writing before booking.',
    rights='© 2026 Prestige Enterprises. All rights reserved.',
    float_wa='WhatsApp',
)

T['hi'] = dict(
    title='कल्याण वेस्ट में लग्ज़री घर | Prestige Enterprises',
    desc='खड़कपाड़ा, कल्याण वेस्ट में घर: प्राइम लोकेशन, लग्ज़री लिविंग, आधुनिक सुविधाएँ और चौबीसों घंटे सुरक्षा। 1, 2 और 3 BHK ₹55 लाख से। निजी साइट विज़िट बुक करें।',
    nav_label='मुख्य मेन्यू', menu_open='मेन्यू खोलें', hero_label='कल्याण वेस्ट में Prestige Enterprises के घर',
    intro_h='एक घर, जिसका इंतज़ार सही लगता है',
    intro=['रोशनी से भरे कमरे। ब्रांडेड फ़िनिश। ऐसी सुविधाएँ जो निजी क्लब जैसी लगें। Prestige Enterprises उन परिवारों के लिए घर बनाता है जो बाज़ार में सिर्फ़ एक और फ़्लैट नहीं चाहते।',
           'घर सीमित हैं और कीमतें साफ़ हैं। यह घर आपका है या नहीं, यह जानने का सबसे तेज़ तरीका है हमारी टीम के साथ निजी विज़िट।'],
    intro_cta='निजी विज़िट बुक करें',
    pillars=[('pin', 'प्राइम लोकेशन', 'खड़कपाड़ा, कल्याण वेस्ट। प्रमुख स्कूल, अस्पताल और शॉपिंग कुछ ही मिनटों में।'),
             ('crown', 'लग्ज़री लिविंग', 'डिज़ाइनर लॉबी, ब्रांडेड फिटिंग्स, विट्रिफाइड फ़्लोरिंग और एल्युमिनियम फ्रेंच विंडो।'),
             ('leaf', 'आधुनिक सुविधाएँ', 'लैंडस्केप्ड रूफटॉप गार्डन, ओपन जिम, पूल, मिनी थिएटर और हर उम्र के लिए कोर्ट।'),
             ('shield', 'सुरक्षा व्यवस्था', 'कॉमन एरिया में CCTV, सुरक्षित प्रवेश द्वार और पावर बैकअप वाली लिफ़्ट।')],
    about_eye='हमारे बारे में', about_h='आपकी जीवनशैली के <em>अनुरूप घर</em>',
    about=['Prestige Enterprises कल्याण वेस्ट में उन परिवारों के लिए घर बनाता और प्रस्तुत करता है जो अपने घर से अधिक की उम्मीद रखते हैं: बेहतर रोशनी, बेहतर प्लानिंग और बेहतर पड़ोस।',
           'हमारा ऑफिस Prestige One, गोदरेज हिल, खड़कपाड़ा में है। हम इन गलियों, इन इमारतों और इनके दस्तावेज़ों को नज़दीक से जानते हैं, इसलिए हर विज़िट में आपके साथ वह व्यक्ति होता है जिसने साइट को खुद देखा है।',
           'हर घर पारदर्शी कीमत, MahaRERA पंजीकृत दस्तावेज़ों और लिखित लागत विवरण के साथ दिया जाता है।'],
    about_alt='कल्याण वेस्ट में Prestige Gold आवासीय टावर',
    quote='घर ज़्यादातर परिवारों का सबसे बड़ा फ़ैसला होता है। हमारा काम इसे भरोसेमंद बनाना है।',
    one_view_alt='Prestige One का लिविंग रूम, बालकनी से नदी किनारे सूर्यास्त का नज़ारा',
    one_poster_alt='Prestige One: One Life. One Home.',
    projects_eye='हमारे प्रोजेक्ट्स', projects_h='दो पते, <em>एक ही मानक</em>',
    projects=[('/projects/prestige-gold/', '/img/prestige-tower-day.jpg', 1920, 1080, 'कल्याण वेस्ट में Prestige Gold आवासीय टावर',
               'Prestige Gold', 'आधुनिक <em>1, 2 और 3 BHK</em> घर',
               'मॉड्यूलर किचन, शहर के दृश्य वाली बालकनी और प्रीमियम विट्रिफाइड फ़्लोरिंग के साथ रोशनी से भरे घर। कल्याण वेस्ट में आवासीय और व्यावसायिक जगह।',
               'Prestige Gold देखें'),
              ('/projects/prestige-one/', '/img/Prestige%20One%20Tower%20in%20Daylight.png', 1011, 1555, 'कल्याण में Prestige One आवासीय टावर',
               'Prestige One', '<em>गोदरेज हिल</em> की पहचान',
               'आकर्षक बालकनियों वाला शानदार टावर, जो खड़कपाड़ा में अलग पहचान रखता है। एलीट 5 BHK घर, जिनकी जानकारी गंभीर खरीदारों को निजी तौर पर दी जाती है।',
               'Prestige One देखें')],
    amen_eye='सुविधाएँ', amen_h='आराम, सेहत और खेल, <em>घर के पास ही</em>',
    amen_lead='सुकून भरी सुबह, सक्रिय शाम और परिवार के साथ वीकेंड के लिए बनाई गई जगहें, सब कुछ सोसाइटी के भीतर।',
    amen_names=['स्विमिंग पूल', 'क्रिकेट प्रैक्टिस पिच', 'गेम्स लाउंज', 'लाइब्रेरी', 'मिनी थिएटर', 'पिकलबॉल कोर्ट', 'रेज़िडेंट्स लाउंज', 'फ़िटनेस सेंटर'],
    roof_eye='ख़ास सुविधा', roof_h='<em>298 वर्ग मीटर</em> का रूफटॉप गार्डन',
    roof_p='दोनों विंग्स में 45.85 मीटर तक फैला यह टेरेस शहर के ऊपर एक निजी आरामगाह है, जहाँ पानी, छाँव, हरियाली और टहलने की जगह है।',
    roof_feats=[('झरने के साथ वॉटर बॉडी', '3.00 × 4.50 मी'), ('बैठने के लिए दो गज़ेबो', 'हर एक 3.00 × 3.00 मी'),
                ('ओपन-एयर जिम', '4.50 × 5.00 मी'), ('पाथवे के साथ प्लांटिंग एरिया', '4.50 × 6.00 मी'),
                ('पत्थर और लकड़ी के डेक का सेंट्रल वॉकवे', '2.00 मी चौड़ा'), ('लिफ़्ट और सीढ़ी से सीधी पहुँच', 'विंग A और B')],
    roof_note='माप प्लान के अनुसार अनुमानित हैं।',
    roof_cta='RERA एरिया प्लान डाउनलोड करें',
    roof_alt='वॉटर बॉडी, गज़ेबो, ओपन जिम और वॉकवे वाला रूफटॉप गार्डन',
    spec_eye='स्पेसिफ़िकेशन और सुरक्षा', spec_h='बारीकी से तैयार, <em>हर समय सुरक्षित</em>',
    spec_h1='स्पेसिफ़िकेशन',
    specs=['डेकोरेटिव प्रवेश द्वार और डिज़ाइनर लॉबी', 'पूरे घर में ब्रांडेड विट्रिफाइड फ़्लोरिंग',
           'पाउडर-कोटेड एल्युमिनियम फ्रेंच विंडो', 'ब्रांडेड फिटिंग्स के साथ डिज़ाइनर बाथरूम',
           'बेडरूम, मुख्य द्वार और बाथरूम के लिए लकड़ी के दरवाज़े', 'पर्याप्त पार्किंग'],
    spec_h2='सुरक्षा व्यवस्था',
    security=['कॉमन एरिया में CCTV निगरानी', 'सुरक्षित, गेटेड प्रवेश', 'पावर बैकअप के साथ ब्रांडेड लिफ़्ट',
              'रोशन लॉबी, कॉरिडोर और पार्किंग'],
    spec_alt='स्पेसिफ़िकेशन और सुविधाएँ: प्रवेश द्वार, लिफ़्ट, पार्किंग, लॉबी, फ़्लोरिंग, CCTV और बाथरूम',
    price_eye='घर और कीमतें', price_h='अपना घर चुनें, <em>पूरी स्पष्टता के साथ</em>',
    price_p='हर कॉन्फ़िगरेशन की शुरुआती कीमत और RERA कारपेट एरिया। हमारी टीम मौजूदा उपलब्धता और विस्तृत लागत विवरण साझा करेगी।',
    area_label='RERA क्षेत्रफल', details='घर की विशेषताएँ', starting='शुरुआती कीमत', onwards='से शुरू · प्रीमियम और कॉर्नर यूनिट अनुरोध पर',
    enquire='पूछताछ करें', tap='देखने के लिए टैप करें', sqft='वर्ग फुट',
    units=[('1 BHK', '404–519', '₹55,00,000', '/img/plans/1bhk-3d.webp', '1 BHK 3D फ़्लोर प्लान',
            ['लिविंग और डाइनिंग रूम', 'अटैच्ड बाथ के साथ बेडरूम', 'मॉड्यूलर किचन की सुविधा', 'शहर के दृश्य वाली बालकनी', 'यूटिलिटी / ड्राई बालकनी', 'प्रीमियम विट्रिफाइड फ़्लोरिंग']),
           ('2 BHK', '577–721', '₹75,00,000', '/img/plans/2bhk-layout.webp', '2 BHK फ़्लोर प्लान',
            ['विशाल लिविंग और डाइनिंग', 'अटैच्ड बाथ के साथ मास्टर बेडरूम', 'कॉमन बाथ के साथ दूसरा बेडरूम', 'मॉड्यूलर किचन और ड्राई बालकनी', 'दो बालकनी', 'UPVC स्लाइडिंग विंडो']),
           ('3 BHK', '999.4–1,001.4', '₹1,40,00,000', '', '3 BHK फ़्लोर प्लान',
            ['पूरे साइट पर उपलब्ध', 'बड़ा लिविंग और डाइनिंग', 'वॉक-इन वार्डरोब के साथ मास्टर बेडरूम', 'दो अतिरिक्त बेडरूम', 'तीन बाथरूम (दो अटैच्ड)', 'दो फुल-साइज़ बालकनी', 'अलग पूजा कक्ष'])],
    plan_req='लेआउट अनुरोध पर',
    more_eye='और विकल्प',
    more_h='कमर्शियल, 4 BHK और 5 BHK',
    more_p='प्रकाशित 1, 2 और 3 BHK घरों के अलावा अलग विकल्प। विवरण गंभीर खरीदारों के साथ निजी तौर पर साझा किए जाते हैं।',
    more_units=[
        ('कमर्शियल', 'CO', 'ग्राउंड और पोडियम लेवल', 'अनुरोध पर',
         ['रिटेल और ऑफिस फ्रंटेज', 'कल्याण वेस्ट का व्यस्त कॉरिडोर', 'ब्रोशर और साइज़ अनुरोध पर', 'कीमत लिखित में साझा'],
         'नमस्ते Prestige Enterprises, मुझे कल्याण वेस्ट में Prestige Gold की कमर्शियल (रिटेल/ऑफिस) जानकारी चाहिए।'),
        ('4 BHK', '4B', 'लेआउट अनुरोध पर', 'अनुरोध पर',
         ['बड़े पारिवारिक लेआउट', 'कई बालकनियाँ', 'प्रीमियम फ़िनिश', 'उपलब्धता निजी तौर पर'],
         'नमस्ते Prestige Enterprises, मुझे कल्याण वेस्ट में 4 BHK घरों की जानकारी चाहिए।'),
        ('5 BHK', '5B', '', 'अनुरोध पर',
         ['Prestige One के एलीट घर', 'विशाल निजी लेआउट', 'गंभीर खरीदारों के साथ निजी', 'साइट विज़िट अनुरोध पर'],
         'नमस्ते Prestige Enterprises, मुझे Prestige One 5 BHK घरों की जानकारी चाहिए।'),
    ],
    more_enquire='जानकारी माँगें',
    price_note='कीमतें और क्षेत्रफल सांकेतिक हैं। बुकिंग से पहले अंतिम कीमत, उपलब्धता, टैक्स, वैधानिक शुल्क और पार्किंग की पुष्टि नवीनतम लिखित लागत विवरण से करें।',
    plans_eye='फ़्लोर प्लान', plans_h='रोज़मर्रा की ज़िंदगी के लिए <em>सोचे-समझे लेआउट</em>',
    plans_p='3D और टॉप-व्यू लेआउट देखें। पूरा आकार देखने के लिए किसी भी प्लान पर टैप करें।',
    plans=[('/img/plans/1bhk-3d.webp', '1 BHK · 3D व्यू', '1 BHK घर', 'बेडरूम, लिविंग, डाइनिंग और किचन एक रोशन, सुविधाजनक लाइन में, दोनों ओर बालकनी के साथ।'),
           ('/img/plans/1bhk-layout.webp', '1 BHK · टॉप व्यू', '1 BHK लेआउट', 'अलग बाथ और पाउडर रूम, यूटिलिटी बालकनी और लिविंग एरिया के पास लाउंज बालकनी।'),
           ('/img/plans/2bhk-layout.webp', '2 BHK · टॉप व्यू', '2 BHK लेआउट', 'विशाल लिविंग और डाइनिंग के चारों ओर दो बेडरूम, दो बाथरूम और तीन बालकनी।')],
    plans_btn='Prestige Gold की जानकारी देखें',
    loc_eye='प्राइम लोकेशन', loc_h='ज़रूरत की हर चीज़, <em>कुछ ही मिनटों में</em>',
    loc_p='खड़कपाड़ा कल्याण वेस्ट के सबसे स्थापित आवासीय इलाकों में से एक है: हरा-भरा, अच्छी कनेक्टिविटी वाला और भरोसेमंद स्कूलों, अस्पतालों व शॉपिंग से घिरा हुआ।',
    loc_titles={'health': 'अस्पताल और स्वास्थ्य सेवा', 'shop': 'मॉल और मनोरंजन', 'school': 'स्कूल और कॉलेज'},
    km='किमी', mins='मिनट', loc_note='दूरी और समय अनुमानित हैं और ट्रैफ़िक के अनुसार बदल सकते हैं।',
    faq_eye='सवाल-जवाब', faq_h='आम <em>सवाल</em>',
    guides_eye='गाइड', guides_h='<em>कल्याण में प्रॉपर्टी खरीदने</em> पर सीधे जवाब',
    guides_btn='सभी गाइड देखें', guides_min='{n} मिनट में पढ़ें',
    guide_cats={'buying': 'खरीद', 'costs': 'खर्च', 'legal': 'कानूनी जाँच', 'finance': 'वित्त', 'tax': 'टैक्स', 'investing': 'निवेश'},
    faq=[('घर कहाँ स्थित हैं?', 'कल्याण वेस्ट में, खड़कपाड़ा और गोदरेज हिल के आसपास। हमारा ऑफिस Prestige One, गोदरेज हिल, खड़कपाड़ा, कल्याण 421301 में है।'),
         ('कौन-से कॉन्फ़िगरेशन उपलब्ध हैं?', '1, 2 और 3 BHK घर, जिनकी शुरुआती कीमत ₹55 लाख से है, साथ ही कमर्शियल जगह भी। 4 BHK और एलीट 5 BHK घर अनुरोध पर निजी तौर पर उपलब्ध हैं।'),
         ('निवासियों के लिए कौन-सी सुविधाएँ हैं?', 'वॉटर बॉडी, गज़ेबो और ओपन जिम के साथ 298 वर्ग मीटर का रूफटॉप गार्डन, साथ ही स्विमिंग पूल, फ़िटनेस सेंटर, मिनी थिएटर, गेम्स लाउंज, लाइब्रेरी और स्पोर्ट्स कोर्ट।'),
         ('सुरक्षा के लिए क्या व्यवस्था है?', 'कॉमन एरिया में CCTV निगरानी, सुरक्षित गेटेड प्रवेश, रोशन कॉमन स्पेस और पावर बैकअप वाली ब्रांडेड लिफ़्ट।'),
         ('क्या प्रोजेक्ट RERA पंजीकृत है?', f'हाँ। MahaRERA पंजीकरण संख्या {RERA}। बुकिंग से पहले हम पंजीकरण विवरण और दस्तावेज़ साझा करते हैं।'),
         ('साइट विज़िट कैसे बुक करें?', 'WhatsApp पर संदेश भेजें या +91 96895 57788 पर कॉल करें। हम आपकी सुविधा के अनुसार समय तय करेंगे और मौजूदा उपलब्धता बताएँगे।')],
    contact_eye='संपर्क', contact_h='<em>निजी साइट विज़िट</em> बुक करें',
    contact_p='हमें बताएँ कि आप कैसा घर चाहते हैं। हमारी खड़कपाड़ा टीम मौजूदा उपलब्धता, फ़्लोर प्लान और लिखित लागत विवरण साझा करेगी और आपकी सुविधा से विज़िट तय करेगी।',
    addr='ऑफिस', phone='फ़ोन', email='ईमेल', wa_btn='WhatsApp पर बात करें', call='कॉल करें', maps='Google Maps में खोलें',
    wa_text='नमस्ते Prestige Enterprises, मैं कल्याण वेस्ट में साइट विज़िट बुक करना और मौजूदा उपलब्धता जानना चाहता/चाहती हूँ।',
    foot_tag='कल्याण वेस्ट, महाराष्ट्र में सोच-समझकर बनाए गए घर।',
    foot_explore='देखें', foot_projects='प्रोजेक्ट्स', foot_contact='संपर्क',
    foot_links=[('#about', 'हमारे बारे में'), ('#amenities', 'सुविधाएँ'), ('#plans', 'फ़्लोर प्लान'), ('#location', 'लोकेशन'), ('/blog/', 'गाइड'), ('#contact', 'संपर्क')],
    privacy='गोपनीयता नीति', rera_verified='सत्यापित और पंजीकृत',
    disclaimer='तस्वीरें केवल प्रस्तुति के लिए कलात्मक चित्रण हैं। सुविधाएँ, स्पेसिफ़िकेशन, कीमतें और दूरियाँ सांकेतिक हैं और बदल सकती हैं; बुकिंग से पहले लिखित में पुष्टि करें।',
    rights='© 2026 Prestige Enterprises. सर्वाधिकार सुरक्षित।',
    float_wa='WhatsApp',
)

T['mr'] = dict(
    title='कल्याण वेस्टमध्ये लक्झरी घरे | Prestige Enterprises',
    desc='खडकपाडा, कल्याण वेस्टमधील घरे: प्राइम लोकेशन, लक्झरी लिव्हिंग, आधुनिक सुविधा आणि चोवीस तास सुरक्षा. 1, 2 आणि 3 BHK ₹55 लाखांपासून. खासगी साइट व्हिजिट बुक करा.',
    nav_label='मुख्य मेनू', menu_open='मेनू उघडा', hero_label='कल्याण वेस्टमधील Prestige Enterprises ची घरे',
    intro_h='एक घर, ज्याची वाट बघणे योग्य वाटते',
    intro=['प्रकाशमान खोल्या. ब्रँडेड फिनिश. अशा सुविधा ज्या खासगी क्लबसारख्या वाटतात. Prestige Enterprises अशा कुटुंबांसाठी घरे उभारते, ज्यांना बाजारातील आणखी एक फ्लॅट नको असतो.',
           'घरे मर्यादित आहेत आणि किंमती स्पष्ट आहेत. हे घर तुमचे आहे का, हे जाणून घेण्याचा सर्वात जलद मार्ग म्हणजे आमच्या टीमसोबत खासगी व्हिजिट.'],
    intro_cta='खासगी व्हिजिट बुक करा',
    pillars=[('pin', 'प्राइम लोकेशन', 'खडकपाडा, कल्याण वेस्ट. नामांकित शाळा, रुग्णालये आणि शॉपिंग काही मिनिटांवर.'),
             ('crown', 'लक्झरी लिव्हिंग', 'डिझायनर लॉबी, ब्रँडेड फिटिंग्ज, व्हिट्रिफाइड फ्लोअरिंग आणि ॲल्युमिनियम फ्रेंच विंडो.'),
             ('leaf', 'आधुनिक सुविधा', 'लँडस्केप केलेले रूफटॉप गार्डन, ओपन जिम, पूल, मिनी थिएटर आणि सर्व वयोगटांसाठी कोर्ट.'),
             ('shield', 'सुरक्षा व्यवस्था', 'कॉमन एरियात CCTV, सुरक्षित प्रवेशद्वार आणि पॉवर बॅकअप असलेल्या लिफ्ट.')],
    about_eye='आमच्याबद्दल', about_h='तुमच्या जीवनशैलीला <em>साजेशी घरे</em>',
    about=['Prestige Enterprises कल्याण वेस्टमध्ये अशा कुटुंबांसाठी घरे उभारते आणि सादर करते, ज्यांना आपल्या घराकडून अधिक अपेक्षा आहेत: अधिक प्रकाश, अधिक चांगले नियोजन आणि अधिक चांगले शेजार.',
           'आमचे कार्यालय Prestige One, गोदरेज हिल, खडकपाडा येथे आहे. आम्ही हे रस्ते, या इमारती आणि त्यांची कागदपत्रे जवळून ओळखतो, त्यामुळे प्रत्येक व्हिजिटमध्ये साइट स्वतः पाहिलेली व्यक्ती तुमच्यासोबत असते.',
           'प्रत्येक घर पारदर्शक किंमत, MahaRERA नोंदणीकृत कागदपत्रे आणि लेखी खर्चपत्रकासह दिले जाते.'],
    about_alt='कल्याण वेस्टमधील Prestige Gold निवासी टॉवर',
    quote='घर हा बहुतेक कुटुंबांचा सर्वात मोठा निर्णय असतो. तो आत्मविश्वासाने घेता यावा, हे आमचे काम आहे.',
    one_view_alt='Prestige One ची लिव्हिंग रूम, बाल्कनीतून नदीकाठचा सूर्यास्त',
    one_poster_alt='Prestige One: One Life. One Home.',
    projects_eye='आमचे प्रकल्प', projects_h='दोन पत्ते, <em>एकच दर्जा</em>',
    projects=[('/projects/prestige-gold/', '/img/prestige-tower-day.jpg', 1920, 1080, 'कल्याण वेस्टमधील Prestige Gold निवासी टॉवर',
               'Prestige Gold', 'आधुनिक <em>1, 2 आणि 3 BHK</em> घरे',
               'मॉड्युलर किचन, शहराचे दृश्य दिसणाऱ्या बाल्कनी आणि प्रीमियम व्हिट्रिफाइड फ्लोअरिंगसह प्रकाशमान घरे. कल्याण वेस्टमध्ये निवासी आणि व्यावसायिक जागा.',
               'Prestige Gold पाहा'),
              ('/projects/prestige-one/', '/img/Prestige%20One%20Tower%20in%20Daylight.png', 1011, 1555, 'कल्याणमधील Prestige One निवासी टॉवर',
               'Prestige One', '<em>गोदरेज हिल</em>ची ओळख',
               'आकर्षक बाल्कनी असलेला देखणा टॉवर, जो खडकपाड्यात वेगळी ओळख निर्माण करतो. एलीट 5 BHK घरे, ज्यांची माहिती गंभीर खरेदीदारांना खासगीरीत्या दिली जाते.',
               'Prestige One पाहा')],
    amen_eye='सुविधा', amen_h='विश्रांती, आरोग्य आणि खेळ, <em>घराजवळच</em>',
    amen_lead='निवांत सकाळ, उत्साही संध्याकाळ आणि कुटुंबासोबतच्या वीकेंडसाठी तयार केलेल्या जागा, सर्व काही सोसायटीच्या आत.',
    amen_names=['स्विमिंग पूल', 'क्रिकेट प्रॅक्टिस पिच', 'गेम्स लाउंज', 'वाचनालय', 'मिनी थिएटर', 'पिकलबॉल कोर्ट', 'रेसिडेंट्स लाउंज', 'फिटनेस सेंटर'],
    roof_eye='खास सुविधा', roof_h='<em>298 चौ. मी.</em> चे रूफटॉप गार्डन',
    roof_p='दोन्ही विंग्जमध्ये 45.85 मीटरपर्यंत पसरलेले हे टेरेस शहराच्या वरचे खासगी विश्रांतीस्थान आहे, जिथे पाणी, सावली, हिरवाई आणि फिरण्यासाठी जागा आहे.',
    roof_feats=[('धबधब्यासह वॉटर बॉडी', '3.00 × 4.50 मी'), ('बसण्यासाठी दोन गझेबो', 'प्रत्येकी 3.00 × 3.00 मी'),
                ('ओपन-एअर जिम', '4.50 × 5.00 मी'), ('पाथवेसह प्लांटिंग एरिया', '4.50 × 6.00 मी'),
                ('दगड आणि लाकडी डेकचा मध्यवर्ती वॉकवे', '2.00 मी रुंद'), ('लिफ्ट आणि जिन्याने थेट प्रवेश', 'विंग A आणि B')],
    roof_note='मापे प्लॅननुसार अंदाजे आहेत.',
    roof_cta='RERA एरिया प्लॅन डाउनलोड करा',
    roof_alt='वॉटर बॉडी, गझेबो, ओपन जिम आणि वॉकवे असलेले रूफटॉप गार्डन',
    spec_eye='स्पेसिफिकेशन आणि सुरक्षा', spec_h='काळजीपूर्वक पूर्ण केलेले, <em>सतत सुरक्षित</em>',
    spec_h1='स्पेसिफिकेशन',
    specs=['डेकोरेटिव्ह प्रवेशद्वार आणि डिझायनर लॉबी', 'संपूर्ण घरात ब्रँडेड व्हिट्रिफाइड फ्लोअरिंग',
           'पावडर-कोटेड ॲल्युमिनियम फ्रेंच विंडो', 'ब्रँडेड फिटिंग्जसह डिझायनर बाथरूम',
           'बेडरूम, मुख्य दरवाजा आणि बाथरूमसाठी लाकडी दरवाजे', 'पुरेशी पार्किंग'],
    spec_h2='सुरक्षा व्यवस्था',
    security=['कॉमन एरियात CCTV देखरेख', 'सुरक्षित, गेटेड प्रवेश', 'पॉवर बॅकअपसह ब्रँडेड लिफ्ट',
              'प्रकाशमान लॉबी, कॉरिडॉर आणि पार्किंग'],
    spec_alt='स्पेसिफिकेशन आणि सुविधा: प्रवेशद्वार, लिफ्ट, पार्किंग, लॉबी, फ्लोअरिंग, CCTV आणि बाथरूम',
    price_eye='घरे आणि किंमती', price_h='तुमचे घर निवडा, <em>पूर्ण स्पष्टतेने</em>',
    price_p='प्रत्येक कॉन्फिगरेशनची सुरुवातीची किंमत आणि RERA कार्पेट एरिया. आमची टीम सध्याची उपलब्धता आणि सविस्तर खर्चपत्रक देईल.',
    area_label='RERA क्षेत्रफळ', details='घराची वैशिष्ट्ये', starting='सुरुवातीची किंमत', onwards='पासून · प्रीमियम आणि कॉर्नर युनिट विनंतीवर',
    enquire='चौकशी करा', tap='पाहण्यासाठी टॅप करा', sqft='चौ. फूट',
    units=[('1 BHK', '404–519', '₹55,00,000', '/img/plans/1bhk-3d.webp', '1 BHK 3D फ्लोअर प्लॅन',
            ['लिव्हिंग आणि डायनिंग रूम', 'अटॅच्ड बाथसह बेडरूम', 'मॉड्युलर किचनची सुविधा', 'शहराचे दृश्य असलेली बाल्कनी', 'युटिलिटी / ड्राय बाल्कनी', 'प्रीमियम व्हिट्रिफाइड फ्लोअरिंग']),
           ('2 BHK', '577–721', '₹75,00,000', '/img/plans/2bhk-layout.webp', '2 BHK फ्लोअर प्लॅन',
            ['प्रशस्त लिव्हिंग आणि डायनिंग', 'अटॅच्ड बाथसह मास्टर बेडरूम', 'कॉमन बाथसह दुसरी बेडरूम', 'मॉड्युलर किचन आणि ड्राय बाल्कनी', 'दोन बाल्कनी', 'UPVC स्लायडिंग विंडो']),
           ('3 BHK', '999.4–1,001.4', '₹1,40,00,000', '', '3 BHK फ्लोअर प्लॅन',
            ['संपूर्ण साइटवर उपलब्ध', 'मोठे लिव्हिंग आणि डायनिंग', 'वॉक-इन वॉर्डरोबसह मास्टर बेडरूम', 'दोन अतिरिक्त बेडरूम', 'तीन बाथरूम (दोन अटॅच्ड)', 'दोन पूर्ण आकाराच्या बाल्कनी', 'स्वतंत्र पूजा कक्ष'])],
    plan_req='लेआउट विनंतीवर',
    more_eye='आणखी पर्याय',
    more_h='कमर्शियल, 4 BHK आणि 5 BHK',
    more_p='प्रकाशित 1, 2 आणि 3 BHK घरांखेरीज वेगळे पर्याय. तपशील गंभीर खरेदीदारांसोबत खासगीरीत्या शेअर केले जातात.',
    more_units=[
        ('कमर्शियल', 'CO', 'ग्राउंड आणि पोडियम लेव्हल', 'विनंतीवर',
         ['रिटेल आणि ऑफिस फ्रंटेज', 'कल्याण वेस्टचा व्यस्त कॉरिडॉर', 'ब्रोशर आणि आकार विनंतीवर', 'किंमत लेखी दिली जाते'],
         'नमस्कार Prestige Enterprises, मला कल्याण वेस्टमधील Prestige Gold कमर्शियल (रिटेल/ऑफिस) माहिती हवी आहे.'),
        ('4 BHK', '4B', 'लेआउट विनंतीवर', 'विनंतीवर',
         ['मोठे कौटुंबिक लेआउट', 'अनेक बाल्कनी', 'प्रीमियम फिनिश', 'उपलब्धता खासगीरीत्या'],
         'नमस्कार Prestige Enterprises, मला कल्याण वेस्टमधील 4 BHK घरांची माहिती हवी आहे.'),
        ('5 BHK', '5B', '', 'विनंतीवर',
         ['Prestige One मधील एलीट घरे', 'प्रशस्त खासगी लेआउट', 'गंभीर खरेदीदारांसोबत खासगी', 'साइट भेट विनंतीवर'],
         'नमस्कार Prestige Enterprises, मला Prestige One 5 BHK घरांची माहिती हवी आहे.'),
    ],
    more_enquire='माहिती मागवा',
    price_note='किंमती आणि क्षेत्रफळ सूचक आहेत. बुकिंगपूर्वी अंतिम किंमत, उपलब्धता, कर, वैधानिक शुल्क आणि पार्किंगची खात्री अद्ययावत लेखी खर्चपत्रकातून करा.',
    plans_eye='फ्लोअर प्लॅन', plans_h='रोजच्या जगण्यासाठी <em>विचारपूर्वक लेआउट</em>',
    plans_p='3D आणि टॉप-व्ह्यू लेआउट पाहा. पूर्ण आकारात पाहण्यासाठी कोणत्याही प्लॅनवर टॅप करा.',
    plans=[('/img/plans/1bhk-3d.webp', '1 BHK · 3D व्ह्यू', '1 BHK घर', 'बेडरूम, लिव्हिंग, डायनिंग आणि किचन एका प्रकाशमान, सोयीस्कर रेषेत, दोन्ही टोकांना बाल्कनीसह.'),
           ('/img/plans/1bhk-layout.webp', '1 BHK · टॉप व्ह्यू', '1 BHK लेआउट', 'स्वतंत्र बाथ आणि पावडर रूम, युटिलिटी बाल्कनी आणि लिव्हिंग एरियाजवळ लाउंज बाल्कनी.'),
           ('/img/plans/2bhk-layout.webp', '2 BHK · टॉप व्ह्यू', '2 BHK लेआउट', 'प्रशस्त लिव्हिंग आणि डायनिंगभोवती दोन बेडरूम, दोन बाथरूम आणि तीन बाल्कनी.')],
    plans_btn='Prestige Gold ची माहिती पाहा',
    loc_eye='प्राइम लोकेशन', loc_h='गरजेचे सर्व काही, <em>काही मिनिटांवर</em>',
    loc_p='खडकपाडा हा कल्याण वेस्टमधील सर्वात प्रस्थापित निवासी परिसरांपैकी एक आहे: हिरवागार, उत्तम कनेक्टिव्हिटी असलेला आणि विश्वासार्ह शाळा, रुग्णालये व शॉपिंगने वेढलेला.',
    loc_titles={'health': 'रुग्णालये आणि आरोग्यसेवा', 'shop': 'मॉल आणि मनोरंजन', 'school': 'शाळा आणि महाविद्यालये'},
    km='किमी', mins='मिनिटे', loc_note='अंतर आणि वेळ अंदाजे आहेत आणि ट्रॅफिकनुसार बदलू शकतात.',
    faq_eye='प्रश्नोत्तरे', faq_h='नेहमीचे <em>प्रश्न</em>',
    guides_eye='मार्गदर्शक', guides_h='<em>कल्याणमधील मालमत्ता खरेदी</em>वर थेट उत्तरे',
    guides_btn='सर्व मार्गदर्शक पाहा', guides_min='{n} मिनिटांत वाचा',
    guide_cats={'buying': 'खरेदी', 'costs': 'खर्च', 'legal': 'कायदेशीर तपासणी', 'finance': 'वित्त', 'tax': 'कर', 'investing': 'गुंतवणूक'},
    faq=[('घरे कुठे आहेत?', 'कल्याण वेस्टमध्ये, खडकपाडा आणि गोदरेज हिल परिसरात. आमचे कार्यालय Prestige One, गोदरेज हिल, खडकपाडा, कल्याण 421301 येथे आहे.'),
         ('कोणते कॉन्फिगरेशन उपलब्ध आहेत?', '1, 2 आणि 3 BHK घरे, ज्यांची सुरुवातीची किंमत ₹55 लाखांपासून आहे, सोबत कमर्शियल जागाही. 4 BHK आणि एलीट 5 BHK घरे विनंतीवर खासगीरीत्या उपलब्ध आहेत.'),
         ('रहिवाशांसाठी कोणत्या सुविधा आहेत?', 'वॉटर बॉडी, गझेबो आणि ओपन जिमसह 298 चौ. मी.चे रूफटॉप गार्डन, तसेच स्विमिंग पूल, फिटनेस सेंटर, मिनी थिएटर, गेम्स लाउंज, वाचनालय आणि स्पोर्ट्स कोर्ट.'),
         ('सुरक्षेसाठी कोणती व्यवस्था आहे?', 'कॉमन एरियात CCTV देखरेख, सुरक्षित गेटेड प्रवेश, प्रकाशमान कॉमन जागा आणि पॉवर बॅकअप असलेल्या ब्रँडेड लिफ्ट.'),
         ('प्रकल्प RERA नोंदणीकृत आहे का?', f'हो. MahaRERA नोंदणी क्रमांक {RERA}. बुकिंगपूर्वी आम्ही नोंदणीचा तपशील आणि कागदपत्रे देतो.'),
         ('साइट व्हिजिट कशी बुक करावी?', 'WhatsApp वर संदेश पाठवा किंवा +91 96895 57788 वर कॉल करा. आम्ही तुमच्या सोयीची वेळ निश्चित करू आणि सध्याची उपलब्धता सांगू.')],
    contact_eye='संपर्क', contact_h='<em>खासगी साइट व्हिजिट</em> बुक करा',
    contact_p='तुम्हाला कसे घर हवे आहे ते सांगा. आमची खडकपाडा टीम सध्याची उपलब्धता, फ्लोअर प्लॅन आणि लेखी खर्चपत्रक देईल आणि तुमच्या सोयीनुसार व्हिजिट ठरवेल.',
    addr='कार्यालय', phone='फोन', email='ईमेल', wa_btn='WhatsApp वर बोला', call='कॉल करा', maps='Google Maps मध्ये उघडा',
    wa_text='नमस्कार Prestige Enterprises, मला कल्याण वेस्टमध्ये साइट व्हिजिट बुक करायची आहे आणि सध्याची उपलब्धता जाणून घ्यायची आहे.',
    foot_tag='कल्याण वेस्ट, महाराष्ट्रातील विचारपूर्वक नियोजित घरे.',
    foot_explore='पाहा', foot_projects='प्रकल्प', foot_contact='संपर्क',
    foot_links=[('#about', 'आमच्याबद्दल'), ('#amenities', 'सुविधा'), ('#plans', 'फ्लोअर प्लॅन'), ('#location', 'लोकेशन'), ('/blog/', 'मार्गदर्शक'), ('#contact', 'संपर्क')],
    privacy='गोपनीयता धोरण', rera_verified='सत्यापित आणि नोंदणीकृत',
    disclaimer='चित्रे केवळ सादरीकरणासाठी कलात्मक प्रतिमा आहेत. सुविधा, स्पेसिफिकेशन, किंमती आणि अंतरे सूचक असून बदलू शकतात; बुकिंगपूर्वी लेखी खात्री करा.',
    rights='© 2026 Prestige Enterprises. सर्व हक्क राखीव.',
    float_wa='WhatsApp',
)


def eye(txt, cls=''):
    return f'<div class="eye {cls}"><span class="eye-line"></span><span class="eye-txt">{e(txt)}</span></div>'


def head(l, t):
    p = PREFIX[l]
    canonical = SITE + p + '/'
    alts = ''.join(f'<link rel="alternate" hreflang="{k}" href="{SITE}{PREFIX[k]}/">' for k in LANGS)
    alts += f'<link rel="alternate" hreflang="x-default" href="{SITE}/">'
    fonts = 'family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400;1,600&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700'
    if l != 'en':
        fonts += '&family=Noto+Sans+Devanagari:wght@300;400;500;600&family=Noto+Serif+Devanagari:wght@300;400;500'
    agent = {'@type': 'RealEstateAgent', '@id': SITE + '/#agent', 'name': 'Prestige Enterprises', 'url': SITE + '/',
             'image': SITE + '/img/logo.png', 'logo': SITE + '/img/logo.png', 'telephone': PHONE_TEL, 'email': EMAIL,
             'address': {'@type': 'PostalAddress', 'streetAddress': 'Prestige One, Godrej Hill, Khadakpada', 'addressLocality': 'Kalyan',
                         'addressRegion': 'Maharashtra', 'postalCode': '421301', 'addressCountry': 'IN'},
             'hasMap': MAPS_URL, 'areaServed': {'@type': 'City', 'name': 'Kalyan'}, 'knowsLanguage': ['en', 'hi', 'mr']}
    website = {'@type': 'WebSite', '@id': SITE + '/#website', 'url': SITE + '/', 'name': 'Prestige Enterprises',
               'inLanguage': ['en-IN', 'hi-IN', 'mr-IN'], 'publisher': {'@id': SITE + '/#agent'}}
    webpage = {'@type': 'WebPage', '@id': canonical + '#webpage', 'url': canonical, 'name': t['title'], 'description': t['desc'],
               'inLanguage': HTML_LANG[l], 'isPartOf': {'@id': SITE + '/#website'}}
    faq = {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': ans}} for q, ans in t['faq']]}
    ld = json.dumps({'@context': 'https://schema.org', '@graph': [agent, website, webpage, faq]}, ensure_ascii=False, separators=(',', ':'))
    return (
        f'<!doctype html>\n<html lang="{HTML_LANG[l]}">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        f'<title>{e(t["title"])}</title>\n<meta name="description" content="{a(t["desc"])}">\n'
        '<meta name="author" content="Munit Lulla">\n<meta name="robots" content="index, follow, max-image-preview:large">\n'
        f'<link rel="canonical" href="{canonical}">\n{alts}\n<meta name="theme-color" content="#0B1220">\n'
        f'<meta property="og:type" content="website"><meta property="og:site_name" content="Prestige Enterprises"><meta property="og:locale" content="{LOCALE[l]}">'
        f'<meta property="og:url" content="{canonical}"><meta property="og:title" content="{a(t["title"])}"><meta property="og:description" content="{a(t["desc"])}">'
        f'<meta property="og:image" content="{SITE}/img/og-default.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
        '<meta name="twitter:card" content="summary_large_image">\n'
        '<link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" type="image/png" sizes="192x192" href="/icon-192.png"><link rel="apple-touch-icon" href="/apple-touch-icon.png">\n'
        f'<link rel="preconnect" href="{VIDEO_HOST}" crossorigin>\n'
        '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        f'<link href="https://fonts.googleapis.com/css2?{fonts}&display=swap" rel="stylesheet">\n'
        f'<link rel="stylesheet" href="/assets/site.css?v={ASSET_VER}">\n'
        f'<script type="application/ld+json">{ld}</script>\n</head>\n'
    )


def nav(l, t):
    p = PREFIX[l]
    langs = ''.join(
        f'<a href="{PREFIX[k]}/" hreflang="{k}" lang="{k}"' + (' aria-current="true"' if k == l else '') + f'>{n}</a>'
        for k, n in (('en', 'EN'), ('hi', 'हिं'), ('mr', 'मराठी')))
    return (
        f'<body class="home-video-page">\n<div id="prog"></div>\n'
        f'<nav id="nav" class="home-hero-nav" aria-label="{a(t["nav_label"])}">'
        f'<button class="nav-ham" id="navHam" type="button" aria-label="{a(t["menu_open"])}" aria-expanded="false" aria-controls="mnav"><span></span><span></span><span></span></button>'
        f'<a class="nav-logo home-wordmark" href="{p}/" aria-label="Prestige Enterprises">'
        '<img class="home-logo-dark" src="/img/logo-on-dark.png" width="248" height="83" alt="Prestige Enterprises" decoding="async">'
        '<img class="home-logo-light" src="/img/logo.png" width="248" height="83" alt="" aria-hidden="true" decoding="async"></a>'
        f'<div class="nav-r nav-r-home-fallback" hidden aria-hidden="true"><div class="lang" role="group">{langs}</div></div></nav>\n'
        '<div class="mnav" id="mnav" hidden aria-hidden="true"></div>\n'
    )


def hero(t):
    return (
        f'<main id="main"><section id="home" class="hero hero-video-hero" aria-label="{a(t["hero_label"])}">\n'
        f'  <video class="hero-video" id="heroVideo" src="{VIDEO}" autoplay muted loop playsinline webkit-playsinline preload="auto" disablepictureinpicture disableremoteplayback x-webkit-airplay="deny" aria-hidden="true" tabindex="-1"></video>\n'
        '  <div class="hero-video-shade" aria-hidden="true"></div>\n</section>\n'
    )


def intro(t):
    paras = ''.join(f'<p>{e(x)}</p>' for x in t['intro'])
    pillars = ''.join(
        f'<article class="home-pillar">{icon(ic, "home-pillar-icon")}<h3>{e(h)}</h3><p>{e(x)}</p></article>'
        for ic, h, x in t['pillars'])
    return (
        '<section class="home-seo-intro home-passion" aria-labelledby="home-seo-title"><div class="in home-passion-in">'
        f'<h1 class="home-passion-title" id="home-seo-title">{e(t["intro_h"])}</h1>'
        f'<div class="home-passion-copy">{paras}</div>'
        f'<p class="home-passion-cta"><button class="btn-o dark enquire-trigger" type="button" data-enquiry-intent="site-visit"><span>{e(t["intro_cta"])}</span>{icon("arrow")}</button></p>'
        '</div>'
        f'<div class="in home-pillars">{pillars}</div></section>\n'
    )


def about(t):
    body = ''.join(f'<p>{e(x)}</p>' for x in t['about'])
    return (
        '<section class="sec home-about" id="about"><div class="in about-grid"><div>'
        f'{eye(t["about_eye"])}<h2 class="dh">{t["about_h"]}</h2><div class="about-body" style="margin-top:30px">{body}</div></div>'
        f'<div><div class="about-photo"><img src="/img/about.jpg" width="900" height="1125" loading="lazy" alt="{a(t["about_alt"])}"></div>'
        f'<div class="about-quote"><p>{e(t["quote"])}</p><cite>Prestige Enterprises</cite></div></div></div></section>\n'
    )


def zoom_img(src, w, h, alt, t, cls):
    return (f'<div class="{cls} plan-img-wrap" data-full="{src}" data-title="{a(alt)}" role="button" tabindex="0" aria-label="{a(alt)}">'
            f'<img src="{src}" width="{w}" height="{h}" loading="lazy" alt="{a(alt)}">'
            f'<span class="plan-zoom-hint">{icon("zoom")}<span>{e(t["tap"])}</span></span></div>')


def projects(t):
    rows = ''
    for i, (href, img, w, h, alt, name, title, lead, btn) in enumerate(t['projects']):
        landscape = ' is-landscape' if w > h else ''
        flip = ' is-flipped' if i % 2 else ''
        is_one = href == '/projects/prestige-one/'
        inline = zoom_img('/img/prestige-one/riverside-interior.webp', 1774, 887, t['one_view_alt'], t, 'project-inline-media') if is_one else ''
        rows += (
            f'<div class="in project-showcase-grid home-project{flip}"><div class="project-showcase-media{landscape}">'
            f'<img src="{img}" width="{w}" height="{h}" loading="lazy" alt="{a(alt)}"></div>'
            f'<div class="project-showcase-copy">{eye(name)}<h3 class="dh">{title}</h3><p class="lead">{e(lead)}</p>{inline}'
            f'<a class="btn-o dark" href="{href}"><span>{e(btn)}</span>{icon("arrow")}</a></div></div>'
        )
        if is_one:
            rows += f'<div class="in project-banner">{zoom_img("/img/prestige-one/one-life-one-home.webp", 1774, 887, t["one_poster_alt"], t, "project-banner-media")}</div>'
    return (
        '<section class="sec project-showcase home-projects" id="projects"><span id="types" class="home-anchor" aria-hidden="true"></span>'
        f'<div class="in home-sec-head">{eye(t["projects_eye"], "eye-center")}<h2 class="dh">{t["projects_h"]}</h2></div>'
        f'{rows}</section>\n'
    )


def amenities(t):
    tiles = ''.join(
        f'<figure class="amen-tile"><img src="/img/amenities/{img}.webp" width="456" height="384" loading="lazy" alt="{a(name)}"><figcaption>{e(name)}</figcaption></figure>'
        for img, name in zip(AMENITY_IMGS, t['amen_names']))
    feats = ''.join(f'<li><span>{e(f)}</span><b>{e(d)}</b></li>' for f, d in t['roof_feats'])
    specs = ''.join(f'<li>{e(x)}</li>' for x in t['specs'])
    sec = ''.join(f'<li>{e(x)}</li>' for x in t['security'])
    return (
        '<section class="sec home-amenities" id="amenities"><span id="services" class="home-anchor" aria-hidden="true"></span>'
        f'<div class="in home-sec-head">{eye(t["amen_eye"], "eye-center")}<h2 class="dh">{t["amen_h"]}</h2><p class="lead">{e(t["amen_lead"])}</p></div>'
        f'<div class="in amen-grid">{tiles}</div>'
        '<div class="in amen-feature">'
        f'<div class="amen-feature-media plan-img-wrap" data-full="/img/amenities/rooftop-garden.webp" data-title="{a(t["roof_alt"])}" role="button" tabindex="0" aria-label="{a(t["roof_alt"])}">'
        f'<img src="/img/amenities/rooftop-garden.webp" width="1024" height="682" loading="lazy" alt="{a(t["roof_alt"])}">'
        f'<span class="plan-zoom-hint">{icon("zoom")}<span>{e(t["tap"])}</span></span></div>'
        f'<div class="amen-feature-copy">{eye(t["roof_eye"])}<h3 class="dh">{t["roof_h"]}</h3><p class="lead">{e(t["roof_p"])}</p>'
        f'<ul class="amen-dims">{feats}</ul><p class="amen-note">{e(t["roof_note"])}</p>'
        f'<div class="amen-feature-actions"><button class="btn-o dark enquire-trigger" type="button" data-enquiry-intent="rera-plan"><span>{e(t["roof_cta"])}</span>{icon("arrow")}</button></div>'
        '</div></div>'
        '<div class="in amen-feature is-flipped">'
        f'<div class="amen-feature-media plan-img-wrap" data-full="/img/amenities/specifications.webp?v=18" data-title="{a(t["spec_alt"])}" role="button" tabindex="0" aria-label="{a(t["spec_alt"])}">'
        f'<img src="/img/amenities/specifications.webp?v=18" width="1024" height="682" loading="lazy" alt="{a(t["spec_alt"])}">'
        f'<span class="plan-zoom-hint">{icon("zoom")}<span>{e(t["tap"])}</span></span></div>'
        f'<div class="amen-feature-copy">{eye(t["spec_eye"])}<h3 class="dh">{t["spec_h"]}</h3>'
        f'<div class="amen-lists"><div><h4>{e(t["spec_h1"])}</h4><ul class="amen-list">{specs}</ul></div>'
        f'<div class="amen-security"><h4>{icon("shield")}{e(t["spec_h2"])}</h4><ul class="amen-list">{sec}</ul></div></div></div></div>'
        '</section>\n'
    )


def pricing(t, l):
    total = len(t['units'])
    rows = ''
    for i, (name, area, price, img, alt, feats) in enumerate(t['units']):
        if img:
            visual = (f'<div class="price-row-visual plan-img-wrap" data-full="{img}" data-title="{a(alt)}" role="button" tabindex="0" aria-label="{a(alt)}">'
                      f'<img src="{img}" width="1024" height="575" loading="lazy" decoding="async" alt="{a(alt)}">'
                      f'<span class="plan-zoom-hint">{icon("zoom")}<span>{e(t["tap"])}</span></span></div>')
        else:
            visual = f'<div class="price-row-visual price-visual-request"><span class="price-visual-monogram">{name[0]}B</span><span>{e(t["plan_req"])}</span></div>'
        msg = t['wa_text'] + f' ({name})'
        rows += (
            f'<article class="price-row"><div class="price-row-visual-wrap">{visual}</div>'
            f'<div class="price-row-identity"><span class="price-row-number">0{i + 1} / 0{total}</span><h3>{name}</h3>'
            f'<span class="price-row-area-label">{e(t["area_label"])}</span><strong class="price-row-area">{area} {e(t["sqft"])}</strong></div>'
            f'<div class="price-row-specs"><span class="price-row-spec-heading">{e(t["details"])}</span><ul>{"".join(f"<li>{e(x)}</li>" for x in feats)}</ul></div>'
            f'<div class="price-row-offer"><span class="price-row-starting">{e(t["starting"])}</span><strong class="price-row-price">{price}</strong>'
            f'<span class="price-row-onwards">{e(t["onwards"])}</span>'
            f'<a class="price-row-cta" href="{a(wa(msg))}" target="_blank" rel="noopener">{e(t["enquire"])}<span aria-hidden="true">↗</span></a></div></article>'
        )
    more_cards = ''.join(
        f'<article class="price-more-card">'
        f'<div class="price-more-top"><span class="price-visual-monogram">{e(mono)}</span>'
        f'<div><span class="price-more-kicker">{e(t["more_eye"])}</span><h3>{e(name)}</h3></div></div>'
        + (f'<p class="price-more-area"><span>{e(t["area_label"])}</span><strong>{e(area)}</strong></p>' if area else '')
        + f'<ul>{"".join(f"<li>{e(x)}</li>" for x in feats)}</ul>'
        f'<div class="price-more-offer"><strong>{e(price)}</strong>'
        f'<a class="price-row-cta" href="{a(wa(msg))}" target="_blank" rel="noopener">{e(t["more_enquire"])}<span aria-hidden="true">↗</span></a></div>'
        f'</article>'
        for name, mono, area, price, feats, msg in t['more_units']
    )
    return (
        '<section class="sec price-section" id="pricing"><div class="in"><div class="price-section-head"><div>'
        f'{eye(t["price_eye"])}<h2 class="dh price-section-title">{t["price_h"]}</h2><p class="price-section-intro">{e(t["price_p"])}</p></div>'
        '<div class="price-section-aside"><span class="price-aside-rule"></span><strong>KALYAN WEST</strong><span>RESIDENTIAL COLLECTION</span></div></div>'
        f'<div class="price-rows">{rows}</div>'
        f'<div class="price-more"><div class="price-more-head">{eye(t["more_eye"])}<h3 class="price-more-title">{t["more_h"]}</h3>'
        f'<p class="price-more-intro">{e(t["more_p"])}</p></div>'
        f'<div class="price-more-grid">{more_cards}</div></div>'
        f'<p class="price-section-note">{e(t["price_note"])}</p></div></section>\n'
    )


def plans(t):
    cards = ''.join(
        f'<div class="plan-card"><div class="plan-card-hd"><span class="plan-badge">{e(badge)}</span><h3>{e(h)}</h3><p>{e(p)}</p></div>'
        f'<div class="plan-img-wrap" data-full="{img}" data-title="{a(h)}" role="button" tabindex="0" aria-label="{a(h)}">'
        f'<img src="{img}" width="1024" height="575" loading="lazy" alt="{a(h)}"><span class="plan-zoom-hint">{icon("zoom")}<span>{e(t["tap"])}</span></span></div></div>'
        for img, badge, h, p in t['plans'])
    return (
        '<section class="sec plans dark-bg" id="plans"><div class="in"><div class="plans-hd"><div>'
        f'{eye(t["plans_eye"])}<h2 class="dh light">{t["plans_h"]}</h2></div>'
        f'<p class="lead light" style="margin-top:16px;max-width:620px">{e(t["plans_p"])}</p></div>'
        f'<div class="plans-grid">{cards}</div>'
        f'<p class="home-plans-cta"><a class="btn-o" href="/projects/prestige-gold/"><span>{e(t["plans_btn"])}</span>{icon("arrow")}</a></p></div></section>\n'
    )


def location(t):
    cards = ''
    for key in ('health', 'shop', 'school'):
        items = ''.join(f'<li><strong>{e(n)}:</strong> {km} {e(t["km"])} – {m} {e(t["mins"])}</li>' for n, km, m in LOCATIONS[key])
        cards += f'<article class="loc-card">{LOC_ICON[key]}<h3>{e(t["loc_titles"][key])}</h3><ul>{items}</ul></article>'
    return (
        '<section class="sec home-location" id="location"><span id="areas" class="home-anchor" aria-hidden="true"></span>'
        f'<div class="in home-sec-head">{eye(t["loc_eye"], "eye-center")}<h2 class="dh">{t["loc_h"]}</h2><p class="lead">{e(t["loc_p"])}</p></div>'
        f'<div class="in loc-grid">{cards}</div><p class="in loc-note">{e(t["loc_note"])}</p></section>\n'
    )


def faq(t):
    items = ''.join(f'<details class="q"><summary>{e(q)}</summary><div class="ans">{e(ans)}</div></details>' for q, ans in t['faq'])
    return (
        '<section class="sec" id="faq"><div class="in faq-center">'
        f'<div class="faq-hd">{eye(t["faq_eye"])}<h2 class="dh">{t["faq_h"]}</h2></div><div class="faq-list">{items}</div></div></section>\n'
    )


def guide_post(l, slug):
    base = dict(POSTS['en'][slug])
    if l != 'en':
        base.update(POSTS[l][slug])
    return base


def guides(t, l):
    pfx = PREFIX[l]
    cards = ''
    for slug in FEATURED_GUIDES:
        p = guide_post(l, slug)
        cat = t['guide_cats'].get(p['cat'], p['cat'])
        cards += (
            f'<a class="card" href="{pfx}/blog/{slug}/">'
            f'<img src="/img/blog/{slug}.jpg?v={BLOG_PHOTO_VERSION}" width="800" height="420" loading="lazy" decoding="async" '
            f'alt="{a(p["title"])}">'
            f'<div class="card-b"><span class="card-k">{e(cat)}</span><h3>{e(p["title"])}</h3>'
            f'<p>{e(p["desc"])}</p><span class="card-m">{e(t["guides_min"].format(n=p["read"]))}</span></div></a>'
        )
    return (
        '<section class="sec home-guides" id="guides" style="background:#fff"><div class="in">'
        f'{eye(t["guides_eye"])}<h2 class="dh">{t["guides_h"]}</h2>'
        f'<div class="cards">{cards}</div>'
        f'<p class="home-guides-cta"><a class="btn-o dark" href="{pfx}/blog/"><span>{e(t["guides_btn"])}</span>{icon("arrow")}</a></p>'
        '</div></section>\n'
    )


def contact(t):
    link = a(wa(t['wa_text']))
    return (
        '<section class="sec contact" id="contact"><div class="in contact-grid"><div>'
        f'{eye(t["contact_eye"])}<h2 class="dh light">{t["contact_h"]}</h2><p class="lead light" style="margin-top:18px">{e(t["contact_p"])}</p>'
        f'<ul class="contact-list"><li><b>{e(t["addr"])}</b><span>{ADDRESS}</span></li>'
        f'<li><b>{e(t["phone"])}</b><a href="tel:{PHONE_TEL}">{PHONE}</a></li>'
        f'<li><b>WhatsApp</b><a href="{link}" target="_blank" rel="noopener">{PHONE}</a></li>'
        f'<li><b>{e(t["email"])}</b><a href="mailto:{EMAIL}">{EMAIL}</a></li></ul>'
        f'<div class="cta-row"><a class="btn-wa" href="{link}" target="_blank" rel="noopener">{icon("chat")}<span>{e(t["wa_btn"])}</span></a>'
        f'<a class="btn-o" href="tel:{PHONE_TEL}">{icon("phone")}<span>{e(t["call"])}</span></a></div></div>'
        f'<div><iframe class="map" src="{MAPS_EMBED}" title="{a(ADDRESS)}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>'
        f'<p style="margin:12px 0 0"><a class="btn-o" href="{MAPS_URL}" target="_blank" rel="noopener">{e(t["maps"])} {icon("arrow")}</a></p></div></div></section>\n</main>\n'
    )


def footer(l, t):
    p = PREFIX[l]
    links = ''.join(f'<li><a href="{p}{href if href.startswith("/") else "/" + href}">{e(lbl)}</a></li>' for href, lbl in t['foot_links'])
    langs = ''.join(f'<a href="{PREFIX[k]}/" hreflang="{k}" lang="{k}"' + (' aria-current="true"' if k == l else '') + f'>{n}</a>'
                    for k, n in (('en', 'English'), ('hi', 'हिन्दी'), ('mr', 'मराठी')))
    return (
        '<footer class="home-footer"><div class="foot-grid">'
        f'<div><a class="foot-logo-link" href="{p}/" aria-label="Prestige Enterprises"><img src="/img/logo-on-dark.png" width="210" height="70" alt="Prestige Enterprises" class="foot-logo"></a>'
        f'<p>{e(t["foot_tag"])}</p><div class="foot-langs">{langs}</div></div>'
        f'<div><h4>{e(t["foot_explore"])}</h4><ul>{links}</ul></div>'
        f'<div><h4>{e(t["foot_projects"])}</h4><ul><li><a href="/projects/prestige-gold/">Prestige Gold</a></li>'
        '<li><a href="/projects/prestige-gold/#shri-durga">Shri Durga Enterprises</a></li>'
        '<li><a href="/projects/prestige-one/">Prestige One</a></li></ul></div>'
        f'<div><h4>{e(t["foot_contact"])}</h4><p>{ADDRESS}</p><p><a href="tel:{PHONE_TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p></div></div>'
        f'<div class="foot-legal"><p class="foot-rera"><strong>MahaRERA Reg. No:</strong> {RERA}</p>'
        f'<p><a href="/privacy/">{e(t["privacy"])}</a></p><p>{e(t["disclaimer"])}</p><p>{e(t["rights"])}</p></div></footer>\n'
        f'<a class="wa" href="{a(wa(t["wa_text"]))}" target="_blank" rel="noopener" aria-label="{a(t["wa_btn"])}">{icon("chat")}<span>{e(t["float_wa"])}</span></a>\n'
        f'<script src="/assets/site.js?v={ASSET_VER}" defer></script>\n</body>\n</html>\n'
    )


def build(l):
    t = T[l]
    page = (head(l, t) + nav(l, t) + hero(t) + intro(t) + about(t) + projects(t) + amenities(t)
            + pricing(t, l) + plans(t) + location(t) + faq(t) + guides(t, l) + contact(t) + footer(l, t))
    out = os.path.join(ROOT, PREFIX[l].lstrip('/'), 'index.html')
    with open(out, 'w', encoding='utf-8') as f:
        f.write(page)
    print('wrote', os.path.relpath(out, ROOT), len(page))


if __name__ == '__main__':
    for lang in LANGS:
        build(lang)
