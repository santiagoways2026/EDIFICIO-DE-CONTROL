# Montaje de reels (Sala de Diseño)

`reel.py` monta un reel 9:16 (1080x1920, 30 fps) con el estilo de la marca a partir de un guion JSON:
clips de Drive recortados a vertical (los horizontales con zoom centrado), texto Montserrat que se escribe,
antetítulo en caja verde en el primer plano, palabra resaltada en verde #7AA606 y cierre oficial
(degradado verde, isotipo blanco, «Tu Camino te espera» y santiagoways.com). Genera mp4 (H.264 + AAC),
webm (VP9 + Opus) y póster jpg.

Requisitos: ffmpeg, Pillow, las fuentes Montserrat 500/600/700/800 en `../fonts/` respecto al script
(descargadas de Google Fonts) y el isotipo blanco. Los clips en bruto se descargan de la carpeta CLAUDE de
Drive a `../clips/<id>.mp4`; no se suben a este repositorio porque contienen imágenes de clientes.

Guion (`guiones/*.json`):

```json
{"slug":"reel-14-dia-1-sarria","antetitulo":"DÍA 1 DESDE SARRIA","vol":0.4,
 "cierre":"Tu Camino\n[te espera]",
 "planos":[{"clip":"<id de Drive>","ini":0.3,"dur":3.5,"texto":"Sarria, 7 de la mañana.\nEmpieza tu [Camino]","cx":0.5}]}
```

`ini` y `dur` en segundos; `[palabra]` marca el resaltado; `cx` (0 a 1) desplaza el recorte en planos
horizontales. Ejecución: `python3 -I reel.py guiones/reel-14-dia-1-sarria.json`. El resultado va a
`../reels/<slug>/` y se publica como `videos/<slug>.mp4` y `.jpg` en el artifact RRSS.

Piezas montadas con los brutos del 26 de octubre: reel-14 (día 1 desde Sarria), reel-15 (la maleta viaja
sola), reel-16 (arriving in Santiago, EN) y reel-17 (cosas de peregrino). Fichas en `diseno_piezas`
con números 48 a 51.

## Miniaturas de YouTube (`thumbs.py`)

Miniaturas 1280x720 según el Brandbook 2027: foto a sangre de peregrinos reales o la Catedral, caja blanca con
sombra, antetítulo en mayúsculas verde sendero (#506718), titular en grafito (#2E2E2D) y minúscula de frase con
Montserrat ExtraBold, subrayado SW en verde Ways (#7AA606) girado -1,5° con letra blanca e isotipo blanco en la
esquina superior, sin tapar caras. Especificación en `miniaturas/*.json` (`foto` es el id de Drive; `cx`, `cy`
desplazan el recorte; `lado` coloca la caja a la izquierda o a la derecha). Ejecución:
`python3 -I thumbs.py miniaturas/youtube_2026-10-29.json`. Los archivos se publican como `img/yt/yt-N-A.jpg` y `-B.jpg`.

Desde el 29 de octubre el montador de reels usa el mismo subrayado recto girado -1,5° (antes, caja redondeada).
