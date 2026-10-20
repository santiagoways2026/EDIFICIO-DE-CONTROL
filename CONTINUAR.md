# Continuar en un chat nuevo

Nota de traspaso para seguir con las Salas del Camino desde otra sesión; por ejemplo, cuando cambia un conector y hay que abrir un chat nuevo. Nada se pierde al cambiar de chat: la página, su código y sus datos están guardados.

## Dónde está todo

- Página: https://claude.ai/artifact/EQuo4jWzUPiuceTb8VzxwC (versión 152 a 20 de octubre de 2026).
- Código: `salas/index.html` en este repo (`santiagoways2026/edificio-de-control`), rama `claude/magical-tesla-rc62sa`. Copia idéntica en `santiagoways2026/brandbook2027` (`salas/index.html`, misma rama).
- Datos: base de datos de la página; se lee y escribe con ArtifactData y la url de la página.
- Protocolos de cada sala: `salas/<sala>/AGENTE.md`.

## Cómo publicar

1. En un chat nuevo, leer primero la página con Artifact (`action: read`) y comprobar que coincide con `salas/index.html`.
2. Editar `salas/index.html` en este repo.
3. Copiarlo a `brandbook2027/salas/index.html`.
4. Publicar con Artifact: ese archivo y la url de la página, sin pasar `capabilities` (así se conservan las que ya tiene).
5. Commit y push de los dos repos en la rama `claude/magical-tesla-rc62sa`.

## Documentos de la base de datos

| Documento | Para qué |
|---|---|
| `rrss_seguimiento/actual` | Community, pestaña Seguimiento RRSS (Metricool y Zoho). La mantiene la rutina «Seguimiento RRSS». |
| `captacion_canales/actual` | Captación, CR por canal (UTM). |
| `captacion_canales_mercado/actual` | Filtro por mercado en CR por canal: ES, EN, DE, IT y PT (campo Language de Zoho). |
| `inversion_plataformas/actual` | Captación, Inversión: barras apiladas por plataforma. |
| `seo_blog` | SEO, zoom del Blog con deals y won por URL. |
| `captacion_canales_pais/actual` | Ya no se usa (se sustituyó por el filtro por mercado). |

## Zoho

- El conector de claude.ai se llama ahora «zoho crm». La página todavía llama a un servidor llamado «Zoho»: 8 llamadas `callTool("Zoho", ...)` y su declaración `mcp`. Cuando el conector nuevo funcione hay que:
  1. Comprobar que tiene las herramientas que usa la página con el mismo nombre: `ZohoCRM_runSpecificReport`, `ZohoCRM_updateReports`, `ZohoAnalytics_createExportJobSQLQuery`, `ZohoAnalytics_getExportJobDetails` y `ZohoAnalytics_downloadExportedData`.
  2. Cambiar «Zoho» por el nombre nuevo en `salas/index.html`.
  3. Volver a declarar `capabilities`. Una declaración nueva sustituye a todas las anteriores, así que hay que repetir también las demás (db, user y Metricool).
- `ZohoCRM_runReport`: usar siempre el tipo matrix con una agrupación de columna por fecha y `date_filter`; si no, da INTERNAL_SERVER_ERROR. Un grupo de filtros con un solo criterio da AMBIGUOUS_GROUP_IN_CRITERIA. En la respuesta, `aggregates[0]` es el número de filas; con `sum`, la suma está en `aggregates[1]`. El formato completo está en el prompt de la rutina «Seguimiento RRSS».
- Correo: hasta ahora todas las herramientas de correo daban OAUTH_SCOPE_MISMATCH (la autorización no incluía el permiso de correo). Los informes sí funcionaban.

## Reglas

- Español con tildes y sin guiones largos; en su lugar, punto, dos puntos o punto y coma.
- Zoho, Meta, Google Ads, Windsor y Metricool son solo lectura. Nunca programar ni crear publicaciones. En Zoho nunca usar herramientas destructivas; la única excepción es el informe 2161768000878444244, que se puede reconfigurar.
- WordPress: no cambiar nada sin avisar antes.
- Correo de los asesores: lo acordado era ver solo métricas. Si se pasa a leer el contenido, avisar antes al equipo.

## Pendiente

1. Correo en Zoho: ver qué asesores tienen el buzón conectado y quién lo comparte (público) y quién no (privado). Después, qué manda cada uno.
2. Cambiar el nombre del servidor Zoho en la página (ver arriba).
3. Añadir los conectores de Metricool y Zoho a la rutina «Seguimiento RRSS» en claude.ai; sin ellos, deja avisos en la pestaña.
4. Dejar como borrador en Gmail el correo `notas/correo-instagram-crecimiento.md` para Jane y Álvaro (hay que reautorizar Gmail y falta la dirección de Jane).
5. Opcional: indicador de guardados y compartidos por cada 1.000 personas alcanzadas en Seguimiento RRSS, y gráfico de seguidores diarios frente a inversión en Meta.
