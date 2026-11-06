import json,collections
r2=lambda v:round(v+1e-9,2)
B=json.load(open('bing/raw.json'))
CAN=json.load(open('oai/db_canales_06.json'));CAN=CAN.get('data',CAN)['filas']
WON=json.load(open('oai/won_amount_utm_06.json'))
DL=json.load(open('mk/deals.json'))
LANG={'Spanish':'ES','English':'EN','German':'DE','Italian':'IT','Portuguese':'PT'}
CMK={'ES_SEARCH_BING':'ES','EN_SEARCH_BING':'EN','EN_OTHERSLANGUAGE_SEARCH_BING':'EN','EN_OTHERSLANGUAGE_SEARCH_BING-Experiment puja':'EN','DE_SEARCH_BING':'DE','IT_SEARCH_BING':'IT','PT_SEARCH':'PT'}
CNOM={'ES_SEARCH_BING':'Búsqueda España','EN_SEARCH_BING':'Búsqueda inglés (EE. UU., Reino Unido...)','EN_OTHERSLANGUAGE_SEARCH_BING':'Búsqueda inglés, otros idiomas','DE_SEARCH_BING':'Búsqueda Alemania','IT_SEARCH_BING':'Búsqueda Italia','PT_SEARCH':'Búsqueda Portugal y Brasil','EN_OTHERSLANGUAGE_SEARCH_BING-Experiment puja':'Experimento de puja (borrado)'}
ym=lambda s:int(s.split('|')[0])*100+int(s.split('|')[1])
# mensual Bing
M=collections.defaultdict(lambda:[0,0,0,0.0])
MC=collections.defaultdict(lambda:collections.defaultdict(lambda:[0,0,0,0.0]))
for r in B['mensual']:
    k=ym(r['year_month']);m=M[k];m[0]+=r['spend'];m[1]+=r['impressions'];m[2]+=r['clicks'];m[3]+=r['conversions_qualified'] or 0
    c=MC[r['campaign']][k];c[0]+=r['spend'];c[1]+=r['impressions'];c[2]+=r['clicks'];c[3]+=r['conversions_qualified'] or 0
# Zoho bing por mes
ZD=collections.Counter();ZW=collections.Counter();ZI=collections.Counter()
for s,m,y,n,won,w0,cl in CAN:
    if (s or '').lower()=='bing':ZD[y]+=n;ZW[y]+=won
for s,m,y,n,amt in WON:
    if (s or '').lower()=='bing':ZI[y]+=amt or 0
mensual=[[k,r2(M[k][0]),M[k][1],M[k][2],round(M[k][3],1),ZD.get(k,0),ZW.get(k,0),round(ZI.get(k,0))] for k in sorted(M)]
# mercado (Zoho Language) 2026
MD=collections.Counter()
for l,s,med,mes,n in DL:
    if (s or '').lower()=='bing' and l in LANG and mes>='2026-01':MD[LANG[l]]+=n
MW=collections.Counter()
for L in ['ES','EN','DE','IT','PT']:
    for s,med,c,cl,n in json.load(open(f'mk/won_{L}.json')):
        if (s or '').lower()=='bing' and c>='2026-01':MW[L]+=n
# campañas 2026 y ultimos meses
camp=[]
for c,d in MC.items():
    y26=[d[k] for k in d if k>=202601]
    if not y26:continue
    g=sum(x[0] for x in y26);i=sum(x[1] for x in y26);cl=sum(x[2] for x in y26);cv=sum(x[3] for x in y26)
    s,o=d.get(202609,[0]*4),d.get(202610,[0]*4)
    camp.append({"clave":c,"nombre":CNOM.get(c,c),"mercado":CMK.get(c),"gasto":r2(g),"impr":i,"clics":cl,"conv":round(cv,1),"sep":r2(s[0]),"oct":r2(o[0]),"conv_sep":round(s[3],1),"conv_oct":round(o[3],1)})
camp.sort(key=lambda x:-x['gasto'])
# mercado: gasto 2026 + deals + ventas
mk=collections.defaultdict(lambda:[0,0,0])
for c in camp:mk[c['mercado']][0]+=c['gasto'];mk[c['mercado']][1]+=c['clics']
mercados=[[k,r2(mk[k][0]),int(MD.get(k,0)),int(MW.get(k,0)),r2(mk[k][0]/MD[k]) if MD.get(k) else None,round(mk[k][0]/MW[k]) if MW.get(k) else None] for k in ['ES','EN','DE','IT','PT']]
# diario por mercado
D=collections.OrderedDict()
for r in sorted(B['daily'],key=lambda r:r['date']):
    d=D.setdefault(r['date'],[r['date'],0,0,0,0,0,0]);k=CMK.get(r['campaign'],'EN')
    i={'ES':1,'EN':2,'DE':3}.get(k,4);d[i]+=r['spend'] or 0;d[5]+=r['clicks'] or 0;d[6]+=r['conversions_qualified'] or 0
diario=[[d[0],r2(d[1]),r2(d[2]),r2(d[3]),r2(d[4]),d[5],round(d[6],1)] for d in D.values() if d[0]>='2026-09-01']
# dispositivos
dv=collections.defaultdict(lambda:[0,0,0])
for r in B['device']:
    v=dv[r['device']];v[0]+=r['spend'];v[1]+=r['clicks'];v[2]+=r['conversions_qualified']
dispositivos=[[{'Computer':'Ordenador','Smartphone':'Móvil','Tablet':'Tableta'}[k],r2(v[0]),v[1],round(v[2],1)] for k,v in sorted(dv.items(),key=lambda x:-x[1][0])]
busq=sorted([[q['search_query'],CNOM.get(q['campaign'],q['campaign']),q['clicks'],r2(q['spend']),round(q['conversions_qualified'],1)] for q in B['queries']],key=lambda x:-x[2])
json.dump({"mensual":mensual,"campanas":camp,"mercados":mercados,"diario":diario,"dispositivos":dispositivos,"busquedas":busq},open('bing/calc.json','w'),ensure_ascii=False)
for x in mensual:print(x)
for c in camp:print(c)
print(mercados);print(dispositivos)
