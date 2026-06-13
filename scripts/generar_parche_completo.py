#!/usr/bin/env python3
"""
Genera un parche unificado con TODOS los cambios de traducción UI.
Incluye:
  - Infraestructura (translation.h/.cc, startup/end hooks, Makefile)
  - Archivos de traducción (dat/ui/es/*.txt)
  - Modificaciones a newgame.cc y menu.cc (llamadas tr())
"""

import subprocess, sys, os

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = "/tmp/dcss-build-3"
BRANCH = "0.34.1"
REPO = "https://github.com/crawl/crawl.git"


def run(cmd, **kwargs):
    print(f"  -> {cmd}")
    return subprocess.run(cmd, shell=True, **kwargs)


print("=== GENERADOR DE PARCHE COMPLETO DCSS-ES ===")
print()

# 1. Clonar
print("[1/6] Clonando fuente...")
r = run(f"git clone --depth 1 --branch {BRANCH} {REPO} {SOURCE} 2>&1 | tail -2")
if r.returncode != 0:
    print("ERROR al clonar. ¿Ya existe?")
    sys.exit(1)

# 2. Aplicar infraestructura
print("[2/6] Aplicando infraestructura...")
os.chdir(f"{SOURCE}/crawl-ref/source")
run(f"git apply {PROJECT}/patches/0001-ui-translation-infra-full.diff")

# 3. Trasladar archivos de traducción
print("[3/6] Copiando archivos de traducción...")
run(f"cp {PROJECT}/translations/ui/es/menu.txt dat/ui/es/")

# 4. Modificar newgame.cc
print("[4/6] Modificando newgame.cc...")
with open("newgame.cc") as f:
    content = f.read()

# Añadir include
content = content.replace(
    '#include "english.h"', '#include "english.h"\n#include "translation.h"'
)

# Reemplazar cadenas estáticas
replacements = [
    # Pantalla de especie/trasfondo
    ('"+ - Recommended species"', 'tr("+ - Recommended species")'),
    ('"+ - Recommended background"', 'tr("+ - Recommended background")'),
    ('"# - Recommended character"', 'tr("# - Recommended character")'),
    ('"% - List aptitudes"', 'tr("% - List aptitudes")'),
    ('"? - Help"', 'tr("? - Help")'),
    ('"Opens the help screen."', 'tr("Opens the help screen.")'),
    (
        '"Lists the numerical skill train aptitudes for all races."',
        'tr("Lists the numerical skill train aptitudes for all races.")',
    ),
    # Pantalla de nombre
    ('"Esc - Quit"', 'tr("Esc - Quit")'),
    ('"* - Random name"', 'tr("* - Random name")'),
    ('formatted_string("Enter - Begin!"', 'formatted_string(tr("Enter - Begin!")'),
    (
        'formatted_string("That\'s a silly name!"',
        'formatted_string(tr("That\'s a silly name!")',
    ),
    (
        'prompt.cprintf("What is your name today? ")',
        'prompt.cprintf("%s", tr("What is your name today? ").c_str())',
    ),
    (
        'prompt.cprintf("You have an existing game under this name; really overwrite? [Y/n]")',
        'prompt.cprintf("%s", tr("You have an existing game under this name; really overwrite? [Y/n]").c_str())',
    ),
    (
        'make_shared<Text>("Do you want to play this combination? [Y/n/q]")',
        'make_shared<Text>(tr("Do you want to play this combination? [Y/n/q]"))',
    ),
    ('"No player name specified."', 'tr("No player name specified.")'),
    # Semilla personalizada
    ('"Seed: "', 'tr("Seed: ")'),
    (
        'set_child(make_shared<ui::Text>("Fully pregenerate the dungeon"))',
        'set_child(make_shared<ui::Text>(tr("Fully pregenerate the dungeon")))',
    ),
    ('formatted_string("[Enter] Begin!"', 'formatted_string(tr("[Enter] Begin!")'),
    ('formatted_string("[-] Clear"', 'formatted_string(tr("[-] Clear")'),
    (
        'formatted_string("[d] Today\'s daily seed"',
        'formatted_string(tr("[d] Today\'s daily seed")',
    ),
    # Armas
    ('"+ - Recommended random choice"', 'tr("+ - Recommended random choice")'),
    ('"* - Random weapon"', 'tr("* - Random weapon")'),
    ('"Picks a random recommended weapon"', 'tr("Picks a random recommended weapon")'),
    ('"Picks a random weapon"', 'tr("Picks a random weapon")'),
    ('"Bksp - Return to character menu"', 'tr("Bksp - Return to character menu")'),
    (
        '"Lets you return back to Character choice menu"',
        'tr("Lets you return back to Character choice menu")',
    ),
    ('"Select your old weapon"', 'tr("Select your old weapon")'),
    ('"You have a choice of weapons."', 'tr("You have a choice of weapons.")'),
    (
        '"Play a new game with your previous choice."',
        'tr("Play a new game with your previous choice.")',
    ),
    # Sprint / Tutorial
    ('"* - Random map"', 'tr("* - Random map")'),
    ('"Picks a random sprint map"', 'tr("Picks a random sprint map")'),
    (
        '"Select your previous sprint map and character"',
        'tr("Select your previous sprint map and character")',
    ),
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        print(f"    ✅ {old[:50]}...")
    else:
        print(f"    ⚠️  NO ENCONTRADO: {old[:50]}...")

# Caso especial: "Choose 0 for a random seed..."
old = '"Choose 0 for a random seed. "\n            "[Tab]/[Shift-Tab] to cycle input focus.\\n"'
new = 'tr("Choose 0 for a random seed. "\n            "[Tab]/[Shift-Tab] to cycle input focus.") + "\\n"'
if old in content:
    content = content.replace(old, new)
    print("    ✅ Choose 0... (multilínea)")
else:
    print("    ⚠️  NO ENCONTRADO: Choose 0... (multilínea)")

# Casos multilínea: Shuffles...
old1 = (
    '"Shuffles through random recommended character combinations "\n'
    '                "until you accept one."'
)
new1 = (
    'tr("Shuffles through random recommended character combinations "\n'
    '                "until you accept one.")'
)
content = content.replace(old1, new1)

old2 = (
    '"Shuffles through random character combinations "\n'
    '                "until you accept one."'
)
new2 = (
    'tr("Shuffles through random character combinations "\n'
    '                "until you accept one.")'
)
content = content.replace(old2, new2)

with open("newgame.cc", "w") as f:
    f.write(content)

# 5. Modificar menu.cc
print("[5/6] Modificando menu.cc...")
with open("menu.cc") as f:
    content = f.read()

content = content.replace(
    '#include "stringutil.h"', '#include "stringutil.h"\n#include "translation.h"'
)

content = content.replace(
    '"Select what (regex)?"', 'tr("Select what (regex)?").c_str()'
)

with open("menu.cc", "w") as f:
    f.write(content)

# 6. Generar cabeceras y crear parche
print("[6/6] Generando cabeceras y creando parche...")
run("python3 util/gen-all.py 2>&1 | grep -v Error")

os.chdir(SOURCE)
run("git add -A")
result = run("git diff --cached --no-color", capture_output=True, text=True)
patch_path = os.path.join(PROJECT, "patches", "0002-complete-menu-translations.patch")
with open(patch_path, "w") as f:
    f.write(result.stdout)

print(f"\n✅ Parche completo creado: {patch_path}")
print(f"   ({len(result.stdout)} bytes)")
print()
print("Para compilar:")
print(f"  cd {SOURCE}/crawl-ref/source")
print("  make -j$(nproc)")
print("  LANGUAGE=es ./crawl")
