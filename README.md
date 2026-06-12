# DCSS — Traducción al español

Traducción al español (de España) de **Dungeon Crawl Stone Soup** v0.34.1.

## Estado actual

| Sección     | EN        | ES      | %         |
| ----------- | --------- | ------- | --------- |
| `descript/` | 3.839     | 637     | 16,6%     |
| `database/` | 2.064     | 0       | 0%        |
| **Total**   | **5.903** | **637** | **10,8%** |

Última actualización: `python3 scripts/stats.py` para datos actualizados.

## Estructura del proyecto

```
dcss-es/
├── translations/          # Nuestros archivos de traducción
│   ├── descript/es/       # Descripciones (habilidades, objetos, hechizos...)
│   └── database/es/       # Diálogos, voces, nombres (pendiente de iniciar)
├── upstream/              # Referencia de los archivos EN originales
│   ├── descript/          # Copia snapshot del inglés
│   └── database/          # Copia snapshot del inglés
├── scripts/               # Herramientas
│   ├── stats.py           # Estadísticas de cobertura
│   ├── extract_entries.py # Extrae entradas sin traducir
│   ├── sync_template.py   # Sincroniza con cambios del upstream
│   ├── sort_entries.py    # Ordena entradas alfabéticamente
│   ├── check_translations.py  # Valida formato y referencia
│   └── update_upstream.py # Actualiza copias de referencia
└── docs/                  # Documentación
```

## Herramientas

### Estadísticas

```bash
python3 scripts/stats.py              # Informe completo
python3 scripts/stats.py --json       # Salida JSON
```

### Extraer entradas sin traducir

```bash
python3 scripts/extract_entries.py                     # Todas las secciones
python3 scripts/extract_entries.py --file spells.txt   # Archivo específico
python3 scripts/extract_entries.py --output pending/   # Guardar pendientes
python3 scripts/extract_entries.py --section database  # Sección database
```

### Sincronizar con upstream

```bash
python3 scripts/sync_template.py                       # Detectar cambios nuevos
python3 scripts/sync_template.py --dry-run             # Vista previa
python3 scripts/sync_template.py --file items.txt      # Archivo específico
```

### Ordenar y validar

```bash
python3 scripts/sort_entries.py                        # Ordenar todo
python3 scripts/sort_entries.py --file items.txt       # Archivo específico
python3 scripts/check_translations.py                  # Validar todo
python3 scripts/check_translations.py --fix            # Corregir automático
```

### Actualizar referencia EN

```bash
python3 scripts/update_upstream.py --repo /ruta/al/crawl
```

## Flujo de trabajo

1. **Elegir un archivo** — mira `scripts/extract_entries.py --file <archivo>` para ver lo que falta
2. **Traducir** — edita `translations/descript/es/<archivo>.txt`
3. **Validar** — `python3 scripts/check_translations.py --file <archivo>`
4. **Verificar** — `python3 scripts/stats.py` para ver el progreso
5. **Commit** — cuando esté listo, abrir PR al [repo oficial](https://github.com/crawl/crawl)

### Formato de los archivos

```
%%%%
Spit Poison ability

Escupes veneno al monstruo que apuntes.
%%%%
```

- `%%%%` separa cada entrada
- La primera línea es la **clave** (siempre en inglés)
- Después de un salto de línea, la **traducción**
- `[[clave]]` para referencias a otras entradas
- `{{ código Lua }}` para lógica condicional
- `#` para comentarios

## Cómo contribuir

1. Haz un fork de [crawl/crawl](https://github.com/crawl/crawl) en GitHub
2. Traduce archivos en `crawl-ref/source/dat/descript/es/`
3. Abre un Pull Request

O si prefieres, haz PR directamente a este repositorio y sincronizamos.

## Licencia

GPLv2+ — igual que Dungeon Crawl Stone Soup.
