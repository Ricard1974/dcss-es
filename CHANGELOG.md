# Changelog

## [1.0.0] - 2026-06-24

### Añadido
- Traducción completa de UI (10 archivos): menús, comandos, estado, nombres, combate
- 716 format strings con `%s` traducidos (95% de cobertura)
- Hook en `do_message_print()` para traducir format strings antes de formatear
- Corrección del filtro en `translation.cc` que descartaba claves con `%s`
- 23 archivos de descripciones (descript) traducidos
- 23 archivos de base de datos (database) traducidos
- Parches C++ (~12) para puntos de salida de traducción
- Script de compilación automatizada (`build_con_traducciones.sh`)
- Bot de prueba QA (`bot_qa.py`)
- Verificador post-build (`verify.py`) con 0 errores

### Corregido
- Bug: filtro `line[0] == '%'` descartaba todas las claves que empezaban con `%`
- Bug: hook en `_mpr()` traducía después de formatear, inútil para strings con `%s`
- 6 casos de "usted" reemplazados por "tú" (tuteo)

### Notas
- Proyecto: https://github.com/Ricard1974/dcss-es
- Basado en DCSS v0.34.1 (crawl/crawl)
- Licencia: GPLv2+
