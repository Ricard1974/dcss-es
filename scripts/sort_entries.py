#!/usr/bin/env python3
"""
Ordena alfabéticamente las entradas de un archivo de traducción de DCSS.
Los archivos de descript deben estar ordenados alfabéticamente por clave.

Uso: python3 scripts/sort_entries.py [--file FILENAME] [--section descript|database]
"""

import argparse
import re
from pathlib import Path

PROJECT = Path(__file__).parent.parent
TRANS_DESCRIPT = PROJECT / "translations" / "descript" / "es"
TRANS_DATABASE = PROJECT / "translations" / "database" / "es"


def parse_entries_ordered(filepath: Path):
    """Parsea entradas manteniendo metadatos."""
    entries = []
    if not filepath.exists():
        return entries

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = re.split(r"\n?%%%%\s*\n?", content)
    for block in blocks:
        if not block.strip():
            continue
        if block.startswith("#"):
            entries.append(("__comment__", block))
            continue
        lines = block.split("\n", 1)
        key = lines[0].strip()
        value = lines[1].strip() if len(lines) > 1 else ""
        if key:
            entries.append((key, value))

    return entries


def rebuild_sorted(entries):
    """Reconstruye el contenido con entradas ordenadas."""
    # Separar comentarios y entradas
    comments = [(k, v) for k, v in entries if k == "__comment__"]
    real_entries = [(k, v) for k, v in entries if k != "__comment__"]

    # Ordenar entradas alfabéticamente (case-insensitive)
    real_entries.sort(key=lambda x: x[0].lower())

    lines = []
    for key, value in real_entries:
        lines.append("%%%%")
        lines.append(key)
        lines.append("")
        if value:
            lines.append(value)
            lines.append("")
    lines.append("%%%%")

    # Añadir comentarios al final
    for _, comment in comments:
        lines.append(comment)

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Ordena entradas alfabéticamente")
    parser.add_argument("--file", "-f", help="Archivo específico")
    parser.add_argument(
        "--section", choices=["descript", "database"], default="descript"
    )
    args = parser.parse_args()

    if args.section == "descript":
        trans_dir = TRANS_DESCRIPT
    else:
        trans_dir = TRANS_DATABASE

    if args.file:
        files = [trans_dir / args.file]
    else:
        files = sorted(trans_dir.glob("*.txt"))

    for f in files:
        if not f.exists():
            continue
        entries = parse_entries_ordered(f)
        if not entries:
            continue

        # Verificar si ya está ordenado
        real_entries = [(k, v) for k, v in entries if k != "__comment__"]
        sorted_keys = sorted([k for k, _ in real_entries], key=str.lower)
        current_keys = [k for k, _ in real_entries]

        if sorted_keys == current_keys:
            print(f"✅ {f.name} ya está ordenado")
            continue

        content = rebuild_sorted(entries)
        with open(f, "w", encoding="utf-8") as out:
            out.write(content)
        print(f"📝 {f.name} ordenado ({len(real_entries)} entradas)")


if __name__ == "__main__":
    main()
