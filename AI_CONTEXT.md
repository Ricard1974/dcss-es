# AI_CONTEXT.md — Contexto para asistentes de IA

Proyecto: **DCSS-es** — Traducción de **Dungeon Crawl Stone Soup** v0.34.1 al español de España.
Repositorio: https://github.com/Ricard1974/dcss-es
Estado: **100% traducido** (UI + descripciones + base de datos + parches C++)

## Reglas lingüísticas
- **Español de España** exclusivamente (nada de modismos latinoamericanos ni argentinos)
- **Tuteo**: "tú", nunca "usted"
- Las claves de traducción deben coincidir exactamente con las cadenas del código (espacios incluidos)

## Estructura del proyecto

### Traducciones de texto (`translations/`)
| Directorio | Archivos | Contenido |
|---|---|---|
| `translations/ui/es/` | 10 | Menús, barra de estado, comandos, nombres |
| `translations/descript/es/` | 23 | Descripciones de monstruos, objetos, etc. |
| `translations/database/es/` | - | Base de datos del juego (referencia) |

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
| `translate_batch.py` | Traducción por lotes con LibreTranslate |
| `extract_untranslated.py` | Detecta cadenas sin traducir en C++ |

### Parches C++ aplicados
| Archivo | Parche | Efecto |
|---|---|---|
| `format.cc` | `tr()` en `cprintf()` | Barra de estado |
| `message.cc` | `tr()` en `_mpr()` | Mensajes del juego |
| `cio.cc` | `tr()` en `wrapcprintf()` | Panel derecho |
| `libunix.cc` | `tr()` en `cprintf()` | Menú principal |
| `startup.cc` | `tr(entry.label)` | Modos de juego |
| `command.cc` | `tr(desc)` + carga localizada | Ayuda de teclas, manual |
| `newgame.cc` | `tr()` en species/jobs | Creación de personaje |
| `menu.cc` | `tr()` línea por línea | Pantalla de ayuda (?) |
| `translation.cc` | names.txt en s_ui_files | Carga de nombres |

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
- El binario se copia a ~/proyectos/dcss-squashfs/squashfs-root/usr/bin/crawl
\n## Archivos importantes
- verify.py: verificación post-build
- bot_qa.py: bot capturador de texto (detecta inglés)
- build_con_traducciones.sh: compila DCSS con parches
