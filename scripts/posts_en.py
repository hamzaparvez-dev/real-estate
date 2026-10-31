"""Blog guides, English (source of truth). posts_hi.py / posts_mr.py mirror this exactly.

Each post: cat, read (minutes), title, desc, answer (answer-first summary),
sections = [(heading, [paragraphs], [bullets])], faq = [(q, a)].

Rates and rules were checked in Oct 2026 and are described "at the time of writing".
Re-check stamp duty, GST and tax rules before each yearly refresh: they change.
"""

ORDER = [
    'how-to-buy-a-flat-in-kalyan-dombivli',
    'stamp-duty-registration-charges-maharashtra',
    'check-rera-registration-before-you-buy',
    'home-loan-eligibility-emi-guide',
    'under-construction-vs-ready-to-move',
    'documents-to-check-before-buying-property',
    'buying-a-resale-flat-checklist',
    'ready-reckoner-rate-explained',
    'rent-or-buy-in-mumbai-metropolitan-region',
    'capital-gains-tax-on-property-sale',
    'property-investment-kalyan-corridor',
    'nri-buying-property-in-maharashtra',
]
FEATURED = ORDER[:3]

POSTS = {
    'how-to-buy-a-flat-in-kalyan-dombivli': {
        'cat': 'buying', 'read': 6,
        'title': 'How to Buy a Flat in Kalyan–Dombivli: A Step-by-Step Guide',
        'desc': 'The full process of buying a flat in Kalyan or Dombivli: budget, shortlist, RERA check, agreement, loan, registration and possession.',
        'answer': 'Set a total budget that includes stamp duty and other costs, shortlist three or four projects, verify RERA and title, sign and register the agreement, then arrange the loan and take possession with an occupancy certificate.',
        'sections': [
            ('1. Fix your real budget', [
                'The price on the brochure is not what you will pay. Add stamp duty and registration, GST on under-construction homes, parking, society charges and moving costs. Many buyers find the true figure is 8% to 12% above the quoted price.',
            ], []),
            ('2. Shortlist by commute, not just price', [
                'In Kalyan–Dombivli the walk or ride to the station often matters more than the number of floors. Visit at peak hours and during rain before you fall for a project.',
            ], ['Time the trip to your workplace on a weekday morning', 'Check water supply, waterlogging and parking', 'Look at schools, hospitals and markets nearby']),
            ('3. Verify before you pay a token', [
                'For a new project, confirm the MahaRERA registration, the approved plan and the promoter\'s track record. For a resale flat, check the society\'s documents. Our guides on RERA and on documents explain exactly what to look at.',
            ], []),
            ('4. Agreement, loan and registration', [
                'Sign the agreement for sale only after your lawyer has read it, and register it. Home loan sanction can run in parallel. Stamp duty and the registration fee are paid at this stage.',
            ], []),
            ('5. Possession', [
                'Take possession only after you have the occupancy certificate, a snag list is cleared and the society handover documents are in order.',
            ], []),
        ],
        'faq': [
            ('How long does it take to buy a flat?', 'A ready resale flat can close in four to eight weeks if the paperwork is clean. Under-construction homes take as long as the project timeline.'),
            ('Should I pay the builder in cash?', 'No. Pay by cheque or bank transfer, get receipts, and make sure every payment is reflected in the agreement or statement of account.'),
        ],
    },
    'stamp-duty-registration-charges-maharashtra': {
        'cat': 'costs', 'read': 5,
        'title': 'Stamp Duty and Registration Charges in Maharashtra Explained',
        'desc': 'How stamp duty and the registration fee work in Maharashtra, the women\'s concession, and a worked example so you know the real cost.',
        'answer': 'At the time of writing, stamp duty in Mumbai is 6% for men and 5% for women buying residential property in their sole name, including 1% metro cess. Registration is 1% of the value, capped at ₹30,000 above ₹30 lakh. Rates in other municipal areas can differ, so confirm locally.',
        'sections': [
            ('What you pay', [
                'Two government charges apply when an agreement is registered: stamp duty, which is a percentage of the property value, and a registration fee. Both are paid by the buyer.',
            ], []),
            ('The rates', [
                'In Mumbai the combined stamp duty is 6% for a man and 5% for a woman buying a residential property in her sole name, and this includes a 1% metro cess. In some other municipal corporation areas of the region a local body tax can apply as well, so the total can be higher. Always confirm the rate for your exact location with the sub-registrar or on the state\'s IGR website before you budget.',
                'The registration fee is 1% of the property value, but for properties above ₹30 lakh it is capped at ₹30,000.',
            ], []),
            ('A worked example', [
                'Take an ₹80 lakh flat in Mumbai, with an agreement value equal to the Ready Reckoner value.',
            ], ['Man buying alone: 6% = ₹4,80,000 stamp duty + ₹30,000 registration = ₹5,10,000', 'Woman buying alone: 5% = ₹4,00,000 stamp duty + ₹30,000 registration = ₹4,30,000']),
            ('Ways the bill changes', [
                'The women\'s concession applies to residential property bought in a woman\'s sole name; joint ownership with a man attracts the standard rate. Stamp duty is calculated on the higher of the agreement value and the Ready Reckoner value, so a low agreement price does not lower it.',
            ], []),
        ],
        'faq': [
            ('Can I pay stamp duty online?', 'Yes. Maharashtra supports e-payment and e-stamping through the state\'s registration and stamps department. Keep the receipt for your records and your loan file.'),
            ('Is the women\'s concession available on commercial property?', 'No. It applies to residential property bought in the woman\'s sole name.'),
        ],
    },
    'check-rera-registration-before-you-buy': {
        'cat': 'legal', 'read': 5,
        'title': 'How to Check RERA Registration Before You Buy in Maharashtra',
        'desc': 'What MahaRERA registration means, how to verify a project, and the red flags to watch for before paying a token amount.',
        'answer': 'Look up the project\'s MahaRERA registration number on the official MahaRERA website, confirm that the promoter, plot, approvals and completion date match what you were told, and never pay a token amount for a project that is not registered.',
        'sections': [
            ('What RERA protects', [
                'Under RERA, projects above a threshold size must be registered with MahaRERA before they are advertised or sold. Registered promoters must put a large share of buyers\' money into a separate project account, quote area on a carpet-area basis, and pay interest if possession is delayed.',
            ], []),
            ('How to verify a project', [
                'Ask the seller for the MahaRERA registration number. Search for it on the official MahaRERA website and compare what you see with the brochure.',
            ], ['Promoter name and address', 'Project name, location and land details', 'Registered completion date and any extensions', 'Approved plans, commencement certificate and quarterly updates', 'Pending complaints against the promoter or project']),
            ('Red flags', [
                'Walk away or ask hard questions if there is no registration number, if the name on the agreement differs from the registered promoter, if the possession date in the brochure is earlier than the registered one, or if you are pressured to pay in cash.',
            ], []),
            ('RERA is not a guarantee', [
                'Registration is a minimum check, not a quality certificate. Combine it with a review of the title, approvals and the builder\'s past deliveries.',
            ], []),
        ],
        'faq': [
            ('Does RERA apply to resale flats?', 'RERA mainly governs promoters of registered projects. For resale you rely on society documents and the title, covered in our resale and document checklists.'),
            ('What if the possession date is delayed?', 'In a registered project, the promoter is liable to pay interest for the delay. Keep all payment receipts and the original agreement safe.'),
        ],
    },
    'home-loan-eligibility-emi-guide': {
        'cat': 'finance', 'read': 6,
        'title': 'Home Loan Eligibility and EMI: A Practical Guide for Buyers',
        'desc': 'What banks look at, how much down payment you need, how EMI is calculated, and mistakes to avoid when taking a home loan in India.',
        'answer': 'Lenders look at your income, existing EMIs, credit score and the property itself. RBI limits how much of the value a lender can finance, so you need to arrange a down payment of roughly 10% to 25% depending on loan size, plus the costs on top of the price.',
        'sections': [
            ('What lenders check', [
                'Most banks and housing finance companies look at age, stable income, existing loans, a credit score (750 and above is generally preferred) and the legal and technical status of the property.',
            ], []),
            ('Loan size and down payment', [
                'RBI\'s loan-to-value rules at the time of writing allow up to 90% financing for loans up to ₹30 lakh, up to 80% for loans from ₹30 lakh to ₹75 lakh, and up to 75% above ₹75 lakh. Stamp duty, registration and other costs are usually not financed, so keep cash aside for them.',
            ], []),
            ('How EMI works', [
                'EMI depends on the loan amount, interest rate and tenure. As an illustration only, a ₹50 lakh loan at 8.5% a year over 20 years has an EMI of about ₹43,400. Rates change, so ask each lender for the current rate and the processing fees.',
                'A longer tenure lowers the EMI but increases the total interest you pay. Many borrowers choose a longer tenure and prepay when they can.',
            ], []),
            ('Mistakes to avoid', [
                'Do not stretch the EMI so far that one unexpected expense becomes a crisis. Do not forget insurance, maintenance and moving costs. Compare at least three lenders, and for a floating-rate loan to an individual, lenders cannot charge you a penalty for prepayment.',
            ], []),
        ],
        'faq': [
            ('Can I get a loan for an under-construction flat?', 'Yes. Lenders usually release money in stages as construction progresses, and you pay interest only on the amount released until possession.'),
            ('Do you provide the loan?', 'No. We help you prepare documents and compare lenders, but the loan decision and the terms are the lender\'s.'),
        ],
    },
    'under-construction-vs-ready-to-move': {
        'cat': 'buying', 'read': 5,
        'title': 'Under-Construction vs Ready-to-Move Flats: What to Choose',
        'desc': 'Compare price, GST, risk, possession and flexibility between under-construction and ready-to-move homes in Maharashtra.',
        'answer': 'Ready-to-move flats cost more upfront but carry less risk and, with an occupancy certificate, no GST. Under-construction homes are cheaper and can be paid in stages, but you wait for possession and carry delivery risk, which RERA reduces but does not remove.',
        'sections': [
            ('Price and tax', [
                'At the time of writing, GST on an under-construction home is 5% without input tax credit for non-affordable housing and 1% for affordable housing within the government\'s limits. A completed home with an occupancy certificate attracts no GST. This difference alone can change which option is cheaper.',
            ], []),
            ('Risk and timing', [
                'With a ready home you see exactly what you are buying and can move in quickly. With an under-construction home you depend on the builder meeting the schedule. Check the MahaRERA completion date and the promoter\'s history.',
            ], []),
            ('Cash flow', [
                'Under-construction homes let you pay in stages and may reduce the early EMI burden, but you may pay rent and EMI together for a while. Run the numbers for both scenarios before choosing.',
            ], ['Ready: higher upfront cost, immediate use, no GST on a completed home with OC', 'Under construction: lower entry price, stage payments, wait for possession']),
            ('Our rule of thumb', [
                'If you need the home soon or dislike uncertainty, go ready-to-move. If you can wait and the builder has a strong delivery record, an under-construction project can be better value.',
            ], []),
        ],
        'faq': [
            ('What is an occupancy certificate (OC)?', 'It is issued by the local authority to confirm a building has been completed as per approved plans and is fit to occupy. Do not take possession without it.'),
            ('Can I switch from under-construction to ready later?', 'Not easily. Decide based on your timeline, budget and risk comfort before paying the token amount.'),
        ],
    },
    'documents-to-check-before-buying-property': {
        'cat': 'legal', 'read': 6,
        'title': 'Documents to Check Before Buying Property in Maharashtra',
        'desc': 'A practical checklist of title, approval and society documents to review before you pay a token amount for a flat, plot or shop.',
        'answer': 'Check the chain of title, the approved plan and commencement or occupancy certificate, RERA registration for new projects, the 7/12 extract or property card for land, and society or builder NOCs. Have your lawyer review everything before you pay.',
        'sections': [
            ('Ownership', [
                'Ask for the chain of ownership documents, the previous agreements and the registration extracts (Index II) that show past transactions. The seller\'s name must match the owner on record.',
            ], []),
            ('Approvals', [
                'For flats: approved plan, commencement certificate, occupancy certificate for completed buildings and the MahaRERA registration for new projects. For land: the 7/12 extract (or property card in city areas), land-use zone and any non-agricultural order.',
            ], []),
            ('Dues and encumbrances', [
                'Ask for property tax receipts, electricity and water bills, society maintenance statements and a clear confirmation that the property is free of loans or disputes.',
            ], ['Share certificate and society NOC for resale', 'Agreement for sale, registered', 'Receipts for all payments made', 'Bank NOC if the property is mortgaged']),
            ('Get a lawyer involved', [
                'We coordinate the checklist and the visits, but a property lawyer should give the title opinion. It is a small cost compared with the price of the home.',
            ], []),
        ],
        'faq': [
            ('What is a 7/12 extract?', 'It is the Maharashtra land record that shows the owner, land-use and encumbrances on a parcel of land. It is essential when you buy a plot or farmland.'),
            ('Is a notarised agreement enough?', 'No. A property transfer should be on a registered agreement with proper stamp duty paid.'),
        ],
    },
    'buying-a-resale-flat-checklist': {
        'cat': 'buying', 'read': 5,
        'title': 'Buying a Resale Flat in Maharashtra: The Complete Checklist',
        'desc': 'The extra checks resale buyers need: society NOC, share certificate, dues, redevelopment prospects and transfer charges.',
        'answer': 'For a resale flat, confirm clear title, a society NOC, the share certificate, no outstanding dues, the state of the building and any redevelopment plan, and ask the society about transfer charges before you commit.',
        'sections': [
            ('Seller and society', [
                'The seller must have a share certificate and the society must give a no-objection certificate for the transfer. Ask for a no-dues statement from the society and recent maintenance receipts.',
            ], []),
            ('Building condition and redevelopment', [
                'Ask for the structural audit if the building is old, and ask whether the society has discussed redevelopment. Redevelopment can add value, but it can also mean years of waiting or disputes.',
            ], []),
            ('Costs on top of the price', [
                'Beyond stamp duty and registration, budget for society transfer charges, brokerage, legal fees and any repairs. Ask the society for the exact transfer fee in writing.',
            ], []),
            ('Before you pay a token', [
                'Agree the price, the date and the conditions in writing, including what is included in the sale. Keep the token amount reasonable and refundable if the seller cannot deliver clear documents.',
            ], []),
        ],
        'faq': [
            ('Can a bank finance a resale flat?', 'Yes, subject to the lender\'s valuation and legal check of the property and your eligibility.'),
            ('Who pays brokerage in a resale?', 'It is agreed between the parties. Settle it in writing before the deal.'),
        ],
    },
    'ready-reckoner-rate-explained': {
        'cat': 'costs', 'read': 4,
        'title': 'What Is the Ready Reckoner Rate and Why Does It Matter?',
        'desc': 'The Ready Reckoner (RR) rate sets a minimum value for stamp duty in Maharashtra. Here is how it works and how to check it.',
        'answer': 'The Ready Reckoner rate is the government\'s minimum per-square-foot value for a locality. Stamp duty is charged on the higher of the agreement value and the Ready Reckoner value, so you cannot reduce stamp duty by showing a lower price.',
        'sections': [
            ('What it is', [
                'The Ready Reckoner rate, also called the circle rate or RR rate, is published by the state\'s registration department for each zone, and revised from time to time. It differs for land, residential, commercial and industrial property.',
            ], []),
            ('How it affects you', [
                'When you register a sale, stamp duty is calculated on the higher of the actual price and the RR value. If you pay less than the RR value, you still pay duty on the RR value.',
            ], []),
            ('How to check', [
                'Use the state\'s IGR portal to look up the RR rate for the exact locality, property type and floor. Ask us if you want us to calculate it with you.',
            ], []),
            ('Why it matters when you negotiate', [
                'If a price is well below the RR value, find out why. Sometimes there is a problem with the title or the condition of the property.',
            ], []),
        ],
        'faq': [
            ('Does the RR rate change every year?', 'It is revised periodically by the state. Check the current rate before you budget.'),
            ('Does the RR rate decide the market price?', 'No. It sets a minimum for duty. The market price depends on demand, condition and location.'),
        ],
    },
    'rent-or-buy-in-mumbai-metropolitan-region': {
        'cat': 'finance', 'read': 5,
        'title': 'Rent or Buy in the Mumbai Metropolitan Region?',
        'desc': 'A simple framework to decide between renting and buying in Mumbai, Thane, Kalyan and Navi Mumbai, with a worked example.',
        'answer': 'Buy if you plan to stay at least five to seven years, can manage the EMI comfortably and have the down payment ready. Rent if you are likely to move, or if the rent is much lower than the EMI and you can invest the difference with discipline.',
        'sections': [
            ('Look at the rental yield', [
                'In much of MMR, the annual rent is only a small percentage of the flat\'s price. For example, a ₹60 lakh flat that rents for ₹15,000 a month earns ₹1.8 lakh a year, which is a gross yield of 3%. That is lower than many loan rates, so owning costs more than renting each month.',
            ], []),
            ('Why people still buy', [
                'Ownership gives stability, an asset that can appreciate, and protection from rent increases. For many families the emotional value is the deciding factor, and that is fair.',
            ], []),
            ('Questions to ask', [
                'Be honest with the answers.',
            ], ['How long will I stay in this city?', 'Can I pay the EMI if my income drops for six months?', 'Will I really invest the difference if I rent?', 'Is my down payment tied up elsewhere?']),
            ('Our suggestion', [
                'If you are close, rent for a year while you build the down payment and an emergency fund, and use that year to shortlist locations. We help with both rentals and purchases.',
            ], []),
        ],
        'faq': [
            ('Is renting wasteful?', 'Not necessarily. Rent buys flexibility. The wasteful option is buying a home you cannot comfortably afford.'),
            ('What is a Leave and License agreement?', 'It is the standard rental agreement in Maharashtra, usually for 11 months, and it must be registered.'),
        ],
    },
    'capital-gains-tax-on-property-sale': {
        'cat': 'tax', 'read': 6,
        'title': 'Capital Gains Tax When You Sell Property in India',
        'desc': 'How long-term capital gains tax on property works after the 2024 changes, how to reduce it, and what changes under the new Income-tax Act.',
        'answer': 'Property held for more than 24 months is taxed on long-term gains at 12.5% without indexation. For property bought before 23 July 2024, resident individuals and HUFs can choose the lower of 12.5% without indexation or 20% with indexation. Reinvestment exemptions can reduce the tax.',
        'sections': [
            ('Short term vs long term', [
                'If you sell a house or plot within 24 months of buying, the gain is short term and taxed at your slab rate. After 24 months it is long term.',
            ], []),
            ('The rate', [
                'At the time of writing, long-term gains on property are taxed at 12.5% without indexation. For property acquired before 23 July 2024, resident individuals and HUFs can compare this with 20% on an indexed basis and pay the lower amount.',
            ], []),
            ('Ways to reduce it', [
                'You can reduce or defer the tax by reinvesting in another residential house within the prescribed period, or by investing in specified bonds within six months, up to ₹50 lakh. The conditions are strict, so plan before you sell.',
            ], []),
            ('Other points', [
                'The buyer deducts 1% TDS on a sale of ₹50 lakh or more. The Income-tax Act, 2025 applies from 1 April 2026 and renumbers sections, so use your accountant for the correct provisions. This is general information, not tax advice.',
            ], []),
        ],
        'faq': [
            ('Is inherited property taxed differently?', 'The holding period and cost of the previous owner are generally taken into account. Speak to a chartered accountant for your case.'),
            ('Should I plan the sale before the financial year ends?', 'Timing can matter for exemptions and filing. Discuss it with your accountant before signing.'),
        ],
    },
    'property-investment-kalyan-corridor': {
        'cat': 'investing', 'read': 5,
        'title': 'Investing in the Kalyan Corridor: Opportunities and Risks',
        'desc': 'What is driving interest in Kalyan, Dombivli and Ulhasnagar, and how to invest without relying on promises.',
        'answer': 'Buyers are watching the Kalyan corridor because of its rail links, lower prices than Thane and Mumbai, and metro and road projects. The risks are project delays, oversupply in some pockets and uneven quality, so choose RERA-registered projects with a strong delivery record.',
        'sections': [
            ('What is attracting buyers', [
                'Kalyan is a major rail junction with comparatively lower prices than Thane or Mumbai. Metro Line 5 (Thane–Bhiwandi–Kalyan) is under construction and further extensions are planned or proposed, which keeps the corridor in the news.',
            ], []),
            ('The risks', [
                'Metro and road timelines have slipped before and may again. Some pockets have many launches at once, which can slow price growth and make exits harder.',
            ], ['Delivery delays', 'Oversupply in specific micro-markets', 'Lower liquidity than Mumbai or Thane', 'Rent that may not cover the EMI']),
            ('How to invest sensibly', [
                'Prefer registered projects near existing stations and markets, compare real rents and resale prices, and keep a reserve for vacant months. Treat any infrastructure promise as a possibility, not a guarantee.',
            ], []),
            ('Our approach', [
                'We do not promise returns. We share rents, resale evidence and project records so you can decide with facts.',
            ], []),
        ],
        'faq': [
            ('Should I buy now or wait for the metro?', 'Nobody can time it. If you plan to hold for many years and the project passes the checks, the start date matters less than the entry price and quality.'),
            ('What is a realistic rental yield here?', 'It varies by lane and building. We compare actual current rents with price before you decide.'),
        ],
    },
    'nri-buying-property-in-maharashtra': {
        'cat': 'finance', 'read': 5,
        'title': 'NRIs Buying Property in Maharashtra: Rules and Steps',
        'desc': 'What NRIs and OCI cardholders can buy, how to pay, and what to know about repatriation and taxes when buying in Mumbai or Kalyan.',
        'answer': 'NRIs and OCI cardholders can buy residential and commercial property in India without special RBI permission, but not agricultural land, plantation property or a farmhouse. Payment must go through proper banking channels, and rules on repatriation and tax apply.',
        'sections': [
            ('What you can buy', [
                'Residential and commercial property is open to NRIs and OCI cardholders. Agricultural land, plantation property and farmhouses are not, unless specifically permitted.',
            ], []),
            ('How to pay', [
                'Pay through inward remittance or from an NRE, NRO or FCNR account. Cash is not allowed. Keep bank proof of every payment.',
            ], []),
            ('Repatriation and tax', [
                'Sale proceeds can be repatriated within RBI limits and conditions, and tax is deducted on the sale of property by NRIs, often at a higher rate. Get your bank and an accountant to confirm the current position before you buy or sell.',
            ], []),
            ('Doing it from abroad', [
                'You can give a power of attorney to a trusted person to sign documents, but it must be drafted and attested correctly. We help NRI clients with virtual visits, verification and coordination with lawyers and banks.',
            ], []),
        ],
        'faq': [
            ('Can NRIs take a home loan in India?', 'Yes. Indian lenders offer loans to NRIs, with documentation and eligibility rules that differ from resident loans.'),
            ('Can an NRI rent out the property?', 'Yes. Rental income is taxable in India, and it can generally be credited to an NRO account.'),
        ],
    },
}
