# AI_CONTEXT.md — Contexto para asistentes de IA

Proyecto: **DCSS-es** — Traducción de **Dungeon Crawl Stone Soup** v0.34.1 al español de España.
Repositorio: https://github.com/Ricard1974/dcss-es (público)
Estado: **UI + descript + database traducido, parches C++ completos**

## Reglas lingüísticas
- **Español de España** exclusivamente (nada de modismos latinoamericanos ni argentinos)
- **Tuteo**: "tú", nunca "usted"
- Las claves de traducción deben coincidir exactamente con las cadenas del código (espacios incluidos)

## Estructura del proyecto

### Traducciones de texto (`translations/`)
| Directorio | Archivos | Contenido |
|---|---|---|
| `translations/ui/es/` | 10 | Menús, barra de estado, comandos, combate, nombres |
| `translations/descript/es/` | 23 | Descripciones de monstruos, objetos, etc. |
| `translations/database/es/` | 23 | Base de datos del juego (speech, FAQ, etc.) |

### Archivos de datos en runtime (`dat/`)
| Directorio | Contenido |
|---|---|
| `dat/ui/es/` | Copia runtime de translations/ui/es/ |
| `dat/descript/es/` | Descripciones traducidas (generadas) |
| `dat/database/es/` | Base de datos traducida |

### Scripts (`scripts/`)
| Script | Propósito |
|---|---|
| `build_con_traducciones.sh` | Compila DCSS con todos los parches y traducciones |
| `fix_newgame.py` | Aplica tr() a newgame.cc |
| `fix_command.py` | Aplica carga localizada a command.cc |
| `fix_libunix.py` | Aplica tr() a libunix.cc |
| `fix_message_mprf.py` | Aplica tr() a do_message_print() (traduce format strings) |
| `translate_batch.py` | Traducción por lotes con LibreTranslate |
| `extract_untranslated.py` | Detecta cadenas sin traducir en C++ |
| `bot_qa.py` | Bot capturador de texto (detecta inglés en juego) |
| `verify.py` | Verificación post-build (0 errores actualmente) |

### Parches C++ aplicados
| Archivo | Parche | Efecto |
|---|---|---|
| `format.cc` | `tr()` en `cprintf()` | Barra de estado |
| `message.cc` | `text = tr(text)` en `_mpr()` | Mensajes del juego (estáticos) |
| `message.cc` | `string fmt = tr(format)` en `do_message_print()` | **Traduce format strings con %s ANTES de sustituir args** |
| `cio.cc` | `tr()` en `wrapcprintf()` | Panel derecho |
| `libunix.cc` | `tr()` en `cprintf()` | Menú principal |
| `startup.cc` | `tr(entry.label)` | Modos de juego |
| `command.cc` | `tr(desc)` + carga localizada | Ayuda de teclas, manual |
| `newgame.cc` | `tr()` en species/jobs | Creación de personaje |
| `menu.cc` | `tr()` línea por línea | Pantalla de ayuda (?) |
| `translation.cc` | names.txt en s_ui_files | Carga de nombres |
| `translation.cc` | **fix filtro**: `line[0]=='%'` → `line.substr(0,2)=="%%"` | No descartar claves con %s |

## Bugs importantes encontrados y solucionados
1. **Filtro en translation.cc**: `line[0] == '%'` descartaba TODAS las claves que empiezan con `%s`, inutilizando las 384 traducciones de combate. Fix: `line.substr(0,2) == "%%"` (solo ignora separadores).
2. **Hook en `_mpr()` insuficiente**: traducía DESPUÉS de `vsnprintf`, por lo que las cadenas con `%s` ya venían con nombres de monstruo interpolados. Fix: hook adicional en `do_message_print()` que traduce el FORMATO antes de formatear.

## Cobertura actual
| Componente | Cobertura | Notas |
|---|---|---|
| UI menús/estático | ~100% | misc.txt, menu.txt, status.txt, etc. |
| Format strings combate | **95%** (716/749) | combat.txt (900 líneas) |
| Nombres (species/jobs) | 100% | names.txt |
| Descript | 100% | 23 archivos |
| Database | 100% | 23 archivos |
| **33 format strings restantes** | Debug/internos | No afectan al jugador |

## Traducción de archivos descript/database
Los archivos descript se traducen con protección de patrones:
1. Proteger: `$cmd[...]`, `$item[...]`, `<tags>`, `@...@`, `%%%%`, `<<...>>`, `[[...]]`, `{{...}}`
2. Reemplazar con `PLH{n}` (placeholders)
3. Traducir con LibreTranslate
4. Restaurar placeholders
5. Post-procesar: eliminar "Will", "usted" → "tú", eliminar §AG

## Notas importantes
- Los `.txt` se cargan en runtime (no necesitan recompilación)
- Los cambios C++ necesitan recompilación
- La compilación se hace en desktop remoto (ricard@100.85.246.74)
- Config de idioma: `echo "language = es" >> ~/.crawl/init.txt` (NO `LANGUAGE=es` env var)
- El binario se copia a `~/proyectos/dcss-squashfs/squashfs-root/usr/bin/crawl`
- `verify.py` debe dar 0 errores antes de declarar "listo"
- Los nombres de monstruo no se traducen (el juego los genera en inglés)
