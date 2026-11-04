/* Prestige Enterprises: small, dependency-free behaviour for every page. */
(function () {
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* Remember the language a visitor picks. Only the English home page ever redirects, and only
     if the visitor chose another language earlier, so crawlers and shared links are unaffected. */
  try {
    $$('.lang a').forEach(function (a) {
      a.addEventListener('click', function () { localStorage.setItem('pe_lang', a.getAttribute('hreflang')); });
    });
    var pref = localStorage.getItem('pe_lang');
    if (pref && pref !== 'en' && location.pathname === '/' && !location.search && !location.hash) {
      var alt = $('link[rel="alternate"][hreflang="' + pref + '"]');
      if (alt) location.replace(alt.href);
    }
  } catch (e) {}

  /* Nav background and progress bar */
  var nav = $('#nav'), prog = $('#prog');
  function onScroll() {
    var y = window.pageYOffset || document.documentElement.scrollTop;
    if (nav) nav.classList.toggle('up', y > 40);
    if (prog) {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      prog.style.width = (h > 0 ? Math.min(100, (y / h) * 100) : 0) + '%';
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* Projects dropdown */
  var projects = $('#navProjects');
  if (projects) {
    var projectsBtn = $('.nav-dd-btn', projects);
    var setProjects = function (o) { projects.classList.toggle('open', o); projectsBtn.setAttribute('aria-expanded', o ? 'true' : 'false'); };
    projectsBtn.addEventListener('click', function (e) { e.stopPropagation(); setProjects(!projects.classList.contains('open')); });
    document.addEventListener('click', function (e) { if (!projects.contains(e.target)) setProjects(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setProjects(false); });
  }

  /* Areas dropdown */
  var dd = $('#navAreas');
  if (dd) {
    var btn = $('.nav-dd-btn', dd);
    var setDd = function (o) { dd.classList.toggle('open', o); btn.setAttribute('aria-expanded', o ? 'true' : 'false'); };
    btn.addEventListener('click', function (e) { e.stopPropagation(); setDd(!dd.classList.contains('open')); });
    document.addEventListener('click', function (e) { if (!dd.contains(e.target)) setDd(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setDd(false); });
  }

  /* Apply the same premium drawer to all legacy interior-page menus. */
  function upgradeMobileMenu(panel) {
    if (!panel || panel.querySelector('.mnav-content')) return;
    var lang = (document.documentElement.lang || 'en').slice(0,2).toLowerCase();
    var t = {
      en:{home:'Home',about:'About',projects:'Projects',plans:'Plans',gold:'Prestige Gold',pricing:'Pricing',services:'Services',guides:'Guides',contact:'Contact',areas:'Areas',kalyan:'Kalyan',whatsapp:'Chat on WhatsApp'},
      hi:{home:'होम',about:'हमारे बारे में',projects:'प्रोजेक्ट्स',plans:'प्लान्स',gold:'प्रेस्टीज गोल्ड',pricing:'कीमत',services:'सेवाएँ',guides:'गाइड',contact:'संपर्क',areas:'क्षेत्र',kalyan:'कल्याण',whatsapp:'व्हाट्सऐप पर चैट करें'},
      mr:{home:'मुख्यपृष्ठ',about:'आमच्याबद्दल',projects:'प्रकल्प',plans:'योजना',gold:'प्रेस्टीज गोल्ड',pricing:'किंमत',services:'सेवा',guides:'मार्गदर्शक',contact:'संपर्क',areas:'परिसर',kalyan:'कल्याण',whatsapp:'व्हॉट्सअ‍ॅपवर चॅट करा'}
    }[lang] || null;
    if (!t) return;
    var oldWhatsApp = panel.querySelector('a[href*="wa.me"]');
    var waHref = oldWhatsApp ? oldWhatsApp.getAttribute('href') :
      'https://wa.me/919689557788?text=Hello%20Prestige%20Enterprises%2C%20I%20would%20like%20more%20information%20about%20properties%20for%20sale%20in%20Kalyan.';
    var prefix = lang === 'en' ? '' : '/' + lang;
    var paths = {
      home:prefix+'/#home',about:prefix+'/#about',pricing:prefix+'/#pricing',
      services:prefix+'/#services',guides:prefix+'/blog/',contact:prefix+'/#contact',
      kalyan:prefix+'/areas/kalyan/'
    };
    var glyphs = {
      home:'<path d="M3 11 12 3l9 8"/><path d="M5 10v10h5v-6h4v6h5V10"/>',
      about:'<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7z"/>',
      project:'<path d="M4 21V9l6-3v15"/><path d="M10 21V4l8 3v14"/><path d="M2 21h20M13 10h2M13 14h2M7 12h0M7 16h0"/>',
      pricing:'<path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.5" cy="8.5" r="1.2"/>',
      services:'<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 12.5l9 5 9-5"/><path d="M3 17l9 5 9-5"/>',
      guides:'<path d="M12 6c-2-1.5-5-2-9-2v14c4 0 7 .5 9 2 2-1.5 5-2 9-2V4c-4 0-7 .5-9 2z"/><path d="M12 6v14"/>',
      contact:'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 7 9-7"/>',
      location:'<path d="M12 22s7-6.5 7-12a7 7 0 1 0-14 0c0 5.5 7 12 7 12z"/><circle cx="12" cy="10" r="2.6"/>',
      whatsapp:'<path d="M3 21l1.6-4.8A9 9 0 1 1 12 21a9 9 0 0 1-4.3-1.1z"/><path d="M9 8.5c0 3.5 3 6.5 6.5 6.5l1-1.8-2-1-1 .8c-1-.4-2-1.4-2.4-2.4l.8-1-1-2z"/>',
      chevron:'<path d="M9 5l7 7-7 7"/>'
    };
    function icon(name, cls) {
      return '<svg class="'+(cls||'')+'" viewBox="0 0 24 24" aria-hidden="true">'+glyphs[name]+'</svg>';
    }
    function item(name, href, iconName, extra) {
      return '<a class="mnav-item mnav-full-item '+(extra||'')+'" href="'+href+'">'+icon(iconName)+
        '<span class="mnav-label">'+t[name]+'</span>'+icon('chevron','mnav-chevron')+'</a>';
    }
    panel.innerHTML =
      '<div class="mnav-content">'+
        '<div class="mnav-top">'+
          '<a class="mnav-item mnav-item-top mnav-item-active" href="'+paths.home+'">'+icon('home')+'<span class="mnav-label">'+t.home+'</span></a>'+
          '<a class="mnav-item mnav-item-top" href="'+paths.about+'">'+icon('about')+'<span class="mnav-label">'+t.about+'</span></a>'+
        '</div>'+
        '<div class="mnav-section">'+t.projects+'</div>'+
        '<div class="mnav-group open" id="mnav-plans">'+
          '<button class="mnav-item mnav-plan-button" type="button" id="mnav-plans-button" aria-expanded="true">'+icon('project')+
            '<span class="mnav-label">'+t.plans+'</span>'+icon('chevron','mnav-chevron')+
          '</button>'+
          '<div class="mnav-plan-sub"><div>'+
            '<a class="mnav-plan-link" href="/projects/prestige-gold/"><span>'+t.gold+'</span>'+icon('chevron')+'</a>'+
          '</div></div>'+
        '</div>'+
        item('pricing',paths.pricing,'pricing','')+
        item('services',paths.services,'services','')+
        item('guides',paths.guides,'guides','')+
        item('contact',paths.contact,'contact','')+
        '<div class="mnav-section">'+t.areas+'</div>'+
        item('kalyan',paths.kalyan,'location','mnav-area-item')+
      '</div>'+
      '<div class="mnav-footer">'+
        '<a class="mnav-whatsapp" href="'+waHref+'" target="_blank" rel="noopener">'+icon('whatsapp')+
          '<span>'+t.whatsapp+'</span>'+icon('chevron','mnav-chevron')+
        '</a>'+
      '</div>';
    var group = panel.querySelector('#mnav-plans');
    var toggle = panel.querySelector('#mnav-plans-button');
    if (group && toggle) {
      toggle.addEventListener('click',function(){
        var open = group.classList.toggle('open');
        toggle.setAttribute('aria-expanded',open ? 'true' : 'false');
      });
    }
  }

  /* Mobile menu: accessible focus and keyboard behavior */
  var ham = $('#navHam'), menu = $('#mnav');
  if (menu) upgradeMobileMenu(menu);
  if (ham && menu) {
    var setMenu = function (open) {
      menu.hidden = !open;
      menu.setAttribute('aria-hidden', open ? 'false' : 'true');
      ham.classList.toggle('open', open);
      ham.setAttribute('aria-expanded', open ? 'true' : 'false');
      ham.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      nav.classList.toggle('menu-open', open);
      document.body.style.overflow = open ? 'hidden' : '';
      document.body.classList.toggle('mobile-menu-open', open);
      if (open) {
        menu.scrollTop = 0;
        var first = $('a[href]', menu);
        if (first) first.focus({preventScroll:true});
      } else ham.focus({preventScroll:true});
    };
    ham.addEventListener('click', function () { setMenu(menu.hidden); });
    menu.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    document.addEventListener('keydown', function (e) {
      if (menu.hidden) return;
      if (e.key === 'Escape') { e.preventDefault(); setMenu(false); return; }
      if (e.key === 'Tab') {
        var items = $$('a[href],button:not([disabled])', menu);
        if (!items.length) return;
        if (e.shiftKey && document.activeElement === items[0]) { e.preventDefault(); items[items.length-1].focus(); }
        else if (!e.shiftKey && document.activeElement === items[items.length-1]) { e.preventDefault(); items[0].focus(); }
      }
    });
    var mq = window.matchMedia('(min-width:981px)');
    (mq.addEventListener ? mq.addEventListener.bind(mq, 'change') : mq.addListener.bind(mq))(function (q) {
      if (q.matches && !menu.hidden) { menu.hidden=true; menu.setAttribute('aria-hidden','true'); ham.classList.remove('open'); ham.setAttribute('aria-expanded','false'); ham.setAttribute('aria-label','Open menu'); nav.classList.remove('menu-open'); document.body.classList.remove('mobile-menu-open'); document.body.style.overflow=''; }
    });
    menu.setAttribute('aria-hidden', menu.hidden ? 'true' : 'false');
  }

  /* Hero slider + rotating tagline (home only) */
  var slides = $$('.hero-slide'), dots = $$('.hc-dot');
  if (slides.length > 1) {
    var i = 0, reduce = window.matchMedia('(prefers-reduced-motion:reduce)').matches;
    var show = function (n) {
      i = (n + slides.length) % slides.length;
      slides.forEach(function (s, k) { s.classList.toggle('active', k === i); });
      dots.forEach(function (d, k) { d.classList.toggle('on', k === i); });
    };
    dots.forEach(function (d, k) { d.addEventListener('click', function () { show(k); }); });
    if (!reduce) setInterval(function () { show(i + 1); }, 6500);
  }
  var tl = $('.hero-tagline');
  if (tl && tl.children.length > 1 && !window.matchMedia('(prefers-reduced-motion:reduce)').matches) {
    var t = 0, n = tl.children.length;
    setInterval(function () { t = (t + 1) % n; tl.style.transform = 'translateY(' + (-t * 34) + 'px)'; }, 3600);
  }

  /* Plan image lightbox modal */
  var planWraps = $$('.plan-img-wrap');
  if (planWraps.length) {
    var modal = document.createElement('div');
    modal.className = 'lightbox-modal';
    modal.innerHTML = '<div class="lightbox-box"><button class="lightbox-close" type="button" aria-label="Close">&times;</button><img src="" alt="Enlarged Prestige Gold floor plan"><div class="lightbox-title"></div></div>';
    document.body.appendChild(modal);
    var modalImg = $('img', modal);
    var modalTitle = $('.lightbox-title', modal);
    var closeModal = function () { modal.classList.remove('open'); document.body.style.overflow = ''; };
    $('.lightbox-close', modal).addEventListener('click', closeModal);
    modal.addEventListener('click', function (e) { if (e.target === modal) closeModal(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && modal.classList.contains('open')) closeModal(); });
    planWraps.forEach(function (w) {
      if (!w.getAttribute('data-full')) return; // Placeholders without an image stay non-interactive.
      var openPlanImage = function () {
        var src = w.getAttribute('data-full');
        var title = w.getAttribute('data-title') || 'Floor plan';
        modalImg.src = src;
        modalImg.alt = title;
        modalTitle.textContent = title;
        modal.classList.add('open');
        document.body.style.overflow = 'hidden';
      };
      w.setAttribute('role', 'button');
      w.setAttribute('tabindex', '0');
      w.setAttribute('aria-label', 'View ' + (w.getAttribute('data-title') || 'floor plan') + ' in full size');
      w.addEventListener('click', openPlanImage);
      w.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          openPlanImage();
        }
      });
    });
  }
  /* Structured enquiry modal: collect buyer requirements and hand off to WhatsApp. */
  (function () {
    var WA = 'https://wa.me/919689557788';
    var modal = document.createElement('div');
    modal.className = 'enq-modal';
    modal.setAttribute('aria-hidden', 'true');
    modal.innerHTML = `
      <div class="enq-box" role="dialog" aria-modal="true" aria-labelledby="enqTitle" aria-describedby="enqIntro">
        <button class="enq-close" type="button" aria-label="Close enquiry form">&times;</button>
        <div class="enq-eyebrow">EXPERIENCE THE SAMPLE FLAT TODAY</div>
        <h3 id="enqTitle">Book Site Visit. Enquire Now.</h3>
        <p id="enqIntro">Limited units available</p>
        <form class="enq-form" novalidate>
          <div class="enq-fields">
            <label class="enq-field">Full Name <span>*</span><input name="name" autocomplete="name" placeholder="Enter your name" required minlength="2"></label>
            <label class="enq-field">Phone Number <span>*</span><input name="phone" type="tel" inputmode="numeric" autocomplete="tel" placeholder="Enter your phone number" required pattern="[6-9][0-9]{9}" maxlength="10"></label>
            <label class="enq-field">Select Configuration <span>*</span><select name="configuration" required><option value="">Select</option><option>1BHK</option><option>2BHK</option><option>3BHK</option><option>4BHK</option><option>5BHK</option><option>Commercial</option></select></label>
            <label class="enq-field">Purpose <select name="purpose"><option value="">Select</option><option>Self Use / End-Use</option><option>Investment / Rental</option><option>First Home</option><option>Upgrade</option></select></label>
          </div>
          <div class="enq-honeypot" aria-hidden="true"><label>Leave this field empty<input name="website" type="text" tabindex="-1" autocomplete="off"></label></div>
          <p class="enq-error" role="alert" aria-live="polite"></p>
          <button class="enq-submit" type="submit">ENQUIRE NOW</button>
        </form>      </div>`;
    document.body.appendChild(modal);
    var form = modal.querySelector('form');
    var lastFocus = null;
    var enquiryIntent = 'property';
    var close = function () {
      modal.classList.remove('open');
      modal.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
      if (lastFocus && typeof lastFocus.focus === 'function') lastFocus.focus();
    };
    var openModal = function (trigger) {
      lastFocus = trigger || document.activeElement;
      enquiryIntent = trigger && trigger.getAttribute('data-enquiry-intent') === 'site-visit' ? 'site-visit' : 'property';
      modal.querySelector('#enqTitle').textContent = enquiryIntent === 'site-visit' ? 'Book Your Site Visit' : 'Enquire Now';
      modal.classList.add('open');
      modal.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
      var error = form.querySelector('.enq-error');
      error.textContent = '';
      window.setTimeout(function () { var name = form.querySelector('[name="name"]'); if (name) name.focus(); }, 30);
    };
    modal.querySelector('.enq-close').addEventListener('click', close);
    modal.addEventListener('click', function (e) { if (e.target === modal) close(); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && modal.classList.contains('open')) close();
      if (e.key === 'Tab' && modal.classList.contains('open')) {
        var focusable = modal.querySelectorAll('button:not([disabled]),input:not([disabled]),select:not([disabled]),textarea:not([disabled])');
        if (!focusable.length) return;
        var first = focusable[0], last = focusable[focusable.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
    form.querySelector('[name="phone"]').addEventListener('input', function () {
      this.value = this.value.replace(/\D/g, '').slice(0, 10);
    });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var error = form.querySelector('.enq-error');
      error.textContent = '';
      if (!form.reportValidity()) return;
      var data = new FormData(form);
      var phone = String(data.get('phone') || '').replace(/\D/g, '');
      if (!/^[6-9][0-9]{9}$/.test(phone)) {
        error.textContent = 'Please enter a valid 10-digit Indian mobile number.';
        form.querySelector('[name="phone"]').focus();
        return;
      }
      var lines = [
        'Hello Prestige Enterprises, I would like to ' + (enquiryIntent === 'site-visit' ? 'book a site visit.' : 'make a property enquiry.'),
        '',
        'Name: ' + data.get('name'),
        'Mobile: ' + phone,
        'Configuration: ' + data.get('configuration'),
        'Purpose: ' + (data.get('purpose') || 'Not specified')
      ];
      var url = WA + '?text=' + encodeURIComponent(lines.join('\\n'));
      var payload = {
        name: String(data.get('name') || '').trim(),
        phone: phone,
        configuration: String(data.get('configuration') || ''),
        purpose: String(data.get('purpose') || ''),
        intent: enquiryIntent,
        message: '',
        source: location.pathname,
        marketingConsent: false,
        website: String(data.get('website') || '')
      };
      var submitButton = form.querySelector('.enq-submit');
      var originalLabel = submitButton.textContent;
      submitButton.disabled = true;
      submitButton.textContent = 'SAVING ENQUIRY…';
      var waWindow = window.open('about:blank', '_blank');
      if (waWindow) waWindow.opener = null;
      fetch('/api/enquiries', {
        method: 'POST',
        credentials: 'same-origin',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      }).then(function (response) {
        return response.json().catch(function () { return {}; }).then(function (body) {
          if (!response.ok) throw new Error(body.error || 'We could not save your enquiry. Please try again.');
          return body;
        });
      }).then(function () {
        close();
        form.reset();
        if (waWindow) waWindow.location.href = url;
        else window.location.href = url;
      }).catch(function (err) {
        if (waWindow) waWindow.close();
        error.textContent = err.message || 'We could not save your enquiry. Please try again.';
      }).finally(function () {
        submitButton.disabled = false;
        submitButton.textContent = originalLabel;
      });
    });

    var float = document.createElement('div');
    float.className = 'floating-cta';
    float.setAttribute('aria-label', 'Quick contact actions');
    float.innerHTML = '<a class="f-book" href="facetime:919689557788" aria-label="Book a site visit using FaceTime">BOOK VISIT</a><a class="f-wa" href="' + WA + '?text=' + encodeURIComponent('Hello Prestige Enterprises, I would like more information about homes in Kalyan.') + '" target="_blank" rel="noopener" aria-label="WhatsApp"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 11.5a8.4 8.4 0 0 1-12.4 7.4L3 20l1.2-4.3A8.4 8.4 0 1 1 20 11.5Z"/><path d="M8.5 8.2c.3-.6.6-.6.9-.6h.4c.2 0 .4.1.5.4l.7 1.7c.1.2.1.4-.1.6l-.5.6c-.2.2-.2.4 0 .7.6 1 1.4 1.7 2.4 2.2.3.1.5.1.7-.1l.7-.8c.2-.2.4-.3.7-.2l1.6.8c.3.1.4.3.4.5 0 .3-.2 1-.7 1.4-.5.4-1.1.6-1.8.5-1-.1-2.2-.6-3.6-1.8-1.6-1.4-2.6-3.1-2.8-4.1-.2-.9.1-1.5.5-1.8Z"/></svg><span>WHATSAPP</span></a><button class="f-enq" type="button" data-enquiry-intent="property" aria-label="Enquire now">ENQUIRE NOW</button>';
    document.body.appendChild(float);
    float.querySelector('.f-enq').addEventListener('click', function () { openModal(this); });

    /* Normalise legacy unclassed CTA markup so older pages cannot ship browser-default buttons. */
    document.querySelectorAll('a[href*="wa.me"],a[aria-label*="WhatsApp"],a[aria-label*="whatsapp"],button[aria-label*="WhatsApp"]').forEach(function (el) {
      if (!el.classList.contains('btn-wa-sm') && !el.classList.contains('f-wa')) el.classList.add('btn-wa');
    });
    document.querySelectorAll('a,button').forEach(function (el) {
      var label = (el.textContent || el.getAttribute('aria-label') || '').trim().toLowerCase();
      if (label.indexOf('whatsapp') !== -1 && !el.classList.contains('btn-wa-sm') && !el.classList.contains('f-wa')) el.classList.add('btn-wa');
    });
    /* Section-wide duplicate WhatsApp/Enquire CTAs intentionally removed. */
    document.querySelectorAll('.enquire-trigger').forEach(function (el) {
      el.addEventListener('click', function (e) { e.preventDefault(); openModal(this); });
    });
    /* One delegated handler covers legacy and newly-rendered enquiry controls on every page. */
    document.addEventListener('click', function (e) {
      var el = e.target && e.target.closest ? e.target.closest('a,button') : null;
      if (!el || modal.contains(el) || el.classList.contains('f-enq') || el.classList.contains('enquire-trigger')) return;
      var label = (el.textContent || el.getAttribute('aria-label') || '').trim().toLowerCase();
      if (label.indexOf('enquire') === -1 && label.indexOf('enquiry') === -1 && label.indexOf('request details') === -1) return;
      e.preventDefault();
      el.classList.add('btn-enquire');
      var card = el.closest('.plan-card');
      var section = el.closest('section');
      var context = card ? (card.querySelector('h3')?.textContent || 'featured project') : (section && (section.id || section.querySelector('h2')?.textContent) || '');
      var details = form.querySelector('[name="message"]');
      if (context && details && !details.value) details.value = 'I am enquiring about: ' + context;
      openModal(el);
    });
  })();
  /* Topic-specific editorial photography for every guide card and article hero. */
  (function () {
    var blogPhotos = {
      'how-to-buy-a-flat-in-kalyan-dombivli': 'https://images.unsplash.com/photo-1751945965597-71171ec7a458?auto=format&fit=crop&w=1400&q=85',
      'stamp-duty-registration-charges-maharashtra': 'https://images.unsplash.com/photo-1759429255330-51145b170dad?auto=format&fit=crop&w=1400&q=85',
      'check-rera-registration-before-you-buy': 'https://images.unsplash.com/photo-1753774050094-867f85e986fa?auto=format&fit=crop&w=1400&q=85',
      'home-loan-eligibility-emi-guide': 'https://images.unsplash.com/photo-1709880945165-d2208c6ad2ec?auto=format&fit=crop&w=1400&q=85',
      'under-construction-vs-ready-to-move': 'https://images.unsplash.com/photo-1765547682681-428452039cd8?auto=format&fit=crop&w=1400&q=85',
      'documents-to-check-before-buying-property': 'https://images.unsplash.com/photo-1762427907123-c7ab022a5de7?auto=format&fit=crop&w=1400&q=85',
      'buying-a-resale-flat-checklist': 'https://images.unsplash.com/photo-1759428679273-11d914866394?auto=format&fit=crop&w=1400&q=85',
      'ready-reckoner-rate-explained': 'https://images.unsplash.com/photo-1732437598333-27141529981f?auto=format&fit=crop&w=1400&q=85',
      'rent-or-buy-in-mumbai-metropolitan-region': 'https://images.unsplash.com/photo-1724582586529-62622e50c0b3?auto=format&fit=crop&w=1400&q=85',
      'capital-gains-tax-on-property-sale': 'https://images.unsplash.com/photo-1762427907123-c7ab022a5de7?auto=format&fit=crop&w=1400&q=85',
      'property-investment-kalyan-corridor': 'https://images.unsplash.com/photo-1759863468440-85130c0dff28?auto=format&fit=crop&w=1400&q=85',
      'nri-buying-property-in-maharashtra': 'https://images.unsplash.com/photo-1763621605783-307c1743e308?auto=format&fit=crop&w=1400&q=85'
    };
    document.querySelectorAll('img[src*="/img/blog/"]').forEach(function (img) {
      var raw = img.getAttribute('src') || '';
      var file = raw.split('/').pop().split('?')[0];
      var slug = file.replace(/\.(jpe?g|webp|png)$/i, '');
      var photo = blogPhotos[slug];
      if (!photo) return;
      img.dataset.localFallback = raw;
      img.onerror = function () {
        if (this.dataset.localFallback) {
          this.onerror = null;
          this.src = this.dataset.localFallback;
        }
      };
      img.src = photo;
      img.decoding = 'async';
      if (img.closest('.ph')) {
        img.loading = 'eager';
        img.fetchPriority = 'high';
      } else {
        img.loading = 'lazy';
      }
    });
  })();


  /* Smooth wheel/trackpad scrolling in both directions.
     Touch scrolling and reduced-motion preferences retain native browser behaviour. */
  (function () {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    var script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/lenis@1.1.20/dist/lenis.min.js';
    script.async = true;
    script.onload = function () {
      if (!window.Lenis || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
      var lenis = new window.Lenis({
        duration: 1.05,
        easing: function (t) { return Math.min(1, 1.001 - Math.pow(2, -10 * t)); },
        smoothWheel: true,
        syncTouch: false,
        wheelMultiplier: 0.9,
        touchMultiplier: 1
      });
      window.__prestigeLenis = lenis;
      function raf(time) {
        lenis.raf(time);
        window.requestAnimationFrame(raf);
      }
      window.requestAnimationFrame(raf);
      document.addEventListener('visibilitychange', function () {
        if (document.hidden) lenis.stop();
        else lenis.start();
      });
    };
    document.head.appendChild(script);
  })();

  /* First-party analytics: records anonymous page/engagement events only after opt-in. Never reads form values. */
  (function () {
    var consentKey='pe_visitor_analytics_consent', sessionKey='pe_analytics_session', memorySession='', seen={};
    function consent(){try{return localStorage.getItem(consentKey)||''}catch(e){return ''}}
    function store(value){try{localStorage.setItem(consentKey,value)}catch(e){}}
    function uuid(){try{if(window.crypto&&crypto.randomUUID)return crypto.randomUUID()}catch(e){}return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g,function(c){var r=Math.random()*16|0;return(c==='x'?r:(r&3|8)).toString(16)})}
    function session(){var sid='';try{sid=sessionStorage.getItem(sessionKey)||''}catch(e){}if(!sid){sid=memorySession||uuid();memorySession=sid;try{sessionStorage.setItem(sessionKey,sid)}catch(e){}}return sid}
    function campaign(){var p=new URLSearchParams(location.search),o={};['utm_source','utm_medium','utm_campaign','utm_term','utm_content'].forEach(function(k){var v=p.get(k);if(v)o[k]=v.slice(0,120)});return o}
    function track(type,extra){
      if(consent()!=='yes'||seen[type])return;seen[type]=true;
      var body={eventId:uuid(),sessionId:session(),page:location.pathname,referrer:document.referrer||'',eventType:type,campaign:campaign(),engagement:extra||{}};
      fetch('/api/visitors',{method:'POST',credentials:'same-origin',headers:{'Content-Type':'application/json'},cache:'no-store',keepalive:true,body:JSON.stringify(body)})
      .then(function(r){if(!r.ok)console.warn('Prestige analytics request failed:',r.status)})
      .catch(function(e){console.warn('Prestige analytics request failed:',e)});
    }
    function start(){if(consent()!=='yes')return;track('pageview');}
    start();
    var started=Date.now(),status=document.getElementById('analytics-consent-status'),toggle=document.getElementById('analytics-consent-toggle');
    var scrollHandler=function(){if(consent()!=='yes')return;var max=document.documentElement.scrollHeight-innerHeight,p=max>0?scrollY/max*100:100;if(p>=50)track('scroll_50');if(p>=75)track('scroll_75')};
    addEventListener('scroll',scrollHandler,{passive:true});
    var dwellTimer=setInterval(function(){if(consent()!=='yes'){clearInterval(dwellTimer);return}if(Date.now()-started>=30000){track('dwell_30s');clearInterval(dwellTimer)}},5000);
    document.addEventListener('click',function(e){if(consent()!=='yes')return;var el=e.target&&e.target.closest?e.target.closest('a,button'):null;if(!el)return;var label=(el.textContent||el.getAttribute('aria-label')||'').toLowerCase();if(/enquir|whatsapp|book visit|call/.test(label))track('contact_cta_click')},true);
    function render(){if(!toggle)return;var enabled=consent()==='yes';toggle.checked=enabled;if(status)status.textContent=enabled?'Anonymous analytics is enabled. Page views and limited engagement events are recorded.':'Anonymous analytics is disabled. No new analytics events will be recorded.'}
    if(toggle){render();toggle.addEventListener('change',function(){if(toggle.checked){store('yes');seen={};render();start()}else{store('no');render()}})}
  })();

})();
