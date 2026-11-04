'use strict';
const {sendJson,getConfig,readJson,rateLimit,verifySession,command}=require('../lib/enquiry-auth');
const DATA_KEY='prestige:visitors:data',INDEX_KEY='prestige:visitors:index';
const SAVE_SCRIPT=[
 "redis.call('HSET',KEYS[1],ARGV[1],ARGV[2])",
 "redis.call('ZADD',KEYS[2],ARGV[3],ARGV[1])",
 "local old=redis.call('ZRANGE',KEYS[2],0,-5001)",
 "for _,id in ipairs(old) do redis.call('ZREM',KEYS[2],id); redis.call('HDEL',KEYS[1],id) end",
 "return redis.call('ZCARD',KEYS[2])"
].join('; ');
const LIST_SCRIPT=[
 "local ids=redis.call('ZREVRANGE',KEYS[1],0,-1)",
 "local out={}",
 "local limit=tonumber(ARGV[1]) or 500",
 "local sessions={}",
 "local pages={}",
 "for _,id in ipairs(ids) do",
 " local raw=redis.call('HGET',KEYS[2],id)",
 " if raw then local ok,item=pcall(cjson.decode,raw); if ok then",
 "  table.insert(out,raw); sessions[item.sessionId]=true; pages[item.page]=(pages[item.page] or 0)+1",
 "  if #out>=limit then break end",
 " end end",
 "end",
 "local unique=0; for _ in pairs(sessions) do unique=unique+1 end",
 "local top=''; local topCount=0; for page,count in pairs(pages) do if count>topCount then top=page; topCount=count end end",
 "return {redis.call('ZCARD',KEYS[1]),unique,top,out}"
].join('; ');
function browser(ua){ua=String(ua||'').toLowerCase();if(ua.includes('edg/'))return'Edge';if(ua.includes('opr/')||ua.includes('opera'))return'Opera';if(ua.includes('firefox/'))return'Firefox';if(ua.includes('chrome/')&&!ua.includes('chromium'))return'Chrome';if(ua.includes('safari/')&&!ua.includes('chrome/'))return'Safari';return'Other'}
function device(ua){ua=String(ua||'').toLowerCase();if(/ipad|tablet/.test(ua))return'Tablet';if(/mobile|iphone|android/.test(ua))return'Mobile';return'Desktop'}
module.exports=async function handler(req,res){
 const config=getConfig();if(!config)return sendJson(res,503,{error:'Visitor analytics storage is not configured.'});
 if(req.method==='POST'){
  const origin=req.headers.origin;
  let originAllowed=false;
  try {
   const requestHost=String(req.headers['x-forwarded-host']||req.headers.host||'').split(',')[0].trim().toLowerCase().split(':')[0].replace(/^www\\./,'');
   const originUrl=new URL(origin||'');
   const originHost=originUrl.hostname.toLowerCase().replace(/^www\\./,'');
   originAllowed=!!requestHost&&originHost===requestHost&&(originUrl.protocol==='https:'||originUrl.hostname==='localhost'||originUrl.hostname==='127.0.0.1');
  } catch (_) {}
  if(!originAllowed)return sendJson(res,403,{error:'Request origin could not be verified.'});
  try{
   const body=await readJson(req,2048),eventId=String(body.eventId||''),sessionId=String(body.sessionId||'');
   if(!/^[0-9a-f-]{36}$/i.test(eventId)||!/^[0-9a-f-]{36}$/i.test(sessionId))return sendJson(res,400,{error:'Invalid analytics event.'});
   const rawPage=typeof body.page==='string'?body.page:'/',page=rawPage.startsWith('/')?rawPage.split('?')[0].slice(0,180):'/';
   let referrer='';try{if(typeof body.referrer==='string'&&body.referrer){const u=new URL(body.referrer);if(u.protocol==='https:'||u.protocol==='http:')referrer=u.hostname.slice(0,120)}}catch(_){}
   if(!await rateLimit(config,req,'visitor',80,3600))return sendJson(res,429,{error:'Analytics rate limit reached.'});
   const ua=String(req.headers['user-agent']||'').slice(0,500),campaign=body.campaign&&typeof body.campaign==='object'?body.campaign:{},allowed=['utm_source','utm_medium','utm_campaign','utm_term','utm_content'],cleanCampaign={};for(const key of allowed)if(typeof campaign[key]==='string')cleanCampaign[key]=campaign[key].slice(0,120);const engagement=body.engagement&&typeof body.engagement==='object'?body.engagement:{};const record=const record={id:eventId,sessionId,visitorId:/^[a-z0-9._-]{8,80}$/i.test(String(body.vid||''))?String(body.vid):null,page,referrer,...
   await command(config,['EVAL',SAVE_SCRIPT,2,DATA_KEY,INDEX_KEY,eventId,JSON.stringify(record),String(Date.now())]);
   return sendJson(res,202,{ok:true});
  }catch(e){return sendJson(res,503,{error:'Visitor analytics could not be saved.'})}
 }
 if(req.method==='GET'){
  if(!verifySession(req,config.authSecret))return sendJson(res,401,{error:'Please sign in again.'});
  
  const n=Math.max(1,Math.min(1000,Number.parseInt(req.query&&req.query.limit,10)||500));
  try{
    const result=await command(config,['EVAL',LIST_SCRIPT,2,INDEX_KEY,DATA_KEY,String(n)]);
    if(!Array.isArray(result))throw Error('Invalid visitor response');
    const items=(result[3]||[]).map(x=>{try{return JSON.parse(x)}catch(_){return null}}).filter(Boolean);
    const vids=[...new Set(items.map(i=>i.visitorId).filter(Boolean))];
    let identities={};
    if(vids.length){
      const rows=await redis(config,[['HMGET',DATA_KEY.replace('visitors','visitors'),...vids]]);
    }
  catch(e){return sendJson(res,503,{error:'Unable to load visitor analytics. Check the database connection.'})}
 }
 res.setHeader('Allow','GET, POST');return sendJson(res,405,{error:'Method not allowed.'});
};




/* Identified visitors panel  for the no cookies banner captured*/
(function () {
  var box = document.getElementById('admin-visitor-list');
  var panel = document.getElementById('admin-visitors');
  if (!box || !panel) return;

  function esc(v) { return String(v == null ? '' : v).replace(/[&<>"']/g, function (c) { return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c] }) }
  function when(v) { var d = new Date(v); return Number.isNaN(d.getTime()) ? '' : new Intl.DateTimeFormat('en-IN', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' }).format(d) }

  async function load() {
    if (document.getElementById('admin-dashboard').hidden) { panel.hidden = true; return }
    panel.hidden = false;
    try {
      var r = await fetch('/api/identity', { credentials: 'same-origin', cache: 'no-store' });
      if (!r.ok) return;
      var b = await r.json(), items = Array.isArray(b.items) ? b.items : [];
      if (!items.length) { box.innerHTML = '<div class="admin-enquiry-empty">No identified visitors yet.</div>'; return }
      box.innerHTML = items.map(function (x) {
        var f = x.fields || {};
        var tone = x.score >= 60 ? 'hot' : x.score >= 30 ? 'warm' : 'cold';
        var loc = [x.city, x.country].filter(Boolean).join(', ');
        var vals = Object.keys(f).map(function (k) { return '<span class="admin-field"><b>' + esc(k) + '</b> ' + esc(f[k]) + '</span>' }).join('');
        var wa = f.phone ? '<a class="admin-enquiry-wa" href="https://wa.me/91' + esc(String(f.phone).replace(/\D/g, '')) + '" target="_blank" rel="noopener">WhatsApp</a>' : '';
        return '<article class="admin-enquiry-card"><div class="admin-enquiry-main">' +
          '<h3 class="admin-enquiry-name">' + esc(x.org || 'Unknown organisation') + ' <span class="admin-score ' + tone + '">' + esc(x.score) + '</span></h3>' +
          '<div class="admin-enquiry-meta"><span>' + esc(loc || 'Unknown location') + '</span><span>' + esc(x.ptr || x.asn || '') + '</span>' +
          '<span>' + esc(x.lastPage) + '</span><span>' + esc(when(x.lastSeen)) + '</span></div>' +
          '<div class="admin-visitor-fields">' + (vals || '<span class="admin-field">no fields yet</span>') + '</div>' +
          '</div><div class="admin-enquiry-actions">' + wa + '</div></article>';
      }).join('');
    } catch (_) {}
  }
  load();
  setInterval(load, 30000);
})();
