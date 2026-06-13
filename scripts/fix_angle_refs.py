#!/usr/bin/env python3
"""
Corrige referencias <...> que LT tradujo como texto normal.

Lee el EN, identifica entradas con referencias <...>, y las retraduce
usando la protección mejorada del script translate_batch.py.

Uso:
  python3 scripts/fix_angle_refs.py                   # Corrige todo descript/
  python3 scripts/fix_angle_refs.py --file spells.txt  # Archivo específico
"""

import argparse
import re
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple

PROJECT = Path(__file__).parent.parent
TRANS_DESCRIPT = PROJECT / "translations" / "descript" / "es"
UPSTREAM_DESCRIPT = PROJECT / "upstream" / "descript"

# Reusar funciones del script principal
sys.path.insert(0, str(PROJECT / "scripts"))
from translate_batch import (
    translate_text,
    protect_game_terms,
    restore_game_terms,
    protect_patterns,
    restore_patterns,
    post_process,
    parse_entries,
    should_translate,
)


def find_affected_entries(
    upstream_file: Path, trans_file: Path
) -> List[Tuple[str, str, str]]:
    """
    Busca entradas en ES que contengan referencias <...> que LT tradujo mal.
    Devuelve [(key, en_value, es_value_corrupta), ...]
    """
    en_entries = dict(parse_entries(upstream_file))
    es_entries = dict(parse_entries(trans_file))

    # Encontrar <...> en el EN
    affected = []
    for key, en_value in en_entries.items():
        has_angle = bool(re.search(r"<[^>]+>", en_value))
        if not has_angle:
            continue
        if key not in es_entries:
            affected.append((key, en_value, ""))
        else:
            es_value = es_entries[key]
            # Verificar si LT se cargó las referencias <...>
            en_refs = set(re.findall(r"<[^>]+>", en_value))
            es_refs = set(re.findall(r"<[^>]+>", es_value) if es_value else set())
            if en_refs - es_refs:
                affected.append((key, en_value, es_value))

    return affected


def fix_file(upstream_file: Path, trans_file: Path, force: bool = False) -> int:
    """Corrige entradas con <...> en un archivo."""
    affected = find_affected_entries(upstream_file, trans_file)

    if not affected:
        print(f"  ✅ {upstream_file.name}: sin entradas con <...> corruptas")
        return 0

    print(
        f"  🔧 {upstream_file.name}: {len(affected)} entradas con <...> por retraducir"
    )

    # Cargar traducciones existentes
    existing = {}
    if trans_file.exists():
        existing = {k: v for k, v in parse_entries(trans_file)}

    fixed = 0
    for key, en_value, old_es_value in affected:
        if not en_value.strip():
            continue

        # 1. Proteger patrones PRIMERO (<...>, refs, lua, vars)
        #    Para que game_terms no toque lo que está DENTRO de <...>
        protected_text, placeholders = protect_patterns(en_value)

        # 2. Proteger términos del juego DESPUÉS
        game_protected, game_ph, game_trans = protect_game_terms(protected_text)

        # 3. Traducir
        translated = translate_text(game_protected)
        if translated is None:
            print(f"    ⚠️  {key}: fallo de traducción, se mantiene original")
            continue

        # 4. Restaurar términos del juego (inverso: restaurar ANTES que patrones)
        translated = restore_game_terms(translated, game_trans)

        # 5. Restaurar patrones (incluye <...> con valores originales)
        translated = restore_patterns(translated, placeholders)

        # 6. Post-procesar
        translated = post_process(translated)

        # Actualizar en existing
        existing[key] = translated
        fixed += 1

        # Progreso
        print(f"    ✅ {key}")
        time.sleep(0.5)

    if fixed > 0:
        # Reconstruir en orden EN
        en_entries = parse_entries(upstream_file)
        result_entries = []
        for k, en_v in en_entries:
            if k in existing:
                result_entries.append((k, existing[k]))
            else:
                result_entries.append((k, en_v))

        from translate_batch import write_entries

        write_entries(trans_file, result_entries)
        print(f"    📝 Guardado: {trans_file}")

    return fixed


def main():
    parser = argparse.ArgumentParser(
        description="Corrige referencias <...> en traducciones DCSS"
    )
    parser.add_argument("--file", "-f", help="Archivo específico a corregir")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Retraducir incluso si ya tiene <...> preservadas",
    )
    args = parser.parse_args()

    if args.file:
        files = [(UPSTREAM_DESCRIPT / args.file, TRANS_DESCRIPT / args.file)]
    else:
        files = [
            (f, TRANS_DESCRIPT / f.name)
            for f in sorted(UPSTREAM_DESCRIPT.glob("*.txt"))
        ]

    total = 0
    for up_file, tr_file in files:
        if not tr_file.exists():
            continue
        fixed = fix_file(up_file, tr_file, force=args.force)
        total += fixed

    if total > 0:
        print(f"\n{'=' * 50}")
        print(f"✅ Total: {total} entradas corregidas")
        print(f"{'=' * 50}")
    else:
        print("\n✅ No hay entradas que corregir")


if __name__ == "__main__":
    main()
