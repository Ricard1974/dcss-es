# AI_CONTEXT.md — Contexto para asistentes de IA

Este documento describe el proyecto **DCSS-es** (traducción al español de España de Dungeon Crawl Stone Soup) para que un asistente de IA pueda entenderlo, navegarlo y contribuir sin necesidad de explicaciones previas.

---

## 📋 Resumen

**Proyecto**: Traducción completa de DCSS v0.34.1 al español de España.
**Repositorio**: https://github.com/Ricard1974/dcss-es
**Estado**: 7.378/7.660 entradas traducidas (96.3%)
**Idioma**: Español de España exclusivamente (nada de modismos latinoamericanos ni argentinos)
**Tuteo**: Sí (tú, no usted)
**Licencia**: GPLv2+

---

## 📁 Estructura de archivos

### 1. Traducciones de texto externo (`translations/descript/es/`)

23 archivos con descripciones de monstruos, objetos, hechizos, dioses, etc.

**Formato** (`%%%%` separador):

```
%%%%
[English key/title]

[Spanish translation text]
%%%%
```

### 2. Base de datos del juego (`translations/database/es/`)

23 archivos con diálogos, nombres aleatorios, voces de monstruos, etc.

**Formato**: Mismo que descript (`%%%%` separador).

### 3. Traducciones de interfaz (`translations/ui/es/`)

9 archivos con cadenas de la interfaz de usuario extraídas del código C++.

**Formato** (`clave|valor`):

```
# Comentarios con #
Texto Inglés exacto|Texto Español
```

**Archivos UI**:

| Archivo         | Origen C++                                                                 | Contenido                                    |
| --------------- | -------------------------------------------------------------------------- | -------------------------------------------- |
| `menu.txt`      | `newgame.cc`, `menu.cc`                                                    | Menús de creación de personaje               |
| `combat.txt`    | `fight.cc`, `melee-attack.cc`, `ranged-attack.cc`, `attack.cc`, `throw.cc` | Mensajes de combate                          |
| `skills.txt`    | `skills.cc`                                                                | Nombres de habilidad, títulos, entrenamiento |
| `status.txt`    | `status.cc`, `duration-data.h`                                             | Efectos de estado, barras                    |
| `commands.txt`  | `command.cc`                                                               | Comandos del juego, ayuda de teclas          |
| `ability.txt`   | `ability.cc`                                                               | Habilidades raciales y divinas               |
| `misc.txt`      | `misc.cc`                                                                  | Cadenas misceláneas                          |
| `inventory.txt` | `inventory.cc`, `item-prop.cc`, `items.cc`                                 | Inventario y objetos                         |
| `religion.txt`  | `religion.cc`                                                              | Religión — mensajes y poderes de dioses      |

**Importante**: Las claves en los archivos UI deben coincidir EXACTAMENTE con las cadenas del código fuente C++, incluyendo espacios, puntuación y caracteres especiales. El separador es `|` (pipe).

---

## 🔧 Pipeline de traducción

```
Texto original EN
    → NO_TRANSLATE (protegido con placeholders §NT0§)
    → FORCED_TERMS compuestos (protegidos con placeholders §GT0§)
    → LibreTranslate (traducción automática local)
    → Restaurar placeholders con traducciones correctas
    → POST_PROCESS (127 correcciones automáticas)
    → Texto traducido ES
```

### scripts/terms.py — Diccionario central

Este archivo contiene tres categorías de reglas:

#### `NO_TRANSLATE` (185 términos)

Términos que NO deben traducirse bajo ninguna circunstancia.

- Nombres de dioses: `Ashenzari`, `Beogh`, `Cheibriados`, etc.
- Nombres de únicos: `Mennas`, `Norris`, etc.
- Marcas de equipo: `speed`, `protection`, `electrocution`, etc. (se dejan en inglés en el juego)

#### `FORCED_TERMS` (1.072 términos)

Traducciones exactas de términos del juego. Prioridad: términos más largos primero.

Ejemplos:

```python
"Deep Elf" → "Elfo Profundo"
"Orb of Zot" → "Orbe de Zot"
"Scroll of Identification" → "Pergamino de Identificación"
"Press" → "Pulsa"
```

#### `POST_PROCESS` (127 patrones)

