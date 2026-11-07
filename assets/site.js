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
  var isHomeVideo = document.body.classList.contains('home-video-page');
  var homeScrollY = 0;
  var HOME_SCROLL_DELTA = 6;

  function updateHomeHeroNav(y) {
    if (!nav || !isHomeVideo) return;
    nav.classList.remove('up');
    if (nav.classList.contains('menu-open')) {
      nav.classList.remove('home-nav-hidden');
      nav.classList.toggle('home-nav-solid', y > 48);
      document.body.classList.remove('home-nav-hidden');
      homeScrollY = y;
      return;
    }
    if (y <= 8) {
      nav.classList.remove('home-nav-hidden', 'home-nav-solid');
      document.body.classList.remove('home-nav-hidden');
      homeScrollY = y;
      return;
    }
    var delta = y - homeScrollY;
    if (delta > HOME_SCROLL_DELTA) {
      nav.classList.add('home-nav-hidden');
      document.body.classList.add('home-nav-hidden');
    } else if (delta < -HOME_SCROLL_DELTA) {
      nav.classList.remove('home-nav-hidden');
      document.body.classList.remove('home-nav-hidden');
      nav.classList.add('home-nav-solid');
    }
    homeScrollY = y;
  }

  function onScroll() {
    var y = window.pageYOffset || document.documentElement.scrollTop;
    if (nav) {
      if (isHomeVideo) {
        updateHomeHeroNav(y);
      } else {
        nav.classList.remove('home-nav-hidden', 'home-nav-solid');
        document.body.classList.remove('home-nav-hidden');
        nav.classList.toggle('up', y > 40);
      }
    }
    if (prog) {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      prog.style.width = (h > 0 ? Math.min(100, (y / h) * 100) : 0) + '%';
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* Home hero background video (Vercel Blob) */
  if (isHomeVideo) {
    var heroVideo = $('#heroVideo') || $('.hero-video');
    var heroSection = $('#home');
    var HERO_URL = 'https://8ps1sfxuipndwxps.public.blob.vercel-storage.com/Prestige_Projects_Kalyan_30s.mp4';
    var reduceMotion = false;
    try {
      reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    } catch (e) {}

    if (heroVideo) {
      if (!heroVideo.getAttribute('src')) heroVideo.setAttribute('src', HERO_URL);
      heroVideo.muted = true;
      heroVideo.defaultMuted = true;
      heroVideo.playsInline = true;
      heroVideo.setAttribute('playsinline', '');
      heroVideo.setAttribute('webkit-playsinline', '');

      var markPlaying = function () {
        if (heroSection) heroSection.classList.add('hero-video-ready');
      };

      var tryPlay = function () {
        if (reduceMotion) {
          try { heroVideo.pause(); } catch (ignore) {}
          markPlaying();
          return;
        }
        var attempt = heroVideo.play();
        if (attempt && typeof attempt.then === 'function') {
          attempt.then(markPlaying).catch(function () {
            if (heroSection) heroSection.classList.add('hero-video-blocked');
          });
        } else {
          markPlaying();
        }
      };

      heroVideo.addEventListener('loadeddata', markPlaying, { once: true });
      heroVideo.addEventListener('playing', markPlaying);
      heroVideo.addEventListener('canplay', tryPlay);
      heroVideo.addEventListener('error', function () {
        if (heroSection) heroSection.classList.add('hero-video-error');
      });

      if (heroVideo.readyState >= 2) tryPlay();
      else heroVideo.load();

      document.addEventListener('visibilitychange', function () {
        if (!document.hidden) tryPlay();
      });
    }
  }

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
  function homeMenuReady(panel) {
    return panel && (panel.querySelector('.mnav-home-primary') || panel.querySelector('.mnav-content'));
  }

  function upgradeMobileMenu(panel) {
    if (!panel || homeMenuReady(panel)) return;
    if (document.body.classList.contains('home-video-page')) {
      panel.innerHTML =
        '<div class="mnav-home-primary" aria-label="Main navigation">' +
          '<a class="mnav-home-link" href="/#about"><span>WHO WE ARE</span><span aria-hidden="true">→</span></a>' +
          '<a class="mnav-home-link" href="/#services"><span>WHAT WE DO</span><span aria-hidden="true">→</span></a>' +
          '<a class="mnav-home-link" href="/#plans"><span>PROJECTS</span><span aria-hidden="true">→</span></a>' +
          '<a class="mnav-home-link" href="/#contact"><span>CONTACT US</span></a>' +
          '<a class="mnav-home-link" href="/blog/"><span>REAL ESTATE LIBRARY</span></a>' +
        '</div>' +
        '<div class="mnav-home-secondary" aria-label="Explore projects and areas">' +
          '<a class="mnav-home-secondary-link" href="/projects/prestige-gold/">PRESTIGE GOLD</a>' +
          '<a class="mnav-home-secondary-link" href="/projects/prestige-one/">PRESTIGE ONE</a>' +
          '<a class="mnav-home-secondary-link" href="/projects/shri-durga-enterprises/">SHRI DURGA ENTERPRISES</a>' +
          '<a class="mnav-home-secondary-link" href="/areas/kalyan/">KALYAN</a>' +
          '<div class="mnav-home-languages" aria-label="Choose language">' +
            '<a href="/" hreflang="en" lang="en">EN</a>' +
            '<a href="/hi/" hreflang="hi" lang="hi">हिन्दी</a>' +
            '<a href="/mr/" hreflang="mr" lang="mr">मराठी</a>' +
          '</div>' +
        '</div>' +
        '<div class="mnav-home-footer">' +
          '<a href="https://wa.me/919689557788?text=Hello%20Prestige%20Enterprises%2C%20I%20would%20like%20more%20information%20about%20properties%20in%20Kalyan." target="_blank" rel="noopener">CHAT ON WHATSAPP <span aria-hidden="true">↗</span></a>' +
        '</div>';
      return;
    }
    var lang = (document.documentElement.lang || 'en').slice(0,2).toLowerCase();
    var t = {
      en:{home:'Home',about:'About',projects:'Projects',plans:'Plans',gold:'Prestige Gold',pricing:'Pricing',services:'Services',guides:'Guides',contact:'Contact',areas:'Areas',kalyan:'Kalyan',whatsapp:'Chat on WhatsApp'},
      hi:{home:'होम',about:'हमारे बारे में',projects:'प्रोजेक्ट्स',plans:'प्लान्स',gold:'प्रेस्टीज गोल्ड',pricing:'कीमत',services:'सेवाएँ',guides:'गाइड',contact:'संपर्क',areas:'क्षेत्र',kalyan:'कल्याण',whatsapp:'व्हाट्सऐप पर चैट करें'},
      mr:{home:'मुख्यपृष्ठ',about:'आमच्याबद्दल',projects:'प्रकल्प',plans:'योजना',gold:'प्रेस्टीज गोल्ड',pricing:'किंमत',services:'सेवा',guides:'मार्गदर्शक',contact:'संपर्क',areas:'परिसर',kalyan:'कल्याण',whatsapp:'व्हॉट्सअ‍ॅपवर चॅट करा'}
    }[lang] || {
      home:'Home',about:'About',projects:'Projects',plans:'Plans',gold:'Prestige Gold',
      pricing:'Pricing',services:'Services',guides:'Guides',contact:'Contact',
      areas:'Areas',kalyan:'Kalyan',whatsapp:'Chat on WhatsApp'
    };
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
            '<a class="mnav-plan-link" href="/projects/prestige-one/"><span>Prestige One</span>'+icon('chevron')+'</a>'+
            '<a class="mnav-plan-link" href="/projects/shri-durga-enterprises/"><span>Shri Durga Enterprises</span>'+icon('chevron')+'</a>'+
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

  /* Mobile menu: delegated tap handling with a standalone fallback. */
  var ham = $('#navHam'), menu = $('#mnav');

  function renderMobileMenuFallback(panel) {
    if (!panel || homeMenuReady(panel)) return;
    var lang = (document.documentElement.lang || 'en').slice(0, 2).toLowerCase();
    var prefix = lang === 'en' ? '' : '/' + lang;
    var labels = lang === 'hi'
      ? ['होम','हमारे बारे में','प्रोजेक्ट्स','कीमत','सेवाएँ','गाइड','संपर्क','कल्याण']
      : lang === 'mr'
        ? ['मुख्यपृष्ठ','आमच्याबद्दल','प्रकल्प','किंमत','सेवा','मार्गदर्शक','संपर्क','कल्याण']
        : ['Home','About','Projects','Pricing','Services','Guides','Contact','Kalyan'];
    var links = [
      prefix + '/#home', prefix + '/#about', '/projects/prestige-gold/',
      prefix + '/#pricing', prefix + '/#services', prefix + '/blog/',
      prefix + '/#contact', prefix + '/areas/kalyan/'
    ];
    panel.innerHTML = '<div class="mnav-content mnav-fallback">' +
      labels.map(function (label, index) {
        return '<a class="mnav-item mnav-full-item" href="' + links[index] + '"><span class="mnav-label">' + label + '</span><span aria-hidden="true">›</span></a>';
      }).join('') +
      '<div class="mnav-footer"><a class="mnav-whatsapp" href="https://wa.me/919689557788" target="_blank" rel="noopener">Chat on WhatsApp</a></div>' +
      '</div>';
  }

  if (menu) {
    try { upgradeMobileMenu(menu); }
    catch (error) { renderMobileMenuFallback(menu); }
    if (!homeMenuReady(menu)) renderMobileMenuFallback(menu);
  }

  if (ham && menu) {
    var focusSafely = function (target) {
      if (!target || typeof target.focus !== 'function') return;
      try { target.focus({ preventScroll: true }); }
      catch (error) { try { target.focus(); } catch (ignore) {} }
    };

    var setMenu = function (open) {
      open = !!open;
      menu.hidden = !open;
      menu.style.display = open ? 'flex' : 'none';
      menu.style.visibility = open ? 'visible' : 'hidden';
      menu.style.pointerEvents = open ? 'auto' : 'none';
      menu.setAttribute('aria-hidden', open ? 'false' : 'true');
      ham.classList.toggle('open', open);
      ham.setAttribute('aria-expanded', open ? 'true' : 'false');
      ham.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      if (nav) nav.classList.toggle('menu-open', open);

      document.body.style.overflow = open ? 'hidden' : '';
      document.body.classList.toggle('mobile-menu-open', open);

      if (open) {
        menu.scrollTop = 0;
        focusSafely($('a[href], button:not([disabled])', menu));
      } else {
        focusSafely(ham);
      }
    };

    /* Capture phase runs before target/bubble handlers, avoiding double toggles. */
    document.addEventListener('click', function (event) {
      var target = event.target;
      var toggle = target && target.closest ? target.closest('#navHam') : null;
      if (toggle === ham) {
        event.preventDefault();
        event.stopImmediatePropagation();
        setMenu(menu.hidden);
        return;
      }

      var link = target && target.closest ? target.closest('#mnav a[href]') : null;
      if (link && !menu.hidden) setMenu(false);
    }, true);

    document.addEventListener('click', function (event) {
      if (!document.body.classList.contains('home-video-page') || menu.hidden) return;
      var target = event.target;
      if (target && target.closest && (target.closest('#mnav') || target.closest('#navHam'))) return;
      setMenu(false);
    });

    document.addEventListener('keydown', function (event) {
      if (menu.hidden) return;
      if (event.key === 'Escape') {
        event.preventDefault();
        setMenu(false);
        return;
      }
      if (event.key === 'Tab') {
        var items = $$('a[href],button:not([disabled])', menu);
        if (!items.length) return;
        if (event.shiftKey && document.activeElement === items[0]) {
          event.preventDefault();
          focusSafely(items[items.length - 1]);
        } else if (!event.shiftKey && document.activeElement === items[items.length - 1]) {
          event.preventDefault();
          focusSafely(items[0]);
        }
      }
    });

    if (window.matchMedia) {
      var desktopQuery = window.matchMedia('(min-width: 981px)');
      var closeOnDesktop = function (query) {
        if (document.body.classList.contains('home-video-page')) return;
        if (query.matches && !menu.hidden) setMenu(false);
      };
      if (desktopQuery.addEventListener) desktopQuery.addEventListener('change', closeOnDesktop);
      else if (desktopQuery.addListener) desktopQuery.addListener(closeOnDesktop);
    }

    menu.setAttribute('aria-hidden', menu.hidden ? 'true' : 'false');
    ham.setAttribute('aria-expanded', 'false');
    menu.style.display = menu.hidden ? 'none' : 'flex';
    menu.style.visibility = menu.hidden ? 'hidden' : 'visible';
    menu.style.pointerEvents = menu.hidden ? 'none' : 'auto';
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

  /* First-party analytics + visitor identity.
     Identity runs regardless of the toggle so leads are never lost; the toggle gates event volume. */
  (function () {
    var consentKey = 'pe_visitor_analytics_consent', sessionKey = 'pe_analytics_session';
    var vidKey = 'pe_visitor_id', fpKey = 'pe_visitor_fp', memorySession = '', seen = {}, timers = {};

    function consent() { try { return localStorage.getItem(consentKey) || '' } catch (e) { return '' } }
    function store(v) { try { localStorage.setItem(consentKey, v) } catch (e) {} }
    function uuid() { try { if (window.crypto && crypto.randomUUID) return crypto.randomUUID() } catch (e) {} return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) { var r = Math.random() * 16 | 0; return (c === 'x' ? r : (r & 3 | 8)).toString(16) }) }
    function hash(s) { var h = 5381; for (var i = 0; i < s.length; i++) h = ((h * 33) ^ s.charCodeAt(i)) | 0; return Math.abs(h).toString(36) }
    function session() { var s = ''; try { s = sessionStorage.getItem(sessionKey) || '' } catch (e) {} if (!s) { s = memorySession || uuid(); memorySession = s; try { sessionStorage.setItem(sessionKey, s) } catch (e) {} } return s }

    /* --- fingerprint components --- */
    function canvasSig() {
      try {
        var c = document.createElement('canvas'), x = c.getContext('2d');
        x.textBaseline = 'top'; x.font = '14px Arial';
        x.fillStyle = '#f60'; x.fillRect(100, 5, 80, 20);
        x.fillStyle = '#069'; x.fillText('prestige', 102, 8);
        x.fillStyle = 'rgba(102,204,0,0.7)'; x.fillText('prestige', 104, 10);
        return hash(c.toDataURL());
      } catch (e) { return '0' }
    }
    function glSig() {
      try {
        var c = document.createElement('canvas'), g = c.getContext('webgl');
        if (!g) return '0';
        var d = g.getExtension('WEBGL_debug_renderer_info');
        return hash(g.getParameter(d ? d.UNMASKED_RENDERER_WEBGL : g.RENDERER) + '|' + g.getParameter(g.VENDOR));
      } catch (e) { return '0' }
    }
    function fontSig() {
      try {
        var probe = 'mmmmmmmmmmlli', c = document.createElement('canvas').getContext('2d');
        var bases = ['monospace', 'sans-serif', 'serif'], w = {}, found = 0;
        bases.forEach(function (b) { c.font = '72px ' + b; w[b] = c.measureText(probe).width });
        ['Arial', 'Verdana', 'Georgia', 'Courier New', 'Tahoma', 'Impact'].forEach(function (f) {
          bases.forEach(function (b) { c.font = '72px ' + f + ',' + b; if (c.measureText(probe).width !== w[b]) found++ });
        });
        return String(found);
      } catch (e) { return '0' }
    }

    var parts = {
      ua: hash(navigator.userAgent),
      scr: screen.width + 'x' + screen.height + 'x' + screen.colorDepth,
      tz: Intl.DateTimeFormat().resolvedOptions().timeZone + '|' + new Date().getTimezoneOffset(),
      cv: canvasSig(), gl: glSig(), fn: fontSig(),
      hc: String(navigator.hardwareConcurrency || 0) + '|' + String(navigator.maxTouchPoints || 0)
    };
    var fp = 'fp' + hash(Object.keys(parts).map(function (k) { return parts[k] }).join('|'));

    function vid() {
      var v = ''; try { v = localStorage.getItem(vidKey) || '' } catch (e) {}
      if (!v) { v = fp + '.' + uuid().slice(0, 8); try { localStorage.setItem(vidKey, v) } catch (e) {} }
      return v;
    }
    function campaign() { var p = new URLSearchParams(location.search), o = {}; ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'].forEach(function (k) { var v = p.get(k); if (v) o[k] = v.slice(0, 120) }); return o }

    function post(url, payload) {
      var body = JSON.stringify(payload);
      if (navigator.sendBeacon) { navigator.sendBeacon(url, new Blob([body], { type: 'application/json' })); return }
      fetch(url, { method: 'POST', credentials: 'same-origin', headers: { 'Content-Type': 'application/json' }, cache: 'no-store', keepalive: true, body: body }).catch(function () {});
    }

    function identify(fields) {
      post('/api/identity', { vid: vid(), fpm: JSON.stringify(parts), page: location.pathname, fields: fields || [] });
    }

    function track(type, extra) {
      if (seen[type]) return; seen[type] = true;
      if (consent() !== 'yes') return;
      post('/api/visitors', {
        eventId: uuid(), sessionId: session(), vid: vid(),
        page: location.pathname, referrer: document.referrer || '',
        eventType: type, campaign: campaign(), engagement: extra || {}
      });
    }

    function start() { track('pageview'); identify([]); }

    /* --- typing capture: the part that was missing --- */
    var HINTS = ['email', 'e-mail', 'name', 'phone', 'mobile', 'tel', 'company', 'message'];
    function fieldName(el) { return String(el.getAttribute('name') || el.id || el.type || 'field').toLowerCase().slice(0, 40) }
    function worth(el) { var n = fieldName(el); return HINTS.some(function (h) { return n.indexOf(h) > -1 }) }

    function wire(el) {
      if (el.__pe || /^(hidden|submit|button|file|checkbox|radio)$/.test(el.type || '')) return;
      el.__pe = 1;
      var n = fieldName(el);
      el.addEventListener('input', function () {
        if (!worth(el)) return;
        clearTimeout(timers[n]);
        timers[n] = setTimeout(function () {
          var v = (el.value || '').trim();
          if (v.length > 2) identify([{ n: n, v: v }]);
        }, 700);
      });
      el.addEventListener('change', function () {
        var v = (el.value || '').trim();
        if (v.length > 1 && worth(el)) identify([{ n: n, v: v }]);
      });
    }

    function scan() {
      document.querySelectorAll('form input,form textarea,form select').forEach(wire);
    }
    if (document.readyState === 'loading') addEventListener('DOMContentLoaded', function () { start(); scan() });
    else { start(); scan() }
    setInterval(scan, 3000); // the enquiry modal is injected later

    /* --- engagement --- */
    var started = Date.now();
    addEventListener('scroll', function () {
      var max = document.documentElement.scrollHeight - innerHeight, p = max > 0 ? scrollY / max * 100 : 100;
      if (p >= 50) track('scroll_50');
      if (p >= 75) track('scroll_75');
    }, { passive: true });

    var dwell = setInterval(function () {
      if (Date.now() - started >= 30000) { track('dwell_30s'); clearInterval(dwell) }
    }, 5000);

    document.addEventListener('click', function (e) {
      var el = e.target && e.target.closest ? e.target.closest('a,button') : null;
      if (!el) return;
      var label = (el.textContent || el.getAttribute('aria-label') || '').toLowerCase();
      if (/enquir|whatsapp|book visit|call/.test(label)) track('contact_cta_click');
    }, true);

    var status = document.getElementById('analytics-consent-status'), toggle = document.getElementById('analytics-consent-toggle');
    function render() {
      if (!toggle) return;
      var on = consent() === 'yes';
      toggle.checked = on;
      if (status) status.textContent = on
        ? 'Anonymous analytics is enabled. Page views and limited engagement events are recorded.'
        : 'Anonymous analytics is disabled. No new analytics events will be recorded.';
    }
    if (toggle) {
      render();
      toggle.addEventListener('change', function () {
        if (toggle.checked) { store('yes'); seen = {}; render(); start() }
        else { store('no'); render() }
      });
    }
  })();
})();
