# Sala de Comunidad: protocolo

Seis especialistas analizan los comentarios de las cuentas de Santiago Ways y la conversación del mercado.

| id | Nombre | Qué hace |
|---|---|---|
| igfb | Carla | Comentarios de Instagram y Facebook por post y formato |
| video | Rubén | Comentarios en YouTube y TikTok |
| faq | Ana | Preguntas y dudas que se repiten (FAQ real) |
| bench | Martín | Qué genera comentarios en la competencia y el mercado |
| cm | Olga | Respuestas modelo e ideas de activación |
| jefa | Bea | Insights para la Sala de Control |

## Fuentes

- `comunidad_snap/{es,en,de}`: foto de los posts de los últimos 90 días con comentarios, me gusta y alcance. La página la escribe desde Metricool cada 6 h cuando se visita la sala (las rutinas no tienen conectores).
- `comunidad_lotes`: comentarios reales pegados por el usuario y ya analizados por la página (`procesado: false` hasta que la rutina los integra).
- `radar`, `comp_cambios`, `control_briefing/actual`, `control_directrices/comunidad` (si existe).
- WebSearch: foros (caminodesantiago.me, Gronze), grupos y prensa para las preguntas del mercado.

## Salida

- `comunidad_analisis/actual`: `fecha, periodo, resumen, totales[{red,mercado,posts,comentarios,media}], porFormato[{tipo,media,posts,lectura,ejemplo}], topPosts[], preguntas[{tema,que,mercado,oportunidad,fuente,fuenteNombre}], quejas[], sugerencias[{tipo: captar|activar|responder, red, titulo, detalle, porque, referencias[]}], competencia[], benchmarks[{texto,fuente,fuenteNombre}], limitaciones`.
- `estado/comunidad`: `ultimaRevision`, `agentes.<id>.ultima`, `bitacora` (máx. 40).

Regla de métricas: cada post citado lleva sus comentarios, me gusta y alcance o vistas. No inventar datos.

## Límite actual

Metricool da el número de comentarios por post, pero no su texto. El texto se obtiene pegándolo en la sala o, en el futuro, con acceso a la API de Meta (Instagram y Facebook) y a YouTube Data API.
