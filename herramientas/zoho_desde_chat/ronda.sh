python3 cache.py $(cat since.txt) && python3 fix1004.py
for f in actualizarCanales actualizarTiempo actualizarCaptacion actualizarVentas actualizarAsesores actualizarEmbudo actualizarValor actualizarAlertas; do node h.js $f > log_$f.txt 2>&1; python3 -c "
import json,sys;t=open('log_$f.txt').read();i=t.find('\"msgs\"');print('$f',t[i:i+200].replace('\n',' '))"; done
python3 needs.py | grep '^##'
