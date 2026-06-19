#!/usr/bin/env python3
"""Aplica tr() calls a newgame.cc - maneja multilínea correctamente"""

import re
import sys


def main():
    filepath = sys.argv[1] if len(sys.argv) > 1 else "newgame.cc"

    with open(filepath, "r") as f:
        content = f.read()

    # 1. Añadir include despues de #include "english.h"
    content = content.replace(
        '#include "english.h"', '#include "english.h"\n#include "translation.h"'
    )

    # 2. Reemplazos línea por línea
    replacements = [
        ('"+ - Recommended species"', 'tr("+ - Recommended species")'),
        ('"+ - Recommended background"', 'tr("+ - Recommended background")'),
        ('"# - Recommended character"', 'tr("# - Recommended character")'),
        ('"% - List aptitudes"', 'tr("% - List aptitudes")'),
        (
            '"Lists the numerical skill train aptitudes for all races."',
            'tr("Lists the numerical skill train aptitudes for all races.")',
        ),
        ('"? - Help"', 'tr("? - Help")'),
        ('"Opens the help screen."', 'tr("Opens the help screen.")'),
        ('"Esc - Quit"', 'tr("Esc - Quit")'),
        ('"* - Random name"', 'tr("* - Random name")'),
        ('formatted_string("Enter - Begin!"', 'formatted_string(tr("Enter - Begin!")'),
        (
            'formatted_string("That\'s a silly name!"',
            'formatted_string(tr("That\'s a silly name!")',
        ),
        (
            'make_shared<Text>("Do you want to play this combination? [Y/n/q]"))',
            'make_shared<Text>(tr("Do you want to play this combination? [Y/n/q]")))',
        ),
        (
            'prompt.cprintf("What is your name today? ")',
            'prompt.cprintf("%s", tr("What is your name today? ").c_str())',
        ),
        ('"Seed: "', 'tr("Seed: ")'),
        (
            'set_child(make_shared<ui::Text>("Fully pregenerate the dungeon"))',
            'set_child(make_shared<ui::Text>(tr("Fully pregenerate the dungeon")))',
        ),
    ]

    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            print(f"OK: {old[:50]}")
        else:
            print(f"SKIP: {old[:50]} (not found)")

    # 3. Caso especial: overwrite (sin parentesis extra en la cadena)
    # Original: prompt.cprintf("You have an existing game under this name; really overwrite? [Y/n]");
    old = 'prompt.cprintf("You have an existing game under this name; really overwrite? [Y/n]");'
    new = 'prompt.cprintf("%s", tr("You have an existing game under this name; really overwrite? [Y/n]").c_str());'
    if old in content:
        content = content.replace(old, new)
        print("OK: overwrite prompt")
    else:
        # Buscar líneas con overwrite que contengan cprintf
        for i, line in enumerate(content.split("\n")):
            if "overwrite" in line and "cprintf" in line:
                print(f"  WARN - Find line {i}: {line.strip()}")

    # 4. Caso especial: Choose 0 multilinea
    lines = content.split("\n")
    for i, line in enumerate(lines):
        if 'const string body_text = "Choose 0 for a random seed. "' in line:
            old = line + "\n" + lines[i + 1]
            # Preservar indentacion original pero envolver en tr()
            indent1 = line[: len(line) - len(line.lstrip())]
            indent2 = lines[i + 1][: len(lines[i + 1]) - len(lines[i + 1].lstrip())]
            new = f'{indent1}const string body_text = tr("Choose 0 for a random seed. "\n{indent2}"[Tab]/[Shift-Tab] to cycle input focus.\\n");'
            content = content.replace(old, new)
            print("OK: Choose 0 / cycle focus")
            break

    with open(filepath, "w") as f:
        f.write(content)

    print("\nDone!")


if __name__ == "__main__":
    main()
