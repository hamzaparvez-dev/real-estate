'use strict';

const dns = require('node:dns').promises;
const {
  sendJson, getConfig, readJson, rateLimit, verifySession, command, redis
} = require('../lib/enquiry-auth');

const VIS = 'prestige:visitors:identity';
const RECENT = 'prestige:visitors:recent';
const ALIAS = 'prestige:visitors:alias';
const GEO = 'prestige:geo:';

const IPV4 = /^\d{1,3}(\.\d{1,3}){3}$/;
const privateIp = (ip) => !ip || /^(10\.|127\.|192\.168\.|172\.(1[6-9]|2\d|3[01])\.)/.test(ip);
const subnet = (ip) => ip.split('.').slice(0, 3).join('.');

function clientIp(req) {
  const f = String(req.headers['x-forwarded-for'] || '').split(',')[0].trim();
  return IPV4.test(f) ? f : '';
}

/* Vercel supplies geo in headers at no cost; only ASN/org needs a lookup. */
function geoHeaders(req) {
  const dec = (v) => (v ? decodeURIComponent(String(v)).slice(0, 120) : null);
  return {
    city: dec(req.headers['x-vercel-ip-city']),
    region: dec(req.headers['x-vercel-ip-country-region']),
    country: dec(req.headers['x-vercel-ip-country'])
  };
}

async function enrich(config, ip) {
  if (privateIp(ip)) return {};
  const hit = await command(config, ['GET', GEO + ip]);
  if (hit) { try { return JSON.parse(hit); } catch (_) {} }
  const out = {};
  try {
    const rev = await dns.reverse(ip);
    if (rev && rev[0]) out.ptr = String(rev[0]).slice(0, 200);
  } catch (_) {}
  if (out.ptr) {
    const d = out.ptr.split('.').slice(-2).join('.');
    if (!/^(comcast|verizon|att|btcentralplus|virginmedia|spectrum|airtel|jio|bsnl|hathway|actcorp|youbroadband|vodafoneidea)/i.test(d)) {
      out.org = d;
    }
  }
  if (!out.org) {
    try {
      const r = await fetch('https://ipapi.co/' + ip + '/json/', { headers: { 'User-Agent': 'prestige-visitors/1' } });
      const j = await r.json();
      if (j && !j.error) { out.org = j.org ? String(j.org).slice(0, 120) : null; out.asn = j.asn || null; }
    } catch (_) {}
  }
  await command(config, ['SET', GEO + ip, JSON.stringify(out), 'EX', '604800']);
  return out;
}

async function canonical(config, vid) {
  const a = await command(config, ['HGET', ALIAS, vid]);
  return a || vid;
}


// / be ready tracker on the instant fetch click at the home opening 
/* Match on >=3 fingerprint components within the same /24 to survive cleared storage. */
async function stitch(config, vid, fpm, ip) {
  let parts;
  try { parts = JSON.parse(fpm); } catch (_) { return null; }
  const keys = Object.keys(parts).filter((k) => parts[k]);
  if (keys.length < 3) return null;

  const recent = (await command(config, ['ZREVRANGE', RECENT, '0', '199'])) || [];
  if (!recent.length) return null;
  const rows = await redis(config, [['HMGET', VIS].concat(recent)]);

  let best = null, bestScore = 0;
  recent.forEach((id, i) => {
    if (id === vid || !rows[0][i]) return;
    let rec; try { rec = JSON.parse(rows[0][i]); } catch (_) { return; }
    if (rec.subnet && ip && rec.subnet !== subnet(ip)) return;
    const cp = rec.fpm || {};
    let s = 0;
    keys.forEach((k) => { if (cp[k] && cp[k] === parts[k]) s++; });
    if (s > bestScore) { bestScore = s; best = id; }
  });
  return bestScore >= 3 ? best : null;
}

function score(rec) {
  const f = rec.fields || {};
  let s = 0;
  if (f.email) s += 25;
  if (f.phone) s += 20;
  if (f.name) s += 10;
  if (f.company) s += 10;
  s += Math.min((rec.hits || 0) * 2, 20);
  s += Math.min((rec.visits || 1) * 5, 15);
  if (rec.org) s += 10;
  return Math.min(100, s);
}

