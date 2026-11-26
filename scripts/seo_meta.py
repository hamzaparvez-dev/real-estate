"""Search-result titles and meta descriptions (head tags only).

These override ONLY <title>, meta description, og:/twitter: title+description and the
WebPage JSON-LD name/description. Visible on-page copy (H1s, card text, body) is untouched.
Keys: 'home', 'areas', 'blog', 'city:<slug>', 'post:<slug>', 'project:<slug>'.
Targets come from the Google Search Console export (last 28 days, Nov 2026).
"""

META = {
    'en': {
        # GSC: 'prestige enterprises' pos 2.7, 'prestige enterprise' 3.3, 'prestige builders' 6, homepage pos 5.0
        'home': ('Prestige Enterprises | Prestige Projects, Kalyan West Flats',
                 '1 to 5 BHK flats in Kalyan West: Prestige Gold 1, 2 & 3 BHK from ₹55 Lakh near Kala Talao and Prestige One 3 & 5 BHK Jodi at Godrej Hill, Khadakpada.'),
        'blog': ('Kalyan Property Guides: RERA, RR Rate, Stamp Duty | Prestige',
                 'Guides for buying a flat in Kalyan West: MahaRERA checks, ready reckoner rate, stamp duty, capital gains tax, 1 to 5 BHK options and local areas.'),
        'city:kalyan': ('Flats & Property in Kalyan West, Maharashtra | Prestige',
                        'Flats in Kalyan West: Khadakpada, Godrej Hill and Kala Talao. Prestige Gold 1–3 BHK and Prestige One 3 & 5 BHK Jodi. Talk to Prestige on WhatsApp.'),
        # GSC: 'prestige gold' pos 17.8 (18 impr), 'prestige gold kalyan' pos 7.2, page pos 12.2 with 0 clicks
        'project:prestige-gold': ('Prestige Gold Kalyan West | 1, 2 & 3 BHK from ₹55 Lakh',
                                  'Prestige Gold near Kala Talao, Kalyan West: 1 BHK from ₹55 Lakh, 2 BHK from ₹75 Lakh, 3 BHK and shops/offices. Sample flat ready. MahaRERA P51700052362.'),
        # GSC: 'prestige one' pos 5.8
        'project:prestige-one': ('Prestige One Kalyan West | 3 & 5 BHK Jodi, Godrej Hill',
                                 'Prestige One at Godrej Hill, Khadakpada, Kalyan West: 3 BHK and 5 BHK Jodi homes. Floor plans and prices on request. Book a site visit with Prestige Projects.'),
        # GSC: page pos 14.3 (41 impr, 0 clicks); 'rr rate' pos 24.8, 'ready reckoner' pos 8.6
        'post:ready-reckoner-rate-explained': ('Ready Reckoner (RR) Rate Maharashtra: Meaning & How to Check',
                                               'What the ready reckoner (RR) rate means, how it sets stamp duty in Maharashtra, and how to check the RR rate for a flat in Kalyan on the IGR eASR site.'),
        'post:documents-to-check-before-buying-property': ('Documents to Check Before Buying a Flat in Maharashtra',
                                                           'Checklist of title, MahaRERA, approval, OC and society documents to verify before paying a token for a flat in Kalyan, Thane or Mumbai.'),
        'post:how-to-buy-a-flat-in-kalyan-dombivli': ('How to Buy a Flat in Kalyan West & Dombivli: Step by Step',
                                                      'Buying a flat in Kalyan West or Dombivli: real budget, shortlist, MahaRERA check, agreement, home loan, registration and possession, step by step.'),
        'post:stamp-duty-registration-charges-maharashtra': ('Stamp Duty & Registration Charges in Maharashtra (Kalyan)',
                                                             'Stamp duty and registration fees in Maharashtra explained with a worked example, the women\'s concession and why rates outside Mumbai, like Kalyan, can differ.'),
        'post:check-rera-registration-before-you-buy': ('How to Check MahaRERA Registration of a Project in Maharashtra',
                                                        'Check a MahaRERA registration number before you buy: search the project, read the filing, spot red flags and verify the promoter.'),
        'post:capital-gains-tax-on-property-sale': ('Capital Gains Tax on Property Sale in India: LTCG Explained',
                                                    'Long-term capital gains tax when you sell a flat or house in India: 12.5% vs 20% with indexation, holding period and ways to save tax.'),
    },
    'hi': {
        'home': ('Prestige Enterprises | Prestige Projects, कल्याण वेस्ट फ्लैट',
                 'कल्याण वेस्ट में Prestige Gold (काला तलाव के पास) 1, 2 और 3 BHK ₹55 लाख से, और Prestige One (गोदरेज हिल, खडकपाडा) 3 व 5 BHK जोड़ी। साइट विज़िट बुक करें।'),
        'blog': ('कल्याण प्रॉपर्टी गाइड: RERA, रेडी रेकनर, स्टांप ड्यूटी | Prestige',
                 'कल्याण वेस्ट में फ्लैट खरीदने के लिए गाइड: MahaRERA जाँच, रेडी रेकनर रेट, स्टांप ड्यूटी, कैपिटल गेन टैक्स और 1 से 5 BHK विकल्प।'),
        # GSC: hi ready-reckoner page pos 8.9; 'रेडी रेकनर' queries
        'post:ready-reckoner-rate-explained': ('रेडी रेकनर रेट क्या है? RR रेट कैसे जाँचें (महाराष्ट्र)',
                                               'रेडी रेकनर (RR) रेट का मतलब, स्टांप ड्यूटी पर इसका असर, और कल्याण के फ्लैट का RR रेट IGR eASR पर कैसे देखें।'),
        # GSC: hi CGT page pos 24.3 (29 impr); queries 'संपत्ति बिक्री पर cgt क्या है' 31, 'प्रॉपर्टी बेचने पर एलटीसीजी टैक्स' 67, 'गृह संपत्ति पर दीर्घकालिक पूंजीगत लाभ' 12
        'post:capital-gains-tax-on-property-sale': ('प्रॉपर्टी बेचने पर कैपिटल गेन टैक्स (LTCG): पूरी जानकारी',
                                                    'संपत्ति बिक्री पर CGT क्या है? मकान या फ्लैट बेचने पर दीर्घकालिक पूंजीगत लाभ (LTCG) टैक्स, 12.5% बनाम 20% इंडेक्सेशन, और टैक्स बचाने के तरीके।'),
        'post:stamp-duty-registration-charges-maharashtra': ('महाराष्ट्र में स्टांप ड्यूटी और रजिस्ट्रेशन चार्ज (कल्याण)',
                                                             'महाराष्ट्र और कल्याण में फ्लैट पर स्टांप ड्यूटी व रजिस्ट्रेशन फ़ीस, महिलाओं के लिए रियायत, और असली खर्च का उदाहरण।'),
        'post:documents-to-check-before-buying-property': ('फ्लैट खरीदने से पहले जाँचने वाले दस्तावेज़ (महाराष्ट्र)',
                                                           'टोकन देने से पहले टाइटल, MahaRERA, मंज़ूरी, OC और सोसाइटी दस्तावेज़ों की चेकलिस्ट: कल्याण, ठाणे और मुंबई के खरीदारों के लिए।'),
    },
    'mr': {
        'home': ('Prestige Enterprises | Prestige Projects, कल्याण पश्चिम फ्लॅट',
                 'कल्याण पश्चिममध्ये Prestige Gold (काळा तलावाजवळ) 1, 2 व 3 BHK ₹55 लाखांपासून आणि Prestige One (गोदरेज हिल, खडकपाडा) 3 व 5 BHK जोडी. साइट भेट बुक करा.'),
        'blog': ('कल्याण मालमत्ता मार्गदर्शक: RERA, रेडी रेकनर, मुद्रांक शुल्क | Prestige',
                 'कल्याण पश्चिममध्ये फ्लॅट खरेदीसाठी मार्गदर्शक: MahaRERA तपासणी, रेडी रेकनर दर, मुद्रांक शुल्क, भांडवली नफा कर आणि 1 ते 5 BHK पर्याय.'),
        # GSC: mr stamp duty page pos 6.4 (the only blog click), mr RR pos 6.1, mr resale checklist pos 6.9
        'post:stamp-duty-registration-charges-maharashtra': ('महाराष्ट्रातील मुद्रांक शुल्क व नोंदणी शुल्क 2026 (कल्याण)',
                                                             'महाराष्ट्र आणि कल्याणमध्ये फ्लॅट खरेदीवर मुद्रांक शुल्क व नोंदणी फी किती? महिलांसाठी सवलत आणि खऱ्या खर्चाचे उदाहरण.'),
        'post:ready-reckoner-rate-explained': ('रेडी रेकनर दर म्हणजे काय? RR दर कसा तपासायचा',
                                               'रेडी रेकनर (RR) दर म्हणजे काय, मुद्रांक शुल्कावर त्याचा परिणाम आणि कल्याणमधील फ्लॅटचा RR दर IGR eASR वर कसा पाहायचा.'),
        'post:buying-a-resale-flat-checklist': ('रिसेल फ्लॅट खरेदी चेकलिस्ट: महाराष्ट्र व कल्याण',
                                                'रिसेल फ्लॅट घेताना सोसायटी NOC, शेअर सर्टिफिकेट, थकबाकी, हस्तांतरण शुल्क आणि पुनर्विकास तपासा: कल्याण, ठाणे खरेदीदारांसाठी.'),
    },
}


def get(l, key, title, desc):
    """Return (title, desc) override for this page, or the defaults."""
    return META.get(l, {}).get(key, (title, desc))
