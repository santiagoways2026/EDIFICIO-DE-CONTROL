# Sala de Control: revisión de dirección de marketing

Rutina: 8:50, 14:50 y 20:50 (hora de Madrid). Seis directores (Victoria CMO, Hugo growth, Clara marca y contenido, Iván internacional, Lola CRM, Tomás inteligencia competitiva) leen el research de 2026 (`control_contexto/research`, solo en la base de datos privada del artifact), el Radar Viral (`radar`) y la Competencia (`comp_cambios`), y escriben:

- `control_briefing/actual`: titular, resumen, prioridades y alertas.
- `control_decisiones/*`: propuestas que el usuario aprueba, descarta o marca como hechas desde la página.
- `control_directrices/radar` y `control_directrices/competencia`: el foco que esas salas leen al empezar cada ronda.
- `estado/control`: bitácora.

Regla de métricas: cualquier mención a un post o vídeo de redes incluye sus métricas.

## Chat directo con el usuario (`control_chat`)

- Desde la página, el botón "Hablar con la dirección" abre un chat en vivo: los directores responden al momento con todo el contexto de las salas (briefing, decisiones, directrices, research, radar con métricas, competencia y diseño).
- Cada mensaje del usuario se guarda como `{rol: "usuario", texto, t, procesado: false}`; las respuestas en vivo como `{rol: "direccion", texto, t, origen: "chat"}`.
- En cada revisión programada, el feedback pendiente (`procesado: false`) tiene máxima prioridad: se aplica en briefing, decisiones y directrices, se responde con un documento `{rol: "direccion", origen: "revision"}` que explica los cambios firmados por director, y se marcan los mensajes como `procesado: true`.

## Cerebro y equipo ampliado

- Cerebro es el superordenador de la sala. Su rutina se ejecuta 20 minutos antes de cada revisión (8:28, 14:28 y 20:28, hora de Madrid), lee todas las colecciones y escribe `control_cerebro/actual`: resumen, nº de datos y fuentes procesados, memoria del proyecto (`memoria.preferencias`: reglas dadas por el usuario; `memoria.aprendizajes`: lo que demuestran los datos), KPIs, resumen por sala, cola de revisión y alertas.
- La revisión de Control parte siempre de Cerebro y respeta su memoria. Los chats de todas las salas reciben esas reglas.
- Incorporaciones: Marina (datos, opera Cerebro), Sonia (calidad y marca, revisión de producción), Raúl (operaciones y cola de revisión), Daniel (paid media) y Alba (SEO).
