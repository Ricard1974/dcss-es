# DCSS-es — Dungeon Crawl Stone Soup en español

Traducción al **español de España** de **Dungeon Crawl Stone Soup** v0.34.1.

[![Estado](https://img.shields.io/badge/estado-100%25-success)](https://github.com/Ricard1974/dcss-es)
[![Versión](https://img.shields.io/badge/dcss-0.34.1-blue)](https://github.com/crawl/crawl)
[![Licencia](https://img.shields.io/badge/licencia-GPLv2%2B-green)](LICENSE)

> **🌐 Repositorio público** — https://github.com/Ricard1974/dcss-es

---

## 📊 Estado del proyecto

| Componente      | Archivos | Cobertura | Estado |
| --------------- | :------: | :-------: | :----: |
| UI (menús, etc) |    10    |   100%    |   ✅   |
| Format strings  | 1 archivo|  **95%**  |   ✅   |
| Descripciones   |    23    |   100%    |   ✅   |
| Base de datos   |    23    |   100%    |   ✅   |
| Parches C++     |    ~12   |    —      |   ✅   |
| **Total**       |  **70**  |  **99%**  |  🎉   |

### Traducciones de interfaz (ui/)

| Archivo         | Entradas | Notas                                                   |
| --------------- | :------: | ------------------------------------------------------- |
| `combat.txt`    |   900    | Mensajes de combate (716 format strings con %s)         |
| `misc.txt`      |   ~1700  | Cadenas misceláneas, mensajes del juego                 |
| `menu.txt`      |    71    | Menús de creación de personaje                          |
| `commands.txt`  |   179    | Comandos, ayuda de teclas, pantalla                     |
| `inventory.txt` |   206    | Descripciones de objetos                                |
| `ability.txt`   |   276    | Habilidades raciales y divinas                          |
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

## 🛠️ Parches de código C++ (~12 cambios)

| Archivo | Parche | Propósito |
|---|---|---|
| `translation.cc` | Infraestructura `tr()` + carga de .txt | Sistema de traducción completo |
| `translation.cc` | Fix filtro: `%%` en vez de `%` | **Bug fix**: no descartar claves con `%s` |
| `message.cc` | `text = tr(text)` en `_mpr()` | Traduce mensajes estáticos |
| `message.cc` | `string fmt = tr(format)` en `do_message_print()` | **Traduce format strings con %s ANTES de formatear** |
| `format.cc` | `tr()` en `cprintf()` | Barra de estado |
| `cio.cc` | `tr()` en `wrapcprintf()` | Panel derecho de stats |
| `libunix.cc` | `tr()` en `cprintf()` | Menú principal y textos |
| `startup.cc` | `tr(entry.label)` | Modos de juego del menú |
| `command.cc` | `tr(desc)` + carga localizada | Descripciones de teclas, ayuda |
| `newgame.cc` | `tr()` en species/jobs/grupos | Nombres en creación de personaje |
| `menu.cc` | `tr()` línea por línea | Pantalla de ayuda (?) |
| `Makefile.obj` | +translation.o | Compilar el sistema de traducción |

### 🔧 Bugs importantes corregidos

1. **Filtro que descartaba %s**: `line[0] == '%'` eliminaba TODAS las claves que empezaban con `%s`, dejando inutilizadas 384 traducciones de combate. Fix: `line.substr(0,2) == "%%"`.
2. **Hook post-formateo**: `_mpr()` recibía el texto ya formateado con nombres de monstruo, haciendo imposible matchear contra las claves con `%s`. Fix: hook en `do_message_print()` que traduce el **formato** antes de `vsnprintf`.

---

## 🚀 Cómo usar

1. Configurar el idioma en `~/.crawl/init.txt`:
```bash
echo "language = es" >> ~/.crawl/init.txt
```

2. Ejecutar el juego:
```bash
cd ~/proyectos/dcss-squashfs/squashfs-root/usr
./bin/crawl
```

O usando un RC personalizado:
```bash
./bin/crawl -rc ~/.crawl/init.txt
```

> ⚠️ **Importante**: NO usar `LANGUAGE=es` como variable de entorno. DCSS v0.34.1
> usa la opción `language` del archivo de configuración, no la variable `LANGUAGE`.

## 🔧 Compilar

```bash
cd ~/proyectos/dcss-es
bash scripts/build_con_traducciones.sh
```

Esto clona el código fuente de DCSS v0.34.1, aplica parches, copia traducciones,
compila y genera el binario en `/tmp/dcss-build-*/crawl-ref/source/crawl`.

## ✅ Verificación

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

### 🧪 Bot de prueba

```bash
cd ~/proyectos/dcss-es
timeout 300 python3 scripts/bot_qa.py
```

Juega automáticamente y detecta texto en inglés en pantalla.

---

## 🌍 Cómo traducir a otro idioma

La infraestructura de traducción ya está lista. No hace falta modificar código C++
para añadir un nuevo idioma. Los parches existentes (`tr()` en los puntos de
salida) funcionan para cualquier idioma.

### Archivos a traducir (56 en total)

| Grupo | Archivos | Descripción |
|---|---|---|
| UI | 10 | Menús, comandos, barra de estado, nombres, combate |
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
- **Configurar con `language = es` en init.txt**, NO con la variable `LANGUAGE`
- Los nombres de monstruo se muestran en inglés (el juego los genera así)

## 📄 Licencia

GPLv2+ (igual que Dungeon Crawl Stone Soup)
