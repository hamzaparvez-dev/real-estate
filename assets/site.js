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

  /* Areas dropdown */
  var dd = $('#navAreas');
  if (dd) {
    var btn = $('.nav-dd-btn', dd);
    var setDd = function (o) { dd.classList.toggle('open', o); btn.setAttribute('aria-expanded', o ? 'true' : 'false'); };
    btn.addEventListener('click', function (e) { e.stopPropagation(); setDd(!dd.classList.contains('open')); });
    document.addEventListener('click', function (e) { if (!dd.contains(e.target)) setDd(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setDd(false); });
  }

  /* Mobile menu */
  var ham = $('#navHam'), menu = $('#mnav');
  if (ham && menu) {
    var setMenu = function (o) {
      menu.hidden = !o; ham.classList.toggle('open', o); ham.setAttribute('aria-expanded', o ? 'true' : 'false');
      nav.classList.toggle('menu-open', o); document.body.style.overflow = o ? 'hidden' : '';
    };
    ham.addEventListener('click', function () { setMenu(menu.hidden); });
    menu.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !menu.hidden) { setMenu(false); ham.focus(); } });
    var mq = window.matchMedia('(min-width:981px)');
    (mq.addEventListener ? mq.addEventListener.bind(mq, 'change') : mq.addListener.bind(mq))(function (q) { if (q.matches) setMenu(false); });
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
    modal.innerHTML = '<div class="lightbox-box"><button class="lightbox-close" type="button" aria-label="Close">&times;</button><img src="" alt=""><div class="lightbox-title"></div></div>';
    document.body.appendChild(modal);
    var modalImg = $('img', modal);
    var modalTitle = $('.lightbox-title', modal);
    var closeModal = function () { modal.classList.remove('open'); document.body.style.overflow = ''; };
    $('.lightbox-close', modal).addEventListener('click', closeModal);
    modal.addEventListener('click', function (e) { if (e.target === modal) closeModal(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && modal.classList.contains('open')) closeModal(); });
    planWraps.forEach(function (w) {
      if (!w.getAttribute('data-full')) return; // "Available on request" placeholders are not lightbox items.
      w.addEventListener('click', function () {
        var src = w.getAttribute('data-full');
        var title = w.getAttribute('data-title');
        modalImg.src = src;
        modalImg.alt = title;
        modalTitle.textContent = title;
        modal.classList.add('open');
        document.body.style.overflow = 'hidden';
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
            <label class="enq-field">Select Configuration <span>*</span><select name="configuration" required><option value="">Select</option><option>1BHK</option><option>2BHK</option><option>3BHK</option><option>Commercial</option></select></label>
            <label class="enq-field">Purpose <select name="purpose"><option value="">Select</option><option>Self Use / End-Use</option><option>Investment / Rental</option><option>First Home</option><option>Upgrade</option></select></label>
          </div>
          <p class="enq-consent">By submitting you authorize us to contact you via call/SMS/email.</p>
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
      var url = WA + '?text=' + encodeURIComponent(lines.join('\n'));
      var popup = window.open(url, '_blank');
      if (popup) popup.opener = null;
      else window.location.href = url;
      close();
      form.reset();
    });

    var float = document.createElement('div');
    float.className = 'floating-cta';
    float.setAttribute('aria-label', 'Quick contact actions');
    float.innerHTML = '<button class="f-book" type="button" data-enquiry-intent="site-visit" aria-label="Book a site visit">BOOK VISIT</button><a class="f-wa" href="' + WA + '?text=' + encodeURIComponent('Hello Prestige Enterprises, I would like more information about homes in Kalyan.') + '" target="_blank" rel="noopener" aria-label="WhatsApp"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 11.5a8.4 8.4 0 0 1-12.4 7.4L3 20l1.2-4.3A8.4 8.4 0 1 1 20 11.5Z"/><path d="M8.5 8.2c.3-.6.6-.6.9-.6h.4c.2 0 .4.1.5.4l.7 1.7c.1.2.1.4-.1.6l-.5.6c-.2.2-.2.4 0 .7.6 1 1.4 1.7 2.4 2.2.3.1.5.1.7-.1l.7-.8c.2-.2.4-.3.7-.2l1.6.8c.3.1.4.3.4.5 0 .3-.2 1-.7 1.4-.5.4-1.1.6-1.8.5-1-.1-2.2-.6-3.6-1.8-1.6-1.4-2.6-3.1-2.8-4.1-.2-.9.1-1.5.5-1.8Z"/></svg><span>WHATSAPP</span></a><button class="f-enq" type="button" data-enquiry-intent="property" aria-label="Enquire now">ENQUIRE NOW</button>';
    document.body.appendChild(float);
    float.querySelector('.f-book').addEventListener('click', function () { openModal(this); });
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

})();
