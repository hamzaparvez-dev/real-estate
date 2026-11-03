'use strict';
const {sendJson,getConfig,readJson,sameOrigin,rateLimit,verifySession,redis}=require('../lib/enquiry-auth');
const KEY='prestige:enquiries',CONFIGS=new Set(['1BHK','2BHK','3BHK','4BHK','5BHK','Commercial']);
module.exports=async function(req,res){
 const c=getConfig();if(!c)return sendJson(res,503,{error:'Enquiry storage is not configured yet.'});
 if(req.method==='POST'){
  if(!sameOrigin(req))return sendJson(res,403,{error:'Request origin could not be verified.'});
  try{
   const b=await readJson(req,8192);if(typeof b.website==='string'&&b.website.trim())return sendJson(res,200,{ok:true});
   const name=typeof b.name==='string'?b.name.trim().slice(0,100):'',phone=typeof b.phone==='string'?b.phone.replace(/\D/g,''):'';
   const configuration=typeof b.configuration==='string'?b.configuration:'',purpose=typeof b.purpose==='string'?b.purpose.trim().slice(0,80):'';
   const intent=b.intent==='site-visit'?'site-visit':'property',message=typeof b.message==='string'?b.message.trim().slice(0,1000):'';
   const raw=typeof b.source==='string'?b.source:'/',source=raw.startsWith('/')?raw.split('?')[0].slice(0,160):'/';
   if(name.length<2)return sendJson(res,400,{error:'Please enter your full name.'});
   if(!/^[6-9][0-9]{9}$/.test(phone))return sendJson(res,400,{error:'Please enter a valid 10-digit Indian mobile number.'});
   if(!CONFIGS.has(configuration))return sendJson(res,400,{error:'Please select a valid configuration.'});
   if(purpose&&!['Self Use / End-Use','Investment / Rental','First Home','Upgrade'].includes(purpose))return sendJson(res,400,{error:'Please select a valid purpose.'});
   if(!await rateLimit(c,req,'enquiry',10,3600))return sendJson(res,429,{error:'Too many enquiries from this connection. Please contact us on WhatsApp or try again later.'});
   const record={id:require('node:crypto').randomUUID(),name,phone,configuration,purpose,intent,message,source,submittedAt:new Date().toISOString()};
   const result=await redis(c,[['LPUSH',KEY,JSON.stringify(record)],['LTRIM',KEY,0,4999]],'/multi-exec');
   if(!Array.isArray(result)||result[0]!=='OK')throw new Error('Storage write failed');
   return sendJson(res,201,{ok:true,id:record.id});
  }catch(e){const big=e&&e.message==='Request too large';return sendJson(res,big?413:503,{error:big?'Request too large':'We could not save your enquiry just now. Please try again or contact us on WhatsApp.'});}
 }
 if(req.method==='GET'){
  if(!verifySession(req,c.authSecret))return sendJson(res,401,{error:'Please sign in again.'});
  const offset=Math.max(0,Math.min(4999,Number.parseInt(req.query&&req.query.offset,10)||0));
  const limit=Math.max(1,Math.min(50,Number.parseInt(req.query&&req.query.limit,10)||25));
  try{const [total,rows]=await redis(c,[['LLEN',KEY],['LRANGE',KEY,offset,offset+limit-1]]);
   const items=(Array.isArray(rows)?rows:[]).map(x=>{try{return JSON.parse(x);}catch{return null;}}).filter(Boolean);
   return sendJson(res,200,{total:Number(total||0),items});
  }catch{return sendJson(res,503,{error:'Unable to load enquiries. Check the storage configuration.'});}
 }
 res.setHeader('Allow','GET, POST');return sendJson(res,405,{error:'Method not allowed.'});
};
