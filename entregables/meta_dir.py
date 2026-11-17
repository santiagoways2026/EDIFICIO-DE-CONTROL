G='#7AA606';GD='#506718';K='#2E2E2D';M='#6F6F6E';L='#D9DED0';BG='#FAFAF7'
meses=['Jun','Jul','Ago','Sep','Oct']
deals=[177,353,367,350,611]
cpd=[34,25,27,25,18]
cr30=[3.4,2.0,1.4,1.1,2.0]
def bars(vals,fmt,maxv,W=760,H=330,hl=4,goal=None,sub=None):
  bw=96;gap=(W-bw*5)/5;s=f'<svg width="{W}" height="{H+90}" viewBox="0 0 {W} {H+90}" xmlns="http://www.w3.org/2000/svg" font-family="Montserrat">'
  base=H
  s+=f'<line x1="0" y1="{base}" x2="{W}" y2="{base}" stroke="{L}" stroke-width="2"/>'
  if goal:
    y=base-goal/maxv*(H-50)
    s+=f'<line x1="0" y1="{y:.0f}" x2="{W}" y2="{y:.0f}" stroke="{K}" stroke-width="2" stroke-dasharray="8 8"/>'
  for i,v in enumerate(vals):
    x=gap/2+i*(bw+gap);h=v/maxv*(H-50);c=G if i==hl else '#C9D3B4'
    s+=f'<path d="M{x},{base} V{base-h+6} q0,-6 6,-6 h{bw-12} q6,0 6,6 V{base} Z" fill="{c}"/>'
    s+=f'<text x="{x+bw/2}" y="{base-h-14}" text-anchor="middle" font-size="{30 if i==hl else 26}" font-weight="{800 if i==hl else 600}" fill="{K if i==hl else M}">{fmt(v)}</text>'
    s+=f'<text x="{x+bw/2}" y="{base+38}" text-anchor="middle" font-size="24" font-weight="{700 if i==hl else 500}" fill="{K}">{meses[i]}</text>'
    if sub: s+=f'<text x="{x+bw/2}" y="{base+74}" text-anchor="middle" font-size="22" fill="{GD if i==hl else M}" font-weight="{700 if i==hl else 500}">{sub[i]}</text>'
  return s+'</svg>'
c1=bars(deals,lambda v:f'{v}',650,sub=[f'{x} €/deal' for x in cpd])
c2=bars(cr30,lambda v:(f'{v:.1f} %').replace('.',','),3.8,goal=2.0)
def tile(lbl,val,cmp,good=True):
  return f'''<div class="t"><p class="tl">{lbl}</p><p class="tv">{val}</p><p class="tc" style="color:{GD if good else M}">{cmp}</p></div>'''
html=f'''<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>@page{{size:1920px 1080px;margin:0}}*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1920px;height:1080px;background:#fff;font-family:Montserrat,Arial,sans-serif;color:{K};padding:72px 96px;position:relative;overflow:hidden}}
h1{{font-size:54px;font-weight:800;line-height:1.1}} .hl{{display:inline-block;background:{G};color:#fff;padding:0 18px;transform:rotate(-1.2deg);margin-top:8px}}
.kp{{display:grid;grid-template-columns:repeat(5,1fr);gap:24px;margin-top:40px}}
.t{{background:{BG};border-top:8px solid {G};padding:22px 26px;border-radius:0 0 16px 16px}}
.tl{{font-size:22px;font-weight:600;color:{M}}} .tv{{font-size:52px;font-weight:800;margin:6px 0}} .tc{{font-size:21px;font-weight:600;line-height:1.3}}
.ch{{display:grid;grid-template-columns:1fr 1fr;gap:72px;margin-top:40px}} .ct{{font-size:28px;font-weight:700;margin-bottom:14px}} .cs{{font-size:20px;color:{M};font-weight:500}}
.ft{{position:absolute;left:96px;right:96px;bottom:28px;font-size:19px;line-height:1.4;color:{M}}}
.pr{{position:absolute;right:96px;top:72px;background:{K};color:#fff;border-radius:16px;padding:20px 26px;width:470px}}
.pr b{{color:#C6E07A}} .pr p{{font-size:21px;line-height:1.4}}</style></head><body>
<h1>Meta Ads: más deals, más baratos</h1><h1><span class="hl">y convirtiendo mejor</span></h1>
<div class="pr"><p><b>Proyección de octubre</b><br>CR final <b>2,6 a 3 %</b> (objetivo 2 %)<br>Coste por venta <b>sigue bajando</b><br>Se confirma a mediados de diciembre</p></div>
<div class="kp">
{tile('Inversión octubre','11,0 k€','+20 % frente a 9,1 k€ de media',False)}
{tile('Deals en CRM','611','+71 % frente a 357 de media')}
{tile('CPL (coste por deal)','18 €','−30 % frente a 25,6 €')}
{tile('CR a 30 días','2,0 %','frente a 1,5 % en jul-sep')}
{tile('Coste por venta','−40 %','jun-sep frente a ene-mar')}
</div>
<div class="ch"><div><p class="ct">Deals de Meta en el CRM por mes de creación</p>{c1}</div>
<div><p class="ct">Conversión a venta a 30 días <span class="cs">(misma edad para todos los meses; línea: objetivo 2 %)</span></p>{c2}</div></div>
<div class="ft"><span><b style="color:#506718">UTMs revisadas en todo el histórico: el crecimiento es real y viene de las audiencias píxel (69 → 386 deals). Por medir: cuánto es incremental.</b><br>Antes del recorte (ene-mar): 40 k€ al mes y CR de 1,4 a 2,5 %; en abril se dejó solo remarketing. 11 ventas en octubre: una venta mueve el CR unas 3 décimas.<br>Fuente: Zoho CRM (deals con utm_source meta, a 16/11/2026) y Meta Ads por Windsor (gasto a 14/11/2026). Noviembre en curso, fuera del gráfico.</span></div>
</body></html>'''
open('meta_direccion.html','w').write(html)
