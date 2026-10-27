# Hojas de contacto: 12 fotos por hoja (4x3), etiqueta con índice. Escribe hojas/hoja_NN.jpg y hojas/indice.json
import sys,json,os,pathlib
from PIL import Image, ImageDraw
src=pathlib.Path(sys.argv[1]); out=pathlib.Path(sys.argv[2]); out.mkdir(parents=True,exist_ok=True)
ids=[l.strip() for l in open(src/'ids.txt') if l.strip()]
ids=[i for i in ids if (src/f'{i}.jpg').exists()]
W,H,COLS,ROWS=380,380,4,3; indice={}
for h in range(0,len(ids),COLS*ROWS):
    lote=ids[h:h+COLS*ROWS]; sheet=Image.new('RGB',(COLS*W,ROWS*(H+28)),'white'); d=ImageDraw.Draw(sheet)
    for k,i in enumerate(lote):
        im=Image.open(src/f'{i}.jpg').convert('RGB'); im.thumbnail((W-10,H-10))
        x=(k%COLS)*W+5; y=(k//COLS)*(H+28)+24; sheet.paste(im,(x,y)); n=h+k+1; indice[n]=i
        d.rectangle([x,y-22,x+60,y-2],fill='black'); d.text((x+6,y-20),f'#{n}',fill='white')
    sheet.save(out/f'hoja_{h//(COLS*ROWS)+1:02d}.jpg',quality=80)
json.dump(indice,open(out/'indice.json','w'),indent=0); print('hojas',(len(ids)+11)//12,'fotos',len(ids))
