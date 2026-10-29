#!/usr/bin/env python3
"""Montaje de reels 9:16 estilo Santiago Ways: clips recortados, texto que se escribe,
antetítulo en caja verde, palabra resaltada y cierre verde oficial.
Uso: python3 -I reel.py spec.json  (rutas dentro del spec)"""
import json, os, sys, subprocess, shutil, math
from PIL import Image, ImageDraw, ImageFont

S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = S + '/fonts'
ISO = S + '/artifact-files/434c68bd-0b8e-40f9-922d-4c8bf145faac/img/isotipo_blanco.png'
W, H, FPS = 1080, 1920, 30
VERDE = (122, 166, 6); OSCURO = (46, 46, 45); VERDE2 = (80, 103, 24)
CPS = 25            # caracteres por segundo
RETARDO = 0.15      # s antes de empezar a escribir
CIERRE = 4.0        # s de cierre

def font(peso, px):
    return ImageFont.truetype(f'{FONTS}/Montserrat-{peso}.ttf', px)

def parse(texto):
    """'Hola [mundo]\\nadiós' -> lineas de [(txt, resaltado)]"""
    lineas = []
    for ln in texto.split('\n'):
        segs = []; buf = ''; hi = False
        for ch in ln:
            if ch == '[': segs.append((buf, hi)); buf = ''; hi = True
            elif ch == ']': segs.append((buf, hi)); buf = ''; hi = False
            else: buf += ch
        segs.append((buf, hi))
        lineas.append([s for s in segs if s[0]])
    return lineas

def nchars(lineas):
    return sum(len(s[0]) for ln in lineas for s in ln)

def revelar(lineas, n):
    out = []
    for ln in lineas:
        l2 = []
        for txt, hi in ln:
            if n <= 0: break
            k = min(len(txt), n); l2.append((txt[:k], hi)); n -= k
        out.append(l2)
    return out

def sombra(img):
    d = ImageDraw.Draw(img)
    y0 = 1050
    for y in range(y0, H):
        a = int(150 * ((y - y0) / (H - y0)) ** 1.3)
        d.line([(0, y), (W, y)], fill=(0, 0, 0, a))

def frame_texto(lineas, ante, n, fs=78):
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sombra(img)
    d = ImageDraw.Draw(img)
    f = font('800', fs); lh = int(fs * 1.28)
    # ancho máximo: si una línea no cabe, reducimos fuente
    while fs > 56:
        f = font('800', fs); lh = int(fs * 1.28)
        anchos = [sum(d.textlength(t, font=f) for t, _ in ln) + 20 * sum(1 for _, h in ln if h) for ln in lineas]
        if max(anchos) <= W - 170: break
        fs -= 4
    vis = revelar(lineas, n)
    x0 = 90; yb = 1660
    ytop = yb - lh * len(lineas)
    for i, ln in enumerate(vis):
        x = x0; y = ytop + i * lh
        for txt, hi in ln:
            w = d.textlength(txt, font=f)
            if hi:
                # subrayado SW del brandbook: bloque verde Ways recto, girado -1,5 grados
                bl = Image.new('RGBA', (int(w) + 24, lh + 8), (0, 0, 0, 0)); db = ImageDraw.Draw(bl)
                db.rectangle([0, 10, int(w) + 23, lh], fill=VERDE + (255,))
                db.text((12, 4), txt, font=f, fill=(255, 255, 255, 255))
                bl = bl.rotate(1.5, resample=Image.BICUBIC, expand=True)
                img.alpha_composite(bl, (int(x) - 12, y - 4)); d = ImageDraw.Draw(img); x += w + 24
            else:
                d.text((x, y), txt, font=f, fill=(255, 255, 255, 255)); x += w
    if ante:
        fa = font('700', 30)
        wa = d.textlength(ante, font=fa) + 2 * (len(ante) - 1)
        ya = ytop - 72; ha = 52
        d.rectangle([x0, ya, x0 + wa + 36, ya + ha], fill=VERDE + (255,))
        # tracking manual
        x = x0 + 18
        for ch in ante:
            d.text((x, ya + 10), ch, font=fa, fill=(255, 255, 255, 255)); x += d.textlength(ch, font=fa) + 2
    return img

