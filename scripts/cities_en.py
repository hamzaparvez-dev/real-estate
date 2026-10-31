"""City pages, English (source of truth). cities_hi.py / cities_mr.py mirror this structure
exactly (same slugs, same number of facts / hoods / why / faq) and build.py asserts it.

Facts about infrastructure were checked in Oct 2026. Anything not yet open is described as
"under construction" or "planned": update those lines as projects open.
"""

# order = order in menus; group key -> label lives in the UI strings
MENU = [
    ('thane-district', ['kalyan', 'dombivli', 'thane', 'ulhasnagar', 'ambernath', 'badlapur', 'bhiwandi']),
    ('mumbai-region', ['mumbai', 'navi-mumbai', 'panvel']),
]

NEAR = {
    'kalyan': ['dombivli', 'ulhasnagar', 'bhiwandi', 'thane'],
    'dombivli': ['kalyan', 'ulhasnagar', 'thane', 'navi-mumbai'],
    'thane': ['mumbai', 'kalyan', 'navi-mumbai', 'bhiwandi'],
    'ulhasnagar': ['kalyan', 'ambernath', 'dombivli'],
    'ambernath': ['ulhasnagar', 'badlapur', 'kalyan'],
    'badlapur': ['ambernath', 'ulhasnagar', 'kalyan'],
    'bhiwandi': ['kalyan', 'thane', 'mumbai'],
    'mumbai': ['thane', 'navi-mumbai', 'kalyan'],
    'navi-mumbai': ['panvel', 'thane', 'mumbai'],
    'panvel': ['navi-mumbai', 'kalyan', 'badlapur'],
}

# which image tells each city's story (see scripts/make_images.py)
IMG = {s: f'/img/areas/{s}.jpg' for s in NEAR}

