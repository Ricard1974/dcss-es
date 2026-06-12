#!/usr/bin/env python3
"""
Extrae entradas sin traducir: compara upstream/ (inglés) con
translations/ (español) y muestra las que faltan.

Uso: python3 scripts/extract_entries.py [--file FILENAME] [--missing] [--output DIR]
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple

PROJECT = Path(__file__).parent.parent
UPSTREAM_DESCRIPT = PROJECT / "upstream" / "descript"
UPSTREAM_DATABASE = PROJECT / "upstream" / "database"
TRANS_DESCRIPT = PROJECT / "translations" / "descript" / "es"
TRANS_DATABASE = PROJECT / "translations" / "database" / "es"


def parse_entries(filepath: Path) -> List[Tuple[str, str]]:
    """
    Parsea un archivo de texto de DCSS.
    Devuelve lista de (clave, valor) por cada entrada %%%%.
    """
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
        # Saltar comentarios (líneas que empiezan con #)
        if block.startswith("#"):
            continue
        lines = block.split("\n", 1)
        key = lines[0].strip()
        value = lines[1].strip() if len(lines) > 1 else ""
        if key:
            entries.append((key, value))

    return entries


def get_entry_keys(filepath: Path) -> set:
    """Obtiene solo las claves de un archivo de entradas."""
    return {key for key, _ in parse_entries(filepath)}


def find_missing(upstream_file: Path, trans_file: Path) -> List[str]:
    """Encuentra entradas presentes en upstream pero no en traducción."""
    en_keys = get_entry_keys(upstream_file)
    es_keys = get_entry_keys(trans_file)
    return sorted(en_keys - es_keys)


def main():
    parser = argparse.ArgumentParser(description="Extrae entradas sin traducir")
    parser.add_argument("--file", "-f", help="Archivo específico (sin ruta)")
    parser.add_argument(
        "--missing",
        action="store_true",
        help="Solo mostrar entradas que faltan (por defecto)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Mostrar todas las entradas (traducidas y sin traducir)",
    )
    parser.add_argument(
        "--output", "-o", help="Directorio de salida para archivos pendientes"
    )
    parser.add_argument(
        "--section",
        choices=["descript", "database"],
        default="descript",
        help="Sección a analizar (descript o database)",
    )
    args = parser.parse_args()

    if args.section == "descript":
        upstream_dir = UPSTREAM_DESCRIPT
        trans_dir = TRANS_DESCRIPT
    else:
        upstream_dir = UPSTREAM_DATABASE
        trans_dir = TRANS_DATABASE

    if not upstream_dir.exists():
        print("Error: No se encuentra upstream/. Ejecuta: scripts/update_upstream.py")
        sys.exit(1)

    if args.file:
        files_to_check = [upstream_dir / args.file]
    else:
        files_to_check = sorted(upstream_dir.glob("*.txt"))

    total_missing = 0

    for upstream_file in files_to_check:
        if not upstream_file.exists():
            print(f"⚠️  {upstream_file.name} no existe en upstream")
            continue

        trans_file = trans_dir / upstream_file.name
        en_entries = parse_entries(upstream_file)
        es_entries = parse_entries(trans_file)
        es_keys = {k for k, _ in es_entries}

        en_count = len(en_entries)
        es_count = len(es_entries)
        missing = find_missing(upstream_file, trans_file)
        total_missing += len(missing)

        print(
            f"\n📄 {upstream_file.name}: {es_count}/{en_count} entradas traducidas "
            f"({es_count * 100 // en_count if en_count else 0}%)"
        )

        if args.all:
            # Mostrar todas las entradas EN con su estado
            for key, value in en_entries:
                if key in es_keys:
                    print(f"  ✅ {key}")
                else:
                    print(f"  ⬜ {key}")
        elif missing:
            print(f"  Faltan {len(missing)} entradas:")
            for key in missing[:20]:  # Mostrar max 20
                # Buscar el valor EN para contexto
                for ek, ev in en_entries:
                    if ek == key:
                        preview = ev[:80].replace("\n", " ")
                        print(f"    ⬜ {key}")
                        print(f"       → {preview}...")
                        break
            if len(missing) > 20:
                print(f"    ... y {len(missing) - 20} más")
        else:
            print(f"  ✅ ¡Completo!")

        # Generar archivo pendiente si se solicita
        if args.output and missing:
            out_dir = Path(args.output)
            out_dir.mkdir(parents=True, exist_ok=True)
            out_file = out_dir / f"pending_{upstream_file.name}"

            with open(out_file, "w", encoding="utf-8") as f:
                en_map = {k: v for k, v in en_entries}
                for key in missing:
                    f.write("%%%%\n")
                    f.write(f"{key}\n\n")
                    f.write(f"{en_map.get(key, '')}\n\n")

            print(f"  📝 Pendientes guardados en: {out_file}")

    print(f"\n{'=' * 50}")
    print(f"Total entradas sin traducir: {total_missing}")
    print(f"{'=' * 50}")


if __name__ == "__main__":
    main()
