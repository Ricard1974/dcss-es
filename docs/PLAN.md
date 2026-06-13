# Plan de proyecto — DCSS-es

## Visión general

Traducir **Dungeon Crawl Stone Soup** al español de España, desde el texto externo
hasta el código C++ hardcodeado, y contribuir la traducción al repositorio oficial.

---

## Fase 1: Texto externo ✅ Completada

### 1a: descript/ — Descripciones del juego

Archivos en `crawl-ref/source/dat/descript/es/` — descripciones de monstruos,
objetos, hechizos, habilidades, mutaciones, estados, razas, trasfondos, etc.

| Archivos | 23 de 23            | Estado      |
| -------- | ------------------- | ----------- |
| Entradas | 3.825 EN → 3.871 ES | ✅ **100%** |

### 1b: database/ — Diálogos y nombres

Archivos en `crawl-ref/source/dat/database/es/` — mensajes de monstruos,
diálogos de dioses, gritos, insultos, nombres de artefactos, etc.

| Archivos | 23 de 23            | Estado      |
| -------- | ------------------- | ----------- |
| Entradas | 2.047 EN → 2.047 ES | ✅ **100%** |

### Herramientas creadas

- `scripts/translate_batch.py` — Traducción masiva con LibreTranslate local
- `scripts/terms.py` — Diccionario de 1.017 términos forzados + 240 NO_TRANSLATE
- `scripts/stats.py` — Estadísticas de cobertura
- `scripts/fix_angle_refs.py` — Corrección de referencias `<...>`
- `scripts/actualizar_juego.sh` — Copia traducciones al juego instalado

---

## Fase 2: C++ hardcode ⏳ Pendiente

### Alcance

Interfaz de usuario, menús, mensajes del juego escritos directamente en C++.
Distribuidos por varios archivos fuente en `crawl-ref/source/`.

Estimación: **~3.300 cadenas** repartidas en:

| Área                       | Cadenas aprox. | Archivos fuente               |
| -------------------------- | -------------- | ----------------------------- |
| Menú principal             | 50             | `menu.cc`, `newgame.cc`       |
| Selección de especie/clase | 200            | `newgame.cc`                  |
| Pantalla de estado         | 100            | `output.cc`                   |
| Mensajes de combate        | 400            | `fight.cc`, `melee_attack.cc` |
| Mensajes de hechizos       | 300            | `spl*.cc`                     |
| Mensajes de objetos        | 250            | `item_use.cc`, `invent.cc`    |
| Pantalla de habilidades    | 150            | `skills.cc`                   |
| Pantalla de capacidades    | 50             | `ability.cc`                  |
| Pantalla de dioses         | 100            | `religion.cc`                 |
| Mensajes de interfaz       | 300            | Varios                        |
| Ayuda y tutorial           | 200            | `hints.cc`, `guide.cc`        |
| Mensajes de error          | 100            | Varios                        |
| Comandos y atajos          | 150            | `command.cc`                  |
| Varios                     | 950            | Resto                         |

### Enfoque propuesto

1. Extraer cadenas con un script de análisis de código fuente
2. Crear archivos de traducción en formato `.po` o similar
3. Usar `translate_batch.py` con el diccionario existente
4. Inyectar las traducciones en el código fuente
5. Compilar y probar

### Desafíos

- El juego usa `string` literales directamente en C++
- No hay infraestructura de internacionalización (gettext, etc.)
- Algunas cadenas usan marcadores de formato `%s`, `%d`
- Las cadenas compuestas (ej: "You hit the %s") necesitan manejo especial
- El tamaño de la ventana puede romperse con textos más largos en español

---

## Fase 3: Revisión de calidad ⏳ Pendiente

- Revisión humana de todas las traducciones automáticas
- Corrección de errores de contexto (LT no entiende el contexto del juego)
- Verificación de coherencia terminológica
- Pruebas de juego completas

---

## Fase 4: Pull Request oficial ⏳ Pendiente

- Probar la traducción completa en la versión oficial
- Sincronizar con los cambios del upstream
- Abrir PR en [github.com/crawl/crawl](https://github.com/crawl/crawl)
- Iterar según feedback del equipo de Crawl

---

## Hitos

| Hito                            | Fecha    | Estado |
| ------------------------------- | -------- | ------ |
| Primer commit                   | Jun 2026 | ✅     |
| descript/ 100%                  | Jun 2026 | ✅     |
| database/ 100%                  | Jun 2026 | ✅     |
| Fase 1 completa (texto externo) | Jun 2026 | ✅     |
| Fase 2 completa (C++ hardcode)  | —        | ⏳     |
| Revisión humana                 | —        | ⏳     |
| PR al upstream                  | —        | ⏳     |
