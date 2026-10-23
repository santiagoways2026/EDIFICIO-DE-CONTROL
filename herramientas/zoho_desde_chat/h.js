// Ejecuta una función actualizarX() de la página con un MCP y una base de datos simulados
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const fn=process.argv[2];const DIR=__dirname;
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage();
const logs=[];p.on('pageerror',e=>logs.push('ERR '+e.message));
const docs={};for(const c of fs.readdirSync(DIR+'/docs'))for(const f of fs.readdirSync(DIR+'/docs/'+c))docs[c+'/'+f.replace(/\.json$/,'')]=JSON.parse(fs.readFileSync(DIR+'/docs/'+c+'/'+f));
const cache=JSON.parse(fs.readFileSync(DIR+'/cache.json'));
await p.addInitScript(([docs,cache])=>{
 const snap=pth=>({exists:pth in docs,data:()=>docs[pth],metadata:{},id:pth.split('/').pop()});
 window.__writes={};window.__need=[];
 const chain={limit:()=>chain,orderBy:()=>chain,where:()=>chain,onSnapshot:cb=>{setTimeout(()=>cb({docs:[]}),10);return()=>{}},get:async()=>({docs:[]})};
 const db={collection:()=>chain,doc:pth=>({onSnapshot:(cb)=>{setTimeout(()=>cb(snap(pth)),10);return()=>{}},get:async()=>snap(pth),set:async d=>{window.__writes[pth]=JSON.parse(JSON.stringify(d))},update:async d=>{window.__writes[pth]={__update:true,...JSON.parse(JSON.stringify(d))}},delete:async()=>{}})};
 const st=o=>o&&typeof o==='object'?(Array.isArray(o)?'['+o.map(st).join(',')+']':'{'+Object.keys(o).sort().map(k=>JSON.stringify(k)+':'+st(o[k])).join(',')+'}'):JSON.stringify(o);
 window.__fake={callTool:async(srv,tool,args)=>{const nz=o=>{const c=JSON.parse(JSON.stringify(o));if(c?.query_params?.CONFIG&&typeof c.query_params.CONFIG==='string'){try{c.query_params.CONFIG=JSON.parse(c.query_params.CONFIG)}catch(_){}}return c};const k=tool+'|'+st(nz(args));if(k in cache){window.__i=window.__i||{};const i=window.__i[k]=(window.__i[k]??-1)+1;const L=cache[k];const t=L[Math.min(i,L.length-1)];return{payload:t,content:[{type:'text',text:t}]}}
   if(!window.__need.some(x=>x.k===k))window.__need.push({k,tool,args});throw{code:'pendiente',message:'pendiente: '+tool}}};
 window.claude={use:async n=>n==='db'?db:null};
},[docs,cache]);
await p.goto('file://'+path.resolve('/home/user/EDIFICIO-DE-CONTROL/salas/index.html'));await p.waitForTimeout(2500);
const r=await p.evaluate(async fn=>{refD.hecho=true;mc.mcp=window.__fake;const t0=Date.now();try{await window[fn]()}catch(e){return{err:String(e?.message||e)}}
  const msgs={};for(const k of Object.keys(st))if(/Act$/.test(k)&&st[k]?.msg)msgs[k]=st[k].msg;return{ms:Date.now()-t0,msgs,need:window.__need,writes:Object.keys(window.__writes)}},fn);
console.log(JSON.stringify({fn,...r,logs:logs.slice(0,5)},null,1).slice(0,6000));
const w=await p.evaluate(()=>window.__writes);fs.mkdirSync(DIR+'/out',{recursive:true});
for(const[k,v]of Object.entries(w)){fs.mkdirSync(path.dirname(DIR+'/out/'+k),{recursive:true});fs.writeFileSync(DIR+'/out/'+k+'.json',JSON.stringify(v))}
fs.writeFileSync(DIR+'/need_'+fn+'.json',JSON.stringify(r.need||[]));await b.close()})();
