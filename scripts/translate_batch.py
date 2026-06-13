#!/usr/bin/env python3
"""
Traducción masiva de archivos DCSS usando LibreTranslate local.

Protege:
- Claves (primera línea de cada entrada, siempre en inglés)
- Referencias [[key]]
- Código Lua {{ }}
- Marcadores @variable@
- Números y placeholders

Uso:
  python3 scripts/translate_batch.py --file spells.txt         # Archivo específico
  python3 scripts/translate_batch.py --section descript        # Todo descript
  python3 scripts/translate_batch.py --missing                 # Solo lo que falta
  python3 scripts/translate_batch.py --dry-run                 # Vista previa
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib import request, error

PROJECT = Path(__file__).parent.parent
TRANS_DESCRIPT = PROJECT / "translations" / "descript" / "es"
TRANS_DATABASE = PROJECT / "translations" / "database" / "es"
UPSTREAM_DESCRIPT = PROJECT / "upstream" / "descript"
UPSTREAM_DATABASE = PROJECT / "upstream" / "database"

LIBRETRANSLATE_URL = "http://localhost:5000/translate"
DELAY_BETWEEN_REQUESTS = 0.5  # segundos para no saturar

# Cargar diccionario de términos DCSS
try:
    from terms import FORCED_TERMS, NO_TRANSLATE, POST_PROCESS

    FORCED = FORCED_TERMS
    NO_TRANS = NO_TRANSLATE
    POST_FIXES = POST_PROCESS
    print(
        f"📖 Diccionario DCSS cargado: {len(FORCED)} términos forzados, "
        f"{len(NO_TRANS)} términos no traducir, {len(POST_FIXES)} correcciones"
    )
except ImportError as e:
    print(f"⚠️  No se pudo cargar terms.py: {e}")
    print("   Las traducciones se harán sin diccionario DCSS.")
    FORCED = {}
    NO_TRANS = set()
    POST_FIXES = []


def translate_text(text: str, source: str = "en", target: str = "es") -> Optional[str]:
    """Traduce un texto con LibreTranslate."""
    data = json.dumps(
        {
            "q": text,
            "source": source,
            "target": target,
        }
    ).encode("utf-8")

    req = request.Request(
        LIBRETRANSLATE_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        # Timeout adaptativo: 30s para textos normales, 120s para textos largos
        timeout = 120 if len(text) > 2000 else 30
        resp = request.urlopen(req, timeout=timeout)
        result = json.loads(resp.read().decode("utf-8"))
        return result.get("translatedText")
    except error.URLError as e:
        print(f"  ❌ Error de conexión con LibreTranslate: {e}")
        print(
            f"     ¿Está corriendo? docker compose -f ~/proyectos/libretranslate/docker-compose.yml up -d"
        )
        return None
    except json.JSONDecodeError as e:
        print(f"  ❌ Error al decodificar respuesta: {e}")
        return None


def protect_game_terms(text: str) -> Tuple[str, Dict[str, str], Dict[str, str]]:
    """
    Reemplaza términos del juego con placeholders para que LT no los mutile.

    Estrategia:
    - NO_TRANSLATE: proteger todos (LT los traduciría como palabras normales)
    - FORCED_TERMS: solo términos COMPUESTOS (2+ palabras, ej: "Deep Elf")
      Las palabras sueltas se las dejamos a LT y las corregimos con POST_PROCESS.

    Los placeholders usan formato §NT0§ que LT preserva aceptablemente.
    """
    placeholders = {}
    translations = {}
    counter = 0

    # 1. NO_TRANSLATE: proteger términos que LT mutilaría (case-insensitive)
    for term in sorted(NO_TRANS, key=lambda x: -len(x), reverse=True):
        key = f"§NT{counter}§"
        pattern = r"\b" + re.escape(term) + r"\b"
        if re.search(pattern, text, flags=re.IGNORECASE):
            placeholders[key] = term
            translations[key] = term
            text = re.sub(pattern, key, text, flags=re.IGNORECASE)
            counter += 1

    # 2. FORCED_TERMS: solo términos COMPUESTOS (2+ palabras, >4 caracteres)
    # Las palabras sueltas se las dejamos a LibreTranslate
    forced_items = [
        (en, es)
        for en, es in sorted(FORCED.items(), key=lambda x: -len(x[0]), reverse=True)
        if len(en.split()) >= 2 and len(en) > 4
    ]
    for en_term, es_term in forced_items:
        pattern = r"\b" + re.escape(en_term) + r"\b"
        if re.search(pattern, text):
            key = f"§GT{counter}§"
            placeholders[key] = en_term
            translations[key] = es_term
            text = re.sub(pattern, key, text)
            counter += 1

    return text, placeholders, translations


def restore_game_terms(text: str, translations: Dict[str, str]) -> str:
    """
    Restaura placeholders §NT0§, §GT0§ en el texto traducido.
    Busca el ID numérico incluso si los § están parcialmente dañados.
    """
    for key, es_value in sorted(translations.items(), reverse=True):
        m = re.search(r"§([GN]T\d+)§", key)
        if not m:
            continue
        ph_id = m.group(1)
        # Buscar variantes: §GT0§, §GT0, GT0§, GT0 suelto
        for pat in [
            rf"§?\s*{re.escape(ph_id)}\s*§?",
            rf"§\s*{re.escape(ph_id)}",
            rf"{re.escape(ph_id)}\s*§",
        ]:
            text = re.sub(pat, es_value, text)
    return text


def post_process(text: str) -> str:
    """
    Aplica correcciones post-traducción sobre el texto ya en español.
    Corrige errores comunes de LibreTranslate.
    """
    for pattern, replacement in POST_FIXES:
        if callable(replacement):
            text = re.sub(pattern, replacement, text)
        else:
            text = re.sub(pattern, replacement, text)
    return text


def protect_patterns(text: str) -> Tuple[str, Dict[str, str]]:
    """Protege patrones especiales reemplazándolos con placeholders."""
    placeholders = {}
    counter = 0

    # Proteger [[referencias]]
    def protect_ref(m):
        nonlocal counter
        key = f"__REF{counter}__"
        placeholders[key] = m.group(0)
        counter += 1
        return key

    text = re.sub(r"\[\[([^\]]+)\]\]", protect_ref, text)

    # Proteger {{código lua}}
    def protect_lua(m):
        nonlocal counter
        key = f"__LUA{counter}__"
        placeholders[key] = m.group(0)
        counter += 1
        return key

    text = re.sub(r"\{\{(.*?)\}\}", protect_lua, text, flags=re.DOTALL)

    # Proteger @variables@
    def protect_var(m):
        nonlocal counter
        key = f"__VAR{counter}__"
        placeholders[key] = m.group(0)
        counter += 1
        return key

    text = re.sub(r"@(\w+)@", protect_var, text)

    # Proteger <referencias> (habilidades, marcas de color, lugares, etc.)
    # Ej: <Berserk ability>, <lightred>, <Desolation>
    # Usamos §AG0§ (formato §...§ que LT respeta, como con los términos del juego)
    def protect_ref_angle(m):
        nonlocal counter
        key = f"§AG{counter}§"
        placeholders[key] = m.group(0)
        counter += 1
        return key

    text = re.sub(r"<[^>]+>", protect_ref_angle, text)

    return text, placeholders


def restore_patterns(text: str, placeholders: Dict[str, str]) -> str:
    """Restaura los patrones protegidos."""
    for key, value in sorted(placeholders.items(), reverse=True):
        # Intentar coincidencia exacta primero
        new_text = text.replace(key, value)
        if new_text != text:
            text = new_text
            continue
        # Si falló, buscar variantes con § rotos (LT tiende a separarlos)
        m = re.search(r"§?(\w+)\d+§?", key)
        if m:
            ph_root = m.group(1)  # ej: "REF", "LUA", "VAR", "AG"
            ph_id = re.search(r"\d+", key)
            if ph_id:
                # Buscar: REF0, REF 0, §REF0, etc.
                id_num = ph_id.group(0)
                for pat in [
                    rf"§?\s*{re.escape(ph_root)}\s*{re.escape(id_num)}\s*§?",
                    rf"§\s*{re.escape(ph_root)}\s*{re.escape(id_num)}",
                    rf"{re.escape(ph_root)}\s*{re.escape(id_num)}\s*§",
                ]:
                    text = re.sub(pat, value, text)
    return text


def parse_entries(filepath: Path) -> List[Tuple[str, str]]:
    """Parsea archivo DCSS a lista de (clave, valor)."""
    entries = []
    if not filepath.exists():
        return entries

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = re.split(r"\n?%%%%\s*\n?", content)
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        # Saltar líneas de comentario y secciones de cabecera
        # La primera entrada puede ir sin %%%% delante (precedida de comentarios)
        lines = block.split("\n")
        key = None
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                key = stripped
                break
        if key is None:
            continue
        # El valor es todo después del título
        value_lines = []
        found_key = False
        for line in lines:
            stripped = line.strip()
            if not found_key:
                if stripped and not stripped.startswith("#"):
                    found_key = True
                continue
            value_lines.append(line)
        value = "\n".join(value_lines).strip()
        if key:
            entries.append((key, value))

    return entries


def write_entries(filepath: Path, entries: List[Tuple[str, str]]):
    """Escribe entradas a archivo DCSS."""
    lines = []
    for key, value in entries:
        lines.append("%%%%")
        lines.append(key)
        lines.append("")
        if value:
            lines.append(value)
            lines.append("")
    lines.append("%%%%")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def should_translate(key: str) -> bool:
    """Determina si una entrada debe traducirse automáticamente."""
    lower_key = key.lower()

    # NO traducir entradas que son solo nombres/IDs
    skip_prefixes = [
        "_",  # Entradas internas (ej: _shouts_, _yells_)
    ]
    if any(lower_key.startswith(p) for p in skip_prefixes):
        return False

    return True


def get_existing_keys(trans_file: Path) -> set:
    """Obtiene las claves ya traducidas."""
    return {k for k, _ in parse_entries(trans_file)}


def translate_batch(
    upstream_file: Path,
    trans_file: Path,
    only_missing: bool = False,
    dry_run: bool = False,
    force: bool = False,
) -> int:
    """
    Traduce un archivo completo.
    Devuelve número de entradas traducidas.
    """
    en_entries = parse_entries(upstream_file)
    if not en_entries:
        print(f"  ⚠️  No hay entradas en {upstream_file.name}")
        return 0

    # Cargar traducciones existentes
    existing = {}
    if trans_file.exists():
        existing = {k: v for k, v in parse_entries(trans_file)}

    # Determinar qué traducir
    to_translate = []
    already_done = 0
    skipped = 0

    for key, value in en_entries:
        if key in existing and existing[key] and not force:
            already_done += 1
            continue
        if only_missing and key in existing:
            already_done += 1
            continue
        if not should_translate(key):
            skipped += 1
            continue
        to_translate.append((key, value))

    if not to_translate:
        print(f"  ✅ {upstream_file.name} — todo traducido ({already_done} entradas)")
        return 0

    if dry_run:
        print(
            f"  📋 {upstream_file.name}: {len(to_translate)} pendientes "
            f"({already_done} ya traducidas, {skipped} omitidas)"
        )
        for key, value in to_translate[:5]:
            preview = value[:80].replace("\n", " ")
            print(f"    ⬜ {key}: {preview}...")
        if len(to_translate) > 5:
            print(f"    ... y {len(to_translate) - 5} más")
        return len(to_translate)

    # Traducir
    print(f"\n  🌐 Traduciendo {upstream_file.name}: {len(to_translate)} entradas...")
    translated_count = 0

    # Almacenar nuevas traducciones: {key: translated_text}
    new_translations = {}

    for i, (key, value) in enumerate(to_translate):
        if not value.strip():
            # Entrada vacía, mantener como está
            new_translations[key] = ""
            continue

        # 1. Proteger patrones especiales PRIMERO (<...>, refs, lua, vars)
        #    Esto evita que game_terms traduzca contenido DENTRO de <...>
        protected_text, placeholders = protect_patterns(value)

        # 2. Proteger términos del juego (NO_TRANSLATE + FORCED) DESPUÉS
        #    Ya no pueden afectar a lo que está dentro de <...>
        game_protected, game_ph, game_trans = protect_game_terms(protected_text)

        # 3. Traducir con LibreTranslate
        translated = translate_text(game_protected)
        if translated is None:
            translated = value  # mantener original si falla
        else:
            translated_count += 1

        # 4. Restaurar términos del juego (inverso: restaurar DESPUÉS de patrones)
        #    No pueden colarse dentro de <...> porque esos ya están protegidos
        translated = restore_game_terms(translated, game_trans)

        # 5. Restaurar patrones especiales (incluye <...> ya con sus valores originales)
        translated = restore_patterns(translated, placeholders)

        # 6. Post-procesar correcciones de español
        translated = post_process(translated)

        new_translations[key] = translated

        # Progreso
        pct = (i + 1) * 100 // len(to_translate)
        bar = "█" * (pct // 10) + "░" * (10 - pct // 10)
        print(f"    [{bar}] {i + 1}/{len(to_translate)} ({pct}%)", end="\r")

        time.sleep(DELAY_BETWEEN_REQUESTS)

    print(f"\n    ✅ {translated_count} entradas traducidas de {len(to_translate)}")

    # Reconstruir en orden EN: mantener orden upstream, no alfabético
    # Prioridad: nueva traducción > existente > original EN (fallback)
    result_entries = []
    for key, en_value in en_entries:
        if key in new_translations:
            result_entries.append((key, new_translations[key]))
        elif key in existing:
            result_entries.append((key, existing[key]))
        else:
            # Entrada no traducible (ej: _internal_) o nueva sin traducir aún
            result_entries.append((key, en_value))

    write_entries(trans_file, result_entries)
    print(f"    📝 Guardado: {trans_file}")

    return translated_count


def get_files(args) -> List[Tuple[Path, Path, str]]:
    """Obtiene lista de (upstream_file, trans_file, section) a procesar."""
    files = []

    if args.section in ("descript", "both"):
        upstream_dir = UPSTREAM_DESCRIPT
        trans_dir = TRANS_DESCRIPT
        if args.file:
            files.append((upstream_dir / args.file, trans_dir / args.file, "descript"))
        else:
            for f in sorted(upstream_dir.glob("*.txt")):
                files.append((f, trans_dir / f.name, "descript"))

    if args.section in ("database", "both"):
        upstream_dir = UPSTREAM_DATABASE
        trans_dir = TRANS_DATABASE
        trans_dir.mkdir(parents=True, exist_ok=True)
        if args.file and args.section == "database":
            files.append((upstream_dir / args.file, trans_dir / args.file, "database"))
        elif args.section != "descript":
            for f in sorted(upstream_dir.glob("*.txt")):
                files.append((f, trans_dir / f.name, "database"))

    return files


def main():
    parser = argparse.ArgumentParser(description="Traducción masiva con LibreTranslate")
    parser.add_argument("--file", "-f", help="Archivo específico a traducir")
    parser.add_argument(
        "--section", choices=["descript", "database", "both"], default="descript"
    )
    parser.add_argument(
        "--missing", action="store_true", help="Solo traducir entradas que faltan"
    )
    parser.add_argument(
        "--force", action="store_true", help="Forzar retraducción aunque ya exista"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Solo mostrar qué se traduciría"
    )
    args = parser.parse_args()

    files = get_files(args)

    if not files:
        print("No hay archivos para procesar.")
        return

    total = 0
    for up_file, tr_file, section in files:
        if not up_file.exists():
            print(f"⚠️  No existe: {up_file}")
            continue
        translated = translate_batch(
            up_file,
            tr_file,
            only_missing=args.missing,
            dry_run=args.dry_run,
            force=args.force,
        )
        total += translated

    if not args.dry_run and total > 0:
        print(f"\n{'=' * 50}")
        print(f"✅ Total: {total} entradas traducidas")
        print(f"📊 Ejecuta 'python3 scripts/stats.py' para ver el estado")
        print(f"{'=' * 50}")
    elif args.dry_run:
        print(f"\n📋 Vista previa: {total} entradas pendientes")
        print(f"   Ejecuta sin --dry-run para traducirlas")


if __name__ == "__main__":
    main()
