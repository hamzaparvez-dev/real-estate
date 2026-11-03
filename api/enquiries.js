'use strict';

const {
  sendJson, getConfig, readJson, sameOrigin, rateLimit,
  verifySession, command
} = require('../lib/enquiry-auth');

const DATA_KEY = 'prestige:enquiries:data';
const INDEX_KEY = 'prestige:enquiries:index';
const ALLOWED_CONFIGURATIONS = new Set(['1BHK', '2BHK', '3BHK', '4BHK', '5BHK', 'Commercial']);
const ALLOWED_PURPOSES = new Set(['Self Use / End-Use', 'Investment / Rental', 'First Home', 'Upgrade']);
const STATUSES = new Set(['new', 'contacted', 'qualified', 'closed']);

const SAVE_SCRIPT = [
  "redis.call('HSET', KEYS[1], ARGV[1], ARGV[2])",
  "redis.call('ZADD', KEYS[2], ARGV[3], ARGV[1])",
  "local old = redis.call('ZRANGE', KEYS[2], 0, -5001)",
  "for _, id in ipairs(old) do redis.call('ZREM', KEYS[2], id); redis.call('HDEL', KEYS[1], id) end",
  "return redis.call('ZCARD', KEYS[2])"
].join('; ');

const LIST_SCRIPT = [
  "local ids = redis.call('ZREVRANGE', KEYS[1], 0, -1)",
  "local out = {0, 0, 0, 0, 0}",
  "local offset = tonumber(ARGV[1]) or 0",
  "local limit = tonumber(ARGV[2]) or 25",
  "local statusFilter = ARGV[3]",
  "local consentFilter = ARGV[4]",
  "local query = string.lower(ARGV[5] or '')",
  "for _, id in ipairs(ids) do",
  "  local raw = redis.call('HGET', KEYS[2], id)",
  "  if raw then",
  "    local ok, item = pcall(cjson.decode, raw)",
  "    if ok then",
  "      local status = item.status or 'new'",
  "      if status == 'new' then out[2] = out[2] + 1 elseif status == 'contacted' then out[3] = out[3] + 1 elseif status == 'qualified' then out[4] = out[4] + 1 elseif status == 'closed' then out[5] = out[5] + 1 end",
  "      local consent = item.marketingConsent == true",
  "      local matchesStatus = statusFilter == 'all' or status == statusFilter",
  "      local matchesConsent = consentFilter == 'all' or (consentFilter == 'yes' and consent) or (consentFilter == 'no' and not consent)",
  "      local haystack = string.lower((item.name or '') .. ' ' .. (item.phone or '') .. ' ' .. (item.configuration or '') .. ' ' .. (item.purpose or '') .. ' ' .. (item.message or '') .. ' ' .. (item.source or ''))",
  "      local matchesQuery = query == '' or string.find(haystack, query, 1, true) ~= nil",
  "      if matchesStatus and matchesConsent and matchesQuery then",
  "        out[1] = out[1] + 1",
  "        if out[1] > offset and (#out - 5) < limit then table.insert(out, raw) end",
  "      end",
  "    end",
  "  end",
  "end",
  "return out"
].join('; ');

const UPDATE_SCRIPT = [
  "local raw = redis.call('HGET', KEYS[1], ARGV[1])",
  "if not raw then return nil end",
  "local ok, item = pcall(cjson.decode, raw)",
  "if not ok then return nil end",
  "item.status = ARGV[2]",
  "item.notes = ARGV[3]",
  "item.updatedAt = ARGV[4]",
  "redis.call('HSET', KEYS[1], ARGV[1], cjson.encode(item))",
  "return cjson.encode(item)"
].join('; ');

function safeInt(value, fallback, min, max) {
  const parsed = Number.parseInt(value, 10);
  return Number.isFinite(parsed) ? Math.max(min, Math.min(max, parsed)) : fallback;
}

