const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080},deviceScaleFactor:1});
await p.goto('file://'+process.cwd()+'/meta_direccion.html');await p.waitForTimeout(1500);
await p.screenshot({path:'meta_check.png'});await p.pdf({path:'meta_ads_direccion.pdf',width:'1920px',height:'1080px',printBackground:true});await b.close()})();
