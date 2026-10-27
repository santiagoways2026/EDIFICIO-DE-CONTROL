# Biblioteca de Diseño: importar fotos de la carpeta «SELECCIÓN MULTIMEDIA 2027»

Proceso seguido el 27 de octubre de 2026 (artifact RRSS). Las fotos nunca van al repo: solo al artifact.

1. Listar la carpeta de Drive (recursiva) con el conector y guardar `drive_listado.json` ({archivos:[{id,title,mimeType,ruta,...}]}).
2. Comparar con `diseno_biblio` (los ids de los documentos son los ids de Drive): nuevos = en Drive y no en la biblioteca; retirados = en la biblioteca y no en Drive (borrar documento y archivo `drive/<id>.jpg` si ninguna pieza lo usa).
3. Descargar los nuevos con `mcp__Google_Drive__download_file_content`, de uno en uno: el harness guarda el base64 en disco y `decodifica.py` lo convierte en `fotos/<id>.jpg`. Límites: el conector rechaza archivos de más de 10 MB y se cae con varios de más de 1 MB seguidos; los enlaces públicos (`drive.google.com/thumbnail?id=…&sz=w1600`) solo funcionan si la carpeta está compartida con cualquiera con el enlace.
4. `hojas.py` monta hojas de contacto de 12 fotos para describirlas mirándolas; las descripciones van en un JSON {id:{descripcion,etiquetas,escena}} siguiendo el índice de posiciones de cada hoja (no el orden alfabético de los ids).
5. `fichas.py` redimensiona a 2000 px, genera la miniatura en base64, escribe las fichas y los lotes de 50 para ArtifactData, y `files_map.json` para publicar los `drive/<id>.jpg`.
