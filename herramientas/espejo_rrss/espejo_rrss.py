#!/usr/bin/env python3
"""Espejo RRSS: calcula qué documentos copiar entre la base de datos de las Salas del Camino
(principal) y la del edificio RRSS · Santiago Ways, y deja los lotes listos para ArtifactData.

Entradas (todas carpetas o archivos creados por ArtifactData con out_dir; se leen, nunca se modifican):
  --principal DIR   volcado de las colecciones del artifact principal (DIR/<coleccion>/<doc>.json, {data, version})
  --rrss DIR        volcado de las mismas colecciones del artifact RRSS
  --config JSON     documento espejo/config (solo el campo data o el archivo de out_dir)
  --estado JSON     documento espejo/estado de la pasada anterior (opcional)
  --out DIR         carpeta de salida (se crea)

Salidas en --out:
  a_rrss_NN.json        lotes (máx. 50) para ArtifactData batch sobre el artifact RRSS
  a_principal_NN.json   lotes para el artifact principal
  datos/<lado>/<coleccion>/<doc>.json  copia solo de `data` de cada documento que se va a escribir
  estado_nuevo.json     documento espejo/estado para guardar al terminar (huellas incluidas)
  resumen.txt           resumen legible

Los documentos listados en excluir_docs de la configuración nunca se copian.
Criterio: se comparan contenidos (hash de `data`), no versiones, porque los contadores de versión
no son comparables entre artifacts. Colecciones de un solo sentido: gana el origen siempre que difiera.
Colecciones de dos sentidos (peticiones): a tres bandas con las huellas de la pasada anterior; si
solo cambió un lado se copia ese lado; si cambiaron los dos, gana el principal y se registra el conflicto.
"""
import argparse, hashlib, json, os, pathlib, datetime

def cargar(dirp, col):
    out = {}
    d = pathlib.Path(dirp) / col
    if not d.is_dir():
        return out
    for f in sorted(d.iterdir()):
        if f.suffix != '.json':
            continue
        raw = json.load(open(f, encoding='utf-8'))
        if isinstance(raw, dict) and 'data' in raw and 'version' in raw:
            out[f.stem] = (raw['data'], raw['version'])
        else:
            out[f.stem] = (raw, None)
    return out

def huella(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode('utf-8')).hexdigest()[:16]

