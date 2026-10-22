# Continuar en un chat nuevo

Nota de traspaso para seguir con las Salas del Camino desde otra sesión; por ejemplo, cuando cambia un conector y hay que abrir un chat nuevo. Nada se pierde al cambiar de chat: la página, su código y sus datos están guardados.

## Dónde está todo

- Página: https://claude.ai/artifact/EQuo4jWzUPiuceTb8VzxwC (versión 157 a 21 de octubre de 2026).
- Código: `salas/index.html` en este repo (`santiagoways2026/edificio-de-control`), rama `claude/magical-tesla-rc62sa`. Copia idéntica en `santiagoways2026/brandbook2027` (`salas/index.html`, misma rama).
- Datos: base de datos de la página; se lee y escribe con ArtifactData y la url de la página.
- Protocolos de cada sala: `salas/<sala>/AGENTE.md`.

## Cómo publicar

1. En un chat nuevo, leer primero la página con Artifact (`action: read`) y comprobar que coincide con `salas/index.html`.
2. Editar `salas/index.html` en este repo.
3. Copiarlo a `brandbook2027/salas/index.html`.
4. Publicar con Artifact: ese archivo y la url de la página, sin pasar `capabilities` (así se conservan las que ya tiene: db, downloads, sample y mcp con Metricool, «zoho crm» y Claude Code Remote/fire_trigger).
5. Commit y push de los dos repos en la rama `claude/magical-tesla-rc62sa`.

## Documentos de la base de datos

| Documento | Para qué |
|---|---|
| `rrss_seguimiento/actual` | Community, pestaña Seguimiento RRSS (Metricool y Zoho). Refresco diario e informe mensual: rutina «Seguimiento RRSS: refresco diario e informe mensual» (trig_01GTVVrfSAxWjPH2pc5YScG2, 23:22; sin conectores, deja avisos). Lecturas de seguidores el día 1 de cada mes, como cierre del mes anterior: la página registra las de Metricool (cuentas propias y competidores de Instagram y Facebook) cuando la abre un administrador en la primera semana del mes, y la rutina «Seguimiento RRSS: lectura del día 1 (competencia)» (trig_01SUxoTJZFju2zQsvur62PtE, día 1 a las 9:17) añade el resto desde los perfiles públicos (embed de Instagram, plugin de Facebook, LinkedIn, TikTok y YouTube). Lectura extra el 21 de octubre de 2026 con todos los competidores salvo CaminoWays en Facebook (su página no se puede leer sin sesión). |
| `captacion_canales/actual` | Captación, CR por canal (UTM). |
| `captacion_canales_mercado/actual` | Filtro por mercado en CR por canal: ES, EN, DE, IT y PT (campo Language de Zoho). |
| `inversion_plataformas/actual` | Captación, Inversión: barras apiladas por plataforma. |
| `seo_blog` | SEO, zoom del Blog con deals y won por URL. |
| `captacion_canales_pais/actual` | Ya no se usa (se sustituyó por el filtro por mercado). |
| `youtube_dash/actual` | YouTube, Dashboard de canales: copia de las filas diarias de Metricool (ES, EN y ES del año anterior). La página la renueva una vez al día con los datos en vivo. |
| `refresco/diario` | Control del refresco diario al abrir la página: qué tablas de Zoho y qué rutinas se han lanzado hoy. |
| `seo_semrush/actual` | SEO, Brecha de palabras clave y parte de SEO técnico: búsquedas más grandes de cada mercado con nuestra mejor posición (`grandes`, mensual, con `hist` por mes; julio de 2026 cargado con el histórico de Semrush a 50 unidades por palabra clave), visibilidad semanal por país, historia de 12 meses por dominio, conjunto fijo de palabras clave por mercado (ES, US, UK, DE) con la posición de cada competidor, palabras que nos faltan, resumen de Site Audit, pautas de Jaime y gasto de unidades. Lo escribe la rutina «Sala SEO: Semrush con tope». |
| `seo_tecnico/actual` | SEO técnico: velocidad de 10 páginas clave con Lighthouse (gratis), historia diaria y pautas técnicas de Pedro. Lo escribe la rutina «Sala SEO: SEO técnico y velocidad». |
| `plan_itpt/actual` | Sala de Control, pestaña «Plan de contingencia IT y PT» (primera de la sala): diagnóstico de los mercados italiano y portugués frente a ES, EN y DE, qué funciona en el resto y no se hace en IT y PT, los tres mercados (Italia, Brasil y Portugal), plan en 3 fases con sala y responsable por acción, objetivos, umbrales de decisión (20 nov, 20 dic y 28 feb), decisiones previas e insights de 21 salas. Escrito a mano desde un chat el 21 de octubre de 2026 (análisis en el scratchpad de esa sesión); no lo actualiza ninguna rutina. |
| `seo_gsc/actual` | Reservado para Search Console (todavía sin conectar). Esquema que lee la página: `mercados.{es,en,de,it,pt}` con `mensual` [[AAAAMM, clics, impresiones, posición]] y `kws` [{kw, clics, impr, pos, pos_prev, pos_ini, url}]. |

