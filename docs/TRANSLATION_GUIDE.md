# Guía de traducción de DCSS al español

## Convenciones

### Idioma

- **Español de España** exclusivamente. Nada de modismos latinoamericanos ni argentinos.
- Tuteo (tú) — no voseo.
- Registro formal para descripciones de objetos y hechizos.
- Registro más informal para diálogos de monstruos y mensajes de estado.

### Términos clave

| Inglés             | Español                | Notas                                        |
| ------------------ | ---------------------- | -------------------------------------------- |
| Spell              | Hechizo                |                                              |
| Ability            | Habilidad              |                                              |
| Skill              | Capacidad              | No "habilidad" (conflicto con ability)       |
| Species            | Raza                   |                                              |
| Background         | Trasfondo              | O "clase" según contexto                     |
| God/Deity          | Dios/Deidad            |                                              |
| Branch             | Rama                   | Mazmorra temática                            |
| Vault              | Bóveda                 | Sala especializada                           |
| Unique             | Único                  | Monstruo único                               |
| Artefact           | Artefacto              |                                              |
| Ego                | Cualidad               | De arma/armadura ("de fuego", "de escarcha") |
| Scroll             | Pergamino              |                                              |
| Potion             | Poción                 |                                              |
| Wand               | Vara                   |                                              |
| Orb of Zot         | Orbe de Zot            |                                              |
| Dungeon            | Mazmorra               |                                              |
| Floor              | Piso/Nivel             |                                              |
| Stairs             | Escaleras              |                                              |
| Trap               | Trampa                 |                                              |
| Monster            | Monstruo / Criatura    |                                              |
| Player             | Jugador / Personaje    |                                              |
| Hit Points (HP)    | Puntos de Vida (PV)    |                                              |
| Magic Points (MP)  | Puntos de Magia (PM)   |                                              |
| Armour Class (AC)  | Clase de Armadura (CA) |                                              |
| Experience (XP)    | Experiencia (EXP)      |                                              |
| Strength (STR)     | Fuerza (FUE)           |                                              |
| Dexterity (DEX)    | Destreza (DES)         |                                              |
| Intelligence (INT) | Inteligencia (INT)     |                                              |

### Verbos de combate

| Inglés | Español   |
| ------ | --------- |
| hit    | golpear   |
| slash  | cercenar  |
| stab   | apuñalar  |
| bite   | morder    |
| claw   | arañar    |
| smash  | aplastar  |
| burn   | quemar    |
| freeze | congelar  |
| poison | envenenar |
| zap    | fulminar  |
| engulf | envolver  |

### Nombres de Dioses (mantener original)

Los nombres de los dioses NO se traducen:

- Trog, Okawaru, Zin, Elyvilon, Sif Muna, etc.
- Los títulos descriptivos SÍ se traducen: "the Shining One" → "el Resplandeciente"

### Referencias [[key]]

Los archivos pueden contener referencias a otras entradas con `[[key]]`.
La clave siempre está en inglés (es el identificador). NO traducir las claves dentro de `[[...]]`.

Ejemplo:

```
Una poción curativa que restaura [[Healing]] puntos de vida.
```

### Código Lua {{ }}

Algunas descripciones contienen código Lua embebido entre `{{` y `}}`.

- Mantener la estructura del código Lua intacta
- Traducir solo los strings literales dentro del código
- Asegurarse de que `return` devuelve el texto en español

## Reglas de formato

1. `%%%%` al inicio y entre cada entrada
2. La clave SIEMPRE en inglés (primera línea tras `%%%%`)
3. Línea en blanco después de la clave
4. La traducción a continuación
5. Sin espacios al final de las líneas
6. UTF-8 sin BOM
7. Archivos ordenados alfabéticamente por clave
8. Las comillas se dejan en su idioma original (no traducir citas)