def frame_cierre(t, titulo):
    """fondo verde con degradado y elementos con fundido"""
    img = Image.new('RGBA', (W, H), VERDE + (255,))
    px = img.load()
    for y in range(0, H, 4):
        for x in range(0, W, 4):
            k = (x / W * 0.45 + y / H * 0.55)
            c = tuple(int(VERDE[i] * (1 - k) + VERDE2[i] * k) for i in range(3))
            for dy in range(4):
                for dx in range(4):
                    px[x + dx, y + dy] = c + (255,)
    capa = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(capa)
    iso = Image.open(ISO).convert('RGBA'); iso = iso.resize((260, int(260 * iso.height / iso.width)))
    capa.alpha_composite(iso, (90, 330))
    d.text((90, 330 + iso.height + 30), 'Santiago Ways', font=font('500', 48), fill=(255, 255, 255, 255))
    lineas = parse(titulo); f = font('800', 92); lh = 118; y = 820
    for ln in lineas:
        x = 90
        for txt, hi in ln:
            w = d.textlength(txt, font=f)
            if hi:
                bl = Image.new('RGBA', (int(w) + 28, lh + 8), (0, 0, 0, 0)); db = ImageDraw.Draw(bl)
                db.rectangle([0, 12, int(w) + 27, lh + 2], fill=VERDE2 + (255,)); db.text((14, 4), txt, font=f, fill=(255, 255, 255, 255))
                bl = bl.rotate(1.5, resample=Image.BICUBIC, expand=True); capa.alpha_composite(bl, (int(x) - 14, y - 4)); d = ImageDraw.Draw(capa); x += w + 28
            else:
                d.text((x, y), txt, font=f, fill=(255, 255, 255, 255)); x += w
        y += lh
    d.text((90, 1740), 'santiagoways.com', font=font('700', 40), fill=(255, 255, 255, 255))
    a = min(1.0, t / 0.6)
    if a < 1:
        alpha = capa.split()[3].point(lambda v: int(v * a)); capa.putalpha(alpha)
    img.alpha_composite(capa)
    return img

def vf(clip_w, clip_h, cx):
    # escala para cubrir 1080x1920 y recorta centrado (cx 0..1 desplaza el recorte horizontal)
    return (f"scale=w='if(gte(iw/ih,{W}/{H}),-2,{W})':h='if(gte(iw/ih,{W}/{H}),{H},-2)',"
            f"crop={W}:{H}:'(iw-{W})*{cx}':'(ih-{H})/2',fps={FPS},setsar=1")

def probe(path):
    out = subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                                   'stream=width,height', '-of', 'csv=p=0', path]).decode().strip().split(',')
    has_a = subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'a:0', '-show_entries',
                                     'stream=codec_name', '-of', 'csv=p=0', path]).decode().strip() != ''
    return int(out[0]), int(out[1]), has_a

def run(cmd):
    subprocess.run(cmd, check=True)

