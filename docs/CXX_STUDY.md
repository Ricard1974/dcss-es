# Estudio: Traducción de cadenas C++ en DCSS

## Contexto

Actualmente DCSS solo tiene un sistema de traducción para **texto externo**:

- `dat/descript/<lang>/` — descripciones de monstruos, objetos, hechizos, etc.
- `dat/database/<lang>/` — diálogos, voces, nombres aleatorios

El **texto de la interfaz** (menús, mensajes de combate, estado, ayudas)
está hardcodeado directamente en C++ mediante string literales.
No existe ningún sistema de internacionalización (gettext, i18n, etc.).

## Alcance

| Métrica                         | Valor        |
| ------------------------------- | ------------ |
| Archivos fuente con UI          | ~23          |
| Cadenas totales estimadas       | ~3.500-4.000 |
| Cadenas simples (sin formato)   | ~3.100 (89%) |
| Cadenas con formato (%s, %d, @) | ~350 (11%)   |

## Categorías de cadenas

### 1. Simples (fáciles)

Texto plano sin variables. Ej:

```
"Good luck, %s!"  →  "¡Buena suerte, %s!"
"Press ? for help"  →  "Pulsa ? para ayuda"
"You die..."  →  "Has muerto..."
```

### 2. Con formato de posición (medias)

Usan `%s`, `%d`, etc. para insertar nombres. El desafío es que
el orden de palabras cambia entre inglés y español:

```
"You hit the %s"  →  "Golpeas a %s"  (orden cambiado)
"%s is confused"  →  "%s está confundido" (género)
```

### 3. Con @variables@ (complejas)

Usan el sistema de marcadores del juego (similar a database/):

```
"The @monster@ hits you!"  →  "@monster@ te golpea"
```

### 4. Compuestas (muy complejas)

Cadenas que se construyen concatenando fragmentos. Ej:

```
you.props["fight_msg"].get_string() + "!"
```

o mensajes que dependen del género del monstruo/jugador.

## Estrategias posibles

### A. Parchear el código fuente (recomendada)

**Idea**: Modificar DCSS para que las cadenas de UI se carguen
desde archivos de texto, igual que las descripciones.

**Ventajas**:

- Las traducciones serían archivos .txt independientes
- Se podría actualizar sin recompilar
- Mismo mecanismo que descript/database

**Desventajas**:

- Requiere modificar el código C++ (cientos de cambios)
- Necesitas compilar el juego para probar
- El PR al upstream sería muy grande

**Esfuerzo estimado**: 2-3 semanas (programación + traducción)

### B. Parche post-compilación (no recomendada)

**Idea**: Modificar el binario compilado para reemplazar cadenas.

**Ventajas**: No requiere recompilar.

**Desventajas**: Frágil, ilegal en muchos casos, solo funciona
para esta versión exacta.

### C. Script de parcheo automático

**Idea**: Script Python que modifica los .cc para reemplazar
string literales por llamadas a una función de traducción.

**Ventajas**: Semiautomático, puedes iterar rápido.

**Desventajas**: El código resultante necesita revisión humana.

## Enfoque recomendado: Estrategia A (parche al código)

### Fase 1: Añadir infraestructura de traducción

1. Crear `translation.h` y `translation.cc` con funciones:

   ```cpp
   string tr(const string &key);  // lookup por clave
   string tr(const string &key, const string &fallback);
   ```

2. Añadir directorio `dat/ui/<lang>/` para archivos de UI:
   ```
   dat/ui/es/menu.txt
   dat/ui/es/combat.txt
   dat/ui/es/status.txt
   ...
   ```

### Fase 2: Migrar cadenas gradualmente

Por orden de impacto visual:

| Prioridad | Archivo                       | Cadenas | Impacto                        |
| --------- | ----------------------------- | ------- | ------------------------------ |
| 1         | `menu.cc`, `newgame.cc`       | ~250    | Menú principal y selección     |
| 2         | `output.cc`                   | ~330    | Barra de estado (HP, MP, etc.) |
| 3         | `fight.cc`, `melee_attack.cc` | ~400    | Mensajes de combate            |
| 4         | `skills.cc`, `ability.cc`     | ~700    | Pantallas de capacidades       |
| 5         | `religion.cc`                 | ~450    | Interfaz de dioses             |
| 6         | `hints.cc`                    | ~440    | Ayuda y tutorial               |
| 7         | `command.cc`                  | ~315    | Lista de comandos              |
| 8         | `invent.cc`, `shopping.cc`    | ~360    | Inventario y tiendas           |
| 9         | Resto                         | ~1.000  | Varios                         |

### Fase 3: Probar y refinar

- Compilar el juego con los cambios
- Probar cada pantalla
- Ajustar traducciones según contexto

## Conclusión

La fase 2 es un proyecto **grande pero factible**.

- Sin prisa: 2-3 semanas de trabajo intermitente
- El resultado sería la traducción más completa de DCSS hasta la fecha
- Ningún otro idioma ha tackledo las cadenas C++ (seríamos pioneros)

## Referencias

- Código fuente: `/tmp/crawl-source/crawl-ref/source/`
- Archivos clave: menu.cc, newgame.cc, output.cc, fight.cc, skills.cc
- Sistema actual de traducción: `database.cc`, `TextDB`
