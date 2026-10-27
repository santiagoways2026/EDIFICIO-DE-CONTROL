# RRSS · Santiago Ways (edificio de redes sociales)

Dashboard propio de la responsable de redes sociales. Es un edificio hermano de las Salas del Camino: mismo código (`salas/index.html`), distinta fachada y distintas salas.

## Dónde está todo

- Página: https://claude.ai/artifact/9JzricUTN6AKMkmdaHcUbM (nacida el 27 de octubre de 2026 en el chat «RRSS · Santiago Ways», rama `claude/rrss-paula`). Es privada: se comparte desde el menú Compartir de la página.
- Código: `salas/index.html` es la fuente común; `salas/build_rrss.py` genera `salas/rrss.html` (cambia el título y añade `<meta name="edificio" content="rrss">`). El bloque `EDIFICIOS` de `index.html` define las salas, pasillos, módulos ocultos y fachada de cada edificio. No tocar la lógica compartida sin avisar a Álvaro: ese archivo también construye las Salas del Camino.
- Capabilities de la página (se conservan omitiendo `capabilities` al republicar): db (lectura para quien pueda ver, escritura solo administradores), downloads, sample y mcp con Metricool (`getAnalyticsDataByMetrics`), «Zoho Suite» (`ZohoCRM_updateReports`, `ZohoCRM_runSpecificReport`, las tres de exportación SQL de Zoho Analytics y `ZohoPageSense_getAbTestReport`) y Claude Code Remote (`fire_trigger`).
- Archivos publicados: los mismos 364 del artifact principal (drive/, firma/, img/, videos/ e index.html), copiados servidor a servidor el 27 de octubre de 2026. Los HTML de firma/ se publicaron como archivos propios porque no se pueden copiar entre artifacts.

## Salas

instagram, youtube, tiktok, community, radar, competencia y diseno (Diseño solo existe en este edificio; las Salas del Camino la ocultan). Pasillos pa11, pa22, pa32, pa28, pa20, pa33, pa29, pr1, pr2 y pr3. Módulos ocultos: cambios, comp_nuevos y comp_bp. `refrescoDiario` solo corre en el edificio camino.

## Base de datos

Independiente de la del artifact principal: no hay lectura cruzada. Semilla del 27 de octubre de 2026: 1.008 documentos en 29 colecciones (comp_cambios 57, comp_exploracion 1, comunidad_analisis 1, comunidad_snap 1, control_brief 1, control_briefing 1, control_directrices 11, diseno_biblio 146, diseno_piezas 47, diseno_tendencias 1, estado 9, ig_capt 1, ig_dash 1, ig_en 1, ig_err 1, ig_ranking 1, insights 2, peticiones 17, players 11, radar 677, radar_prev 7, radar_sintesis 1, roadmap 5, rrss_seguimiento 1, seo_red 1, tk_ranking 1, youtube_analisis 2, youtube_dash 1, youtube_ranking 1). Los contadores de versión empiezan en 1 y no son comparables con los del principal. El mismo día se borraron 12 documentos de salas ajenas al edificio (estado de control, mdirecto, paid y seo; directrices de comercial, mdirecto, paid, producto y seo; roadmap de lifecycle y seo; insights de lifecycle): el RRSS solo guarda datos de sus 7 salas y del briefing, brief, directrices e insights que necesita Diseño.

Edificio cerrado: `entrar()` rechaza cualquier sala que no esté en `EDIFICIOS.rrss.salas` (también por `#hash` en la URL) y el panel de capas no lista las salas en obras de las Salas del Camino.

Documentos propios de este edificio:

| Documento | Para qué |
|---|---|
| `espejo/config` | Qué colecciones copia el espejo y en qué sentido, y con qué criterio. |
| `espejo/estado` | Resultado de cada pasada del espejo (últimas 20) y huellas por documento de los dos lados. |

## Cómo publicar

1. Editar `salas/index.html`, ejecutar `python3 salas/build_rrss.py` y comprobar `salas/rrss.html`.
2. Publicar con Artifact `salas/rrss.html` pasando la url de la página y sin `capabilities`. Desde otro chat hay que leer antes la página con `Artifact read`.
3. Commit y push en `claude/rrss-paula`.

## Espejo con las Salas del Camino

Ver `salas/rrss/ESPEJO.md` (prompt de la rutina) y `herramientas/espejo_rrss/espejo_rrss.py` (calcula los lotes). La rutina no se crea hasta que Álvaro confirme la cadencia.
