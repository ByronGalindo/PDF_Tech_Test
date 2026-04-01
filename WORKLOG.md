# Worklog

## 2026-04-01

## English

Short log:
- Reviewed the PDF and the three provided JSON files.
- Confirmed that the target window for `B.1` is pages `89` to `122`.
- Confirmed that `B.2` begins on page `123`.
- Wrote the first planning, notes, and estimate files.
- Created the first Python scaffold and a simple `B.1` inspection script.
- Added the first section detection logic from page content.
- Added an initial two-column layout helper for inspection.
- Added a first content-area filter to skip page headers.
- Added a first record grouping pass using `111` as the record anchor.
- Added a first field extraction pass for the target INID fields.
- Added footer-noise filtering for page markers such as `2024/007`.
- Added the first output builder for the final `B -> 1` JSON shape.
- Moved generated output to `solution/output` to keep test inputs untouched.
- Added a basic validation pass for missing fields, duplicates, and field format.
- Added a deeper raw-record analysis for cross-page and suspiciously short records.
- Added validation directly against the generated JSON file in `solution/output`.

Next:
- inspect page layout,
- define the column split,
- and detect record boundaries.

## Español

Resumen corto:
- Revisé el PDF y los tres JSON entregados.
- Confirmé que la ventana de trabajo para `B.1` es de la página `89` a la `122`.
- Confirmé que `B.2` empieza en la página `123`.
- Dejé creados los archivos iniciales de plan, notas y estimación.
- Creé el primer esqueleto en Python y un script simple para inspeccionar `B.1`.
- Agregué la primera lógica para detectar la sección desde el contenido.
- Agregué una primera ayuda de layout para inspeccionar las dos columnas.
- Agregué un primer filtro de área útil para saltar encabezados de página.
- Agregué una primera agrupación de registros usando `111` como ancla.
- Agregué una primera extracción de los campos INID objetivo.
- Agregué un filtro de ruido para pies de página como `2024/007`.
- Agregué el primer generador del JSON final con la forma `B -> 1`.
- Dejé la salida generada en `solution/output` para no mezclarla con los insumos.
- Agregué una validación básica para campos faltantes, duplicados y formato.
- Agregué un análisis más fino de registros crudos para ver cruces de página y casos cortos.
- Agregué validación directa sobre el JSON generado en `solution/output`.

Siguiente:
- revisar el layout de las páginas,
- definir el corte entre columnas,
- y detectar el inicio y fin de cada registro.
