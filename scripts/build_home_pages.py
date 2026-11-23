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
ASSET_VER = 'prestige-home-revamp-20261123-v82'
BLOG_PHOTO_VERSION = '20261114-blog-insight-photos-2'
FEATURED_GUIDES = posts_en.FEATURED
# Homepage cards use the three uploaded blog artworks (1st / 2nd / 3rd blog PNGs).
FEATURED_GUIDE_IMAGES = {
    'how-to-buy-a-flat-in-kalyan-dombivli': '/img/front-blog-buying.webp',
    'stamp-duty-registration-charges-maharashtra': '/img/front-blog-stamp-duty.webp',
    'check-rera-registration-before-you-buy': '/img/front-blog-rera.webp',
}
POSTS = {'en': posts_en.POSTS, 'hi': posts_hi.POSTS, 'mr': posts_mr.POSTS}
VIDEO = '/video/Prestige_Sales_Hero_Video_1080p.mp4'
VIDEO_HOST = ''


def video_preconnect():
    if not VIDEO_HOST:
        return ''
    return f'<link rel="preconnect" href="{VIDEO_HOST}" crossorigin>\n'


PHONE_TEL = '+919689557788'
PHONE = '+91 96895 57788'
WA = 'https://wa.me/919689557788'
EMAIL = 'prestigeprojects1956@gmail.com'
ADDRESS = 'Prestige One, Godrej Hill, Khadakpada, Kalyan, Maharashtra 421301'
MAPS_EMBED = 'https://www.google.com/maps?q=19.262936,73.1425496&z=17&output=embed'
MAPS_URL = 'https://www.google.com/maps/place/PRESTIGE+ONE/@19.262936,73.1425496,17z/data=!3m1!4b1!4m6!3m5!1s0x3be7968ee12f5ffd:0x3b8bf633a3480b65!8m2!3d19.262936!4d73.1425496!16s%2Fg%2F11yjshmnqv'
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
    'check': '<circle cx="12" cy="12" r="9"/><path d="M8.5 12.2l2.3 2.3 4.7-4.8"/>',
    'compass': ('<circle cx="12" cy="12" r="9"/>'
                '<path d="M12 3v2.5M12 18.5V21M3 12h2.5M18.5 12H21"/>'
                '<path d="M5.6 5.6l1.8 1.8M16.6 16.6l1.8 1.8M18.4 5.6l-1.8 1.8M7.4 16.6l-1.8 1.8"/>'
                '<path d="M12 7l1.5 3.6L17 12l-3.5 1.4L12 17l-1.5-3.6L7 12l3.5-1.4z"/>'),
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

AMENITY_IMGS = [
    'entrance-gate', 'elevator-lobby', 'parking', 'main-lobby',
    'cctv-security', 'bedroom',
]
AMENITY_IMG_BASE = '/img/prestige-gold/gallery'

# Outline icons for the Features & Amenities card grid (reference layout).
FEAT_ICONS = {
    'pool': '/img/features/infinity-pool.svg',
    'star': '/img/features/stargazing-deck.svg',
    'cinema': '/img/features/private-cinema.svg',
    'club': '/img/features/clubhouse.svg',
    'vip': '/img/features/vip-guest-suites.svg',
    'lift': '/img/features/high-speed-elevators.svg',
}

# Approximate road distances / drive times from Prestige One, Godrej Hill, Khadakpada.
# Verified against public map listings; times vary with traffic.
LOCATIONS = {
    'health': [
        ('Aayush Hospital', 1, 3),
        ('Shwaas Multispeciality Hospital', 1, 4),
        ('Fortis Hospital, Kalyan', 4, 10),
    ],
    'shop': [
        ('DMart, Godrej Hill', 1, 3),
        ('Metro Junction Mall', 6, 16),
        ('Mukta A2 Cinemas', 6, 16),
        ('Xperia Mall, Dombivli', 14, 28),
        ('Viviana Mall, Thane', 22, 40),
    ],
    'school': [
        ('Podar International School', 1, 3),
        ('Vibgyor Roots & Rise', 1, 3),
        ('K. M. Agrawal College', 1, 4),
        ('Birla College', 2, 5),
    ],
}

T = {}

