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
  /* Enquiry modal + floating CTA + per-section CTAs */
  (function () {
    var WA = 'https://wa.me/919689557788';
    var modal = document.createElement('div');
    modal.className = 'enq-modal';
    modal.innerHTML = '<div class="enq-box"><button class="enq-close" type="button" aria-label="Close">&times;</button><h3>Enquire Now</h3><p>Share your details and we will get back to you shortly.</p><form class="enq-form"><input name="name" placeholder="Your name" required><input name="phone" placeholder="Phone number" required><input name="email" type="email" placeholder="Email (optional)"><textarea name="message" placeholder="What are you looking for?"></textarea><button type="submit">Send Enquiry</button></form></div>';
    document.body.appendChild(modal);
    var close = function () { modal.classList.remove('open'); document.body.style.overflow = ''; };
    modal.querySelector('.enq-close').addEventListener('click', close);
    modal.addEventListener('click', function (e) { if (e.target === modal) close(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && modal.classList.contains('open')) close(); });
    modal.querySelector('form').addEventListener('submit', function (e) {
      e.preventDefault();
      var f = e.target;
      var msg = 'Hi Prestige Enterprises, my name is ' + (f.name.value || '') + '. Phone: ' + (f.phone.value || '') + '. ' + (f.message.value || '');
      window.open(WA + '?text=' + encodeURIComponent(msg), '_blank');
      close();
    });

    var openModal = function () { modal.classList.add('open'); document.body.style.overflow = 'hidden'; };

    var float = document.createElement('div');
    float.className = 'floating-cta';
    float.innerHTML = '<a class="f-wa" href="' + WA + '?text=' + encodeURIComponent('Hi Prestige Enterprises, I would like more information.') + '" target="_blank" rel="noopener" aria-label="WhatsApp">&#9990;</a><button class="f-enq" type="button" aria-label="Enquire">&#9998;</button>';
    document.body.appendChild(float);
    float.querySelector('.f-enq').addEventListener('click', openModal);

    document.querySelectorAll('section').forEach(function (sec) {
      if (sec.querySelector('.section-cta')) return;
      if (sec.classList.contains('hero') ) return;
      var cta = document.createElement('div');
      cta.className = 'section-cta';
      cta.innerHTML = '<a class="cta-wa" href="' + WA + '?text=' + encodeURIComponent('Hi Prestige Enterprises, I saw your website section and I would like more information.') + '" target="_blank" rel="noopener">WhatsApp</a><button class="cta-enq" type="button">Enquire Now</button>';
      sec.appendChild(cta);
      cta.querySelector('.cta-enq').addEventListener('click', openModal);
    });

    document.querySelectorAll('.enquire-trigger').forEach(function (el) { el.addEventListener('click', function (e) { e.preventDefault(); openModal(); }); });
  })();
})();