## Zoho

- La página ya llama al conector «zoho crm» (constante `ZO` en `salas/index.html`) y lo tiene declarado en `capabilities`.
- `ZohoCRM_runReport`: usar siempre el tipo matrix con una agrupación de columna por fecha y `date_filter`; si no, da INTERNAL_SERVER_ERROR. Un grupo de filtros con un solo criterio da AMBIGUOUS_GROUP_IN_CRITERIA. En la respuesta, `aggregates[0]` es el número de filas; con `sum`, la suma está en `aggregates[1]`. El formato completo está en el prompt de la rutina «Seguimiento RRSS».
- Último refresco completo hecho desde un chat: 21 de octubre de 2026 (las 8 tablas, el filtro por mercado, los deals de redes de Seguimiento RRSS y el Blog). El informe 2161768000878444244 quedó con la última configuración de CR por canal.
- Alerta web del 21 de octubre de 2026 (comprobada con navegador): en las homes /it/ y /pt/ el botón principal («Richiedi un preventivo!» / «Solicite um orçamento!») y las tarjetas de Sarria y Saint-Jean llevan a un 404 en español; las fichas buenas están en URL «-old» y los nuevos hubs del Francés en noindex. Además, las 128 etapas IT y las 127 PT usan el formulario español (Language = Spanish). No se ha tocado WordPress: está en el plan de contingencia para validarlo con Álvaro.
- GA4 en Windsor: el 21 de octubre de 2026 el conector de Google Analytics no estaba configurado para el usuario; los datos de GA4 son la copia de `ga4/actual` del 6 de octubre.
- Alerta del 21 de octubre de 2026: los deals con `Utm_Source = blog_org` de octubre llevan parados en 52 al menos desde el 16 de octubre (igual el 16, el 19, el 20 y el 21), mientras el resto de canales sigue creciendo. Parece que el blog dejó de enviar la etiqueta a Zoho hacia el 7 u 8 de octubre. Está en el análisis de `seo_blog`. No se ha tocado WordPress: revisarlo con Álvaro.
- Correo: desde el 22 de octubre de 2026 el conector «zoho crm» tiene permiso de administrador: responden el resumen de almacenamiento de correo, el almacenamiento por usuario y las carpetas y recuentos del buzón de otros usuarios (antes daba NO_PERMISSION). Solo se han leído metadatos. Leer el contenido de los correos de los asesores exige avisar antes al equipo (ver Reglas); para revisar las plantillas IT y PT basta con las plantillas de email del CRM, que no son correo personal.
- Almacenamiento de correo de Zoho lleno a 22 de octubre de 2026: 770 GB usados frente a 175 GB de capacidad y 41 MB libres; 297 GB son de usuarios borrados.

## Refresco diario y pestañas ocultas

- Al abrir la página (solo quien puede escribir en la base de datos), `refrescoDiario()` revisa qué no es de hoy (hora de Madrid): actualiza las tablas de Zoho con el conector de quien abre (`REF_ZOHO`) y lanza con fire_trigger las rutinas de Cerebro, Control, Community, Lifecycle, YouTube y SEO cuyo análisis no sea de hoy (`REF_RUT`). Lo apunta en `refresco/diario` para no repetirlo el mismo día.
- Rutinas en horario de mañana (Madrid): SEO 6:17 (ahora diaria), YouTube 6:47 y 17:47, Community 7:07, Lifecycle 7:22, Cerebro 7:28, 14:28 y 20:28, Control 7:50, 14:50 y 20:50.
- La rutina «Análisis comercial» (Zoho) está pausada: usaba el conector antiguo y escribía filas sin el mes de cierre; ahora lo actualiza la página al abrirse.
- SEO: pestañas nuevas «Brecha de palabras clave» (`seo_brecha`) y «SEO técnico» (`seo_tecnico`). La antigua «Auditoría técnica» se llama ahora «Rastreo propio: detalle». La rutina «Sala SEO: SEO técnico y velocidad (diario, gratis)» (trig_017VppgD2vzZjjtxwujJGWw5, 6:32) está en el refresco diario; la de Semrush no.
- Ocultas sin borrar (`MODS_OCULTOS`): «Desde SEO» en todas las salas, «SEO para cada sala», el brief de Control en Diseño y, en YouTube, la auditoría y la estrategia Hub & Spoke. Los datos siguen circulando por la base de datos.

## Semrush

