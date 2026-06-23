# DCSS-es — Dungeon Crawl Stone Soup en español

Traducción al **español de España** de **Dungeon Crawl Stone Soup** v0.34.1.

[![Estado](https://img.shields.io/badge/estado-100%25-success)](https://github.com/Ricard1974/dcss-es)
[![Versión](https://img.shields.io/badge/dcss-0.34.1-blue)](https://github.com/crawl/crawl)
[![Licencia](https://img.shields.io/badge/licencia-GPLv2%2B-green)](LICENSE)

---

## 📊 Estado del proyecto

| Componente     | Archivos | Estado |
| -------------- | :------: | :----: |
| UI (menús, etc)|    10    |   ✅   |
| Descripciones  |    23    |   ✅   |
| Base de datos  |    23    |   ✅   |
| Código C++     |    8     |   ✅   |
| **Total**      |  **64**  |  🎉   |

### Traducciones de interfaz (ui/)

| Archivo         | Entradas | Notas                                                   |
| --------------- | :------: | ------------------------------------------------------- |
| `ability.txt`   |   276    | Habilidades raciales y divinas                          |
| `combat.txt`    |    93    | Mensajes de combate                                     |
| `commands.txt`  |   179    | Comandos, ayuda de teclas, pantalla                     |
| `inventory.txt` |   206    | Descripciones de objetos                                |
| `menu.txt`      |    71    | Menús de creación de personaje                          |
| `misc.txt`      |    15    | Cadenas misceláneas                                     |
| `religion.txt`  |   297    | Los 28 dioses — mensajes, poderes, títulos              |
| `skills.txt`    |   325    | Descripciones de habilidades                            |
| `status.txt`    |    28    | Estados de duración y efectos                           |
| `names.txt`     |   118    | Nombres de especies, clases, modos de juego             |

### Archivos de ayuda y descripciones (descript/)

23 archivos con descripciones de monstruos, objetos, hechizos, dioses, razas,
clases, tutorial, etc. Todos traducidos al español.

### Archivos de base de datos (database/)

23 archivos con speech de monstruos, FAQ, ayuda, nombres aleatorios, etc.
Todos traducidos al español.

---

## 🛠️ Parches de código C++

| Archivo       | Parche                                              | Propósito                           |
| ------------- | --------------------------------------------------- | ----------------------------------- |
| `format.cc`   | `ops.push_back(tr(s))` en `cprintf()`               | Barra de estado                     |
| `message.cc`  | `text = tr(text)` en `_mpr()`                       | Mensajes del juego                  |
| `output.cc`   | `buf = tr(buf)` en `wrapcprintf()`                  | Panel derecho de stats              |
| `cio.cc`      | `buf = tr(buf)` en `wrapcprintf()`                  | Texto de UI en consola              |
| `libunix.cc`  | `buf = tr(buf)` en `cprintf()`                      | Menú principal y textos             |
| `startup.cc`  | `tr(entry.label)` en menú                           | Modos de juego del menú             |
| `command.cc`  | `tr(desc)` en `_add_command`, carga localizada      | Descripciones de teclas, ayuda      |
| `newgame.cc`  | `tr()` en species/jobs/grupos                       | Nombres en creación de personaje    |
| `menu.cc`     | `tr()` línea por línea en `add_formatted()`         | Pantalla de ayuda (?)               |
| `translation.cc` | `names.txt` añadido a `s_ui_files`              | Carga de traducciones de nombres    |

---

## 🚀 Cómo usar

```bash
cd ~/proyectos/dcss-squashfs/squashfs-root/usr
LANGUAGE=es ./bin/crawl
```

O usando el script incluido:

```bash
cd ~/proyectos/dcss-es
./jugar.sh
```

## 🔧 Compilar

```bash
cd ~/proyectos/dcss-es
bash scripts/build_con_traducciones.sh
```

Esto clona el código fuente de DCSS v0.34.1, aplica parches, compila y genera
el binario en `/tmp/dcss-build-*/crawl-ref/source/crawl`.

## ✅ Verificación

Después de compilar o actualizar traducciones, ejecutar:

```bash
cd ~/proyectos/dcss-es
python3 scripts/verify.py
```

Esto verifica:
- Binario: tamaño y parches clave
- Archivos UI: 10 archivos en translations/, dat/ y squashfs
- Traducciones de ayuda: secciones de teclas, menús, nombres
- Archivos descript: 23 archivos con estructura correcta
- Archivos database: 23 archivos presentes
- Problemas textuales: 0 Will, 0 usted, 0 §, 0 fideos, 0 $cmd rotos
- Sincronización: translations/ coincide con dat/

---

## 🌍 Cómo traducir a otro idioma

La infraestructura de traducción ya está lista. No hace falta modificar código C++
para añadir un nuevo idioma. Los parches existentes (`tr()` en los puntos de
salida) funcionan para cualquier idioma.

### Archivos a traducir (56 en total)

| Grupo | Archivos | Descripción |
|---|---|---|
| UI | 10 | Menús, comandos, barra de estado, nombres |
| Descript | 23 | Descripciones de monstruos, objetos, hechizos, etc. |
| Database | 23 | FAQ, speech de monstruos, nombres, ayuda |

### Pasos

```bash
# 1. Crear directorios para el nuevo idioma
#    (código ISO 639-1: fr, pt, de, it, etc.)
LANG=pt  # cambiar al código deseado

mkdir -p translations/ui/$LANG translations/descript/$LANG
mkdir -p dat/ui/$LANG dat/descript/$LANG dat/database/$LANG

# 2. Copiar originales en inglés como base
cp dat/ui/*.txt translations/ui/$LANG/ 2>/dev/null
cp dat/descript/*.txt translations/descript/$LANG/
cp dat/database/*.txt dat/database/$LANG/

# 3. Traducir los archivos
#    Opción A: manualmente (recomendado para calidad)
#    Opción B: con LibreTranslate (rápido, requiere revisión)
#      Los scripts existentes protegen automáticamente:
#      - $cmd[...] / $item[...] (comandos del juego)
#      - @The_monster@, @player_name@ (placeholders)
#      - <tags> HTML (formato)
#      - %%%% (separadores de entrada)
#      - %s, %d, %f (format strings)

# 4. Compilar (los parches C++ ya funcionan)
bash scripts/build_con_traducciones.sh

# 5. Configurar el idioma
echo "language = $LANG" >> ~/.crawl/init.txt
```

### Protección de patrones

Al traducir con herramientas automáticas, estos patrones deben protegerse
(reemplazar con placeholders antes de traducir y restaurar después):

| Patrón | Ejemplo | Proteger |
|---|---|---|
| `$cmd[...]` | `$cmd[CMD_REST]` | ✅ Siempre |
| `$item[...]` | `$item[gold]` | ✅ Siempre |
| `@...@` | `@The_monster@` | ✅ Siempre |
| `<...>` | `<w>`, `<input>`, `<bat>` | ✅ Siempre |
| `%%%%` | Separador de entrada | ✅ Siempre |
| `%s`, `%d`, `%f` | Format strings | ✅ Siempre |
| `<<...>>` | `<<query>>` | ✅ Siempre |
| `[[...]]` / `{{...}}` | Código Lua | ✅ Siempre |

### Tiempo estimado

| Método | Tiempo | Calidad |
|---|---|---|
| LibreTranslate automático | ~2-3 horas | Aceptable, requiere revisión |
| Traducción manual | Semanas | Excelente |
| Híbrido (automático + revisión) | ~1 semana | Buena |

### Notas importantes

- Los archivos `.txt` se cargan en tiempo de ejecución (no necesitan recompilación)
- Solo los cambios en `source/*.cc` necesitan recompilar
- El verificador `scripts/verify.py` detecta problemas estructurales
- Las caches SQLite en `~/.crawl/saves/db/` deben eliminarse al cambiar de idioma
- No usar "usted" en español (tuteo: "tú")
- Las claves de entrada (primera línea tras `%%%%`) deben permanecer en inglés

## 📄 Licencia

GPLv2+ (igual que Dungeon Crawl Stone Soup)