module.exports = async function handler(req, res) {
  const config = getConfig();
  if (!config) return sendJson(res, 503, { error: 'Visitor storage is not configured.' });

  /* ---------------- POST: beacon ---------------- */
  if (req.method === 'POST') {
    const origin = req.headers.origin;
    if (origin) {
      try {
        const host = String(req.headers['x-forwarded-host'] || req.headers.host || '').split(',')[0].trim().toLowerCase();
        if (new URL(origin).host.toLowerCase() !== host) return sendJson(res, 403, { error: 'Origin not verified.' });
      } catch (_) { return sendJson(res, 403, { error: 'Origin not verified.' }); }
    }

    try {
      const body = await readJson(req, 4096);
      const rawVid = String(body.vid || '');
      if (!/^[a-z0-9._-]{8,80}$/i.test(rawVid)) return sendJson(res, 400, { error: 'Invalid visitor id.' });

      if (!await rateLimit(config, req, 'identity', 240, 3600)) return sendJson(res, 429, { error: 'Rate limit.' });

      const ip = clientIp(req);
      const existing = await canonical(config, rawVid);
      const stored = await command(config, ['HGET', VIS, existing]);
      let rec = null;
      if (stored) { try { rec = JSON.parse(stored); } catch (_) {} }

      if (!rec) {
        const twin = await stitch(config, existing, body.fpm, ip);
        if (twin) {
          await command(config, ['HSET', ALIAS, rawVid, twin]);
          const t = await command(config, ['HGET', VIS, twin]);
          try { rec = t ? JSON.parse(t) : null; } catch (_) {}
          if (rec) { rec.visits = (rec.visits || 1) + 1; }
          if (rec) { await command(config, ['ZADD', RECENT, String(Date.now()), twin]); return sendJson(res, 202, { ok: true, vid: twin, stitched: true }); }
        }
      }

      const now = new Date().toISOString();
      if (!rec) {
        const g = await enrich(config, ip);
        const geo = geoHeaders(req);
        rec = {
          id: existing, fpm: null, ip: ip || null, subnet: ip ? subnet(ip) : null,
          city: geo.city, region: geo.region, country: geo.country,
          asn: g.asn || null, org: g.org || null, ptr: g.ptr || null,
          ua: String(req.headers['user-agent'] || '').slice(0, 400),
          fields: {}, visits: 1, hits: 0, firstSeen: now, lastSeen: now
        };
      }

      if (body.fpm) { try { rec.fpm = JSON.parse(body.fpm); } catch (_) {} }
      rec.hits = (rec.hits || 0) + 1;
      rec.lastSeen = now;
      if (body.page) rec.lastPage = String(body.page).slice(0, 180);

      const fields = Array.isArray(body.fields) ? body.fields.slice(0, 8) : [];
      fields.forEach((f) => {
        const n = String(f && f.n || '').toLowerCase().slice(0, 40);
        const v = String(f && f.v || '').trim().slice(0, 200);
        if (n && v.length > 1) rec.fields[n] = v;
      });

      await command(config, ['HSET', VIS, existing, JSON.stringify(rec)]);
      await command(config, ['ZADD', RECENT, String(Date.now()), existing]);
      await command(config, ['ZREMRANGEBYRANK', RECENT, '0', '-5001']);
      return sendJson(res, 202, { ok: true, vid: existing });
    } catch (e) {
      return sendJson(res, 503, { error: 'Could not record visitor.' });
    }
  }

  /* ---------------- GET: admin list ---------------- */
  if (req.method === 'GET') {
    if (!verifySession(req, config.authSecret)) return sendJson(res, 401, { error: 'Please sign in again.' });
    try {
      const ids = (await command(config, ['ZREVRANGE', RECENT, '0', '299'])) || [];
      if (!ids.length) return sendJson(res, 200, { items: [] });
      const rows = await redis(config, [['HMGET', VIS].concat(ids)]);
      const items = [];
      ids.forEach((id, i) => {
        if (!rows[0][i]) return;
        let rec; try { rec = JSON.parse(rows[0][i]); } catch (_) { return; }
        items.push({
          id, score: score(rec), city: rec.city, country: rec.country,
          org: rec.org, ptr: rec.ptr, asn: rec.asn, ua: rec.ua,
          fields: rec.fields || {}, hits: rec.hits || 0, visits: rec.visits || 1,
          lastPage: rec.lastPage || '/', lastSeen: rec.lastSeen
        });
      });
      items.sort((a, b) => b.score - a.score);
      return sendJson(res, 200, { items });
    } catch (_) {
      return sendJson(res, 503, { error: 'Unable to load visitors.' });
    }
  }

  res.setHeader('Allow', 'GET, POST');
  return sendJson(res, 405, { error: 'Method not allowed.' });
};