def doc_de(arch):
    raw = json.load(open(arch, encoding='utf-8'))
    return raw['data'] if isinstance(raw, dict) and 'data' in raw and 'version' in raw else raw

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--principal', required=True); ap.add_argument('--rrss', required=True)
    ap.add_argument('--config', required=True); ap.add_argument('--estado'); ap.add_argument('--out', required=True)
    a = ap.parse_args()
    cfg = doc_de(a.config)
    prev = doc_de(a.estado) if a.estado and os.path.exists(a.estado) else {}
    hp = prev.get('huellas', {}).get('principal', {}) if prev.get('huellas_fiables', True) else {}
    hr = prev.get('huellas', {}).get('rrss', {}) if prev.get('huellas_fiables', True) else {}
    out = pathlib.Path(a.out); (out / 'datos').mkdir(parents=True, exist_ok=True)
    a_rrss, a_principal = [], []
    nuevas_hp, nuevas_hr = {}, {}
    copiados = {}; conflictos = []; iguales = 0

    def planear(col, src, dst, lado_dst, lista, key, data, ver_dst):
        p = out / 'datos' / lado_dst / col; p.mkdir(parents=True, exist_ok=True)
        f = p / f'{key.split("/",1)[1]}.json'
        f.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
        e = {'op': 'set', 'collection': col, 'doc_id': key.split('/', 1)[1], 'file_path': str(f)}
        if ver_dst is not None:
            e['if_version'] = ver_dst
        lista.append(e); copiados[col] = copiados.get(col, 0) + 1

    excluir = set(cfg.get('excluir_docs', []))  # 'coleccion/doc' que nunca se copian (salas ajenas al edificio RRSS)
    ambos = set(cfg.get('principal_a_rrss', [])) & set(cfg.get('rrss_a_principal', []))
    solo_pr = [c for c in cfg.get('principal_a_rrss', []) if c not in ambos]
    solo_rp = [c for c in cfg.get('rrss_a_principal', []) if c not in ambos]

    for col in solo_pr + solo_rp + sorted(ambos):
        P = cargar(a.principal, col); R = cargar(a.rrss, col)
        for doc in sorted(set(P) | set(R)):
            key = f'{col}/{doc}'
            if key in excluir:
                continue
            dp = P.get(doc); dr = R.get(doc)
            hP = huella(dp[0]) if dp else None; hR = huella(dr[0]) if dr else None
            if hP == hR:
                iguales += 1; nuevas_hp[key] = hP; nuevas_hr[key] = hR; continue
            if col in solo_pr:
                if dp:
                    planear(col, 'principal', 'rrss', 'rrss', a_rrss, key, dp[0], dr[1] if dr else None)
                    nuevas_hp[key] = hP; nuevas_hr[key] = hP
                else:
                    nuevas_hr[key] = hR  # solo existe en RRSS: se deja estar
            elif col in solo_rp:
                if dr:
                    planear(col, 'rrss', 'principal', 'principal', a_principal, key, dr[0], dp[1] if dp else None)
                    nuevas_hp[key] = hR; nuevas_hr[key] = hR
                else:
                    nuevas_hp[key] = hP
            else:  # dos sentidos, a tres bandas
                cambioP = hP != hp.get(key); cambioR = hR != hr.get(key)
                if dp and (not dr or (cambioP and not cambioR)):
                    planear(col, 'principal', 'rrss', 'rrss', a_rrss, key, dp[0], dr[1] if dr else None)
                    nuevas_hp[key] = hP; nuevas_hr[key] = hP
                elif dr and (not dp or (cambioR and not cambioP)):
                    planear(col, 'rrss', 'principal', 'principal', a_principal, key, dr[0], dp[1] if dp else None)
                    nuevas_hp[key] = hR; nuevas_hr[key] = hR
                else:  # cambiaron los dos (o primera pasada con diferencias): gana el principal
                    conflictos.append(key)
                    planear(col, 'principal', 'rrss', 'rrss', a_rrss, key, dp[0], dr[1] if dr else None)
                    nuevas_hp[key] = hP; nuevas_hr[key] = hP

    def lotes(lista, nombre):
        n = 0
        for i in range(0, len(lista), 50):
            (out / f'{nombre}_{n:02d}.json').write_text(json.dumps(lista[i:i+50], ensure_ascii=False, indent=1), encoding='utf-8'); n += 1
        return n
    n1 = lotes(a_rrss, 'a_rrss'); n2 = lotes(a_principal, 'a_principal')
    ahora = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
    pasada = {'fecha': ahora, 'copiados_a_rrss': len(a_rrss), 'copiados_a_principal': len(a_principal),
              'por_coleccion': copiados, 'conflictos': conflictos, 'iguales': iguales, 'errores': []}
    estado = {'ultima_pasada': ahora, 'pasadas': ([pasada] + prev.get('pasadas', []))[:20],
              'huellas_fiables': True, 'huellas': {'principal': nuevas_hp, 'rrss': nuevas_hr}}
    (out / 'estado_nuevo.json').write_text(json.dumps(estado, ensure_ascii=False), encoding='utf-8')
    res = (f'Pasada {ahora}\nIguales: {iguales}\nA RRSS: {len(a_rrss)} documentos en {n1} lotes\n'
           f'A principal: {len(a_principal)} documentos en {n2} lotes\nPor colección: {json.dumps(copiados, ensure_ascii=False)}\n'
           f'Conflictos (gana principal): {conflictos}\n')
    (out / 'resumen.txt').write_text(res, encoding='utf-8'); print(res)

if __name__ == '__main__':
    main()
