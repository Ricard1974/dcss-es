# DCSS-es — Dungeon Crawl Stone Soup en español

Traducción al **español de España** de **Dungeon Crawl Stone Soup** v0.34.1.

[![Estado](https://img.shields.io/badge/estado-96%25-success)](https://github.com/Ricard1974/dcss-es)
[![Versión](https://img.shields.io/badge/dcss-0.34.1-blue)](https://github.com/crawl/crawl)
[![Licencia](https://img.shields.io/badge/licencia-GPLv2%2B-green)](LICENSE)

---

## 📊 Estado del proyecto

| Sección     | Archivos | Entradas  | Traducidas |     %     | Estado |
| ----------- | :------: | :-------: | :--------: | :-------: | :----: |
| `descript/` |    23    |   3.899   |   3.899    |   100%    |   ✅   |
| `database/` |    23    |   2.070   |   2.070    |   100%    |   ✅   |
| `ui/`       |    9     |   1.691   |   1.409    |   83.3%   |   ✅   |
| **Total**   |  **55**  | **7.660** | **7.378**  | **96.3%** |   🎉   |

### Traducciones de interfaz (ui/)

| Archivo         | Total | Trad. | Notas                                       |
| --------------- | :---: | :---: | ------------------------------------------- |
| `ability.txt`   |  280  |  280  | Habilidades raciales y divinas              |
| `combat.txt`    |  92   |  92   | Mensajes de combate                         |
| `commands.txt`  |  221  |  115  | 106 en inglés (formato HTML complejo)       |
| `inventory.txt` |  286  |  284  | 2 cadenas de depuración                     |
| `menu.txt`      |  41   |  41   | Menús de creación de personaje              |
| `misc.txt`      |   4   |   4   | Cadenas misceláneas                         |
| `religion.txt`  |  315  |  315  | Los 28 dioses — mensajes, poderes, títulos  |
| `skills.txt`    |  324  |  158  | 166 nombres de título en inglés (canónicos) |
| `status.txt`    |  128  |  120  | 8 abreviaturas de barra de estado           |

> **Nota**: 282 entradas UI se mantienen deliberadamente en inglés: nombres de título de habilidad (canónicos del juego), textos de ayuda con formato HTML complejo (`<w>`, `<bg:...>`), y abreviaturas de interfaz.

---

## 🚀 Cómo usar

### Opción 1: Jugar con las traducciones (AppImage)

```bash
# 1. Descargar DCSS 0.34.1
wget https://github.com/crawl/crawl/releases/download/0.34.1/crawl-0.34.1-linux-x86_64.AppImage

# 2. Extraer
chmod +x crawl-0.34.1-linux-x86_64.AppImage
./crawl-0.34.1-linux-x86_64.AppImage --appimage-extract

# 3. Clonar este repositorio
git clone https://github.com/Ricard1974/dcss-es.git
cd dcss-es

# 4. Copiar traducciones al juego
bash scripts/instalar.sh --dir ../squashfs-root

# 5. Configurar idioma
echo "language = es" >> ~/.crawl/init.txt

# 6. Jugar
../squashfs-root/usr/bin/crawl
```

### Opción 2: Compilar desde código fuente

Ver [docs/INSTALL.md](docs/INSTALL.md) para instrucciones de compilación con las traducciones integradas.

### Opción 3: Lanzador incluido

```bash
./jugar.sh
```

Configura automáticamente `language = es` en `~/.crawl/init.txt`.

---

## 📁 Estructura del proyecto

```
dcss-es/
├── translations/
│   ├── descript/es/          # 23 archivos — descripciones del juego
│   ├── database/es/          # 23 archivos — diálogos, voces, nombres
│   └── ui/es/                # 9 archivos — interfaz de usuario (C++)
│       ├── ability.txt       # Habilidades raciales y divinas
│       ├── combat.txt        # Mensajes de combate
│       ├── commands.txt      # Comandos del juego
│       ├── inventory.txt     # Inventario y objetos
│       ├── menu.txt          # Menús de creación de personaje
│       ├── misc.txt          # Miscelánea
│       ├── religion.txt      # Religión y dioses
│       ├── skills.txt        # Habilidades y entrenamiento
│       └── status.txt        # Efectos de estado
├── src/
│   ├── translation.h         # Cabecera del sistema de traducción UI
│   └── translation.cc        # Implementación C++ del cargador
├── scripts/
│   ├── terms.py              # Diccionario DCSS-es (1072+185+127)
│   ├── translate_batch.py    # Traducción masiva con LibreTranslate
│   ├── translate_html.py     # Traductor que preserva etiquetas HTML
│   ├── stats.py              # Estadísticas de cobertura
│   ├── check_translations.py # Validación de formato
│   ├── extract_entries.py    # Extracción de cadenas del código fuente
│   ├── sort_entries.py       # Ordenación de archivos
│   ├── fix_angle_refs.py     # Corrección de referencias <...>
│   ├── sync_template.py      # Sincronización de plantillas
│   ├── update_upstream.py    # Actualización desde upstream
│   ├── generar_parche_completo.py  # Genera parche C++ completo
│   ├── build_con_traducciones.sh   # Script de compilación
│   ├── instalar.sh           # Instalación en AppImage extraída
│   └── actualizar_juego.sh   # Actualización del juego instalado
├── patches/
│   └── 0001-ui-translation-infra-full.diff  # Parche C++ para UI
├── docs/
│   ├── PLAN.md               # Plan de proyecto y hoja de ruta
│   ├── INSTALL.md            # Guía de instalación detallada
│   ├── TRANSLATION_GUIDE.md  # Convenciones de traducción
│   ├── ARCHIVOS_TRADUCIDOS.md # Listado completo de archivos
│   └── CXX_STUDY.md          # Estudio de traducción C++
├── AI_CONTEXT.md             # Documento para asistentes de IA
├── jugar.sh                  # Lanzador del juego en español
├── README.md
└── .gitignore
```

---

## 🤖 Sistema de traducción UI (Fase 2 C++)

La interfaz de usuario de DCSS está hardcodeada en C++. Se ha creado un sistema de traducción desde cero:

1. **Archivos `.txt`** con formato `clave|valor` en `translations/ui/es/`
2. **Infraestructura C++** (`translation.h`/`.cc`) que carga los archivos en memoria
3. **Macro `tr()`** que envuelve literales en el código fuente
4. **Parche** (`patches/0001-ui-translation-infra-full.diff`) que modifica los `.cc`

Las cadenas se buscan por clave exacta (texto inglés original) y se devuelve la traducción española.

---

## 🔤 Diccionario de términos (scripts/terms.py)

| Categoría      | Cantidad | Propósito                                             |
| -------------- | :------: | ----------------------------------------------------- |
| `FORCED_TERMS` |  1.072   | Traducciones exactas de términos del juego            |
| `NO_TRANSLATE` |   185    | Términos que se mantienen en inglés (nombres propios) |
| `POST_PROCESS` |   127    | Correcciones automáticas post-traducción              |

El flujo de traducción es:

1. `NO_TRANSLATE` se protegen con placeholders → no los toca LibreTranslate
2. `FORCED_TERMS` (compuestos) se protegen con placeholders
3. LibreTranslate traduce el texto restante
4. Se restauran los placeholders con las traducciones correctas
5. `POST_PROCESS` aplica correcciones (tuteo, concordancia, términos mal traducidos)

---

## 🛠 Herramientas

### Traducción automática (requiere LibreTranslate)

```bash
# Requiere LibreTranslate en localhost:5000
docker run -d -p 5000:5000 libretranslate/libretranslate

# Traducir todo lo que falte
python3 scripts/translate_batch.py --missing

# Archivo específico
python3 scripts/translate_batch.py --file spells.txt

# Traducir preservando etiquetas HTML
python3 scripts/translate_html.py --translate "Press <w>?</w> for help"
python3 scripts/translate_html.py --file commands.txt
```

### Estadísticas

```bash
python3 scripts/stats.py               # Informe completo
python3 scripts/stats.py --json        # Salida JSON
```

### Validación

```bash
python3 scripts/check_translations.py   # Validar formato de archivos
```

### Generar parche C++

```bash
python3 scripts/generar_parche_completo.py
```

### Compilar con traducciones

```bash
bash scripts/build_con_traducciones.sh   # Ver docs/INSTALL.md
```

---

## 📚 Documentación

| Archivo                                                    | Descripción                                 |
| ---------------------------------------------------------- | ------------------------------------------- |
| [docs/PLAN.md](docs/PLAN.md)                               | Plan de proyecto y hoja de ruta             |
| [docs/INSTALL.md](docs/INSTALL.md)                         | Guía de instalación detallada               |
| [docs/TRANSLATION_GUIDE.md](docs/TRANSLATION_GUIDE.md)     | Convenciones de traducción y estilo         |
| [docs/ARCHIVOS_TRADUCIDOS.md](docs/ARCHIVOS_TRADUCIDOS.md) | Listado completo de archivos                |
| [docs/CXX_STUDY.md](docs/CXX_STUDY.md)                     | Estudio de la infraestructura C++           |
| [AI_CONTEXT.md](AI_CONTEXT.md)                             | Documento de contexto para asistentes de IA |

---

## 🗺 Plan de desarrollo

| Fase   | Contenido                                       | Estado       |
| ------ | ----------------------------------------------- | ------------ |
| **1a** | `descript/` (23 archivos)                       | ✅ 100%      |
| **1b** | `database/` (23 archivos)                       | ✅ 100%      |
| **2**  | Infraestructura C++ (translation.h/.cc, parche) | ✅ Completo  |
| **2b** | Traducciones UI (9 archivos, ~1700 cadenas)     | ✅ 96.3%     |
| **3**  | Revisión humana de calidad                      | ⏳ Pendiente |
| **4**  | Compilación y pruebas de juego                  | ⏳ Pendiente |
| **5**  | PR al repositorio oficial                       | ⏳ Pendiente |

Ver [PLAN.md](docs/PLAN.md) para detalles.

---

## 🤝 Cómo contribuir

1. Lee [TRANSLATION_GUIDE.md](docs/TRANSLATION_GUIDE.md) para las convenciones
2. Lee [AI_CONTEXT.md](AI_CONTEXT.md) si usas un asistente de IA
3. Revisa qué falta traducir con `python3 scripts/stats.py`
4. Traduce editando directamente los archivos en `translations/ui/es/`
5. Ejecuta `python3 scripts/check_translations.py` para validar
6. Abre un Pull Request

---

## 📜 Licencia

**GPLv2+** — misma licencia que [Dungeon Crawl Stone Soup](https://github.com/crawl/crawl).

---

## 🙏 Atribuciones

- [Crawl DevTeam](https://github.com/crawl/crawl) — el juego original
- [LibreTranslate](https://libretranslate.com/) — motor de traducción automática
- [LTEngine](https://github.com/LibreTranslate/LTEngine) — motor de traducción con LLMs (alternativa recomendada)
- Todos los contribuyentes que ayuden a mejorar esta traducción
