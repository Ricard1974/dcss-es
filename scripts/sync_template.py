#!/usr/bin/env python3
"""
Sincroniza las traducciones con el upstream.
Detecta entradas nuevas, eliminadas o modificadas en los archivos
EN y actualiza los archivos ES en consecuencia.

Uso: python3 scripts/sync_template.py [--file FILENAME]
"""

import argparse
import re
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

PROJECT = Path(__file__).parent.parent
UPSTREAM_DESCRIPT = PROJECT / "upstream" / "descript"
UPSTREAM_DATABASE = PROJECT / "upstream" / "database"
TRANS_DESCRIPT = PROJECT / "translations" / "descript" / "es"
TRANS_DATABASE = PROJECT / "translations" / "database" / "es"


def parse_entries(filepath: Path) -> Dict[str, str]:
    """Parsea archivo DCSS a diccionario clave->valor."""
    entries = {}
    if not filepath.exists():
        return entries

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = re.split(r"\n?%%%%\s*\n?", content)
    for block in blocks:
        block = block.strip()
        if not block or block.startswith("#"):
            continue
        lines = block.split("\n", 1)
        key = lines[0].strip()
        value = lines[1].strip() if len(lines) > 1 else ""
        if key:
            entries[key] = value

    return entries


def build_file_content(entries: List[Tuple[str, str]]) -> str:
    """Construye el contenido del archivo .txt a partir de entradas ordenadas."""
    lines = []
    for key, value in entries:
        lines.append("%%%%")
        lines.append(key)
        lines.append("")
        if value:
            lines.append(value)
            lines.append("")
    lines.append("%%%%")
    return "\n".join(lines)


def sync_file(
    upstream_file: Path, trans_file: Path, dry_run: bool = False
) -> List[str]:
    """
    Sincroniza un archivo de traducción con su upstream.
    - Añade entradas nuevas que están en EN pero no en ES
    - Marca entradas eliminadas que están en ES pero no en EN
    Devuelve lista de acciones realizadas.
    """
    actions = []
    en_entries = parse_entries(upstream_file)
    es_entries = parse_entries(trans_file)

    en_keys = set(en_entries.keys())
    es_keys = set(es_entries.keys())

    # Entradas nuevas (en EN pero no en ES)
    new_keys = en_keys - es_keys
    for key in sorted(new_keys):
        actions.append(f"  ➕ NUEVA: {key}")

    # Entradas eliminadas (en ES pero no en EN)
    removed_keys = es_keys - en_keys
    for key in sorted(removed_keys):
        actions.append(f"  🗑️  OBSOLETA: {key}")

    if not new_keys and not removed_keys:
        actions.append("  ✅ Sin cambios")
        return actions

    if dry_run:
        return actions

    # Si no hay archivo ES, crear copia de EN
    if not trans_file.exists():
        shutil.copy2(upstream_file, trans_file)
        actions.append(f"  📝 Creado nuevo archivo: {trans_file.name}")
        return actions

    # Reconstruir el archivo: mantener entries ES existentes, añadir nuevas
    # Orden: entradas existentes en ES + nuevas entradas de EN
    new_entries = []

    # Primero las entradas ES existentes (que todavía existen en EN)
    for key, value in es_entries.items():
        if key in en_keys:
            new_entries.append((key, value))

    # Luego las nuevas entradas de EN (con texto EN como placeholder)
    for key in sorted(new_keys):
        new_entries.append((key, en_entries[key]))

    # Escribir archivo
    content = build_file_content(new_entries)
    with open(trans_file, "w", encoding="utf-8") as f:
        f.write(content)

    return actions


def main():
    parser = argparse.ArgumentParser(description="Sincroniza traducciones con upstream")
    parser.add_argument("--file", "-f", help="Archivo específico")
    parser.add_argument(
        "--section",
        choices=["descript", "database", "both"],
        default="descript",
        help="Sección a sincronizar",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Solo mostrar qué se haría, sin modificar",
    )
    args = parser.parse_args()

    if args.section in ("descript", "both"):
        upstream_dir = UPSTREAM_DESCRIPT
        trans_dir = TRANS_DESCRIPT
        section_name = "descript"

        print(f"\n📁 Sincronizando {section_name}/...")
        if args.file:
            files = [upstream_dir / args.file]
        else:
            files = sorted(upstream_dir.glob("*.txt"))

        for f in files:
            tf = trans_dir / f.name
            print(f"\n📄 {f.name}:")
            actions = sync_file(f, tf, dry_run=args.dry_run)
            for a in actions:
                print(a)

    if args.section in ("database", "both"):
        upstream_dir = UPSTREAM_DATABASE
        trans_dir = TRANS_DATABASE
        section_name = "database"

        print(f"\n📁 Sincronizando {section_name}/...")
        if args.file:
            files = [upstream_dir / args.file]
        else:
            files = sorted(upstream_dir.glob("*.txt"))

        trans_dir.mkdir(parents=True, exist_ok=True)

        for f in files:
            tf = trans_dir / f.name
            print(f"\n📄 {f.name}:")
            actions = sync_file(f, tf, dry_run=args.dry_run)
            for a in actions:
                print(a)

    if not args.dry_run:
        print(f"\n✅ Sincronización completada.")
        print(f"   Ejecuta 'python3 scripts/stats.py' para ver el estado actual.")


if __name__ == "__main__":
    main()
