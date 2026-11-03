'use strict';
const {sendJson,getConfig,readJson,sameOrigin,rateLimit,verifySession,setCookie,verifyPassword,command,clientHash}=require('../lib/enquiry-auth');
module.exports=async function(req,res){
 const c=getConfig();if(!c)return sendJson(res,503,{error:'Dashboard setup is incomplete.'});
 if(req.method==='GET')return sendJson(res,200,{authenticated:verifySession(req,c.authSecret)});
 if(req.method==='DELETE'){res.setHeader('Set-Cookie','pe_admin=; Path=/; HttpOnly; SameSite=Strict; Max-Age=0; Secure');return sendJson(res,200,{ok:true});}
 if(req.method!=='POST'){res.setHeader('Allow','GET, POST, DELETE');return sendJson(res,405,{error:'Method not allowed.'});}
 if(!sameOrigin(req))return sendJson(res,403,{error:'Request origin could not be verified.'});
 try{
  if(!await rateLimit(c,req,'login',5,900))return sendJson(res,429,{error:'Too many sign-in attempts. Try again in 15 minutes.'});
  const body=await readJson(req,2048),password=typeof body.password==='string'?body.password:'';
  if(password.length>256||!verifyPassword(password,c.passwordHash))return sendJson(res,401,{error:'Incorrect password.'});
  await command(c,['DEL','prestige:rate:login:'+clientHash(req,c.authSecret)]);
  res.setHeader('Set-Cookie',setCookie(req,c.authSecret));return sendJson(res,200,{ok:true});
 }catch(e){const tooLarge=e&&e.message==='Request too large';return sendJson(res,tooLarge?413:503,{error:tooLarge?'Request too large':'Sign-in service is temporarily unavailable.'});}
};
