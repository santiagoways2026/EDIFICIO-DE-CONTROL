# Construye fichas diseno_biblio a partir de descripciones.json {id:{descripcion,etiquetas,escena,orientacion?}}
import sys,json,os,pathlib,base64,io
from PIL import Image
fotos=pathlib.Path(sys.argv[1]); desc=json.load(open(sys.argv[2])); listado={a['id']:a for a in json.load(open(sys.argv[3]))['archivos']}
bib_dir=pathlib.Path(sys.argv[4]); out=pathlib.Path(sys.argv[5]); out.mkdir(parents=True,exist_ok=True); orden0=int(sys.argv[6])
existentes={f.stem:json.load(open(f)) for f in bib_dir.glob('*.json')}
nuevos=[];updates=[]; orden=orden0
for i,dsc in desc.items():
    f0=fotos/f'{i}.jpg'; im0=Image.open(f0).convert('RGB'); pub=fotos.parent/'fotos_pub'; pub.mkdir(exist_ok=True); f=pub/f'{i}.jpg'
    if not f.exists():
        im1=im0.copy(); im1.thumbnail((2000,2000)); im1.save(f,'JPEG',quality=86,optimize=True)
    im=Image.open(f); w,h=im.size
    mini=im.copy(); mini.thumbnail((240,240)); b=io.BytesIO(); mini.convert('RGB').save(b,'JPEG',quality=60)
    data_uri='data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
    a=listado[i]
    campos={'alto':h,'ancho':w,'bytes':f.stat().st_size,'descargado':True,'local':f'drive/{i}.jpg','miniatura':data_uri,
            'orientacion':dsc.get('orientacion') or ('horizontal' if w>h else 'vertical' if h>w else 'cuadrada'),
            'descripcion':dsc['descripcion'],'etiquetas':dsc['etiquetas'],'escena':dsc.get('escena'),'mimeType':'image/jpeg','titulo':a['title'],'ruta':a['ruta'],
            'url':f'https://drive.google.com/file/d/{i}/view?usp=drivesdk'}
    if i in existentes:
        updates.append({'op':'update','collection':'diseno_biblio','doc_id':i,'file_path':str(out/f'{i}.json'),'if_version':1}); json.dump(campos,open(out/f'{i}.json','w'),ensure_ascii=False)
    else:
        orden+=1
        doc={'aprobado':True,'carpeta':'imagen','duracion':None,'fuente':'SELECCIÓN MULTIMEDIA 2027','id':i,'orden':orden,**campos}
        json.dump(doc,open(out/f'{i}.json','w'),ensure_ascii=False); nuevos.append({'op':'set','collection':'diseno_biblio','doc_id':i,'file_path':str(out/f'{i}.json')})
writes=nuevos+updates
for k in range(0,len(writes),50): json.dump(writes[k:k+50],open(out/f'batch_{k//50:02d}.json','w'),ensure_ascii=False)
json.dump({f'drive/{i}.jpg':str(fotos.parent/'fotos_pub'/f'{i}.jpg') for i in desc},open(out/'files_map.json','w'))
print('nuevos',len(nuevos),'updates',len(updates),'lotes',(len(writes)+49)//50,'orden final',orden)
