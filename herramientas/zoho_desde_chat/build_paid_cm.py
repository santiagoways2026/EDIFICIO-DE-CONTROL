import json,collections
L=lambda f:(lambda d:d.get('data',d))(json.load(open(f)))
G=json.load(open('../gads/gads_camp_10.json')); M=L('meta_report/actual.json'); I=L('captacion_inversion/actual.json')
C=json.load(open('/home/user/EDIFICIO-DE-CONTROL/herramientas/zoho_desde_chat/out/captacion_canales/actual.json'))
r2=lambda x:round(x,2)
# ---- Google
gs=[]
for f in G['filas']:
  m={}
  for ym in sorted(set(list(f['m'].keys())+list(f.get('crm',{}).keys()))):
    p=f['m'].get(ym,[0,0,0,0,0]); c=f.get('crm',{}).get(ym,[0,0,0])
    m[ym]=[r2(p[2]),round(p[3],1),c[0],c[1],round(c[2])]
  gs.append({'id':f['camps'][0],'n':f['c'],'t':f.get('tipo',''),'e':f.get('estado',''),'m':m})
gs.append({'id':'sin_campana','n':'Sin campaña identificable (sitelinks y otros)','t':'Otros','e':'','m':{ym:[0,0,c[0],c[1],round(c[2])] for ym,c in G['sin_campana'].items()}})
# ---- Meta total
cost={str(r[1]):r[2] for r in I['filas'] if r[0]=='PAID|META|META'}
import collections as _C
_fb=_C.Counter()
for r in json.load(open('../ov10/raw.json'))['facebook']:_fb[r['date'][:7].replace('-','')]+=r['spend']
cost.update({k:round(v,2) for k,v in _fb.items()})
imp={str(r[1]):r[3] for r in I['filas'] if r[0]=='PAID|META|META'}
SRC={'meta','fb','ig','fb-sitelink','facebook'}
dl=collections.Counter();wn=collections.Counter()
for r in C['filas']:
  if str(r[0]).lower() in SRC and 'org' not in str(r[1]).lower():
    dl[str(r[2])]+=r[3];wn[str(r[2])]+=r[4]
leads=collections.Counter()
mk=collections.defaultdict(lambda:collections.defaultdict(lambda:[0,0,0,0,0]))
NOM={'esp':'España','latam':'Latam','arg':'Argentina','mex':'México','uk':'Reino Unido','usa':'EE. UU.','de':'Alemania','it':'Italia','br':'Brasil y Portugal','sin':'Sin mercado'}
PMK={'ES':'esp','EN':'uk','DE':'de'}
for k,v in M['datos'].items():
  if k.startswith('p:'):
    mkk=None
    nm=k[2:]
    if 'Latam' in nm: mkk='latam'
    elif 'Spain' in nm: mkk='esp'
    elif 'United States' in nm: mkk='usa'
    elif 'German' in nm: mkk='de'
    elif 'Ireland' in nm or 'United Kingdom' in nm or 'English' in nm or 'Others' in nm: mkk='uk'
    else: mkk='sin'
  else: mkk=k.split('|')[0]
  for ym,a in v.get('m',{}).items():
    leads[ym]+=a[3]; x=mk[mkk][ym]; x[0]+=a[2]; x[1]+=a[3]
  for ym,n in v.get('d',{}).items():
    if ym>='202609': mk[mkk][ym][2]+=n
  for ym,w in v.get('w',{}).items():
    if ym>='202609': mk[mkk][ym][3]+=sum(w.values())
meses=sorted(set(cost)|set(dl))
mt={ym:[r2(cost.get(ym,0)),leads.get(ym,0),dl.get(ym,0),wn.get(ym,0),round(imp.get(ym,0))] for ym in meses if ym>='202501'}
ms=[{'id':k,'n':NOM.get(k,k),'m':{ym:[r2(a[0]),a[1],a[2],a[3],0] for ym,a in sorted(v.items())}} for k,v in mk.items()]
ms.sort(key=lambda s:-sum(a[0] for a in s['m'].values()))
doc={'fecha':'2026-11-10','cols':['coste','leads','deals','won','importe'],
 'google':{'segs':gs,'desde':'202506','crm_desde':'202506','fuente':'Google Ads por Windsor (coste y conversiones) y Zoho CRM (deals por utm_campaign y mes de creación). Octubre completo; noviembre al día 9.','leads_n':'Conversiones'},
 'meta':{'leads_desde':'202601','total':mt,'segs':ms,'desde':'202506','crm_desde':'202506','seg_crm_desde':'202609','fuente':'Meta Ads por Windsor (coste y leads del píxel, leads solo de 2026) y Zoho CRM (deals con utm_source meta, fb o ig de pago). Coste hasta el 9 de noviembre; leads y deals por mercado, desde septiembre de 2026 (antes la UTM no separaba campañas).','leads_n':'Leads Meta'},
 'nota':'Won = deals que hoy están ganados, por mes de creación: los dos últimos meses aún madurarán. CPL = coste / leads de la plataforma. Coste por deal = coste / deals del CRM. CPA = coste / ventas.'}
json.dump(doc,open('paid_cm.json','w'),ensure_ascii=False)
print(len(json.dumps(doc)))
for ym in ['202506','202509','202510','202601','202609','202610']: print(ym,mt.get(ym))
print({s['n']:sum(a[2] for a in s['m'].values()) for s in ms})
print('meta_report d sum sept',sum(v.get('d',{}).get('202609',0) for v in M['datos'].values()), 'canales', dl['202609'])