Correcciones que se aplican DESPUÉS de la traducción automática para arreglar errores comunes de LibreTranslate.

Ejemplos:

```python
(r"\bUsted\b", "Tú"),           # Corregir formal → tuteo
(r"\busted\b", "tú"),
(r"el armadura", "la armadura"), # Corregir género
(r"\btrafica\b", "reparte"),     # Corregir "deals" mal traducido
(r"\bPrensa\b", "Pulsa"),        # Corregir "Press" mal traducido
(r"^no ", "No "),                # Mayúscula inicial en frases
```

---

## 🤖 Cómo usar un asistente de IA para traducir

### Para traducir cadenas UI nuevas:

1. Extraer cadenas del código fuente C++:

   ```bash
   python3 scripts/extract_entries.py --source fight.cc --output combat.txt
   ```

2. Traducir automáticamente (requiere LibreTranslate):

   ```bash
   python3 scripts/translate_batch.py --file combat.txt
   ```

3. Para cadenas con etiquetas HTML, usar el pipeline especial:

   ```bash
   python3 scripts/translate_html.py --file commands.txt
   ```

4. Revisar y corregir manualmente las traducciones dudosas.

### Para corregir una traducción existente:

1. Localizar la cadena en el archivo `.txt` correspondiente
2. Editar el lado español (después del `|`)
3. Si el error es recurrente, añadir una regla en `POST_PROCESS`

### Buenas prácticas:

- **Preservar placeholders**: `%s`, `%d`, `@monster@`, `§NT0§` deben mantenerse intactos
- **Preservar etiquetas HTML**: `<w>`, `<lightred>`, etc. no deben modificarse
- **Consistencia**: Usar FORCED_TERMS para términos del juego, no traducir libremente
- **Tuteo**: Siempre "tú", nunca "usted"
- **Género**: "el/la" deben concordar con el sustantivo
- **Nombres de dioses**: No se traducen (excepto "the Shining One" → "el Resplandeciente")

---

## ⚠️ Errores comunes de LibreTranslate

| Problema             | Ejemplo EN        | LT da                         | Corregido              |
| -------------------- | ----------------- | ----------------------------- | ---------------------- |
| Tuteo → formal       | "you are"         | "usted está"                  | "estás"                |
| Press → Prensa       | "Press key"       | "Prensa tecla"                | "Pulsa tecla"          |
| HTML dañado          | `<w>?</w>`        | `‹w›?‹/w›`                    | Preservar intacto      |
| Texto duplicado      | "as you use them" | "mientras las usass las usas" | "mientras las usas"    |
| Concordancia         | "the armour"      | "el armadura"                 | "la armadura"          |
| "deals" → tráfica    | "deals cards"     | "trafica cartas"              | "reparte cartas"       |
| "turn on" → encender | "turn on you"     | "te encienden"                | "se vuelven contra ti" |
| Mayúsculas           | "There is..."     | "no hay..."                   | "No hay..."            |

---

## 📊 Estadísticas (actualizado: junio 2026)

```
CATEGORÍA     ARCHIVOS  ENTRADAS  TRADUCIDAS  %
descript/     23        3.899     3.899      100%
database/     23        2.070     2.070      100%
ui/            9        1.691     1.409       83.3%
───────────────────────────────────────────────
TOTAL         55        7.660     7.378       96.3%
```

### Lo que queda pendiente:

1. **106 cadenas HTML** en `commands.txt` — tienen formato con `<w>`, `<bg:...>` que LibreTranslate daña. Requieren traducción manual preservando las etiquetas.
2. **Revisión humana** de calidad — jugar una partida para detectar errores de contexto.
3. **Compilación** — probar que el parche C++ funciona con el código fuente de DCSS.

---

## 🔗 Referencias

- [DCSS官方代码](https://github.com/crawl/crawl)
- [LibreTranslate](https://github.com/LibreTranslate/LibreTranslate)
- [LTEngine](https://github.com/LibreTranslate/LTEngine) — alternativa mejorada con LLMs locales
- `scripts/terms.py` — diccionario de traducción (FORCED_TERMS + NO_TRANSLATE + POST_PROCESS)
- `scripts/translate_html.py` — pipeline que preserva etiquetas HTML
- `patches/0001-ui-translation-infra-full.diff` — parche C++ para traducciones UI
