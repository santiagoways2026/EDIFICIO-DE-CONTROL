# Rutina «Espejo RRSS»

Rutina de Claude Code Remote (`create_trigger` con `create_new_session_on_fire`, cadencia pendiente de confirmar por Álvaro; propuesta: cada 3 horas). Cada pasada abre una sesión nueva en este repo y ejecuta el prompt de abajo. Coste estimado por pasada con pocos cambios: entre 80.000 y 120.000 tokens (la mayor parte son los listados de las 30 colecciones en los dos artifacts); con muchos documentos cambiados sube en proporción.

## Prompt de la rutina

```
Eres la rutina «Espejo RRSS» del repo santiagoways2026/edificio-de-control (rama claude/rrss-paula). Copias documentos entre la base de datos del artifact principal «Salas del Camino» (https://claude.ai/artifact/EQuo4jWzUPiuceTb8VzxwC) y la del artifact «RRSS · Santiago Ways» (https://claude.ai/artifact/9JzricUTN6AKMkmdaHcUbM). Responde en español, breve, con tildes y sin guiones largos.

Reglas: solo usas la herramienta ArtifactData (cárgala con ToolSearch "select:ArtifactData") y Bash. Nunca publicas ni modificas ninguna página. Nunca borras documentos. Los archivos que devuelve ArtifactData con out_dir son de solo lectura: no los modifiques en sitio. No uses ningún otro conector.

Pasos:
1. Lee espejo/config y espejo/estado del artifact RRSS con ArtifactData get y out_dir (carpeta de trabajo: espejo/ dentro del scratchpad de la sesión; guarda la version de espejo/estado).
2. Para cada colección de principal_a_rrss y rrss_a_principal (sin repetir), haz ArtifactData list con query {"limit":1000} y out_dir en los dos artifacts: carpeta espejo/principal para el principal y espejo/rrss para RRSS. Si una colección devuelve next_cursor, sigue paginando con cursor.
3. Ejecuta: python3 -I herramientas/espejo_rrss/espejo_rrss.py --principal espejo/principal --rrss espejo/rrss --config espejo/rrss/espejo/config.json --estado espejo/rrss/espejo/estado.json --out espejo/salida. Lee espejo/salida/resumen.txt.
4. Aplica los lotes: cada archivo espejo/salida/a_rrss_NN.json es un array de escrituras para ArtifactData batch sobre el artifact RRSS, y cada a_principal_NN.json sobre el artifact principal. Copia las entradas tal cual (op, collection, doc_id, file_path e if_version cuando venga). Si un lote falla por versión cambiada, no lo reintentes: anótalo en errores.
5. Escribe espejo/estado en el artifact RRSS con ArtifactData set, file_path espejo/salida/estado_nuevo.json e if_version la version leída en el paso 1. Si hubo errores en el paso 4, antes de escribirlo edita una copia del archivo (no el original) poniendo huellas_fiables en false y los errores en pasadas[0].errores, y usa esa copia.
6. Termina con un resumen de una línea: documentos copiados en cada sentido, conflictos y errores. Si no hay nada que copiar, dilo en una línea y termina.
```

## Criterio de copia

- Se comparan contenidos (huella sha256 de `data`), nunca versiones: los contadores de versión no son comparables entre artifacts.
- Principal a RRSS (un sentido): seo_red, control_brief, control_briefing, control_directrices, estado, insights, roadmap, radar, radar_prev, radar_sintesis, comunidad_snap, comunidad_analisis, rrss_seguimiento, comp_cambios, comp_exploracion, players, ig_capt, ig_dash, ig_en, ig_err, ig_ranking, tk_ranking, youtube_analisis, youtube_dash, youtube_ranking y diseno_tendencias. Gana el principal siempre que difiera.
- RRSS a principal (un sentido): diseno_piezas y diseno_videos. Gana RRSS siempre que difiera.
- peticiones (dos sentidos): a tres bandas con las huellas de la pasada anterior. Si solo cambió un lado se copia ese lado; si cambiaron los dos, gana el principal y se registra el conflicto.
- diseno_biblio se copió solo en la semilla; las fotos de drive/ no se tocan. comunidad_lotes y diseno_videos estaban vacías en la semilla.
- Las escrituras sobre documentos que ya existen van pinadas con `if_version` del destino; si falla, se reintenta en la pasada siguiente.