def main(spec_path):
    spec = json.load(open(spec_path))
    out = f"{S}/reels/{spec['slug']}"; shutil.rmtree(out, ignore_errors=True); os.makedirs(out + '/txt'); os.makedirs(out + '/fin')
    shots = spec['planos']
    # 1) intermedios por plano
    inter = []
    for i, sh in enumerate(shots):
        src = f"{S}/clips/{sh['clip']}.mp4"; w, h, has_a = probe(src)
        dst = f'{out}/p{i}.mp4'
        a = (['-af', f"volume={spec.get('vol',0.4)},afade=t=in:d=0.3,afade=t=out:st={sh['dur']-0.3}:d=0.3,aformat=sample_rates=48000:channel_layouts=stereo"]
             if has_a else [])
        cmd = ['ffmpeg', '-v', 'error', '-y', '-ss', str(sh['ini']), '-i', src]
        if not has_a: cmd += ['-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo']
        cmd += ['-t', str(sh['dur']), '-vf', vf(w, h, sh.get('cx', 0.5)), '-c:v', 'libx264', '-preset', 'fast', '-crf', '16',
                '-pix_fmt', 'yuv420p'] + a + ['-c:a', 'aac', '-b:a', '160k', '-shortest', dst]
        run(cmd); inter.append(dst); print('plano', i, 'ok', flush=True)
    # 2) secuencia de texto (estados únicos + enlaces)
    cache = {}; n = 0; t0 = 0.0
    for i, sh in enumerate(shots):
        lineas = parse(sh['texto']); total = nchars(lineas); ante = spec['antetitulo'] if i == 0 else None
        nf = round(sh['dur'] * FPS)
        for k in range(nf):
            t = k / FPS; c = max(0, min(total, int((t - RETARDO) * CPS) + 1)) if t >= RETARDO else 0
            key = (i, c)
            if key not in cache:
                p = f'{out}/txt/s{i}_{c}.png'; frame_texto(lineas, ante, c).save(p); cache[key] = p
            os.symlink(cache[key], f'{out}/txt/f{n:05d}.png'); n += 1
        t0 += sh['dur']
    ncont = n
    # 3) cierre
    nfc = int(CIERRE * FPS); cc = {}
    for k in range(nfc):
        t = k / FPS; key = round(min(t, 0.6), 3)
        if key not in cc:
            p = f'{out}/fin/c{key}.png'; frame_cierre(t, spec.get('cierre', 'Tu Camino\n[te espera]')).convert('RGB').save(p); cc[key] = p
        os.symlink(cc[key], f'{out}/fin/f{k:05d}.png')
    # 4) montaje final
    inputs = []; fc = ''
    for i, p in enumerate(inter): inputs += ['-i', p]
    inputs += ['-framerate', str(FPS), '-i', f'{out}/txt/f%05d.png', '-framerate', str(FPS), '-i', f'{out}/fin/f%05d.png',
               '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo']
    k = len(inter)
    fc += ''.join(f'[{i}:v][{i}:a]' for i in range(k)) + f'concat=n={k}:v=1:a=1[cv][ca];'
    fc += f'[{k}:v]format=rgba[tx];[cv][tx]overlay=shortest=1:format=auto[cvt];'
    fc += f'[{k+1}:v]format=yuv420p,setsar=1[fv];[{k+2}:a]atrim=duration={CIERRE}[fa];'
    fc += '[cvt][ca][fv][fa]concat=n=2:v=1:a=1[v][a]'
    mp4 = f"{out}/{spec['slug']}.mp4"
    run(['ffmpeg', '-v', 'error', '-y'] + inputs + ['-filter_complex', fc, '-map', '[v]', '-map', '[a]',
         '-c:v', 'libx264', '-preset', 'medium', '-crf', '25', '-maxrate', '4.5M', '-bufsize', '9M', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
         '-c:a', 'aac', '-b:a', '128k', mp4])
    print('mp4 ok', flush=True)
    run(['ffmpeg', '-v', 'error', '-y', '-i', mp4, '-c:v', 'libvpx-vp9', '-crf', '38', '-b:v', '0', '-deadline', 'good',
         '-cpu-used', '4', '-row-mt', '1', '-c:a', 'libopus', '-b:a', '96k', f"{out}/{spec['slug']}.webm"])
    tp = max(0.5, shots[0]['dur'] - 0.3)
    run(['ffmpeg', '-v', 'error', '-y', '-ss', str(tp), '-i', mp4, '-frames:v', '1', '-q:v', '3', f"{out}/{spec['slug']}.jpg"])
    dur = sum(sh['dur'] for sh in shots) + CIERRE
    print('listo', spec['slug'], 'duración', round(dur, 1), 's')

if __name__ == '__main__':
    main(sys.argv[1])