T['en'] = dict(
    title='Luxury Homes in Kalyan West | Prestige Projects',
    desc='Residences in Khadakpada, Kalyan West: prime location, luxury living, modern amenities and round-the-clock security. 1, 2 & 3 BHK from ₹55 Lakh. Book a private site visit.',
    nav_label='Main menu', menu_open='Open menu', hero_label='Prestige Projects residences in Kalyan West',
    intro_h='Finally, a home that you deserve',
    intro=['Prestige Projects create spacious living for families who deserve more.'],
    intro_cta='Book a private viewing',
    pillars=[('crown', 'Luxury living', 'Designer lobbies, high-speed lifts and French windows and more.'),
             ('leaf', 'For families who deserve more', 'Rooftop garden, outdoor gym, indoor games room and multipurpose hall — amenities for everyday family life.'),
             ('shield', 'Security systems', 'CCTV across common areas, a secured entrance gate and lifts with power backup.'),
             ('compass', 'Vastu compliant', 'Homes designed with Vastu principles, natural light, good airflow and balanced living.')],
    about_eye='Who we are', about_h='Homes built around <em>how you live</em>',
    about=['Our projects are situated in the most established locations in Kalyan West, offering a friendly and convenient neighbourhood. Surrounded by tree-lined surroundings and well-connected roads, with hospitals and shopping destinations nearby, our homes make everyday living comfortable and hassle-free.'],
    about_alt='Prestige One living room opening onto a balcony with riverside sunset views',
    quote='A home is more than just a place to live. It\'s about finding the right neighbourhood, everyday convenience and a lifestyle that feels truly yours.',
    one_view_alt='Prestige One living room opening onto a balcony with riverside sunset views',
    one_poster_alt='Prestige One: One Life. One Home.',
    enq_eye='Enquire', enq_h='Book a site visit <em>today</em>',
    enq_lead='Share your details and our team will connect with you on WhatsApp.',
    enq_submit='Enquire now',
    projects_eye='Our projects', projects_h='Our projects are located in Kalyan West’s <em>most established neighbourhoods</em>',
    projects=[('/projects/prestige-one/', '/img/Prestige%20One%20Tower%20in%20Daylight.png', 1011, 1555, 'Prestige One residential tower in daylight, Kalyan',
               'Prestige One', 'Elite <em>3 &amp; 5 BHK (Jodi)</em> residences',
               'Reserved for those who deserve more',
               'Spacious rooms with balconies and premium finishes built for families who deserve more — Elite 3 & 5 BHK (Jodi).',
               'Visit Prestige One'),
              ('/projects/prestige-gold/', '/img/prestige-tower-day.jpg', 1920, 1080, 'Prestige Gold residential tower in Kalyan West',
               'Prestige Gold', 'Premium living · <em>elevated in every detail</em>',
               'Reserved for those who deserve more',
               'Spacious rooms with balconies and premium finishes built for families who deserve more — 1, 2 & 3 BHK plus retail and office space.',
               'Visit Prestige Gold')],
    amen_eye='Key selling points', amen_h='Limited units. <em>Elevated lifestyle.</em>',
    amen_lead='A premium mixed-use proposition built for lifestyle convenience and long-term investment growth.',
    amen_gallery_h='Premium amenities, <em>everyday leisure</em>',
    amen_names=['Entrance gate', 'Elevator lobby', 'Parking', 'Main lobby', 'CCTV security', 'Bedroom'],
    feat_p='Crafted for buyers and investors, Prestige Gold brings residential comfort and commercial momentum into one premium address in Kalyan West.',
    feat_cards=[
        ('lift', 'High-speed lifts', 'Branded high-speed elevators with power backup for smooth vertical transit.'),
        ('star', 'Rooftop garden', 'A landscaped terrace retreat above the city for fresh air and quiet evenings.'),
        ('club', 'Outdoor gym', 'An outdoor fitness space for everyday workouts without leaving home.'),
        ('cinema', 'Indoor games room', 'A dedicated indoor games room for family leisure and weekend play.'),
        ('vip', 'Multipurpose hall', 'A flexible hall for gatherings, celebrations and community events.'),
    ],
    roof_eye='Amenities', roof_h='Everyday comforts, <em>elevated living</em>',
    roof_p='Amenities redesigned around how families actually live — from high-speed lifts to rooftop leisure.',
    roof_feats=['High-speed lifts', 'Rooftop garden', 'Outdoor gym', 'Indoor games room', 'Multipurpose hall'],
    one_amen_eye='Amenities', one_amen_h='Everyday comforts, <em>a floor away</em>',
    one_amen=['High-speed lifts', 'Rooftop garden', 'Outdoor gym', 'Indoor games room', 'Multipurpose hall'],
    spec_eye='Specifications & security', spec_h='Finished with care, <em>protected around the clock</em>',
    spec_h1='Specifications',
    specs=['Decorative entrance gate and designer lobby', 'Branded vitrified flooring throughout',
           'Powder-coated aluminium French windows', 'Designer bathrooms with branded fittings',
           'Wooden doors for bedrooms, main door and bathrooms', 'Ample parking space'],
    spec_h2='Security systems',
    security=['CCTV surveillance across common areas', 'Secured, gated entrance', 'Branded lifts with power backup',
              'Well-lit lobbies, corridors and parking'],
    spec_alt='Specifications and amenities: entrance gate, lifts, parking, lobby, flooring, CCTV and bathrooms',
    price_eye='Pricing & RERA area', price_h='Premium configurations · <em>clear size compliance</em>',
    price_p='Unit sizes are presented consistently in RERA area (sq. ft.) for quick comparison. Limited units available.',
    area_label='RERA area (sq. ft.)', details='Configuration details', starting='All-in price starting from', onwards='Onwards · Premium / corner units on request',
    enquire='Enquire now', tap='Tap to view', sqft='sq. ft.', on_request='On request',
    gold_aside_k='Prestige Gold', gold_aside_v='Limited units · from ₹55 Lakh',
    gold_eye='Prestige Gold', gold_h='Commercial + residential · <em>elevated lifestyle</em>',
    gold_p='Prestige Gold offers thoughtfully designed 1, 2 and 3 BHK residences in Kalyan West, paired with a future-ready mixed-use ecosystem for end users and investors.',
    units=[('1 BHK', '404–519', '₹55,00,000', '/img/plans/1bhk-3d.webp', '1 BHK flat in Kalyan West',
            ['Living + dining room', '1 bedroom + attached bath', 'Modular kitchen provision', 'Balcony with city view', 'Utility / dry balcony', 'Premium vitrified flooring']),
           ('2 BHK', '577–721', '₹75,00,000', '/img/plans/2bhk-layout.webp', '2 BHK apartment in Kalyan West',
            ['Spacious living + dining', 'Master bedroom + attached bath', '2nd bedroom + common bath', 'Modular kitchen + dry balcony', 'Main balcony — panoramic view', 'UPVC sliding windows', 'ISI marked electrical fittings']),
           ('3 BHK', '', '₹1,40,00,000', '', '3 BHK images available on request',
            ['Available across the complete site', 'Grand living + dining space', 'Master BR + walk-in wardrobe', '2 additional bedrooms', '3 bathrooms (2 attached)', '2 full-sized balconies', 'Dedicated pooja room', 'Premium marble-look flooring'])],
    plan_req='Layout shared on request',
    gold_extra=[
        ('Commercial', 'CO', '', 'On request',
         ['Retail and office opportunity', 'High-footfall Kalyan West corridor', 'Sizes and brochure on request', 'Dual-growth mixed-use address'],
         'Hello Prestige Projects, I would like the Prestige Gold commercial brochure for retail and office space in Kalyan West.'),
    ],
    one_eye='Prestige One', one_h='A <em>luxury address</em>',
    one_p='A luxury address at Godrej Hill, Khadakpada — offered only as 3 & 5 BHK (Jodi). Layouts, carpet areas and pricing are shared privately with serious buyers.',
    one_units=[
        ('3 BHK', '3B', '', 'On request',
         ['Prestige One only', 'Spacious family layout', 'Shared privately with serious buyers', 'Site visit on request'],
         'Hello Prestige Projects, I would like details for Prestige One 3 BHK residences. Please share layouts, carpet areas and pricing.'),
        ('5 BHK (Jodi)', '5B', '', 'On request',
         ['Prestige One only', 'Elite private layouts', 'Shared privately with serious buyers', 'Site visit on request'],
         'Hello Prestige Projects, I would like details for Prestige One 5 BHK (Jodi) residences. Please share layouts, carpet areas and pricing.'),
    ],
    more_enquire='Request details',
    price_note='Limited units available. 70% completed and sample flat ready for immediate walkthrough. Prices and areas are indicative; final values are confirmed in writing before booking.',
    plans_eye='Floor plans', plans_h='Layouts planned <em>for everyday life</em>',
    plans_p='Explore 3D and top-view layouts. Tap any plan to view it full size.',
    plans=[('/img/plans/1bhk-3d.webp', '1 BHK · 3D view', '1 BHK residence', 'Bedroom, living, dining and kitchen arranged in one bright, efficient line, with balconies at both ends.'),
           ('/img/plans/1bhk-layout.webp', '1 BHK · Top view', '1 BHK layout', 'Separate bath and powder room, a utility balcony and a lounge balcony beside the living area.'),
           ('/img/plans/2bhk-layout.webp', '2 BHK · Top view', '2 BHK layout', 'Two bedrooms, two baths and three balconies around a generous living and dining space.')],
    plans_btn='View Prestige Gold details',
    loc_eye='Prime location', loc_h='Everything you need, <em>minutes away</em>',
    loc_p='Our projects are situated at the most established locations in Kalyan West — friendly, convenient neighbourhoods that are tree-lined, well connected, and close to trusted schools, hospitals and shopping zones for a hassle-free life.',
    loc_titles={'health': 'Hospitals & Healthcare', 'shop': 'Malls & Entertainment', 'school': 'Schools & Colleges'},
    km='km', mins='min', loc_note='Distances and drive times are approximate from Prestige One, Godrej Hill, Khadakpada, and vary with traffic.',
    faq_eye='FAQ', faq_h='Common <em>questions</em>',
    faq=[('Where are the residences located?', 'In Kalyan West, around Khadakpada and Godrej Hill. Our office is at Prestige One, Godrej Hill, Khadakpada, Kalyan 421301.'),
         ('Which configurations are available?', 'Prestige Gold offers 1, 2 and 3 BHK residences from ₹55 Lakh, plus commercial space. Prestige One offers only 3 & 5 BHK (Jodi) residences, shared privately on request.'),
         ('What amenities do residents enjoy?', 'High-speed lifts, a rooftop garden, outdoor gym, indoor games room and multipurpose hall — with security and well-kept common areas throughout.'),
         ('What security systems are in place?', 'CCTV surveillance across common areas, a secured gated entrance, well-lit common spaces and branded lifts with power backup.'),
         ('Is the project RERA registered?', f'Yes. MahaRERA registration number {RERA}. We share the registration details and documents before you book.'),
         ('How do I book a site visit?', 'Message us on WhatsApp or call +91 96895 57788. We will confirm a time that suits you and share the latest availability.')],
    guides_eye='Guides',
    guides_h='Straight answers on <em>buying property in Kalyan</em>',
    guides_p='Practical buyer guides on 1, 2 & 3 BHK homes, stamp duty, MahaRERA checks and what to verify before you book in Kalyan West.',
    guides_btn='View all guides', guides_date='October 29, 2026', guides_min='{n} min read',
    guide_cats={'buying': 'Buying', 'costs': 'Costs', 'legal': 'Legal checks', 'finance': 'Finance', 'tax': 'Tax', 'investing': 'Investing'},
    contact_eye='Contact', contact_h='Arrange a <em>private site visit</em>',
    contact_p='Tell us the home you have in mind. Our Khadakpada team will share live availability, floor plans and a written cost sheet, and arrange a visit at your convenience.',
    addr='Office', phone='Phone', email='Email', wa_btn='Chat on WhatsApp', call='Call us', maps='Open in Google Maps',
    wa_text='Hello Prestige Projects, I would like to arrange a site visit and receive current availability in Kalyan West.',
    foot_tag='Thoughtfully planned residences in Kalyan West, Maharashtra.',
    foot_explore='Explore', foot_projects='Projects', foot_contact='Contact',
    foot_links=[('/', 'Home'), ('/projects/prestige-one/', 'Prestige One'), ('/projects/prestige-gold/', 'Prestige Gold'), ('#contact', 'Contact')],
    privacy='Privacy Policy', rera_verified='Verified & Registered',
    disclaimer='Images are artistic impressions for representation only. Amenities, specifications, prices and distances are indicative and may change.',
    rights='© 2026 Prestige Projects. All rights reserved.',
    float_wa='WhatsApp',
)

