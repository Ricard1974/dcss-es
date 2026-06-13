# DCSS-es — Dungeon Crawl Stone Soup en español

Traducción al **español de España** de **Dungeon Crawl Stone Soup** v0.34.1.

[![Estado](https://img.shields.io/badge/estado-100%25-success)](https://github.com/tu_usuario/dcss-es)
[![Versión](https://img.shields.io/badge/dcss-0.34.1-blue)](https://github.com/crawl/crawl)
[![Licencia](https://img.shields.io/badge/licencia-GPLv2%2B-green)](LICENSE)

---

## 📊 Estado

| Sección     | EN        | ES        | %           |
| ----------- | --------- | --------- | ----------- |
| `descript/` | 3.825     | 3.871     | **100%** ✅ |
| `database/` | 2.047     | 2.047     | **100%** ✅ |
| **Total**   | **5.872** | **5.918** | **100%** 🎉 |

**Todo el texto externo** (descripciones de monstruos, objetos, hechizos, diálogos, nombres de artefactos, etc.) está traducido.

> Pendiente: interfaz de usuario y menús (C++ hardcode, ~3.300 cadenas) — [PLAN.md](docs/PLAN.md)

---

## 🚀 Cómo usar

### Opción 1: Jugar con las traducciones (Linux)

```bash
# Descargar DCSS 0.34.1 AppImage
wget https://github.com/crawl/crawl/releases/download/0.34.1/crawl-0.34.1-linux-x86_64.AppImage

# Extraer
chmod +x crawl-0.34.1-linux-x86_64.AppImage
./crawl-0.34.1-linux-x86_64.AppImage --appimage-extract

# Clonar este repositorio
git clone https://github.com/tu_usuario/dcss-es.git
cd dcss-es

# Copiar traducciones al juego
bash scripts/instalar.sh --dir ../squashfs-root

# Configurar idioma en ~/.crawl/init.txt
echo "language = es" >> ~/.crawl/init.txt

# Jugar
../squashfs-root/usr/bin/crawl
```

### Opción 2: Usar el lanzador incluido

```bash
./jugar.sh
```

El lanzador configura automáticamente `language = es` en `~/.crawl/init.txt`.

---

## 📁 Estructura del proyecto

```
dcss-es/
├── translations/
│   ├── descript/es/        # 23 archivos — descripciones del juego
│   └── database/es/        # 23 archivos — diálogos, voces, nombres
├── upstream/
│   ├── descript/           # Originales EN (referencia)
│   └── database/           # Originales EN (referencia)
├── scripts/
│   ├── translate_batch.py   # Traducción masiva con LibreTranslate
│   ├── stats.py             # Estadísticas de cobertura
│   ├── terms.py             # Diccionario DCSS-es (1017 términos)
│   ├── fix_angle_refs.py    # Corrige referencias <...>
│   ├── actualizar_juego.sh  # Copia traducciones al juego instalado
│   ├── check_translations.py
│   ├── extract_entries.py
│   ├── sort_entries.py
│   ├── sync_template.py
│   └── update_upstream.py
├── docs/
│   ├── PLAN.md              # Plan de proyecto y hoja de ruta
│   ├── INSTALL.md           # Guía de instalación detallada
│   └── TRANSLATION_GUIDE.md # Convenciones de traducción
├── jugar.sh                 # Lanzador del juego en español
├── README.md
└── .gitignore
```

---

## 📚 Documentación

| Archivo                                                    | Descripción                                            |
| ---------------------------------------------------------- | ------------------------------------------------------ |
| [docs/PLAN.md](docs/PLAN.md)                               | Plan de proyecto y hoja de ruta (fases, hitos, estado) |
| [docs/INSTALL.md](docs/INSTALL.md)                         | Guía de instalación detallada paso a paso              |
| [docs/TRANSLATION_GUIDE.md](docs/TRANSLATION_GUIDE.md)     | Convenciones de traducción y normas de estilo          |
| [docs/ARCHIVOS_TRADUCIDOS.md](docs/ARCHIVOS_TRADUCIDOS.md) | Listado completo de los 46 archivos traducidos         |

---

## 🛠 Herramientas

### Estadísticas de cobertura

```bash
python3 scripts/stats.py           # Informe completo
python3 scripts/stats.py --json    # Salida JSON
```

### Traducción automática (requiere LibreTranslate)

```bash
# Traducir todo lo que falte
python3 scripts/translate_batch.py --missing

# Archivo específico
python3 scripts/translate_batch.py --file spells.txt

# Sección database
python3 scripts/translate_batch.py --section database --missing
```

Requiere [LibreTranslate](https://github.com/LibreTranslate/LibreTranslate) corriendo en `localhost:5000`:

```bash
docker run -d -p 5000:5000 libretranslate/libretranslate
```

### Actualizar juego instalado

```bash
bash scripts/actualizar_juego.sh
```

### Validar formato

```bash
python3 scripts/check_translations.py
```

---

## 🔤 Diccionario de términos (1017 entradas)

El archivo `scripts/terms.py` contiene:

| Categoría    | Cantidad | Propósito                                   |
| ------------ | -------- | ------------------------------------------- |
| FORCED_TERMS | 1.017    | Términos que NO deben traducirse libremente |
| NO_TRANSLATE | 240      | Palabras que deben mantenerse en inglés     |
| POST_PROCESS | 103      | Correcciones automáticas post-traducción    |

Ejemplos de términos protegidos:

- `Deep Elf` → `Elfo Profundo` (traducción exacta)
- `Orb of Zot` → `Orbe de Zot` (se mantiene)
- `AC`, `EV`, `SH` → se conservan (siglas del juego)

---

## 🗺 Plan de desarrollo

| Fase   | Contenido                           | Estado       |
| ------ | ----------------------------------- | ------------ |
| **1a** | `descript/` inicial (23 archivos)   | ✅ 100%      |
| **1b** | `database/` inicial (23 archivos)   | ✅ 100%      |
| **2**  | C++ hardcode (~3.300 cadenas de UI) | ⏳ Pendiente |
| **3**  | Revisión humana de calidad          | ⏳ Pendiente |
| **4**  | PR al repositorio oficial           | ⏳ Pendiente |

Ver [PLAN.md](docs/PLAN.md) para detalles.

---

## 🤝 Cómo contribuir

1. Lee [TRANSLATION_GUIDE.md](docs/TRANSLATION_GUIDE.md) para las convenciones
2. Revisa qué falta traducir con `python3 scripts/stats.py`
3. Traduce editando directamente los archivos en `translations/`
4. Ejecuta `python3 scripts/check_translations.py` para validar
5. Abre un Pull Request

---

## 📜 Licencia

**GPLv2+** — misma licencia que [Dungeon Crawl Stone Soup](https://github.com/crawl/crawl).

---

## 🙏 Atribuciones

- [Crawl DevTeam](https://github.com/crawl/crawl) — el juego original
- [LibreTranslate](https://libretranslate.com/) — motor de traducción automática
- Todos los contribuyentes que ayuden a mejorar esta traducción