CITIES = {
    'kalyan': {
        'name': 'Kalyan',
        'desc': 'Property in Kalyan, Maharashtra: flats, plots and rentals in Khadakpada, Kalyan West, Kalyan East and Titwala. Talk to Prestige Enterprises on WhatsApp.',
        'alt': 'Illustration of Kalyan with a hill fort, towers and a suburban train at sunrise',
        'lead': 'Buy, sell or rent in Kalyan with a local team based at Godrej Hill, Khadakpada. We help you compare localities, check RERA and close the deal with clean paperwork.',
        'card': 'Khadakpada, Kalyan West, Kalyan East and Titwala. Our home base.',
        'intro': [
            'Kalyan is one of the busiest rail junctions on the Central line, where routes to Mumbai, Pune and Nashik meet. That connectivity, plus homes that usually cost less than in Thane or Mumbai, is why so many families and first-time buyers look here first.',
            "Our office is in Khadakpada, so site visits are quick. We help you check what a brochure won't show: monsoon waterlogging, society paperwork, approach roads and the builder's RERA record.",
        ],
        'facts': [
            ('District', 'Thane'),
            ('Rail', 'Kalyan Junction on the Central line, with routes towards Kasara and Karjat'),
            ('Roads', 'Kalyan–Shil Road, Kalyan–Murbad Road, Kalyan–Bhiwandi Road'),
            ('Coming up', 'Metro Line 5 (Thane–Bhiwandi–Kalyan) is under construction; Metro 12 towards Taloja is planned'),
        ],
        'hoods': [
            ('Khadakpada and Godrej Hill', 'Kalyan West, near the creek and our office. A mix of newer towers and established societies.'),
            ('Adharwadi and Wayle Nagar', 'Dense, well-served Kalyan West neighbourhoods close to the station, schools and markets.'),
            ('Kalyan East', 'Tisgaon, Katemanivali and nearby areas, with local markets and a steady supply of new projects.'),
            ('Titwala and Shahad', 'Stations on either side of Kalyan with lower entry prices and a longer commute.'),
        ],
        'why': [
            ('Connectivity', 'Fast and slow locals, long-distance trains and the Kalyan–Shil and Murbad roads all start here.'),
            ('Value', 'Compare a 2 BHK here with the same size in Thane or Mumbai and the saving is usually large.'),
            ('Pipeline', 'Metro and road projects in the corridor are why buyers and investors are watching Kalyan.'),
        ],
        'faq': [
            ('Which part of Kalyan is best for a first home?', 'It depends on budget, commute and schools. Khadakpada and Kalyan West suit families who want newer societies. Titwala and Shahad cost less but add commute time. Tell us your budget and we will shortlist three or four options to visit.'),
            ('Can you check a Kalyan project\'s RERA registration for me?', 'Yes. Send us the project name or MahaRERA number and we will check the registration, the promoter and the promised possession date with you before you pay a token amount.'),
        ],
    },
    'dombivli': {
        'name': 'Dombivli',
        'desc': 'Property in Dombivli East and West: flats, resale homes and rentals near the station, Manpada Road and Palava. Talk to Prestige Enterprises on WhatsApp.',
        'alt': 'Illustration of Dombivli with residential towers, a small temple and a local train at dusk',
        'lead': 'Dombivli sits right next to Kalyan and has long been a favourite for salaried families. We help you choose between East and West, new and resale, and check the paperwork.',
        'card': 'Dombivli East and West, Manpada Road, Thakurli and Palava.',
        'intro': [
            "Dombivli is Kalyan's twin on the Central line and part of the same municipal corporation, KDMC. It has well-established schools, markets and cultural life, and a large pool of resale flats alongside new towers.",
            'Because the stock is so varied, the right choice depends on the building: its age, society records, parking and redevelopment prospects. We walk through those with you before you commit.',
        ],
        'facts': [
            ('District', 'Thane'),
            ('Rail', 'Dombivli station on the Central line, between Thakurli and Kopar'),
            ('Roads', 'Kalyan–Shil Road, Manpada Road and links towards Thane and Navi Mumbai'),
            ('Coming up', 'Metro Line 5 and the Kalyan–Taloja metro (Line 12) would improve links; both are still in progress'),
        ],
        'hoods': [
            ('Dombivli East', 'Manpada Road and the MIDC Residential Zone: a mix of older societies and newer projects.'),
            ('Dombivli West', 'Gopi Nagar, Kopar and surrounding lanes, with markets and schools within walking distance.'),
            ('Thakurli and Pandurangwadi', 'Quieter residential pockets with their own station access.'),
            ('Nilje and Palava', 'Along Kalyan–Shil Road: larger planned townships and newer towers.'),
        ],
        'why': [
            ('Established', 'Schools, hospitals, markets and community life are already in place.'),
            ('Choice', 'Resale, new launches and redevelopment projects all exist side by side.'),
            ('Nearby jobs', 'Thane, Navi Mumbai and Mumbai are reachable by rail or road.'),
        ],
        'faq': [
            ('Is a resale flat in Dombivli a good idea?', 'Often yes, if the society paperwork is clean. We check the share certificate, society NOC, maintenance dues and any redevelopment plans before you pay a token amount.'),
            ('Is Dombivli cheaper than Kalyan?', 'Prices vary lane by lane, not just by city. We pull recent sale and listing prices for the exact locality so you compare like with like.'),
        ],
    },
    'thane': {
        'name': 'Thane',
        'desc': 'Property in Thane: apartments in Majiwada, Ghodbunder Road, Naupada and Kolshet. Buy, sell or rent with Prestige Enterprises. Message us on WhatsApp.',
        'alt': 'Illustration of Thane with a lake, hills and residential towers',
        'lead': 'Thane combines city amenities with lakes and hills nearby. We help buyers and investors compare Thane micro-markets, from older Thane West to the Ghodbunder Road towers.',
        'card': 'Naupada, Majiwada, Ghodbunder Road and Kolshet.',
        'intro': [
            'Thane is often called the City of Lakes. It has a major junction station, malls, hospitals and a large base of working professionals, and it sits right at the edge of Sanjay Gandhi National Park.',
            'Prices rise quickly as you move closer to the station and the Eastern Express Highway, so the choice of micro-market matters more here than almost anywhere else on the Central line.',
        ],
        'facts': [
            ('District', 'Thane'),
            ('Rail', 'Thane Junction on the Central line and the Trans-Harbour line to Navi Mumbai and Panvel'),
            ('Roads', 'Eastern Express Highway, Ghodbunder Road and the Mumbai–Nashik highway'),
            ('Coming up', 'Metro Line 4 (Wadala–Kasarvadavali) and Line 5 (Thane–Bhiwandi–Kalyan) are under construction'),
        ],
        'hoods': [
            ('Naupada and Charai', 'Thane West centre: established, walkable, close to the station and markets.'),
            ('Majiwada and Manpada', 'Along the Eastern Express Highway, with quick access to Mumbai and plenty of high-rise options.'),
            ('Ghodbunder Road', 'Kasarvadavali, Owale and Hiranandani Estate: newer townships with open spaces.'),
            ('Kolshet and Balkum', 'Growing residential belt with a range of mid-budget projects.'),
        ],
        'why': [
            ('Amenities', 'Lakes, malls, hospitals and schools within the city.'),
            ('Access', 'Rail, the highway and several metro lines serve the city.'),
            ('Demand', 'Strong rental and resale demand from people working in Mumbai and Navi Mumbai.'),
        ],
        'faq': [
            ('How much does a 2 BHK cost in Thane?', 'It varies a lot by micro-market, age and amenities. Ask us for a short comparison for your budget and we will share recent listings and sale prices for the exact localities you are considering.'),
            ('Is stamp duty in Thane different from Mumbai?', 'Rates differ between municipal areas, and a woman buying in her sole name gets a concession. See our stamp duty guide and confirm the current rate with the sub-registrar before you sign.'),
        ],
    },
    'ulhasnagar': {
        'name': 'Ulhasnagar',
        'desc': 'Property in Ulhasnagar: flats, resale homes and shops across Camps 1 to 5. Buy, sell or rent with Prestige Enterprises. Message us on WhatsApp.',
        'alt': 'Illustration of Ulhasnagar with colourful buildings, market awnings and festive bunting',
        'lead': 'Ulhasnagar is a dense, lively market city between Kalyan and Ambernath. We help you buy, sell or rent homes and shops here, including redevelopment projects.',
        'card': 'Camps 1 to 5, Vitthalwadi and the Shahad edge.',
        'intro': [
            "Ulhasnagar grew from a post-Partition settlement and is known for its large markets and entrepreneurial energy. It is organised into numbered 'Camps' and has its own municipal corporation.",
            'Homes and shops here are often in older buildings, so title checks, society records and redevelopment rights matter. We work through those details with you before any payment.',
        ],
        'facts': [
            ('District', 'Thane'),
            ('Rail', 'Ulhasnagar and Vitthalwadi stations, between Kalyan and Ambernath'),
            ('Roads', 'Kalyan–Badlapur Road and links to Kalyan and Shahad'),
            ('Coming up', 'A metro extension from Durgadi (Kalyan) to Ulhasnagar and Ambernath (Metro 5A) has been proposed'),
        ],
        'hoods': [
            ('Camps 1 and 2', 'Older residential blocks and local markets; several buildings are candidates for redevelopment.'),
            ('Camps 3 and 4', 'The busiest commercial areas, with shops, small offices and dense housing.'),
            ('Camp 5', 'Outer parts of the city with newer buildings and more open space.'),
            ('Vitthalwadi and the Shahad edge', 'Close to Kalyan stations, convenient for daily commuters.'),
        ],
        'why': [
            ('Affordable', 'Ticket sizes are often lower than in Kalyan or Thane.'),
            ('Commerce', 'A strong market economy supports shop and small-office demand.'),
            ('Location', 'One or two stations from Kalyan Junction.'),
        ],
        'faq': [
            ('Can you help with shops and commercial units in Ulhasnagar?', 'Yes. We help with shops, offices and small commercial units, including checking ownership documents and agreements before you pay.'),
            ('Should I buy in an old building here?', 'It can work if the title is clean and the society is organised. We check the paperwork and ask about structural condition and redevelopment plans first.'),
        ],
    },
    'ambernath': {
        'name': 'Ambernath',
        'desc': 'Property in Ambernath East and West: affordable flats, plots and rentals near the station and Anand Nagar MIDC. Talk to Prestige Enterprises on WhatsApp.',
        'alt': 'Illustration of the ancient Ambernath temple against hills at sunrise',
        'lead': 'Ambernath offers affordable homes on the Kalyan–Karjat line, with an industrial belt nearby. We help you find a home, a plot or a rental that fits your budget.',
        'card': 'Ambernath East and West, Anand Nagar and the Badlapur road belt.',
        'intro': [
            "Ambernath is best known for its ancient Shiva temple, which dates back to the 11th century, and for its industrial areas, including the Anand Nagar MIDC and an ordnance factory. It has steady demand from people who work locally and from Kalyan–Dombivli commuters looking for lower prices.",
            'New projects keep appearing along the Ambernath–Badlapur road, so it pays to check RERA registration and possession timelines carefully. We do that with you.',
        ],
        'facts': [
            ('District', 'Thane'),
            ('Rail', 'Ambernath station on the Kalyan–Karjat line of the Central railway'),
            ('Roads', 'Kalyan–Badlapur Road and Ambernath–Badlapur Road'),
            ('Coming up', 'A metro extension from Kalyan (Durgadi) has been proposed; check current status before relying on it'),
        ],
        'hoods': [
            ('Ambernath West', 'Station side with the main market, schools and older housing.'),
            ('Ambernath East', 'Anand Nagar MIDC side, popular with those who work in the industrial area.'),
            ('Along Ambernath–Badlapur Road', 'Newer projects and townships with more open space.'),
            ('Near the temple and hills', 'Quiet pockets with greenery, popular for weekend homes and plots.'),
        ],
        'why': [
            ('Price', 'Among the more affordable stations on the Kalyan–Karjat line.'),
            ('Industry', 'Jobs and tenants from the MIDC and nearby units.'),
            ('Greenery', 'Hills and open land close by.'),
        ],
        'faq': [
            ('Is Ambernath a good place to invest?', 'It can be if you buy a well-located, RERA-registered project and plan for a longer holding period. We share realistic rent and resale evidence rather than promises.'),
            ('Do you help with plots in Ambernath?', 'Yes. For plots we check the 7/12 extract, land-use status and approvals with your lawyer before any token payment.'),
        ],
    },
    'badlapur': {
        'name': 'Badlapur',
        'desc': 'Property in Badlapur: flats, row houses and plots in Katrap, Belvali, Kulgaon and near Barvi Dam. Buy, sell or rent with Prestige Enterprises.',
        'alt': 'Illustration of Badlapur with green hills, mist, a river and small houses',
        'lead': 'Badlapur is green, quieter and more affordable than most of MMR. We help you pick the right locality and verify the project before you commit.',
        'card': 'Katrap, Belvali, Kulgaon and the Barvi Dam side.',
        'intro': [
            'Badlapur sits near the Ulhas river with the Sahyadri foothills close by. It is popular with buyers who want more space for their budget and are comfortable with a longer train commute to Kalyan, Thane or Mumbai.',
            'With so many new launches, the main risk is picking a project with unclear approvals or a weak delivery record. We check the MahaRERA page, approvals and the promoter track record before you pay.',
        ],
        'facts': [
            ('District', 'Thane'),
            ('Rail', 'Badlapur station on the Central line, towards Karjat'),
            ('Roads', 'Kalyan–Badlapur Road and Badlapur–Murbad Road'),
            ('Nature', 'Near the Ulhas river, Barvi Dam and the Sahyadri foothills'),
        ],
        'hoods': [
            ('Katrap and Belvali', 'Fast-growing residential areas with many newer projects.'),
            ('Kulgaon and Sonivali', 'Established pockets near markets and schools.'),
            ('Around the station', 'Convenient for daily commuters, with the highest rental demand.'),
            ('Barvi Dam side', 'Open and green, of interest to plot and weekend-home buyers.'),
        ],
        'why': [
            ('Space', 'Larger homes for the money than in most of MMR.'),
            ('Environment', 'Hills, greenery and cleaner air nearby.'),
            ('Entry price', 'A realistic option for first-time buyers.'),
        ],
        'faq': [
            ('Is the commute from Badlapur practical?', 'Many people do it daily by train. Check the first and last trains on your route and the time to the station from the project before you decide.'),
            ('Can you help me find a rental in Badlapur?', 'Yes. Tell us your budget and preferred area and we will shortlist rental homes and handle the Leave and License agreement.'),
        ],
    },
    'bhiwandi': {
        'name': 'Bhiwandi',
        'desc': 'Property in Bhiwandi: flats, rentals, shops and warehouse space near Kalyan Road and Dhamankar Naka. Talk to Prestige Enterprises on WhatsApp.',
        'alt': 'Illustration of Bhiwandi with warehouses, trucks and a highway at sunset',
        'lead': 'Bhiwandi is a major logistics and powerloom centre. We help you with flats, rentals, shops and commercial space, and with the checks they need.',
        'card': 'Dhamankar Naka, Kalyan Road, Anjurphata and Kasheli.',
        'intro': [
            'Bhiwandi is one of the biggest warehousing and powerloom hubs in the region, with direct highway access to Mumbai, Nashik and Gujarat. Demand for both homes and commercial space is driven by that economy.',
            'Commercial and industrial property needs careful checks on land use, approvals and lease terms. We help you read the paperwork and bring in your lawyer at the right moment.',
        ],
        'facts': [
            ('District', 'Thane'),
            ('Rail', 'Bhiwandi Road station on the Diva–Vasai line; Kalyan and Thane are the practical rail links'),
            ('Roads', 'Mumbai–Nashik highway, Kalyan–Bhiwandi Road and the road towards Wada'),
            ('Coming up', 'Metro Line 5 stations are planned at Dhamankar Naka, Anjurphata, Purna, Kalher and Kasheli'),
        ],
        'hoods': [
            ('Dhamankar Naka', 'The main junction, with shops, offices and mixed housing.'),
            ('Kalyan Road and Anjurphata', 'Along the Kalyan–Bhiwandi corridor, with new residential projects.'),
            ('Kasheli and Kalher', 'Close to the Thane side and many warehouses, popular for rentals.'),
            ('Purna', 'Industrial and warehousing activity, with growing nearby housing.'),
        ],
        'why': [
            ('Economy', 'Warehousing and textiles create steady tenant demand.'),
            ('Access', 'Highways and the planned metro line connect Bhiwandi to Thane and Kalyan.'),
            ('Value', 'Typically lower ticket sizes than Thane.'),
        ],
        'faq': [
            ('Do you help with warehouse or industrial space?', 'We can help you find and evaluate commercial space and walk through lease terms. Your lawyer should review the final agreement.'),
            ('Is Bhiwandi good for rental income?', 'Rental demand from workers and logistics staff is steady in many pockets. Yields vary, so we compare actual rents in your exact locality.'),
        ],
    },
    'mumbai': {
        'name': 'Mumbai',
        'desc': 'Property in Mumbai: resale flats, redevelopment and new projects across the central, eastern and western suburbs. Talk to Prestige Enterprises on WhatsApp.',
        'alt': 'Illustration of the Mumbai skyline with a cable-stayed sea link at dusk',
        'lead': 'Looking at Mumbai from our Kalyan base? We help buyers, sellers and investors with flats in the central and eastern suburbs and beyond, with clear numbers on every cost.',
        'card': 'Central and eastern suburbs, Western suburbs, island city and the harbour belt.',
        'intro': [
            "Mumbai is India's most expensive and most liquid property market. Prices differ enormously from one station to the next, and extra costs such as stamp duty, GST on under-construction homes, society charges and parking all change the real budget.",
            'Many of our clients live in Kalyan–Dombivli and buy or rent closer to work in Mumbai. We build the full cost picture before you visit a single flat.',
        ],
        'facts': [
            ('Rail', 'Central, Western and Harbour suburban lines'),
            ('Roads', 'Eastern and Western Express Highways, the Coastal Road and Atal Setu to Navi Mumbai'),
            ('Metro', 'A growing network, with more lines under construction'),
            ('Stamp duty', 'At the time of writing, 6% for men and 5% for women buying residential property in their sole name in Mumbai (including 1% metro cess). Confirm before you buy.'),
        ],
        'hoods': [
            ('Central and eastern suburbs', 'Mulund, Ghatkopar, Kurla and Powai: strong rail links and many redevelopment projects.'),
            ('Western suburbs', 'Andheri, Goregaon, Kandivali and Borivali: established, in demand and higher priced.'),
            ('Island city', 'Dadar, Parel, Worli and South Mumbai: premium, space-constrained and heavily redevelopment-driven.'),
            ('Harbour belt', 'Chembur, Wadala and Sion: central location and good connectivity.'),
        ],
        'why': [
            ('Jobs', 'The widest employment base in India.'),
            ('Liquidity', 'Resale and rental demand are consistently high.'),
            ('Redevelopment', 'Old buildings are being replaced with larger modern homes.'),
        ],
        'faq': [
            ('Can you help me buy a flat in Mumbai if I live in Kalyan?', 'Yes. We handle shortlisting and site visits with you, check the RERA and society documents, and walk through every cost before you pay a token amount.'),
            ('What extra costs should I expect in Mumbai?', 'Stamp duty and registration, GST if the home is under construction, society transfer charges for resale, brokerage and parking. We give you a one-page total before you decide.'),
        ],
    },
    'navi-mumbai': {
        'name': 'Navi Mumbai',
        'desc': 'Property in Navi Mumbai: flats in Kharghar, Ulwe, Vashi, Nerul and Airoli. Buy, sell or rent with Prestige Enterprises. Message us on WhatsApp.',
        'alt': 'Illustration of Navi Mumbai towers beside the creek and an arched bridge at night',
        'lead': 'Navi Mumbai is a planned city with wide roads and good open space. We help you compare nodes from Airoli to Ulwe and check each project carefully.',
        'card': 'Kharghar, Ulwe, Vashi, Nerul and Airoli.',
        'intro': [
            'Navi Mumbai was planned by CIDCO, which shows in its wide roads and organised nodes. It has a harbour rail line, a trans-harbour line, a metro line and Atal Setu close by, and the Navi Mumbai International Airport at Ulwe is changing the outlook for the south.',
            'Each node behaves like its own market, so the best choice depends on where you work, your budget and whether you prefer ready or under-construction homes.',
        ],
        'facts': [
            ('District', 'Thane and Raigad'),
            ('Rail', 'Harbour line and Trans-Harbour line; Navi Mumbai Metro Line 1 (Belapur–Pendhar)'),
            ('Roads', 'Palm Beach Road, Sion–Panvel Highway and Atal Setu'),
            ('Airport', 'Navi Mumbai International Airport, Ulwe'),
        ],
        'hoods': [
            ('Vashi, Nerul and Belapur', 'The established core, with a mature social infrastructure.'),
            ('Airoli, Ghansoli and Koparkhairane', 'North nodes with quick access to Thane and Mumbai.'),
            ('Kharghar and Kamothe', 'Parks, open space and newer towers.'),
            ('Ulwe and Dronagiri', 'The southern growth belt near the airport and Atal Setu.'),
        ],
        'why': [
            ('Planning', 'Wide roads, organised sectors and open spaces.'),
            ('Connectivity', 'Rail, metro, highways and a bridge to Mumbai.'),
            ('Growth', 'Airport and port-linked infrastructure in the south.'),
        ],
        'faq': [
            ('Which Navi Mumbai node is best for a first home?', 'It depends on your workplace and budget. Kharghar and Kamothe offer more space for the money; Vashi and Nerul have mature facilities. We shortlist based on your commute.'),
            ('Is Ulwe a safe bet?', 'It has strong infrastructure momentum, but project quality varies widely. We check RERA records and delivery history for every project before recommending one.'),
        ],
    },
    'panvel': {
        'name': 'Panvel',
        'desc': 'Property in Panvel: flats, plots and rentals in New Panvel, Kalamboli, Khanda Colony and Kamothe. Talk to Prestige Enterprises on WhatsApp.',
        'alt': 'Illustration of Panvel with a creek, rail viaduct, hills and towers at dusk',
        'lead': 'Panvel is the gateway to Raigad and the Mumbai–Pune and Konkan routes, with the airport nearby. We help buyers and investors compare the nodes around it.',
        'card': 'New Panvel, Old Panvel, Kalamboli and Khanda Colony.',
        'intro': [
            'Panvel is a major rail and road junction. It sits near the start of the Mumbai–Pune Expressway, the Sion–Panvel Highway, the Konkan route and the Navi Mumbai airport, and it is close to the JNPT port.',
            'Growth has brought many new projects, plus plot and land offers around the city. Land and plot purchases here need especially careful title and land-use checks, which we organise with your lawyer.',
        ],
        'facts': [
            ('District', 'Raigad'),
            ('Rail', 'Panvel Junction links the Harbour line, the Konkan Railway and routes towards Pune and Vasai'),
            ('Roads', 'Mumbai–Pune Expressway, Sion–Panvel Highway, NH 48'),
            ('Nearby', 'Navi Mumbai International Airport, Atal Setu and JNPT port'),
        ],
        'hoods': [
            ('New Panvel', 'Planned and organised, with good road layout and many newer societies.'),
            ('Old Panvel', 'The traditional market town, with older homes and high footfall.'),
            ('Kalamboli and Khanda Colony', 'Close to the highway and expressway start, with a broad range of projects.'),
            ('Kamothe and Taloja', 'Growing residential and industrial belt on the Harbour line and metro corridor.'),
        ],
        'why': [
            ('Junction', 'Major rail and road links in every direction.'),
            ('Infrastructure', 'Airport, port and Atal Setu proximity.'),
            ('Choice', 'From flats to plots across a range of budgets.'),
        ],
        'faq': [
            ('Are plots in Panvel a safe investment?', 'Only with proper checks. We verify the 7/12 extract, land-use zone and approvals, and bring in your lawyer before any token payment. We do not promise appreciation.'),
            ('How far is Panvel from Kalyan?', 'Both are on different rail lines, so most people go by road or via Thane or Diva. Test the actual journey at the time you would travel before you decide.'),
        ],
    },
}