T['hi'] = dict(
    title='कल्याण वेस्ट में लग्ज़री घर | Prestige Projects',
    desc='खड़कपाड़ा, कल्याण वेस्ट में घर: प्राइम लोकेशन, लग्ज़री लिविंग, आधुनिक सुविधाएँ और चौबीसों घंटे सुरक्षा। 1, 2 और 3 BHK ₹55 लाख से। निजी साइट विज़िट बुक करें।',
    nav_label='मुख्य मेन्यू', menu_open='मेन्यू खोलें', hero_label='कल्याण वेस्ट में Prestige Projects के घर',
    intro_h='आख़िरकार, वह घर जिसके आप हक़दार हैं',
    intro=['Prestige Projects उन परिवारों के लिए विशाल जीवन बनाता है जो अधिक के हक़दार हैं।'],
    intro_cta='निजी विज़िट बुक करें',
    pillars=[('crown', 'लग्ज़री लिविंग', 'डिज़ाइनर लॉबी, हाई-स्पीड लिफ़्ट और फ्रेंच विंडो और बहुत कुछ।'),
             ('leaf', 'उन परिवारों के लिए जो अधिक के हक़दार हैं', 'रूफटॉप गार्डन, जिम, इंडोर गेम्स रूम और मल्टीपर्पस हॉल — रोज़मर्रा के परिवार जीवन के लिए।'),
             ('shield', 'सुरक्षा व्यवस्था', 'कॉमन एरिया में CCTV, सुरक्षित प्रवेश द्वार और पावर बैकअप वाली लिफ़्ट।'),
             ('compass', 'वास्तु अनुरूप', 'आठ-दिशा वास्तु कम्पास के साथ रोशनी, हवा और संतुलित जीवन के लिए बने घर।')],
    about_eye='हमारे बारे में', about_h='आपकी जीवनशैली के <em>अनुरूप घर</em>',
    about=['हमारे प्रोजेक्ट्स कल्याण वेस्ट की सबसे स्थापित लोकेशन पर हैं — दोस्ताना और सुविधाजनक पड़ोस में। पेड़ों से घिरी सड़कें, अच्छी कनेक्टिविटी, और पास में अस्पताल व शॉपिंग डेस्टिनेशन — ताकि रोज़मर्रा की ज़िंदगी आरामदायक और बिना झंझट के रहे।'],
    about_alt='Prestige One का लिविंग रूम, बालकनी से नदी किनारे सूर्यास्त का नज़ारा',
    quote='घर सिर्फ़ रहने की जगह नहीं है। सही पड़ोस, रोज़मर्रा की सुविधा और ऐसी जीवनशैली जो सच में आपकी लगे — यही मायने रखता है।',
    one_view_alt='Prestige One का लिविंग रूम, बालकनी से नदी किनारे सूर्यास्त का नज़ारा',
    one_poster_alt='Prestige One: One Life. One Home.',
    enq_eye='पूछताछ', enq_h='आज ही <em>साइट विज़िट बुक करें</em>',
    enq_lead='अपना विवरण साझा करें — हमारी टीम WhatsApp पर आपसे जुड़ जाएगी।',
    enq_submit='पूछताछ करें',
    projects_eye='हमारे प्रोजेक्ट्स', projects_h='हमारे प्रोजेक्ट्स कल्याण वेस्ट के <em>सबसे स्थापित पड़ोस</em> में हैं',
    projects=[('/projects/prestige-one/', '/img/Prestige%20One%20Tower%20in%20Daylight.png', 1011, 1555, 'कल्याण में Prestige One आवासीय टावर',
               'Prestige One', 'एलीट <em>3 और 5 BHK (Jodi)</em> घर',
               'Reserved for those who deserve more',
               'बालकनी वाले विशाल कमरे और प्रीमियम फ़िनिश — उन परिवारों के लिए जो अधिक के हक़दार हैं। एलीट 3 और 5 BHK (Jodi) गोदरेज हिल पर, लेआउट और कीमत गंभीर खरीदारों के साथ निजी तौर पर।',
               'Visit Prestige One'),
              ('/projects/prestige-gold/', '/img/prestige-tower-day.jpg', 1920, 1080, 'कल्याण वेस्ट में Prestige Gold आवासीय टावर',
               'Prestige Gold', 'प्रीमियम जीवन · <em>हर डिटेल में ऊँचा</em>',
               'Reserved for those who deserve more',
               'बालकनी वाले विशेष कमरे और प्रीमियम फ़िनिश — उन परिवारों के लिए जो अधिक के हक़दार हैं। 1, 2 और 3 BHK साथ रिटेल व ऑफिस, कल्याण वेस्ट के दिल में।',
               'Visit Prestige Gold')],
    amen_eye='सुविधाएँ', amen_h='आराम, सेहत और खेल, <em>घर के पास ही</em>',
    amen_lead='सुकून भरी सुबह, सक्रिय शाम और परिवार के साथ वीकेंड के लिए बनाई गई जगहें, सब कुछ सोसाइटी के भीतर।',
    amen_gallery_h='पूरी जीवनशैली, <em>दरवाज़े से कुछ कदम पर</em>',
    amen_names=['प्रवेश द्वार', 'एलिवेटर लॉबी', 'पार्किंग', 'मुख्य लॉबी', 'CCTV सुरक्षा', 'बेडरूम'],
    feat_p='Prestige Kalyan उन परिवारों के लिए है जो घर में हर दिन से ज़्यादा उम्मीद करते हैं: ऊँचा आराम, शांत सुविधाएँ और खुली, परिष्कृत वास्तुकला।',
    feat_cards=[
        ('lift', 'हाई-स्पीड लिफ़्ट', 'पावर बैकअप के साथ ब्रांडेड हाई-स्पीड एलिवेटर।'),
        ('star', 'रूफटॉप गार्डन', 'शहर के ऊपर हरियाली भरा टेरेस।'),
        ('club', 'जिम', 'घर के भीतर रोज़ाना फ़िटनेस के लिए जगह।'),
        ('cinema', 'इंडोर गेम्स रूम', 'परिवार के मनोरंजन के लिए समर्पित गेम्स रूम।'),
        ('vip', 'मल्टीपर्पस हॉल', 'मिलन, उत्सव और समुदाय कार्यक्रमों के लिए हॉल।'),
    ],
    roof_eye='सुविधाएँ', roof_h='रोज़मर्रा का आराम, <em>ऊँचा जीवन</em>',
    roof_p='हाई-स्पीड लिफ़्ट से रूफटॉप लीज़र तक — परिवार के जीवन के हिसाब से सुविधाएँ।',
    roof_feats=['हाई-स्पीड लिफ़्ट', 'रूफटॉप गार्डन', 'जिम', 'इंडोर गेम्स रूम', 'मल्टीपर्पस हॉल'],
    one_amen_eye='सुविधाएँ', one_amen_h='रोज़मर्रा का आराम, <em>एक मंज़िल दूर</em>',
    one_amen=['हाई-स्पीड लिफ़्ट', 'रूफटॉप गार्डन', 'जिम', 'इंडोर गेम्स रूम', 'मल्टीपर्पस हॉल'],
    roof_note='',
    roof_cta='',
    roof_alt='रूफटॉप गार्डन और सुविधाएँ',
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
    price_p='नीचे Prestige Gold और Prestige One अलग-अलग हैं। प्रकाशित शुरुआती कीमतें Prestige Gold की हैं; अनुरोध पर वाले लेआउट और क्षेत्रफल निजी तौर पर साझा होते हैं।',
    area_label='RERA क्षेत्रफल', details='घर की विशेषताएँ', starting='शुरुआती कीमत', onwards='से शुरू · प्रीमियम और कॉर्नर यूनिट अनुरोध पर',
    enquire='पूछताछ करें', tap='देखने के लिए टैप करें', sqft='वर्ग फुट', on_request='अनुरोध पर',
    gold_aside_k='Prestige Gold', gold_aside_v='प्रीमियम क्वालिटी · ₹55 लाख से',
    gold_eye='Prestige Gold', gold_h='प्रीमियम जीवन · <em>हर डिटेल में ऊँचा</em>',
    gold_p='उच्च-फिनिश 1, 2 और 3 BHK घर — रोशन कमरे, परिष्कृत डिटेलिंग और ₹55 लाख से स्पष्ट शुरुआती कीमतें — साथ ही उसी कल्याण वेस्ट पते पर रिटेल और ऑफिस स्पेस।',
    units=[('1 BHK', '404–519', '₹55,00,000', '/img/plans/1bhk-3d.webp', '1 BHK 3D फ़्लोर प्लान',
            ['लिविंग और डाइनिंग रूम', 'अटैच्ड बाथ के साथ बेडरूम', 'मॉड्यूलर किचन की सुविधा', 'शहर के दृश्य वाली बालकनी', 'यूटिलिटी / ड्राई बालकनी', 'प्रीमियम विट्रिफाइड फ़्लोरिंग']),
           ('2 BHK', '577–721', '₹75,00,000', '/img/plans/2bhk-layout.webp', '2 BHK फ़्लोर प्लान',
            ['विशाल लिविंग और डाइनिंग', 'अटैच्ड बाथ के साथ मास्टर बेडरूम', 'कॉमन बाथ के साथ दूसरा बेडरूम', 'मॉड्यूलर किचन और ड्राई बालकनी', 'दो बालकनी', 'UPVC स्लाइडिंग विंडो']),
           ('3 BHK', '', '₹1,40,00,000', '', '3 BHK फ़्लोर प्लान',
            ['पूरे साइट पर उपलब्ध', 'बड़ा लिविंग और डाइनिंग', 'वॉक-इन वार्डरोब के साथ मास्टर बेडरूम', 'दो अतिरिक्त बेडरूम', 'तीन बाथरूम (दो अटैच्ड)', 'दो फुल-साइज़ बालकनी', 'अलग पूजा कक्ष'])],
    plan_req='लेआउट अनुरोध पर',
    gold_extra=[
        ('कमर्शियल', 'CO', '', 'अनुरोध पर',
         ['Prestige Gold रिटेल और ऑफिस', 'कल्याण वेस्ट का व्यस्त कॉरिडोर', 'साइज़ और ब्रोशर अनुरोध पर', 'कीमत लिखित में साझा'],
         'नमस्ते Prestige Projects, मुझे कल्याण वेस्ट में Prestige Gold की कमर्शियल (रिटेल/ऑफिस) जानकारी चाहिए।'),
    ],
    one_eye='Prestige One', one_h='एक <em>लग्ज़री पता</em>',
    one_p='गोदरेज हिल, खड़कपाड़ा पर एक लग्ज़री पता — केवल 3 और 5 BHK (Jodi)। लेआउट, कारपेट एरिया और कीमत गंभीर खरीदारों के साथ निजी तौर पर।',
    one_units=[
        ('3 BHK', '3B', '', 'अनुरोध पर',
         ['केवल Prestige One', 'विशाल पारिवारिक लेआउट', 'गंभीर खरीदारों के साथ निजी', 'साइट विज़िट अनुरोध पर'],
         'नमस्ते Prestige Projects, मुझे Prestige One 3 BHK घरों की जानकारी चाहिए।'),
        ('5 BHK (Jodi)', '5B', '', 'अनुरोध पर',
         ['केवल Prestige One', 'एलीट निजी लेआउट', 'गंभीर खरीदारों के साथ निजी', 'साइट विज़िट अनुरोध पर'],
         'नमस्ते Prestige Projects, मुझे Prestige One 5 BHK (Jodi) घरों की जानकारी चाहिए।'),
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
    loc_p='हमारे प्रोजेक्ट्स कल्याण वेस्ट की सबसे स्थापित और सुविधाजनक लोकेशन पर हैं — हरे-भरे, शांत इलाके जो स्कूलों, अस्पतालों और शॉपिंग ज़ोन से अच्छी तरह जुड़े हैं, ताकि आपकी ज़िंदगी आसान रहे।',
    loc_titles={'health': 'अस्पताल और स्वास्थ्य सेवा', 'shop': 'मॉल और मनोरंजन', 'school': 'स्कूल और कॉलेज'},
    km='किमी', mins='मिनट', loc_note='दूरी और समय Prestige One, गोदरेज हिल, खड़कपाड़ा से अनुमानित हैं और ट्रैफ़िक के अनुसार बदल सकते हैं।',
    faq_eye='सवाल-जवाब', faq_h='आम <em>सवाल</em>',
    guides_eye='गाइड',
    guides_h='<em>कल्याण में प्रॉपर्टी खरीदने</em> पर सीधे जवाब',
    guides_p='1, 2 और 3 BHK घर, स्टैंप ड्यूटी, MahaRERA जाँच और कल्याण वेस्ट में बुकिंग से पहले क्या देखें — इन व्यावहारिक गाइड्स को पढ़ें।',
    guides_btn='सभी गाइड देखें', guides_date='29 अक्टूबर 2026', guides_min='{n} मिनट में पढ़ें',
    guide_cats={'buying': 'खरीद', 'costs': 'खर्च', 'legal': 'कानूनी जाँच', 'finance': 'वित्त', 'tax': 'टैक्स', 'investing': 'निवेश'},
    faq=[('घर कहाँ स्थित हैं?', 'कल्याण वेस्ट में, खड़कपाड़ा और गोदरेज हिल के आसपास। हमारा ऑफिस Prestige One, गोदरेज हिल, खड़कपाड़ा, कल्याण 421301 में है।'),
         ('कौन-से कॉन्फ़िगरेशन उपलब्ध हैं?', 'Prestige Gold में 1, 2 और 3 BHK घर ₹55 लाख से, साथ ही कमर्शियल जगह। Prestige One केवल 3 BHK और 5 BHK में उपलब्ध है, अनुरोध पर निजी तौर पर।'),
         ('निवासियों के लिए कौन-सी सुविधाएँ हैं?', 'हाई-स्पीड लिफ़्ट, रूफटॉप गार्डन, जिम, इंडोर गेम्स रूम और मल्टीपर्पस हॉल — साथ में सुरक्षा और सुव्यवस्थित कॉमन एरिया।'),
         ('सुरक्षा के लिए क्या व्यवस्था है?', 'कॉमन एरिया में CCTV निगरानी, सुरक्षित गेटेड प्रवेश, रोशन कॉमन स्पेस और पावर बैकअप वाली ब्रांडेड लिफ़्ट।'),
         ('क्या प्रोजेक्ट RERA पंजीकृत है?', f'हाँ। MahaRERA पंजीकरण संख्या {RERA}। बुकिंग से पहले हम पंजीकरण विवरण और दस्तावेज़ साझा करते हैं।'),
         ('साइट विज़िट कैसे बुक करें?', 'WhatsApp पर संदेश भेजें या +91 96895 57788 पर कॉल करें। हम आपकी सुविधा के अनुसार समय तय करेंगे और मौजूदा उपलब्धता बताएँगे।')],
    contact_eye='संपर्क', contact_h='<em>निजी साइट विज़िट</em> बुक करें',
    contact_p='हमें बताएँ कि आप कैसा घर चाहते हैं। हमारी खड़कपाड़ा टीम मौजूदा उपलब्धता, फ़्लोर प्लान और लिखित लागत विवरण साझा करेगी और आपकी सुविधा से विज़िट तय करेगी।',
    addr='ऑफिस', phone='फ़ोन', email='ईमेल', wa_btn='WhatsApp पर बात करें', call='कॉल करें', maps='Google Maps में खोलें',
    wa_text='नमस्ते Prestige Projects, मैं कल्याण वेस्ट में साइट विज़िट बुक करना और मौजूदा उपलब्धता जानना चाहता/चाहती हूँ।',
    foot_tag='कल्याण वेस्ट, महाराष्ट्र में सोच-समझकर बनाए गए घर।',
    foot_explore='देखें', foot_projects='प्रोजेक्ट्स', foot_contact='संपर्क',
    foot_links=[('/', 'होम'), ('/projects/prestige-one/', 'Prestige One'), ('/projects/prestige-gold/', 'Prestige Gold'), ('#contact', 'संपर्क')],
    privacy='गोपनीयता नीति', rera_verified='सत्यापित और पंजीकृत',
    disclaimer='तस्वीरें केवल प्रस्तुति के लिए कलात्मक चित्रण हैं। सुविधाएँ, स्पेसिफ़िकेशन, कीमतें और दूरियाँ सांकेतिक हैं और बदल सकती हैं।',
    rights='© 2026 Prestige Projects. सर्वाधिकार सुरक्षित।',
    float_wa='WhatsApp',
)

T['mr'] = dict(
    title='कल्याण वेस्टमध्ये लक्झरी घरे | Prestige Projects',
    desc='खडकपाडा, कल्याण वेस्टमधील घरे: प्राइम लोकेशन, लक्झरी लिव्हिंग, आधुनिक सुविधा आणि चोवीस तास सुरक्षा. 1, 2 आणि 3 BHK ₹55 लाखांपासून. खासगी साइट व्हिजिट बुक करा.',
    nav_label='मुख्य मेनू', menu_open='मेनू उघडा', hero_label='कल्याण वेस्टमधील Prestige Projects ची घरे',
    intro_h='शेवटी, ते घर ज्याचे तुम्ही पात्र आहात',
    intro=['Prestige Projects ज्या कुटुंबांना अधिक हवे आहे त्यांच्यासाठी प्रशस्त जीवन उभारते.'],
    intro_cta='खासगी व्हिजिट बुक करा',
    pillars=[('crown', 'लक्झरी लिव्हिंग', 'डिझायनर लॉबी, हाय-स्पीड लिफ्ट आणि फ्रेंच विंडो आणि आणखी बरेच काही.'),
             ('leaf', 'ज्या कुटुंबांना अधिक हवे आहे त्यांच्यासाठी', 'रूफटॉप गार्डन, जिम, इंडोर गेम्स रूम आणि मल्टीपर्पस हॉल — रोजच्या कौटुंबिक जीवनासाठी.'),
             ('shield', 'सुरक्षा व्यवस्था', 'कॉमन एरियात CCTV, सुरक्षित प्रवेशद्वार आणि पॉवर बॅकअप असलेल्या लिफ्ट.'),
             ('compass', 'वास्तु अनुरूप', 'आठ-दिशा वास्तु कंपाससह प्रकाश, हवा आणि संतुलित जीवनासाठी घरे.')],
    about_eye='आमच्याबद्दल', about_h='तुमच्या जीवनशैलीला <em>साजेशी घरे</em>',
    about=['आमचे प्रकल्प कल्याण वेस्टमधील सर्वात प्रस्थापित ठिकाणी आहेत — मैत्रीपूर्ण आणि सोयीस्कर परिसरात. झाडांनी वेढलेल्या रस्त्यांभोवती, चांगल्या कनेक्टिव्हिटीसह, जवळच रुग्णालये आणि शॉपिंग डेस्टिनेशन्स — जेणेकरून रोजचे जीवन आरामदायी आणि त्रासमुक्त राहील.'],
    about_alt='Prestige One ची लिव्हिंग रूम, बाल्कनीतून नदीकाठचा सूर्यास्त',
    quote='घर हे फक्त राहण्याचे ठिकाण नाही. योग्य शेजार, रोजची सोय आणि तुमचीच वाटणारी जीवनशैली — यातच खरी किंमत आहे.',
    one_view_alt='Prestige One ची लिव्हिंग रूम, बाल्कनीतून नदीकाठचा सूर्यास्त',
    one_poster_alt='Prestige One: One Life. One Home.',
    enq_eye='चौकशी', enq_h='आजच <em>साइट व्हिजिट बुक करा</em>',
    enq_lead='तुमचे तपशील शेअर करा — आमची टीम WhatsApp वर तुमच्याशी संपर्क साधेल.',
    enq_submit='चौकशी करा',
    projects_eye='आमचे प्रकल्प', projects_h='आमचे प्रकल्प कल्याण वेस्टमधील <em>सर्वात प्रस्थापित परिसरात</em> आहेत',
    projects=[('/projects/prestige-one/', '/img/Prestige%20One%20Tower%20in%20Daylight.png', 1011, 1555, 'कल्याणमधील Prestige One निवासी टॉवर',
               'Prestige One', 'एलीट <em>3 आणि 5 BHK (Jodi)</em> घरे',
               'Reserved for those who deserve more',
               'बाल्कनी असलेल्या प्रशस्त खोल्या आणि प्रीमियम फिनिश — ज्या कुटुंबांना अधिक हवे आहे त्यांच्यासाठी. एलीट 3 आणि 5 BHK (Jodi) गोदरेज हिलवर, लेआउट आणि किंमत गंभीर खरेदीदारांसोबत खासगीरीत्या.',
               'Visit Prestige One'),
              ('/projects/prestige-gold/', '/img/prestige-tower-day.jpg', 1920, 1080, 'कल्याण वेस्टमधील Prestige Gold निवासी टॉवर',
               'Prestige Gold', 'प्रीमियम जीवन · <em>प्रत्येक डिटेलमध्ये उन्नत</em>',
               'Reserved for those who deserve more',
               'बाल्कनी असलेल्या विशेष खोल्या आणि प्रीमियम फिनिश — ज्या कुटुंबांना अधिक हवे आहे त्यांच्यासाठी. 1, 2 आणि 3 BHK सोबत रिटेल व ऑफिस, कल्याण वेस्टच्या हृदयात.',
               'Visit Prestige Gold')],
    amen_eye='सुविधा', amen_h='विश्रांती, आरोग्य आणि खेळ, <em>घराजवळच</em>',
    amen_lead='निवांत सकाळ, उत्साही संध्याकाळ आणि कुटुंबासोबतच्या वीकेंडसाठी तयार केलेल्या जागा, सर्व काही सोसायटीच्या आत.',
    amen_gallery_h='पूर्ण जीवनशैली, <em>दारापासून काही पावलांवर</em>',
    amen_names=['प्रवेशद्वार', 'एलिव्हेटर लॉबी', 'पार्किंग', 'मुख्य लॉबी', 'CCTV सुरक्षा', 'बेडरूम'],
    feat_p='Prestige Kalyan त्या कुटुंबांसाठी आहे जे घरातून दररोज अधिक अपेक्षा करतात: उन्नत विश्रांती, शांत सुविधा आणि खुली, परिष्कृत वास्तुकला.',
    feat_cards=[
        ('lift', 'हाय-स्पीड लिफ्ट', 'पॉवर बॅकअपसह ब्रँडेड हाय-स्पीड एलिव्हेटर.'),
        ('star', 'रूफटॉप गार्डन', 'शहराच्या वरचे हिरवे टेरेस.'),
        ('club', 'जिम', 'घरातच रोजच्या फिटनेससाठी जागा.'),
        ('cinema', 'इंडोर गेम्स रूम', 'कुटुंबीय मनोरंजनासाठी समर्पित गेम्स रूम.'),
        ('vip', 'मल्टीपर्पस हॉल', 'मेळावे, उत्सव आणि समुदाय कार्यक्रमांसाठी हॉल.'),
    ],
    roof_eye='सुविधा', roof_h='रोजचा आराम, <em>उन्नत जीवन</em>',
    roof_p='हाय-स्पीड लिफ्टपासून रूफटॉप विश्रांतीपर्यंत — कुटुंबाच्या जीवनशैलीनुसार सुविधा.',
    roof_feats=['हाय-स्पीड लिफ्ट', 'रूफटॉप गार्डन', 'जिम', 'इंडोर गेम्स रूम', 'मल्टीपर्पस हॉल'],
    one_amen_eye='सुविधा', one_amen_h='रोजचा आराम, <em>एका मजल्यावर</em>',
    one_amen=['हाय-स्पीड लिफ्ट', 'रूफटॉप गार्डन', 'जिम', 'इंडोर गेम्स रूम', 'मल्टीपर्पस हॉल'],
    roof_note='',
    roof_cta='',
    roof_alt='रूफटॉप गार्डन आणि सुविधा',
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
    price_p='खाली Prestige Gold आणि Prestige One वेगवेगळे दाखवले आहेत. प्रकाशित सुरुवातीच्या किंमती Prestige Gold च्या आहेत; विनंतीवरील लेआउट आणि क्षेत्रफळ खासगीरीत्या शेअर होतात.',
    area_label='RERA क्षेत्रफळ', details='घराची वैशिष्ट्ये', starting='सुरुवातीची किंमत', onwards='पासून · प्रीमियम आणि कॉर्नर युनिट विनंतीवर',
    enquire='चौकशी करा', tap='पाहण्यासाठी टॅप करा', sqft='चौ. फूट', on_request='विनंतीवर',
    gold_aside_k='Prestige Gold', gold_aside_v='प्रीमियम क्वॉलिटी · ₹55 लाखांपासून',
    gold_eye='Prestige Gold', gold_h='प्रीमियम जीवन · <em>प्रत्येक डिटेलमध्ये उन्नत</em>',
    gold_p='उच्च-फिनिश 1, 2 आणि 3 BHK घरे — प्रकाशमान खोल्या, परिष्कृत डिटेलिंग आणि ₹55 लाखांपासून स्पष्ट सुरुवातीच्या किंमती — तसेच त्याच कल्याण वेस्ट पत्त्यावर रिटेल आणि ऑफिस जागा.',
    units=[('1 BHK', '404–519', '₹55,00,000', '/img/plans/1bhk-3d.webp', '1 BHK 3D फ्लोअर प्लॅन',
            ['लिव्हिंग आणि डायनिंग रूम', 'अटॅच्ड बाथसह बेडरूम', 'मॉड्युलर किचनची सुविधा', 'शहराचे दृश्य असलेली बाल्कनी', 'युटिलिटी / ड्राय बाल्कनी', 'प्रीमियम व्हिट्रिफाइड फ्लोअरिंग']),
           ('2 BHK', '577–721', '₹75,00,000', '/img/plans/2bhk-layout.webp', '2 BHK फ्लोअर प्लॅन',
            ['प्रशस्त लिव्हिंग आणि डायनिंग', 'अटॅच्ड बाथसह मास्टर बेडरूम', 'कॉमन बाथसह दुसरी बेडरूम', 'मॉड्युलर किचन आणि ड्राय बाल्कनी', 'दोन बाल्कनी', 'UPVC स्लायडिंग विंडो']),
           ('3 BHK', '', '₹1,40,00,000', '', '3 BHK फ्लोअर प्लॅन',
            ['संपूर्ण साइटवर उपलब्ध', 'मोठे लिव्हिंग आणि डायनिंग', 'वॉक-इन वॉर्डरोबसह मास्टर बेडरूम', 'दोन अतिरिक्त बेडरूम', 'तीन बाथरूम (दोन अटॅच्ड)', 'दोन पूर्ण आकाराच्या बाल्कनी', 'स्वतंत्र पूजा कक्ष'])],
    plan_req='लेआउट विनंतीवर',
    gold_extra=[
        ('कमर्शियल', 'CO', '', 'विनंतीवर',
         ['Prestige Gold रिटेल आणि ऑफिस', 'कल्याण वेस्टचा व्यस्त कॉरिडॉर', 'आकार आणि ब्रोशर विनंतीवर', 'किंमत लेखी दिली जाते'],
         'नमस्कार Prestige Projects, मला कल्याण वेस्टमधील Prestige Gold कमर्शियल (रिटेल/ऑफिस) माहिती हवी आहे.'),
    ],
    one_eye='Prestige One', one_h='एक <em>लक्झरी पत्ता</em>',
    one_p='गोदरेज हिल, खडकपाडा येथील एक लक्झरी पत्ता — फक्त 3 आणि 5 BHK (Jodi). लेआउट, कार्पेट एरिया आणि किंमत गंभीर खरेदीदारांसोबत खासगीरीत्या.',
    one_units=[
        ('3 BHK', '3B', '', 'विनंतीवर',
         ['फक्त Prestige One', 'प्रशस्त कौटुंबिक लेआउट', 'गंभीर खरेदीदारांसोबत खासगी', 'साइट भेट विनंतीवर'],
         'नमस्कार Prestige Projects, मला Prestige One 3 BHK घरांची माहिती हवी आहे.'),
        ('5 BHK (Jodi)', '5B', '', 'विनंतीवर',
         ['फक्त Prestige One', 'एलीट खासगी लेआउट', 'गंभीर खरेदीदारांसोबत खासगी', 'साइट भेट विनंतीवर'],
         'नमस्कार Prestige Projects, मला Prestige One 5 BHK (Jodi) घरांची माहिती हवी आहे.'),
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
    loc_p='आमचे प्रकल्प कल्याण वेस्टमधील सर्वात प्रस्थापित आणि सोयीच्या ठिकाणी आहेत — हिरवागार, शांत परिसर जो शाळा, रुग्णालये आणि शॉपिंग झोनशी उत्तम जोडलेला आहे, जेणेकरून तुमचे आयुष्य त्रासमुक्त राहील.',
    loc_titles={'health': 'रुग्णालये आणि आरोग्यसेवा', 'shop': 'मॉल आणि मनोरंजन', 'school': 'शाळा आणि महाविद्यालये'},
    km='किमी', mins='मिनिटे', loc_note='अंतर आणि वेळ Prestige One, गोदरेज हिल, खडकपाडा येथून अंदाजे आहेत आणि ट्रॅफिकनुसार बदलू शकतात.',
    faq_eye='प्रश्नोत्तरे', faq_h='नेहमीचे <em>प्रश्न</em>',
    guides_eye='मार्गदर्शक',
    guides_h='<em>कल्याणमधील मालमत्ता खरेदी</em>वर थेट उत्तरे',
    guides_p='1, 2 आणि 3 BHK घरे, स्टॅम्प ड्यूटी, MahaRERA तपासणी आणि कल्याण वेस्टमध्ये बुकिंगपूर्वी काय पाहावे — या व्यावहारिक मार्गदर्शकांचे अवलोकन करा.',
    guides_btn='सर्व मार्गदर्शक पाहा', guides_date='29 ऑक्टोबर 2026', guides_min='{n} मिनिटांत वाचा',
    guide_cats={'buying': 'खरेदी', 'costs': 'खर्च', 'legal': 'कायदेशीर तपासणी', 'finance': 'वित्त', 'tax': 'कर', 'investing': 'गुंतवणूक'},
    faq=[('घरे कुठे आहेत?', 'कल्याण वेस्टमध्ये, खडकपाडा आणि गोदरेज हिल परिसरात. आमचे कार्यालय Prestige One, गोदरेज हिल, खडकपाडा, कल्याण 421301 येथे आहे.'),
         ('कोणते कॉन्फिगरेशन उपलब्ध आहेत?', 'Prestige Gold मध्ये 1, 2 आणि 3 BHK घरे ₹55 लाखांपासून, सोबत कमर्शियल जागा. Prestige One फक्त 3 BHK आणि 5 BHK मध्ये उपलब्ध आहे, विनंतीवर खासगीरीत्या.'),
         ('रहिवाशांसाठी कोणत्या सुविधा आहेत?', 'हाय-स्पीड लिफ्ट, रूफटॉप गार्डन, जिम, इंडोर गेम्स रूम आणि मल्टीपर्पस हॉल — सोबत सुरक्षा आणि व्यवस्थित कॉमन एरिया.'),
         ('सुरक्षेसाठी कोणती व्यवस्था आहे?', 'कॉमन एरियात CCTV देखरेख, सुरक्षित गेटेड प्रवेश, प्रकाशमान कॉमन जागा आणि पॉवर बॅकअप असलेल्या ब्रँडेड लिफ्ट.'),
         ('प्रकल्प RERA नोंदणीकृत आहे का?', f'हो. MahaRERA नोंदणी क्रमांक {RERA}. बुकिंगपूर्वी आम्ही नोंदणीचा तपशील आणि कागदपत्रे देतो.'),
         ('साइट व्हिजिट कशी बुक करावी?', 'WhatsApp वर संदेश पाठवा किंवा +91 96895 57788 वर कॉल करा. आम्ही तुमच्या सोयीची वेळ निश्चित करू आणि सध्याची उपलब्धता सांगू.')],
    contact_eye='संपर्क', contact_h='<em>खासगी साइट व्हिजिट</em> बुक करा',
    contact_p='तुम्हाला कसे घर हवे आहे ते सांगा. आमची खडकपाडा टीम सध्याची उपलब्धता, फ्लोअर प्लॅन आणि लेखी खर्चपत्रक देईल आणि तुमच्या सोयीनुसार व्हिजिट ठरवेल.',
    addr='कार्यालय', phone='फोन', email='ईमेल', wa_btn='WhatsApp वर बोला', call='कॉल करा', maps='Google Maps मध्ये उघडा',
    wa_text='नमस्कार Prestige Projects, मला कल्याण वेस्टमध्ये साइट व्हिजिट बुक करायची आहे आणि सध्याची उपलब्धता जाणून घ्यायची आहे.',
    foot_tag='कल्याण वेस्ट, महाराष्ट्रातील विचारपूर्वक नियोजित घरे.',
    foot_explore='पाहा', foot_projects='प्रकल्प', foot_contact='संपर्क',
    foot_links=[('/', 'होम'), ('/projects/prestige-one/', 'Prestige One'), ('/projects/prestige-gold/', 'Prestige Gold'), ('#contact', 'संपर्क')],
    privacy='गोपनीयता धोरण', rera_verified='सत्यापित आणि नोंदणीकृत',
    disclaimer='चित्रे केवळ सादरीकरणासाठी कलात्मक प्रतिमा आहेत. सुविधा, स्पेसिफिकेशन, किंमती आणि अंतरे सूचक असून बदलू शकतात.',
    rights='© 2026 Prestige Projects. सर्व हक्क राखीव.',
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
    agent = {'@type': 'RealEstateAgent', '@id': SITE + '/#agent', 'name': 'Prestige Projects', 'url': SITE + '/',
             'image': SITE + '/img/logo.png', 'logo': SITE + '/img/logo.png', 'telephone': PHONE_TEL, 'email': EMAIL,
             'address': {'@type': 'PostalAddress', 'streetAddress': 'Prestige One, Godrej Hill, Khadakpada', 'addressLocality': 'Kalyan',
                         'addressRegion': 'Maharashtra', 'postalCode': '421301', 'addressCountry': 'IN'},
             'hasMap': MAPS_URL, 'areaServed': {'@type': 'City', 'name': 'Kalyan'}, 'knowsLanguage': ['en', 'hi', 'mr']}
    website = {'@type': 'WebSite', '@id': SITE + '/#website', 'url': SITE + '/', 'name': 'Prestige Projects',
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
        f'<meta property="og:type" content="website"><meta property="og:site_name" content="Prestige Projects"><meta property="og:locale" content="{LOCALE[l]}">'
        f'<meta property="og:url" content="{canonical}"><meta property="og:title" content="{a(t["title"])}"><meta property="og:description" content="{a(t["desc"])}">'
        f'<meta property="og:image" content="{SITE}/img/og-default.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
        '<meta name="twitter:card" content="summary_large_image">\n'
        '<link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" type="image/png" sizes="192x192" href="/icon-192.png"><link rel="apple-touch-icon" href="/apple-touch-icon.png">\n'
        f'{video_preconnect()}'
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
        f'<a class="nav-logo home-wordmark" href="{p}/" aria-label="Prestige Projects">'
        '<img class="home-logo-dark" src="/img/logo-on-dark.png" width="248" height="83" alt="Prestige Projects" decoding="async">'
        '<img class="home-logo-light" src="/img/logo.png" width="248" height="83" alt="" aria-hidden="true" decoding="async"></a>'
        f'<div class="nav-r nav-r-home-fallback" hidden aria-hidden="true"><div class="lang" role="group">{langs}</div></div></nav>\n'
        '<div class="mnav" id="mnav" hidden aria-hidden="true"></div>\n'
    )


def hero(t):
    return (
        f'<main id="main"><section id="home" class="hero hero-video-hero site-video-hero" aria-label="{a(t["hero_label"])}">\n'
        f'  <video class="hero-video" id="heroVideo" src="{VIDEO}" autoplay muted loop playsinline webkit-playsinline preload="auto" controlsList="nodownload nofullscreen noremoteplayback" disablepictureinpicture disableremoteplayback x-webkit-airplay="deny" aria-hidden="true" tabindex="-1"></video>\n'
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


def enquiry(t):
    return (
        '<section class="sec home-enquiry" id="enquiry" aria-labelledby="home-enq-title">'
        '<div class="in home-enquiry-in">'
        f'{eye(t["enq_eye"])}'
        f'<h2 class="dh" id="home-enq-title">{t["enq_h"]}</h2>'
        f'<p class="lead home-enquiry-lead">{e(t["enq_lead"])}</p>'
        '<form class="enq-form home-enq-form" id="homeEnquiryForm" data-enquiry-intent="site-visit" novalidate>'
        '<div class="enq-fields">'
        '<label class="enq-field">Full Name <span>*</span><input name="name" autocomplete="name" placeholder="Enter your name" required minlength="2"></label>'
        '<label class="enq-field">Phone Number <span>*</span><input name="phone" type="tel" inputmode="numeric" autocomplete="tel" placeholder="Enter your phone number" required pattern="[6-9][0-9]{9}" maxlength="10"></label>'
        '<label class="enq-field">Select Configuration <span>*</span><select name="configuration" required><option value="">Select</option><option>1BHK</option><option>2BHK</option><option>3BHK</option><option>4BHK</option><option>5BHK</option><option>Commercial</option></select></label>'
        '<label class="enq-field">Purpose <select name="purpose"><option value="">Select</option><option>Self Use / End-Use</option><option>Investment / Rental</option><option>First Home</option><option>Upgrade</option></select></label>'
        '</div>'
        '<div class="enq-honeypot" aria-hidden="true"><label>Leave this field empty<input name="website" type="text" tabindex="-1" autocomplete="off"></label></div>'
        '<p class="enq-error" role="alert" aria-live="polite"></p>'
        f'<button class="enq-submit" type="submit">{e(t["enq_submit"])}</button>'
        '</form></div></section>\n'
    )


def about(t):
    body = ''.join(f'<p>{e(x)}</p>' for x in t['about'])
    quote = t.get('quote') or ''
    quote_html = (
        f'<div class="about-quote"><p>{e(quote)}</p><cite>Prestige Projects</cite></div>'
        if quote else ''
    )
    return (
        '<section class="sec home-about" id="about"><div class="in about-grid"><div>'
        f'{eye(t["about_eye"])}<h2 class="dh">{t["about_h"]}</h2><div class="about-body" style="margin-top:30px">{body}</div></div>'
        f'<div><div class="about-photo about-photo-wide"><img src="/img/about.jpg?v={ASSET_VER}" width="1024" height="512" loading="lazy" alt="{a(t["about_alt"])}"></div>'
        f'{quote_html}</div></div></section>\n'
    )


def zoom_img(src, w, h, alt, t, cls):
    return (f'<div class="{cls} plan-img-wrap" data-full="{src}" data-title="{a(alt)}" role="button" tabindex="0" aria-label="{a(alt)}">'
            f'<img src="{src}" width="{w}" height="{h}" loading="lazy" alt="{a(alt)}">'
            f'<span class="plan-zoom-hint">{icon("zoom")}<span>{e(t["tap"])}</span></span></div>')


def projects(t):
    one_rows = ''
    gold_rows = ''
    for i, (href, img, w, h, alt, name, title, sell, lead, btn) in enumerate(t['projects']):
        landscape = ' is-landscape' if w > h else ''
        flip = ' is-flipped' if i % 2 else ''
        alt_band = ' is-alt' if i % 2 else ''
        is_one = href == '/projects/prestige-one/'
        is_gold = href == '/projects/prestige-gold/'
        inline = zoom_img('/img/prestige-one/riverside-interior.webp', 1774, 887, t['one_view_alt'], t, 'project-inline-media') if is_one else ''
        if is_gold:
            media = (
                f'<div class="project-showcase-media{landscape} project-media-rotator" data-project-rotator data-interval="4500">'
                f'<img class="is-active" src="{img}" width="{w}" height="{h}" loading="lazy" alt="{a(alt)}">'
                f'<img src="/img/prestige-gold-night.webp" width="1024" height="576" loading="lazy" alt="{a(alt)} — night view">'
                '</div>'
            )
        else:
            media = (
                f'<div class="project-showcase-media{landscape}">'
                f'<img src="{img}" width="{w}" height="{h}" loading="lazy" alt="{a(alt)}"></div>'
            )
        band = (
            f'<div class="home-project-band{alt_band}">'
            f'<div class="in project-showcase-grid home-project{flip}">{media}'
            f'<div class="project-showcase-copy">{eye(name)}<h3 class="dh">{title}</h3>'
            f'<p class="project-sell">{e(sell)}</p><p class="lead">{e(lead)}</p>{inline}'
            f'<p class="home-project-cta-wrap"><a class="btn-g home-project-cta" href="{href}"><span>{e(btn)}</span>{icon("arrow")}</a></p></div></div>'
        )
        if is_one:
            poster = f'/img/prestige-one/one-life-one-home.webp?v={ASSET_VER}'
            band += f'<div class="in project-banner">{zoom_img(poster, 1024, 512, t["one_poster_alt"], t, "project-banner-media")}</div>'
        band += '</div>'
        if is_one:
            one_rows += band
        else:
            gold_rows += band
    return (
        '<section class="sec project-showcase home-projects" id="projects"><span id="types" class="home-anchor" aria-hidden="true"></span>'
        f'<div class="in home-sec-head">{eye(t["projects_eye"], "eye-center")}<h2 class="dh">{t["projects_h"]}</h2></div>'
        f'{one_rows}</section>\n'
        f'<section class="sec project-showcase home-projects">{gold_rows}</section>\n'
    )


def features_amenities(t):
    cards = ''.join(
        f'<article class="feat-card"><div class="feat-icon" aria-hidden="true">'
        f'<img src="{FEAT_ICONS[ic]}" alt="" width="72" height="72" loading="lazy" decoding="async">'
        f'</div><h3>{e(title)}</h3><p>{e(desc)}</p></article>'
        for ic, title, desc in t['feat_cards']
    )
    return (
        '<section class="sec home-features" id="amenities"><span id="services" class="home-anchor" aria-hidden="true"></span>'
        f'<div class="in home-sec-head">{eye(t["amen_eye"], "eye-center")}<h2 class="dh">{t["amen_h"]}</h2>'
        f'<p class="lead">{e(t["feat_p"])}</p></div>'
        f'<div class="in feat-grid">{cards}</div></section>\n'
    )


def amenity_cards(eyebrow, heading, lead, items, sec_id='amenity-details'):
    cards = ''.join(f'<li>{icon("check", "amen-card-icon")}<span>{e(x)}</span></li>' for x in items)
    return (
        f'<section class="sec home-amenities" id="{sec_id}"><div class="in amen-block">'
        f'<div class="amen-block-head">{eye(eyebrow)}<h2 class="dh">{heading}</h2>'
        + (f'<p class="lead">{e(lead)}</p>' if lead else '') +
        f'</div><ul class="amen-cards">{cards}</ul></div></section>\n'
    )


def amenities(t):
    return amenity_cards(t['roof_eye'], t['roof_h'], t['roof_p'], t['roof_feats'])


def specifications(t):
    specs = ''.join(f'<li>{e(x)}</li>' for x in t['specs'])
    sec = ''.join(f'<li>{e(x)}</li>' for x in t['security'])
    return (
        '<section class="sec home-amenities" id="specifications"><div class="in amen-block">'
        f'<div class="amen-block-head">{eye(t["spec_eye"])}<h2 class="dh">{t["spec_h"]}</h2></div>'
        f'<div class="amen-lists"><div><h4>{e(t["spec_h1"])}</h4><ul class="amen-list">{specs}</ul></div>'
        f'<div class="amen-security"><h4>{icon("shield")}{e(t["spec_h2"])}</h4><ul class="amen-list">{sec}</ul></div></div>'
        '</div></section>\n'
    )


def amenity_gallery(t):
    tiles = ''.join(
        f'<figure class="amen-tile"><img src="{AMENITY_IMG_BASE}/{slug}.webp" width="512" height="288" loading="lazy" alt="{a(name)}">'
        f'<figcaption>{e(name)}</figcaption></figure>'
        for slug, name in zip(AMENITY_IMGS, t['amen_names'])
    )
    return (
        '<section class="sec home-amenities home-amenity-gallery" id="amenity-gallery"><div class="in">'
        f'{eye(t["amen_eye"])}<h2 class="dh">{t["amen_gallery_h"]}</h2>'
        f'<p class="lead">{e(t["amen_lead"])}</p>'
        f'<div class="amen-grid">{tiles}</div></div></section>\n'
    )


def _area_display(t, area):
    if not area:
        return e(t['on_request'])
    return f'{e(area)} {e(t["sqft"])}'


def _price_row(t, index, total, name, mono, area, price, feats, msg, img='', alt=''):
    if img:
        visual = (
            f'<div class="price-row-visual plan-img-wrap" data-full="{img}" data-title="{a(alt)}" role="button" tabindex="0" aria-label="{a(alt)}">'
            f'<img src="{img}" width="1024" height="575" loading="lazy" decoding="async" alt="{a(alt)}">'
            f'<span class="plan-zoom-hint">{icon("zoom")}<span>{e(t["tap"])}</span></span></div>'
        )
    else:
        visual = (
            f'<div class="price-row-visual price-visual-request">'
            f'<span class="price-visual-monogram">{e(mono)}</span><span>{e(t["plan_req"])}</span></div>'
        )
    return (
        f'<article class="price-row"><div class="price-row-visual-wrap">{visual}</div>'
        f'<div class="price-row-identity"><span class="price-row-number">0{index} / 0{total}</span><h3>{e(name)}</h3>'
        f'<span class="price-row-area-label">{e(t["area_label"])}</span><strong class="price-row-area">{_area_display(t, area)}</strong></div>'
        f'<div class="price-row-specs"><span class="price-row-spec-heading">{e(t["details"])}</span>'
        f'<ul>{"".join(f"<li>{e(x)}</li>" for x in feats)}</ul></div>'
        f'<div class="price-row-offer"><span class="price-row-starting">{e(t["starting"])}</span>'
        f'<strong class="price-row-price">{e(price)}</strong>'
        f'<span class="price-row-onwards">{e(t["onwards"])}</span>'
        f'<a class="price-row-cta" href="{a(wa(msg))}" target="_blank" rel="noopener">{e(t["enquire"])}'
        f'<span aria-hidden="true">↗</span></a></div></article>'
    )


def pricing_gold(t):
    gold_total = len(t['units']) + len(t['gold_extra'])
    rows = ''
    for i, (name, area, price, img, alt, feats) in enumerate(t['units']):
        mono = f'{name[0]}B'
        msg = t['wa_text'] + f' ({name})'
        rows += _price_row(t, i + 1, gold_total, name, mono, area, price, feats, msg, img, alt)
    for j, (name, mono, area, price, feats, msg) in enumerate(t['gold_extra']):
        rows += _price_row(t, len(t['units']) + j + 1, gold_total, name, mono, area, price, feats, msg)
    return (
        '<section class="sec price-section" id="pricing"><div class="in"><div class="price-section-head"><div>'
        f'{eye(t["price_eye"])}<h2 class="dh price-section-title">{t["price_h"]}</h2>'
        f'<p class="price-section-intro">{e(t["gold_p"])}</p></div>'
        f'<div class="price-section-aside"><span class="price-aside-rule"></span><strong>{e(t["gold_aside_k"]).upper()}</strong>'
        f'<span>{e(t["gold_aside_v"])}</span></div></div>'
        f'<div class="price-brand price-brand-gold"><div class="price-brand-head">{eye(t["gold_eye"])}'
        f'<h3 class="price-brand-title">{t["gold_h"]}</h3>'
        f'<p class="price-brand-intro">{e(t["gold_p"])}</p></div>'
        f'<div class="price-rows">{rows}</div></div>'
        f'<p class="price-section-note">{e(t["price_note"])}</p></div></section>\n'
    )


def pricing_one(t):
    one_total = len(t['one_units'])
    one_rows = ''
    for i, (name, mono, area, price, feats, msg) in enumerate(t['one_units']):
        one_rows += _price_row(t, i + 1, one_total, name, mono, area, price, feats, msg)
    return (
        '<section class="sec price-section" id="pricing"><div class="in"><div class="price-section-head"><div>'
        f'{eye(t["price_eye"])}<h2 class="dh price-section-title">{t["one_h"]}</h2>'
        f'<p class="price-section-intro">{e(t["one_p"])}</p></div>'
        f'<div class="price-section-aside"><span class="price-aside-rule"></span><strong>{e(t["one_eye"]).upper()}</strong>'
        f'<span>3 &amp; 5 BHK (Jodi) · on request</span></div></div>'
        f'<div class="price-brand price-brand-one"><div class="price-brand-head">{eye(t["one_eye"])}'
        f'<h3 class="price-brand-title">{t["one_h"]}</h3>'
        f'<p class="price-brand-intro">{e(t["one_p"])}</p></div>'
        f'<div class="price-rows">{one_rows}</div></div>'
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
        img = FEATURED_GUIDE_IMAGES[slug]
        cat = t['guide_cats'].get(p['cat'], p['cat'])
        cards += (
            f'<a class="card home-guide-card" href="{pfx}/blog/{slug}/">'
            f'<img src="{img}?v={BLOG_PHOTO_VERSION}" width="1400" height="933" loading="lazy" decoding="async" alt="{a(p["title"])}">'
            f'<div class="card-b"><span class="card-k">{e(cat)}</span><h3>{e(p["title"])}</h3>'
            f'<p>{e(p["desc"])}</p>'
            f'<span class="card-m"><time datetime="2026-10-29">{e(t["guides_date"])}</time> · {e(t["guides_min"].format(n=p["read"]))}</span></div></a>'
        )
    return (
        '<section class="sec home-guides" id="guides"><div class="in">'
        f'<div class="home-sec-head">{eye(t["guides_eye"], "eye-center")}<h2 class="dh">{t["guides_h"]}</h2>'
        f'<p class="lead">{e(t["guides_p"])}</p></div>'
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
        f'<div><iframe class="map" src="{MAPS_EMBED}" title="{a(ADDRESS)}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div></div></section>\n</main>\n'
    )


def footer(l, t):
    p = PREFIX[l]

    def foot_href(href):
        if href.startswith('/projects/') or href.startswith('http'):
            return href
        if href.startswith('#'):
            return (p + '/' if p else '') + href
        if href.startswith('/'):
            return (p + href) if p and not href.startswith(p + '/') and href != p + '/' else href
        return p + '/' + href

    links = ''.join(
        f'<li><a href="{foot_href(href)}">{e(lbl)}</a></li>'
        for href, lbl in t['foot_links'])
    langs = ''.join(f'<a href="{PREFIX[k]}/" hreflang="{k}" lang="{k}"' + (' aria-current="true"' if k == l else '') + f'>{n}</a>'
                    for k, n in (('en', 'English'), ('hi', 'हिन्दी'), ('mr', 'मराठी')))
    return (
        '<footer class="home-footer"><div class="foot-grid">'
        f'<div><a class="foot-logo-link" href="{p}/" aria-label="Prestige Projects"><img src="/img/logo-on-dark.png" width="210" height="70" alt="Prestige Projects" class="foot-logo"></a>'
        f'<p>{e(t["foot_tag"])}</p><div class="foot-langs">{langs}</div></div>'
        f'<div><h4>{e(t["foot_explore"])}</h4><ul>{links}</ul></div>'
        f'<div><h4>{e(t["foot_contact"])}</h4><p><a href="{MAPS_URL}" target="_blank" rel="noopener">{ADDRESS}</a></p>'
        f'<p><a href="tel:{PHONE_TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p></div></div>'
        f'<div class="foot-legal"><p class="foot-rera"><strong>MahaRERA Reg. No:</strong> {RERA}</p>'
        f'<p><a href="/privacy/">{e(t["privacy"])}</a></p><p>{e(t["disclaimer"])}</p><p>{e(t["rights"])}</p></div></footer>\n'
        f'<a class="wa" href="{a(wa(t["wa_text"]))}" target="_blank" rel="noopener" aria-label="{a(t["wa_btn"])}">{icon("chat")}<span>{e(t["float_wa"])}</span></a>\n'
        f'<script src="/assets/site.js?v={ASSET_VER}" defer></script>\n</body>\n</html>\n'
    )


def build(l):
    t = T[l]
    page = (head(l, t) + nav(l, t) + hero(t) + intro(t) + enquiry(t) + about(t) + projects(t)
            + location(t) + faq(t) + guides(t, l) + contact(t) + footer(l, t))
    out_dir = os.path.join(ROOT, PREFIX[l].lstrip('/')) if PREFIX[l] else ROOT
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, 'index.html')
    with open(out, 'w', encoding='utf-8') as f:
        f.write(page)
    print('wrote', os.path.relpath(out, ROOT), len(page))


if __name__ == '__main__':
    for lang in LANGS:
        build(lang)
