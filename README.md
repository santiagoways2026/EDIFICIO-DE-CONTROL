# Salas del Camino

Sistema de salas con especialistas de IA trabajando sobre el Camino de Santiago.

- Interfaz en vivo (lienzo infinito con zoom): https://claude.ai/artifact/EQuo4jWzUPiuceTb8VzxwC (fuente: `salas/index.html`)
- Datos: base de datos compartida del artifact (colecciones `radar` y `estado`)

## Salas

| Sala | Estado | Protocolo |
|---|---|---|
| Sala de Control | Activa, revisión 3 veces al día | `salas/control/AGENTE.md` |
| Radar Viral (con métricas de interacción) | Activa, barrida automática cada 2 h (minuto 18, hora UTC) | `salas/radar-viral/AGENTE.md` |
| Diseño | Activa, propuesta semanal (lunes) | `salas/diseno/AGENTE.md` |
| Competencia | Activa, ronda de investigación cada 4 h | `salas/competencia/AGENTE.md` |
| Redacción | En obras | |
| Comunidad (comentarios, preguntas e interacción) | Activa, análisis diario (8:37 Madrid) | `salas/comunidad/AGENTE.md` |
| SEO | En obras | |
| Paid Media | En obras | |
