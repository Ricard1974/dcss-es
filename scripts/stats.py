#!/usr/bin/env python3
"""
Estadísticas de cobertura de la traducción al español de DCSS.
Compara archivos en upstream/ (inglés) con translations/ (español).

Uso: python3 scripts/stats.py [--json]
"""

import argparse
import json
import re
import os
import sys
from pathlib import Path

PROJECT = Path(__file__).parent.parent
UPSTREAM_DESCRIPT = PROJECT / "upstream" / "descript"
UPSTREAM_DATABASE = PROJECT / "upstream" / "database"
TRANS_DESCRIPT = PROJECT / "translations" / "descript" / "es"
TRANS_DATABASE = PROJECT / "translations" / "database" / "es"


def count_entries(filepath: Path) -> int:
    """Cuenta el número de entradas (separadas por %%%%) en un archivo."""
    if not filepath.exists():
        return 0
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    return len(re.findall(r"^%%%%", content, re.MULTILINE))


def count_lines(filepath: Path) -> int:
    """Cuenta líneas totales."""
    if not filepath.exists():
        return 0
    with open(filepath, "r", encoding="utf-8") as f:
        return sum(1 for _ in f)


def analyze_section(name: str, upstream_dir: Path, trans_dir: Path) -> dict:
    """Analiza una sección (descript o database)."""
    files = sorted(upstream_dir.glob("*.txt"))
    total_entries = 0
    total_translated = 0
    file_stats = []

    for f in files:
        en_entries = count_entries(f)
        total_entries += en_entries

        tf = trans_dir / f.name
        es_entries = count_entries(tf)
        total_translated += es_entries

        en_lines = count_lines(f)
        es_lines = count_lines(tf)

        pct = (es_entries / en_entries * 100) if en_entries > 0 else 0
        status = "✅" if pct >= 90 else "🟡" if pct >= 50 else "🔴" if pct > 0 else "⬜"

        file_stats.append(
            {
                "file": f.name,
                "en_entries": en_entries,
                "es_entries": es_entries,
                "en_lines": en_lines,
                "es_lines": es_lines,
                "coverage_pct": round(pct, 1),
                "status": status.strip(),
                "missing": en_entries - es_entries,
            }
        )

    overall_pct = (total_translated / total_entries * 100) if total_entries > 0 else 0

    return {
        "section": name,
        "total_en_entries": total_entries,
        "total_es_entries": total_translated,
        "overall_pct": round(overall_pct, 1),
        "files": file_stats,
    }


def print_report(descript_stats: dict, database_stats: dict, json_output: bool = False):
    """Imprime el informe de estadísticas."""
    if json_output:
        print(
            json.dumps(
                {
                    "descript": descript_stats,
                    "database": database_stats,
                },
                indent=2,
                ensure_ascii=False,
            )
        )
        return

    # Cabecera
    print("=" * 72)
    print("  DCSS - Estadísticas de traducción al español")
    print("=" * 72)
    print()

    for section_stats in [descript_stats, database_stats]:
        if not section_stats["files"]:
            continue

        print(f"📁 {section_stats['section']}/")
        print(
            f"   {section_stats['total_en_entries']} EN  →  {section_stats['total_es_entries']} ES  "
            f"({section_stats['overall_pct']}% completo)"
        )
        print("-" * 72)
        print(f"  {'Archivo':<30} {'EN':>5} {'ES':>5} {'%':>6} {'Faltan':>7}")
        print("-" * 72)

        for f in section_stats["files"]:
            pct_str = f"{f['coverage_pct']:.0f}%"
            print(
                f"  {f['status']} {f['file']:<28} {f['en_entries']:>5} {f['es_entries']:>5} "
                f"{pct_str:>6} {f['missing']:>7}"
            )

        print()

    # Totales
    total_en = descript_stats["total_en_entries"] + database_stats["total_en_entries"]
    total_es = descript_stats["total_es_entries"] + database_stats["total_es_entries"]
    total_pct = (total_es / total_en * 100) if total_en > 0 else 0
    missing = total_en - total_es

    print("=" * 72)
    print(f"  TOTAL: {total_en} EN  →  {total_es} ES  ({total_pct:.1f}%)")
    print(f"  Pendientes: {missing} entradas por traducir")
    print("=" * 72)


def main():
    parser = argparse.ArgumentParser(description="Estadísticas de traducción de DCSS")
    parser.add_argument("--json", action="store_true", help="Salida en JSON")
    args = parser.parse_args()

    if not UPSTREAM_DESCRIPT.exists():
        print("Error: No se encuentra upstream/. Ejecuta: scripts/update_upstream.py")
        sys.exit(1)

    descript_stats = analyze_section("descript", UPSTREAM_DESCRIPT, TRANS_DESCRIPT)
    database_stats = analyze_section("database", UPSTREAM_DATABASE, TRANS_DATABASE)

    print_report(descript_stats, database_stats, json_output=args.json)


if __name__ == "__main__":
    main()