module.exports = async function handler(req, res) {
  const config = getConfig();
  if (!config) return sendJson(res, 503, { error: 'Dashboard setup is incomplete. Configure the Vercel environment variables.' });

  if (req.method === 'POST') {
    if (!sameOrigin(req)) return sendJson(res, 403, { error: 'Request origin could not be verified.' });
    try {
      const body = await readJson(req, 8192);

      // Honeypot field: bot submissions are acknowledged but never stored.
      if (typeof body.website === 'string' && body.website.trim()) return sendJson(res, 200, { ok: true });

      const name = typeof body.name === 'string' ? body.name.trim().slice(0, 100) : '';
      const phone = typeof body.phone === 'string' ? body.phone.replace(/\D/g, '') : '';
      const configuration = typeof body.configuration === 'string' ? body.configuration : '';
      const purpose = typeof body.purpose === 'string' ? body.purpose.trim().slice(0, 80) : '';
      const intent = body.intent === 'site-visit' ? 'site-visit' : 'property';
      const message = typeof body.message === 'string' ? body.message.trim().slice(0, 1000) : '';
      const sourceRaw = typeof body.source === 'string' ? body.source : '/';
      const source = sourceRaw.startsWith('/') ? sourceRaw.split('?')[0].slice(0, 160) : '/';
      const marketingConsent = body.marketingConsent === true;

      if (name.length < 2) return sendJson(res, 400, { error: 'Please enter your full name.' });
      if (!/^[6-9][0-9]{9}$/.test(phone)) return sendJson(res, 400, { error: 'Please enter a valid 10-digit Indian mobile number.' });
      if (!ALLOWED_CONFIGURATIONS.has(configuration)) return sendJson(res, 400, { error: 'Please select a valid configuration.' });
      if (purpose && !ALLOWED_PURPOSES.has(purpose)) return sendJson(res, 400, { error: 'Please select a valid purpose.' });

      if (!await rateLimit(config, req, 'enquiry', 10, 3600)) {
        return sendJson(res, 429, { error: 'Too many enquiries from this connection. Please contact us on WhatsApp or try again later.' });
      }

      const now = new Date().toISOString();
      const record = {
        id: require('node:crypto').randomUUID(),
        name, phone, configuration, purpose, intent, message, source,
        status: 'new',
        notes: '',
        marketingConsent,
        marketingConsentCapturedAt: marketingConsent ? now : null,
        submittedAt: now
      };

      await command(config, [
        'EVAL', SAVE_SCRIPT, 2, DATA_KEY, INDEX_KEY,
        record.id, JSON.stringify(record), String(Date.now())
      ]);

      return sendJson(res, 201, { ok: true, id: record.id });
    } catch (error) {
      if (error && error.message === 'Request too large') return sendJson(res, 413, { error: 'Request too large.' });
      return sendJson(res, 503, { error: 'We could not save your enquiry just now. Please try again or contact us on WhatsApp.' });
    }
  }

  if (req.method === 'GET') {
    if (!verifySession(req, config.authSecret)) return sendJson(res, 401, { error: 'Please sign in again.' });

    const offset = safeInt(req.query && req.query.offset, 0, 0, 4999);
    const limit = safeInt(req.query && req.query.limit, 25, 1, 5000);
    const status = String((req.query && req.query.status) || 'all');
    const consent = String((req.query && req.query.consent) || 'all');
    const query = String((req.query && req.query.q) || '').trim().slice(0, 80).toLowerCase();

    if (status !== 'all' && !STATUSES.has(status)) return sendJson(res, 400, { error: 'Invalid status filter.' });
    if (!['all', 'yes', 'no'].includes(consent)) return sendJson(res, 400, { error: 'Invalid marketing-consent filter.' });

    try {
      const result = await command(config, [
        'EVAL', LIST_SCRIPT, 2, INDEX_KEY, DATA_KEY,
        String(offset), String(limit), status, consent, query
      ]);
      if (!Array.isArray(result)) throw new Error('Invalid enquiry list response');
      const count = Number(result[0] || 0);
      return sendJson(res, 200, {
        total: count,
        counts: {
          new: Number(result[1] || 0),
          contacted: Number(result[2] || 0),
          qualified: Number(result[3] || 0),
          closed: Number(result[4] || 0)
        },
        items: result.slice(5).map(raw => {
          try { return JSON.parse(raw); } catch (_) { return null; }
        }).filter(Boolean)
      });
    } catch (_) {
      return sendJson(res, 503, { error: 'Unable to load enquiries. Check the database connection.' });
    }
  }

  if (req.method === 'PATCH') {
    if (!sameOrigin(req)) return sendJson(res, 403, { error: 'Request origin could not be verified.' });
    if (!verifySession(req, config.authSecret)) return sendJson(res, 401, { error: 'Please sign in again.' });

    try {
      const body = await readJson(req, 4096);
      const id = typeof body.id === 'string' ? body.id : '';
      const status = typeof body.status === 'string' ? body.status : '';
      const notes = typeof body.notes === 'string' ? body.notes.trim().slice(0, 2000) : '';
      if (!/^[0-9a-f-]{36}$/i.test(id)) return sendJson(res, 400, { error: 'Invalid enquiry ID.' });
      if (!STATUSES.has(status)) return sendJson(res, 400, { error: 'Select a valid lead status.' });

      const updated = await command(config, [
        'EVAL', UPDATE_SCRIPT, 1, DATA_KEY,
        id, status, notes, new Date().toISOString()
      ]);
      if (!updated) return sendJson(res, 404, { error: 'Enquiry not found.' });
      return sendJson(res, 200, { ok: true, item: JSON.parse(updated) });
    } catch (error) {
      const tooLarge = error && error.message === 'Request too large';
      return sendJson(res, tooLarge ? 413 : 503, { error: tooLarge ? 'Request too large.' : 'Could not update this enquiry.' });
    }
  }

  res.setHeader('Allow', 'GET, POST, PATCH');
  return sendJson(res, 405, { error: 'Method not allowed.' });
};
