"""Structured data that ties the brand and both projects together (JSON-LD only, nothing visible).

Prestige Projects (also searched as "Prestige Enterprises", the domain name) -> makesOffer ->
Prestige Gold / Prestige One apartments. Facts mirror what the site already shows.
"""
import config as C

AGENT_ID = C.SITE + '/#agent'
WEBSITE_ID = C.SITE + '/#website'
GOLD_ID = C.SITE + '/projects/prestige-gold/#project'
ONE_ID = C.SITE + '/projects/prestige-one/#project'
ALT_NAMES = ['Prestige Enterprises', 'Prestige Enterprises Kalyan', 'Prestige Projects Kalyan']

GOLD_ADDRESS = {'@type': 'PostalAddress', 'streetAddress': 'Near Mahavir Jain School, Kala Talao, Kalyan West',
                'addressLocality': 'Kalyan', 'addressRegion': 'Maharashtra', 'postalCode': '421301', 'addressCountry': 'IN'}
ONE_ADDRESS = {'@type': 'PostalAddress', 'streetAddress': C.STREET, 'addressLocality': C.LOCALITY,
               'addressRegion': C.REGION, 'postalCode': C.POSTAL, 'addressCountry': C.COUNTRY}

AMENITIES = ['High-speed lifts', 'Rooftop garden', 'Outdoor gym', 'Indoor games room', 'Multipurpose hall',
             'CCTV surveillance', 'Secured gated entrance', 'Lifts with power backup', 'Parking']


def _amen():
    return [{'@type': 'LocationFeatureSpecification', 'name': a, 'value': True} for a in AMENITIES]


def gold_project():
    return {
        '@type': 'ApartmentComplex', '@id': GOLD_ID, 'name': 'Prestige Gold', 'url': C.SITE + '/projects/prestige-gold/',
        'description': 'Mixed-use residential and commercial project in Kalyan West near Kala Talao: 1, 2 & 3 BHK flats from ₹55 Lakh plus retail and office space. Sample flat ready.',
        'image': C.SITE + '/img/prestige-tower-day.jpg', 'address': GOLD_ADDRESS,
        'containedInPlace': {'@type': 'Place', 'name': 'Kalyan West, Kalyan, Maharashtra'},
        'amenityFeature': _amen(), 'telephone': '+918446652600',
        'subjectOf': {'@id': C.SITE + '/projects/prestige-gold/#webpage'},
    }


def one_project():
    return {
        '@type': 'ApartmentComplex', '@id': ONE_ID, 'name': 'Prestige One', 'url': C.SITE + '/projects/prestige-one/',
        'description': 'Residential project at Godrej Hill, Khadakpada, Kalyan West offering only 3 BHK and 5 BHK (Jodi) homes. Layouts and pricing shared on request.',
        'image': C.SITE + '/img/Prestige%20One%20Tower%20in%20Daylight.png', 'address': ONE_ADDRESS,
        'geo': {'@type': 'GeoCoordinates', 'latitude': 19.262936, 'longitude': 73.1425496}, 'hasMap': C.MAPS_URL,
        'containedInPlace': {'@type': 'Place', 'name': 'Khadakpada, Kalyan West, Maharashtra'},
        'amenityFeature': _amen(), 'telephone': C.PHONE_TEL,
        'subjectOf': {'@id': C.SITE + '/projects/prestige-one/#webpage'},
    }


def _offer(oid, name, place_id, rooms, price=None, size=None):
    item = {'@type': 'Apartment', 'name': name, 'containedInPlace': {'@id': place_id}}
    if rooms:
        item['numberOfBedrooms'] = rooms
    if size:
        item['floorSize'] = {'@type': 'QuantitativeValue', 'minValue': size[0], 'maxValue': size[1], 'unitCode': 'FTK',
                             'description': 'RERA area (sq. ft.) as listed on the project page'}
    o = {'@type': 'Offer', '@id': oid, 'name': name, 'itemOffered': item, 'offeredBy': {'@id': AGENT_ID},
         'availability': 'https://schema.org/LimitedAvailability', 'areaServed': 'Kalyan West'}
    if price:
        o.update({'priceCurrency': 'INR', 'priceSpecification': {'@type': 'PriceSpecification', 'minPrice': price, 'priceCurrency': 'INR',
                                                                  'description': 'All-in price starting from, as listed on the site'}})
    return o


def offers():
    g = C.SITE + '/projects/prestige-gold/#offer-'
    o = C.SITE + '/projects/prestige-one/#offer-'
    return [
        _offer(g + '1bhk', 'Prestige Gold 1 BHK, Kalyan West', GOLD_ID, 1, 5500000, (404, 519)),
        _offer(g + '2bhk', 'Prestige Gold 2 BHK, Kalyan West', GOLD_ID, 2, 7500000, (577, 721)),
        _offer(g + '3bhk', 'Prestige Gold 3 BHK, Kalyan West', GOLD_ID, 3, 14000000),
        _offer(o + '3bhk', 'Prestige One 3 BHK, Godrej Hill, Kalyan West', ONE_ID, 3),
        _offer(o + '5bhk-jodi', 'Prestige One 5 BHK (Jodi), Godrej Hill, Kalyan West', ONE_ID, 5),
    ]


def agent_extra():
    """Extra fields merged into every RealEstateAgent node."""
    return {'alternateName': ALT_NAMES,
            'makesOffer': [{'@id': x['@id']} for x in offers()]}


def project_graph():
    """Both projects + their offers, for pages that should carry the full brand-project link."""
    return [gold_project(), one_project()] + offers()


def strip_links(text):
    import re
    return re.sub(r'\[([^\]]+)\]\((/[^)\s]*)\)', r'\1', text)
