#!/usr/bin/env python3
"""Miniaturas de YouTube según el Brandbook 2027: foto a sangre, caja blanca con sombra,
antetítulo en mayúsculas verde sendero, titular grafito en minúscula de frase (Montserrat 800)
y subrayado SW (bloque verde Ways girado -1,5°, letra blanca). Isotipo blanco arriba a la derecha."""
import json, sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS=S+'/fonts'; DRIVE=S+'/artifact-files/434c68bd-0b8e-40f9-922d-4c8bf145faac/drive'
ISO=S+'/artifact-files/434c68bd-0b8e-40f9-922d-4c8bf145faac/img/isotipo_blanco.png'
W,H=1280,720; WAYS=(122,166,6); SENDERO=(80,103,24); GRAFITO=(46,46,45)
def font(p,px): return ImageFont.truetype(f'{FONTS}/Montserrat-{p}.ttf',px)
def cover(path,cx,cy,w=W,h=H):
    im=Image.open(path).convert('RGB'); r=max(w/im.width,h/im.height)
    im=im.resize((round(im.width*r),round(im.height*r)),Image.LANCZOS)
    x=int((im.width-w)*cx); y=int((im.height-h)*cy); return im.crop((x,y,x+w,y+h))
def parse(t):
    out=[]
    for ln in t.split('\n'):
        segs=[];buf='';hi=False
        for ch in ln:
            if ch=='[': segs.append((buf,hi));buf='';hi=True
            elif ch==']': segs.append((buf,hi));buf='';hi=False
            else: buf+=ch
        segs.append((buf,hi)); out.append([s for s in segs if s[0]])
    return out
def render(spec,out):
    img=cover(f"{DRIVE}/{spec['foto']}.jpg",spec.get('cx',.5),spec.get('cy',.5)).convert('RGBA')
    # overlay suave desde el lado de la caja
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
    lado=spec.get('lado','izq')
    for x in range(W):
        k=(1-x/W) if lado=='izq' else x/W
        d.line([(x,0),(x,H)],fill=(10,14,8,int(90*max(0,k-0.2))))
    img.alpha_composite(ov)
    # caja blanca
    fs=spec.get('fs',62); ft=font('800',fs); fa=font('700',24); lh=int(fs*1.1)
    lineas=parse(spec['titulo']); d0=ImageDraw.Draw(img)
    anchos=[sum(d0.textlength(t,font=ft) for t,_ in ln)+sum(24 for _,h in ln if h) for ln in lineas]
    pad=44; bw=int(max(max(anchos),d0.textlength(spec['ante'],font=fa)*1.15)+2*pad); bh=2*pad+40+lh*len(lineas)
    bw=min(bw,W-120)
    bx=56 if lado=='izq' else W-56-bw; by=spec.get('by',H-56-bh)
    sh=Image.new('RGBA',(W,H),(0,0,0,0)); ds=ImageDraw.Draw(sh); ds.rectangle([bx,by+8,bx+bw,by+bh+8],fill=(46,46,45,70)); sh=sh.filter(ImageFilter.GaussianBlur(18)); img.alpha_composite(sh)
    d=ImageDraw.Draw(img); d.rectangle([bx,by,bx+bw,by+bh],fill=(255,255,255,255))
    # antetítulo con tracking
    x=bx+pad; y=by+pad-4
    for ch in spec['ante']:
        d.text((x,y),ch,font=fa,fill=SENDERO+(255,)); x+=d.textlength(ch,font=fa)+3.6
    y=by+pad+40
    for ln in lineas:
        x=bx+pad
        for t,hi in ln:
            w=d.textlength(t,font=ft)
            if hi:
                # bloque verde Ways girado -1,5°, letra blanca
                bl=Image.new('RGBA',(int(w)+20,lh+8),(0,0,0,0)); db=ImageDraw.Draw(bl); db.rectangle([0,6,int(w)+19,lh+1],fill=WAYS+(255,))
                db.text((10,-int(fs*0.06)),t,font=ft,fill=(255,255,255,255))
                bl=bl.rotate(1.5,resample=Image.BICUBIC,expand=True)
                img.alpha_composite(bl,(int(x)-10,y-4)); d=ImageDraw.Draw(img); x+=w+20
            else:
                d.text((x,y),t,font=ft,fill=GRAFITO+(255,)); x+=w
        y+=lh
    # isotipo blanco arriba a la derecha (o izquierda si la caja va a la derecha)
    iso=Image.open(ISO).convert('RGBA'); iso=iso.resize((84,int(84*iso.height/iso.width)))
    ix=W-56-84 if lado=='izq' else 56
    img.alpha_composite(iso,(ix,48))
    img.convert('RGB').save(out,quality=90)
if __name__=='__main__':
    specs=json.load(open(sys.argv[1]))
    for sp in specs: render(sp,f"{S}/yt_new/{sp['out']}.jpg"); print(sp['out'])
