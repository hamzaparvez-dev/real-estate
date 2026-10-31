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
        <div class="enq-eyebrow">PRESTIGE ENTERPRISES · PROPERTY ENQUIRY</div>
        <h3 id="enqTitle">Let’s find your next home.</h3>
        <p id="enqIntro">Share a few details. Our property team will contact you to understand your requirements.</p>
        <form class="enq-form" novalidate>
          <div class="enq-fields">
            <label class="enq-field enq-wide">Full name <span>*</span><input name="name" autocomplete="name" placeholder="Enter your full name" required minlength="2"></label>
            <label class="enq-field">Mobile number <span>*</span><input name="phone" type="tel" inputmode="numeric" autocomplete="tel" placeholder="10-digit mobile number" required pattern="[6-9][0-9]{9}" maxlength="10"></label>
            <label class="enq-field">Email address<input name="email" type="email" autocomplete="email" placeholder="name@example.com"></label>
            <label class="enq-field">I am looking to <span>*</span><select name="requirement" required><option value="">Select requirement</option><option>Buy a property</option><option>Rent a property</option><option>Sell my property</option><option>Investment enquiry</option></select></label>
            <label class="enq-field">Property type <span>*</span><select name="property" required><option value="">Select property type</option><option>1 BHK</option><option>2 BHK</option><option>3 BHK or larger</option><option>Villa / Row house</option><option>Residential plot</option><option>Other residential property</option></select></label>
            <label class="enq-field">Preferred location<input name="location" placeholder="e.g. Kalyan, Dombivli, Thane"></label>
            <label class="enq-field">Approximate budget<select name="budget"><option value="">Select budget</option><option>Below ₹25 lakh</option><option>₹25–40 lakh</option><option>₹40–60 lakh</option><option>₹60–80 lakh</option><option>₹80 lakh–₹1 crore</option><option>Above ₹1 crore</option><option>Not decided yet</option></select></label>
            <label class="enq-field">Buying / moving timeline<select name="timeline"><option value="">Select timeline</option><option>Immediately</option><option>Within 1 month</option><option>Within 3 months</option><option>Within 6 months</option><option>Just exploring</option></select></label>
            <label class="enq-field enq-wide">Additional details<textarea name="message" rows="3" placeholder="Anything else we should know? (Optional)"></textarea></label>
          </div>
          <p class="enq-consent">By continuing, you agree that Prestige Enterprises may contact you about this enquiry.</p>
          <p class="enq-error" role="alert" aria-live="polite"></p>
          <button class="enq-submit" type="submit">Continue to WhatsApp <span aria-hidden="true">→</span></button>
          <p class="enq-foot">Your details will be shared with our team through WhatsApp. No online payment is required.</p>
        </form>
      </div>`;
    document.body.appendChild(modal);
    var form = modal.querySelector('form');
    var lastFocus = null;
    var close = function () {
      modal.classList.remove('open');
      modal.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
      if (lastFocus && typeof lastFocus.focus === 'function') lastFocus.focus();
    };
    var openModal = function (trigger) {
      lastFocus = trigger || document.activeElement;
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
        'Hello Prestige Enterprises, I would like to make a property enquiry.',
        '',
        'Name: ' + data.get('name'),
        'Mobile: ' + phone,
        'Email: ' + (data.get('email') || 'Not provided'),
        'Requirement: ' + data.get('requirement'),
        'Property type: ' + data.get('property'),
        'Preferred location: ' + (data.get('location') || 'Not specified'),
        'Budget: ' + (data.get('budget') || 'Not specified'),
        'Timeline: ' + (data.get('timeline') || 'Not specified'),
        'Additional details: ' + (data.get('message') || 'None')
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
    float.innerHTML = '<a class="f-wa" href="' + WA + '?text=' + encodeURIComponent('Hello Prestige Enterprises, I would like more information about residential properties.') + '" target="_blank" rel="noopener" aria-label="WhatsApp">&#9990;</a><button class="f-enq" type="button" aria-label="Open property enquiry form">&#9998;</button>';
    document.body.appendChild(float);
    float.querySelector('.f-enq').addEventListener('click', function () { openModal(this); });

    document.querySelectorAll('section').forEach(function (sec) {
      if (sec.querySelector('.section-cta') || sec.classList.contains('hero')) return;
      var cta = document.createElement('div');
      cta.className = 'section-cta';
      cta.innerHTML = '<a class="cta-wa" href="' + WA + '?text=' + encodeURIComponent('Hello Prestige Enterprises, I would like more information about this section of your website.') + '" target="_blank" rel="noopener">WhatsApp</a><button class="cta-enq" type="button">Enquire Now</button>';
      sec.appendChild(cta);
      cta.querySelector('.cta-enq').addEventListener('click', function () {
        var section = sec.id || sec.querySelector('h2')?.textContent || 'Website enquiry';
        var details = form.querySelector('[name="message"]');
        if (details && !details.value) details.value = 'I am enquiring about: ' + section;
        openModal(this);
      });
    });
    document.querySelectorAll('.enquire-trigger').forEach(function (el) {
      el.addEventListener('click', function (e) { e.preventDefault(); openModal(this); });
    });
    document.querySelectorAll('a,button').forEach(function (el) {
      if (el.classList.contains('cta-enq') || el.classList.contains('f-enq') || el.classList.contains('enquire-trigger')) return;
      var label = (el.textContent || el.getAttribute('aria-label') || '').trim().toLowerCase();
      if (!/\\b(enquire|enquiry|send enquiry|request details)\\b/.test(label)) return;
      var href = el.getAttribute('href') || '';
      if (el.tagName === 'A' && href && !/^#/.test(href) && href.indexOf('wa.me') === -1) return;
      el.addEventListener('click', function (e) {
        if (el.tagName === 'A') e.preventDefault();
        var card = el.closest('.plan-card');
        var section = el.closest('section');
        var context = card ? (card.querySelector('h3')?.textContent || 'featured project') : (section?.id || '');
        var details = form.querySelector('[name="message"]');
        if (context && details && !details.value) details.value = 'I am enquiring about: ' + context;
        openModal(this);
      });
    });
  })();
})();
