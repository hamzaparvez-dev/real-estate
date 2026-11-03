/* Prestige Enterprises private enquiry dashboard */
(function () {
  var $ = function (selector) { return document.querySelector(selector); };
  var loginView = $('#admin-login'), dashboard = $('#admin-dashboard');
  var loginForm = $('#admin-login-form'), loginError = $('#admin-login-error');
  var dashboardError = $('#admin-dashboard-error'), logout = $('#admin-logout');
  var list = $('#admin-enquiry-list'), search = $('#admin-search');
  var offset = 0, limit = 25, total = 0, items = [], busy = false;
  function esc(value) {
    return String(value == null ? '' : value).replace(/[&<>"']/g, function (c) {
      return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c];
    });
  }
  function date(value) {
    var d = new Date(value);
    return Number.isNaN(d.getTime()) ? 'Date unavailable' :
      new Intl.DateTimeFormat('en-IN', { day:'2-digit', month:'short', year:'numeric', hour:'2-digit', minute:'2-digit' }).format(d);
  }
  function showLogin(message) {
    loginView.hidden = false; dashboard.hidden = true; logout.hidden = true; loginError.textContent = message || '';
  }
  function showDashboard() {
    loginView.hidden = true; dashboard.hidden = false; logout.hidden = false; loginError.textContent = '';
  }
  function render() {
    var q = (search.value || '').trim().toLowerCase();
    var rows = items.filter(function (x) {
      return [x.name,x.phone,x.configuration,x.purpose,x.intent,x.message,x.source].join(' ').toLowerCase().indexOf(q) !== -1;
    });
    $('#admin-total').textContent = String(total);
    $('#admin-showing').textContent = String(rows.length);
    if (!rows.length) {
      list.innerHTML = '<div class="admin-enquiry-empty">' + (items.length ? 'No enquiries match this search.' : 'No enquiries have been received yet.') + '</div>';
    } else {
      list.innerHTML = rows.map(function (x) {
        var phone = String(x.phone || '').replace(/\D/g, '');
        var extra = x.message ? '<p class="admin-enquiry-message">' + esc(x.message) + '</p>' : '';
        var intent = x.intent === 'site-visit' ? 'SITE VISIT' : 'PROPERTY ENQUIRY';
        var wa = encodeURIComponent('Hello ' + (x.name || '') + ', this is Prestige Enterprises following up on your enquiry.');
        return '<article class="admin-enquiry-card"><div class="admin-enquiry-main">' +
          '<h2 class="admin-enquiry-name">' + esc(x.name || 'Unnamed enquiry') + '</h2>' +
          '<div class="admin-enquiry-meta"><span>' + esc(date(x.submittedAt)) + '</span>' +
          (phone ? '<a href="tel:+91' + phone + '">+91 ' + esc(phone) + '</a>' : '') +
          '<span>' + esc(x.source || '/') + '</span></div>' +
          '<div class="admin-enquiry-badges"><span class="admin-enquiry-badge red">' + esc(x.configuration || 'Not specified') + '</span>' +
          '<span class="admin-enquiry-badge">' + esc(x.purpose || 'Not specified') + '</span>' +
          '<span class="admin-enquiry-badge">' + esc(intent) + '</span></div></div>' +
          '<div class="admin-enquiry-actions">' + (phone ? '<a class="admin-enquiry-call" href="tel:+91' + phone + '">Call</a>' : '') +
          (phone ? '<a class="admin-enquiry-wa" href="https://wa.me/91' + phone + '?text=' + wa + '" target="_blank" rel="noopener">WhatsApp</a>' : '') +
          '</div>' + extra + '</article>';
      }).join('');
    }
    $('#admin-page-label').textContent = 'Showing ' + (total ? offset + 1 : 0) + '–' + Math.min(offset + limit,total) + ' of ' + total;
    $('#admin-prev').disabled = offset <= 0 || busy;
    $('#admin-next').disabled = offset + limit >= total || busy;
  }
  async function load() {
    if (busy) return;
    busy = true; dashboardError.textContent = ''; $('#admin-refresh').disabled = true;
    try {
      var r = await fetch('/api/enquiries?offset=' + offset + '&limit=' + limit, { credentials:'same-origin', cache:'no-store' });
      var b = await r.json().catch(function () { return {}; });
      if (r.status === 401) { showLogin('Your session has expired. Please sign in again.'); return; }
      if (!r.ok) throw new Error(b.error || 'Unable to load enquiries.');
      items = Array.isArray(b.items) ? b.items : []; total = Number(b.total || 0); render();
    } catch (e) { dashboardError.textContent = e.message || 'Unable to load enquiries.'; }
    finally { busy = false; $('#admin-refresh').disabled = false; render(); }
  }
  async function checkSession() {
    try {
      var r = await fetch('/api/auth', { credentials:'same-origin', cache:'no-store' });
      var b = await r.json().catch(function () { return {}; });
      if (r.ok && b.authenticated) { showDashboard(); await load(); }
      else if (r.status === 503) showLogin('Dashboard setup is incomplete. Configure the required Vercel environment variables.');
      else showLogin('');
    } catch (_) { showLogin('Could not connect to the dashboard. Check your internet connection.'); }
  }
  loginForm.addEventListener('submit', async function (e) {
    e.preventDefault(); loginError.textContent = '';
    var button = loginForm.querySelector('button[type="submit"]'), password = $('#admin-password').value;
    if (!password) { loginError.textContent = 'Enter the dashboard password.'; return; }
    button.disabled = true; button.textContent = 'Signing in…';
    try {
      var r = await fetch('/api/auth', { method:'POST', credentials:'same-origin', headers:{'Content-Type':'application/json'}, body:JSON.stringify({password:password}) });
      var b = await r.json().catch(function () { return {}; });
      if (!r.ok) throw new Error(b.error || 'Sign-in failed.');
      loginForm.reset(); offset = 0; showDashboard(); await load();
    } catch (err) { loginError.textContent = err.message || 'Sign-in failed.'; }
    finally { button.disabled = false; button.textContent = 'Sign in securely'; }
  });
  logout.addEventListener('click', async function () {
    try { await fetch('/api/auth', {method:'DELETE',credentials:'same-origin'}); }
    finally { items = []; total = 0; showLogin('You have signed out.'); }
  });
  $('#admin-refresh').addEventListener('click', load);
  $('#admin-prev').addEventListener('click', function () { if (offset >= limit) { offset -= limit; load(); } });
  $('#admin-next').addEventListener('click', function () { if (offset + limit < total) { offset += limit; load(); } });
  search.addEventListener('input', render);
  checkSession();
})();
