#!/usr/bin/env python3
"""
Valida la integridad de los archivos de traducción:
- Formato correcto (%%%%, clave, valor)
- Referencias [[key]] válidas (que existan)
- Sintaxis Lua {{ }} básica
- Sin caracteres extraños o BOM

Uso: python3 scripts/check_translations.py [--file FILENAME] [--fix]
"""

import argparse
import re
from pathlib import Path
from typing import List, Tuple

PROJECT = Path(__file__).parent.parent
TRANS_DESCRIPT = PROJECT / "translations" / "descript" / "es"
TRANS_DATABASE = PROJECT / "translations" / "database" / "es"
UPSTREAM_DESCRIPT = PROJECT / "upstream" / "descript"


def get_all_keys() -> set:
    """Obtiene todas las claves disponibles en upstream (para validar referencias)."""
    keys = set()
    for f in UPSTREAM_DESCRIPT.glob("*.txt"):
        with open(f, "r", encoding="utf-8") as fh:
            content = fh.read()
        blocks = re.split(r"\n?%%%%\s*\n?", content)
        for block in blocks:
            if block.strip() and not block.startswith("#"):
                key = block.split("\n")[0].strip()
                if key:
                    keys.add(key.lower())
    return keys


def check_file(filepath: Path, all_keys: set) -> List[Tuple[str, str, int]]:
    """
    Valida un archivo de traducción.
    Devuelve lista de (tipo, mensaje, línea).
    """
    issues = []
    if not filepath.exists():
        return [("ERROR", f"Archivo no encontrado: {filepath}", 0)]

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        lines = content.split("\n")

    # Check BOM
    if len(content) > 0 and ord(content[0]) == 0xFEFF:
        issues.append(("WARN", "Archivo tiene BOM (Byte Order Mark)", 1))

    # Parse entries and check
    blocks = re.split(r"\n?%%%%\s*\n?", content)
    line_num = 0

    for block in blocks:
        block = block.strip()
        if not block:
            continue
        if block.startswith("#"):
            continue

        # Verificar que hay clave
        if "\n" not in block and len(block) < 200:
            # Entrada de una sola línea (solo clave, sin descripción) - OK
            key = block
        else:
            key = block.split("\n")[0].strip()

        if not key:
            issues.append(("ERROR", "Entrada sin clave", line_num))
            continue

        # Verificar referencias [[key]]
        refs = re.findall(r"\[\[([^\]]+)\]\]", block)
        for ref in refs:
            ref_lower = ref.strip().lower()
            if ref_lower not in all_keys:
                issues.append(
                    ("WARN", f"Referencia a clave inexistente: [[{ref}]]", line_num)
                )

        # Verificar bloques Lua {{ }}
        lua_blocks = re.findall(r"\{\{(.*?)\}\}", block, re.DOTALL)
        for lua in lua_blocks:
            # Verificar que tiene return
            if "return" not in lua:
                issues.append(("WARN", "Bloque Lua sin 'return'", line_num))
            # Verificar paréntesis balanceados
            if lua.count("(") != lua.count(")"):
                issues.append(
                    ("ERROR", "Paréntesis desbalanceados en bloque Lua", line_num)
                )
            if lua.count("{") != lua.count("}"):
                issues.append(
                    ("ERROR", "Llaves desbalanceadas en bloque Lua", line_num)
                )

        line_num += block.count("\n") + 1

    # Check trailing whitespace
    for i, line in enumerate(lines, 1):
        if line != line.rstrip() and not line.startswith("#"):
            issues.append(("STYLE", "Espacios al final de línea", i))

    return issues


def main():
    parser = argparse.ArgumentParser(description="Valida archivos de traducción")
    parser.add_argument("--file", "-f", help="Archivo específico")
    parser.add_argument(
        "--fix", action="store_true", help="Corregir problemas automáticos"
    )
    args = parser.parse_args()

    all_keys = get_all_keys()

    for section_dir in [TRANS_DESCRIPT, TRANS_DATABASE]:
        if not section_dir.exists():
            continue

        if args.file:
            files = [section_dir / args.file]
        else:
            files = sorted(section_dir.glob("*.txt"))

        for f in files:
            if not f.exists():
                continue

            issues = check_file(f, all_keys)
            if not issues:
                print(f"✅ {f.name} — sin problemas")
            else:
                print(f"\n📄 {f.name} — {len(issues)} problema(s):")
                for typ, msg, line in issues:
                    icon = {"ERROR": "❌", "WARN": "⚠️", "STYLE": "📝"}.get(typ, "❓")
                    line_info = f" (línea {line})" if line else ""
                    print(f"  {icon} [{typ}] {msg}{line_info}")

                if args.fix:
                    # Corregir trailing whitespace
                    if any(t == "STYLE" for t, _, _ in issues):
                        with open(f, "r", encoding="utf-8") as fh:
                            content = fh.read()
                        fixed = "\n".join(line.rstrip() for line in content.split("\n"))
                        with open(f, "w", encoding="utf-8") as fh:
                            fh.write(fixed)
                        print(f"  📝 Corregidos espacios al final de línea")


if __name__ == "__main__":
    main()