- El conector de Semrush de claude.ai entra con la subcuenta de Álvaro, que no tiene unidades de API (no_api_units).
- La API key con unidades está guardada en la configuración del entorno como `SEMRUSH_API_KEY` (añadida el 21 de octubre de 2026). Se lee solo en sesiones nuevas. Úsala desde Bash con la API REST de Semrush (https://api.semrush.com/), sin imprimirla ni guardarla en archivos del repo ni de la página.
- Las unidades son de toda la empresa y no se recargan solas. El 21 de octubre de 2026 una prueba gastó 129.000 unidades (de 207.100 a 78.100) por dos llamadas al historial de Site Audit. Antes de usar un informe nuevo, prueba con una sola fila y mira el coste.
- Coste medido por llamada o por fila (21 de octubre de 2026):

| Informe | Coste |
|---|---|
| `siteaudit/history` | 60.000 por llamada. **No usar nunca.** |
| `tracking_competitors_organic` | 1.000 por fila. No usar. |
| `tracking_position_organic` (proyecto 1001436) | 100 por palabra clave, con todos los días del rango |
| `tracking_overview_organic` | 100 por llamada |
| `siteaudit/info`, `siteaudit/meta/issues`, `management/v1/projects/{id}` | 100 por llamada |
| `domain_domains` (brecha) | 80 por fila |
| `domain_organic` y `phrase_organic` históricos (`display_date`) | 50 por fila |
| `domain_organic_organic` (competidores) | 40 por fila |
| `domain_organic`, `domain_ranks`, `domain_rank_history`, `phrase_organic`, `phrase_these` | 10 por fila |
| `management/v1/projects` (lista) y `countapiunits` | gratis |

- Rutina «Sala SEO: Semrush con tope (brecha y competencia)» (trig_019QiQanw1bPkBpDmb9m6HpV), los lunes a las 5:47 de Madrid. Lleva el script con tope: 3.500 unidades al mes (7.000 en octubre de 2026, el primer mes), y no gasta nada si el saldo baja de 40.000. Cada semana, visibilidad por país (60 unidades); cada mes, historia, posiciones del conjunto frente a la competencia (domain_organic con filtro por palabra clave, unas 10 unidades por dominio y palabra) y Site Audit; cada trimestre, palabras que nos faltan. No la pongas en el refresco diario de la página: es semanal a propósito. No le pases texto extra al lanzarla con fire_trigger, porque repite la ejecución.
- `domain_domains` devuelve solo palabras en las que posicionan todos los dominios (intersección); sirve para «nos faltan», no para la brecha.
- Primera carga del 21 de octubre de 2026: 6.040 unidades; con las búsquedas más grandes y su posición de julio, 8.180 en octubre (por encima del tope de 7.000 del primer mes, a petición de Álvaro) y saldo 69.930. La rutina no gastará más en octubre. Coste mensual previsto: unas 2.200 unidades (3.330 en enero, abril, julio y octubre por «nos faltan»).
- Proyectos de Semrush: 1001436 (Position Tracking con 10 palabras clave, Site Audit de 1.000 páginas y más herramientas), 28068064 (Site Audit de 100 páginas) y 28088077 (Position Tracking; la API responde «campaign not found»).

## Reglas

- Español con tildes y sin guiones largos; en su lugar, punto, dos puntos o punto y coma.
- Zoho, Meta, Google Ads, Windsor y Metricool son solo lectura. Nunca programar ni crear publicaciones. En Zoho nunca usar herramientas destructivas; la única excepción es el informe 2161768000878444244, que se puede reconfigurar.
- WordPress: no cambiar nada sin avisar antes.
- Conectores: si se pierde o falla una conexión (Zoho, Metricool, Windsor, Gmail, Semrush, Google), avisar a Álvaro antes de seguir y revisarlo juntos; no rodearlo en silencio.
- Correo de los asesores: lo acordado era ver solo métricas. Si se pasa a leer el contenido, avisar antes al equipo.

## Pendiente

0. Search Console: Álvaro tiene que conectarlo en Windsor.ai (searchconsole). Después, crear una rutina diaria que escriba `seo_gsc/actual` (las rutinas creadas desde aquí no llevan conectores: o la crea Álvaro desde claude.ai con Windsor, o se rellena desde un chat). CMS de WordPress: pendiente de que Álvaro lo conecte; solo lectura.

1. Correo en Zoho: ver qué asesores tienen el buzón conectado y quién lo comparte (público) y quién no (privado). Después, qué manda cada uno.
2. Cambiar el nombre del servidor Zoho en la página (ver arriba).
3. Añadir los conectores de Metricool y Zoho a la rutina «Seguimiento RRSS» en claude.ai; sin ellos, deja avisos en la pestaña.
4. Dejar como borrador en Gmail el correo `notas/correo-instagram-crecimiento.md` para Jane y Álvaro (hay que reautorizar Gmail y falta la dirección de Jane).
5. Opcional: indicador de guardados y compartidos por cada 1.000 personas alcanzadas en Seguimiento RRSS, y gráfico de seguidores diarios frente a inversión en Meta.
