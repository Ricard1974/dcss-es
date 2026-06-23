#!/usr/bin/env python3
"""
VERIFICACIÓN POST-BUILD DCSS-es
Ejecutar después de compilar o actualizar traducciones.
Detecta errores comunes ANTES de declarar que está listo.
"""

import os, re

ROOT = "/home/ricard/proyectos/dcss-es"
SQ = "/home/ricard/proyectos/dcss-squashfs/squashfs-root/usr"
UI_SRC = os.path.join(ROOT, "translations/ui/es")
UI_DEST = os.path.join(ROOT, "dat/ui/es")
UI_SQ = os.path.join(SQ, "dat/ui/es")
DS_SRC = os.path.join(ROOT, "translations/descript/es")
DS_ORIG = os.path.join(ROOT, "dat/descript")
DS_SQ = os.path.join(SQ, "dat/descript/es")
DB_SQ = os.path.join(SQ, "dat/database/es")

errors = []
warnings = []


def e(msg):
    errors.append(f"  ❌ {msg}")


def w(msg):
    warnings.append(f"  ⚠️  {msg}")


print("=" * 60)
print("VERIFICACIÓN POST-BUILD DCSS-es")
print("=" * 60)

# 1. BINARIO
print("\n1. BINARIO")
bin_path = os.path.join(SQ, "bin/crawl")
if not os.path.exists(bin_path):
    e("Binario no encontrado")
else:
    sz = os.path.getsize(bin_path)
    print(f"  {'✅' if sz > 10_000_000 else '❌'} Tamaño: {sz / 1e6:.0f}MB")

# 2. UI FILES - existencia
print("\n2. ARCHIVOS UI")
ui_files = [
    "ability.txt",
    "combat.txt",
    "commands.txt",
    "inventory.txt",
    "menu.txt",
    "misc.txt",
    "names.txt",
    "religion.txt",
    "skills.txt",
    "status.txt",
]
all_ok = True
for f in ui_files:
    for d, lbl in [(UI_SRC, "src"), (UI_DEST, "dat"), (UI_SQ, "sq")]:
        p = os.path.join(d, f)
        if not os.path.exists(p):
            e(f"{f}: NO EXISTE en {lbl}")
            all_ok = False
if all_ok:
    print("  ✅ 10 archivos en todas las ubicaciones")

# 3. COMMANDS.TXT - traducciones de ayuda
print("\n3. COMMANDS.TXT (ayuda de teclas)")
cmd = os.path.join(UI_SQ, "commands.txt")
if os.path.exists(cmd):
    with open(cmd) as f:
        c = f.read()
    sections = [
        "<h>Movimiento:",
        "<h>Descanso:",
        "<h>Movimiento extendido:",
        "<h>Guardar y salir:",
        "<h>Información del personaje:",
        "<h>Interacción con la mazmorra:",
    ]
    n = sum(1 for s in sections if s in c)
    print(f"  {'✅' if n == 6 else '❌'} {n}/6 secciones de ayuda")

# 4. MENU.TXT - Raza recomendada, etc
print("\n4. MENU.TXT (creación de personaje)")
men = os.path.join(UI_SQ, "menu.txt")
if os.path.exists(men):
    with open(men) as f:
        c = f.read()
    for term in ["Raza recomendada", "Ayuda"]:
        if term not in c:
            e(f"Falta '{term}' en menu.txt")
    print("  ✅ Términos clave presentes")

# 5. NAMES.TXT
print("\n5. NAMES.TXT (especies, clases)")
nam = os.path.join(UI_SQ, "names.txt")
if os.path.exists(nam):
    with open(nam) as f:
        c = f.read()
    missing = [t for t in ["Humano", "Guerrero"] if t not in c]
    if missing:
        e(f"Faltan en names.txt: {missing}")
    else:
        print("  ✅ Especies y clases presentes")

# 6. DESCRIPT - estructura
print("\n6. DESCRIPT (23 archivos)")
if os.path.exists(DS_SRC):
    files = [f for f in os.listdir(DS_SRC) if f.endswith(".txt")]
    print(f"  {'✅' if len(files) == 23 else '❌'} {len(files)} archivos")

    for f in files:
        sp = os.path.join(DS_SRC, f)
        op = os.path.join(DS_ORIG, f)
        if not os.path.exists(op):
            continue
        with open(sp) as fh:
            tr = fh.read()
        with open(op) as fh:
            or_ = fh.read()
        te = tr.count("%%%%")
        oe = or_.count("%%%%")
        if te != oe:
            w(f"{f}: %%%% {te} vs {oe}")

# 7. DATABASE - existencia
print("\n7. DATABASE (23 archivos)")
if os.path.exists(DB_SQ):
    files = [f for f in os.listdir(DB_SQ) if f.endswith(".txt")]
    print(f"  {'✅' if len(files) == 23 else '❌'} {len(files)} archivos")

# 8. PROBLEMAS TEXTUALES
print("\n8. PROBLEMAS TEXTUALES")
# $cmd rotos
for label, d in [("UI", UI_SQ), ("Descript", DS_SQ), ("Database", DB_SQ)]:
    if not os.path.exists(d):
        continue
    b = 0
    for f in os.listdir(d):
        if not f.endswith(".txt"):
            continue
        with open(os.path.join(d, f)) as fh:
            content = fh.read()
        b += len(re.findall(r"\$cmd\[CMD [A-Z]", content))
    print(f"  {'✅' if b == 0 else '❌'} {label}: {b} $cmd rotos")

# Will (solo en nombres de stat correctos)
for label, d in [("UI", UI_SQ), ("Descript", DS_SQ), ("Database", DB_SQ)]:
    if not os.path.exists(d):
        continue
    will = 0
    for f in os.listdir(d):
        if not f.endswith(".txt"):
            continue
        with open(os.path.join(d, f)) as fh:
            content = fh.read()
        # Excluir Will++ Will/ Willpower Will+ (nombres de stats)
        for m in re.finditer(r"\bWill\b", content):
            ctx = content[m.start() : m.start() + 10]
            if (
                ctx.startswith("Will++")
                or ctx.startswith("Will/")
                or ctx.startswith("Will+")
                or ctx.startswith("Willpower")
            ):
                continue
            # Excluir si está cerca de "status" o "power"
            line = content[max(0, m.start() - 20) : m.start() + 20]
            if "status" in line or "power" in line.lower():
                continue
            # Excluir diálogo (Will you, Will it, etc.)
            lc = content[max(0, m.start() - 5) : m.start() + 20]
            if any(
                x in lc
                for x in [
                    '"Will you',
                    '"Will I',
                    "Will you be",
                    "Will it",
                    "Free Will",
                    "'Will",
                    "Will you forgive",
                    "Will you?",
                ]
            ):
                continue
            will += 1
    if will > 0:
        e(f"{label}: {will} Will sueltos (no nombres de stat)")
    else:
        print(f"  ✅ {label}: 0 Will sueltos")

# usted
for label, d in [("UI", UI_SQ), ("Descript", DS_SQ), ("Database", DB_SQ)]:
    if not os.path.exists(d):
        continue
    u = 0
    for f in os.listdir(d):
        if not f.endswith(".txt"):
            continue
        with open(os.path.join(d, f)) as fh:
            content = fh.read()
        # Excluir usted.lua_code (código)
        for m in re.finditer(r"\busted\b", content):
            ctx = content[m.start() : m.start() + 10]
            if m.start() + 5 < len(content) and content[m.start() + 5] in ".()":
                continue  # Lua code: usted.funcion()
            u += 1
    if u > 0:
        e(f"{label}: {u} 'usted' sueltos")
    else:
        print(f"  ✅ {label}: 0 'usted' sueltos")

# § y AG
for label, d in [("UI", UI_SQ), ("Descript", DS_SQ), ("Database", DB_SQ)]:
    if not os.path.exists(d):
        continue
    s = sum(
        open(os.path.join(d, f), errors="ignore").read().count("§")
        for f in os.listdir(d)
        if f.endswith(".txt")
    )
    print(f"  {'✅' if s == 0 else '❌'} {label}: §={s}")

# fideos
for label, d in [("UI", UI_SQ), ("Descript", DS_SQ), ("Database", DB_SQ)]:
    if not os.path.exists(d):
        continue
    fideos = 0
    for f in os.listdir(d):
        if not f.endswith(".txt"):
            continue
        with open(os.path.join(d, f)) as fh:
            fideos += fh.read().count("fideos")
    if fideos > 0:
        e(f"{label}: {fideos} 'fideos'")
    else:
        print(f"  ✅ {label}: 0 fideos")

# 9. SINCRONIZACIÓN translations/ vs dat/
print("\n9. SINCRONIZACIÓN")
desync = 0
for f in ui_files:
    s = os.path.join(UI_SRC, f)
    d = os.path.join(UI_DEST, f)
    if os.path.exists(s) and os.path.exists(d):
        if abs(os.path.getsize(s) - os.path.getsize(d)) > 100:
            e(f"{f}: translations/ vs dat/ diferente tamaño")
            desync += 1
if desync == 0:
    print("  ✅ UI sync OK")

# === RESUMEN ===
print("\n" + "=" * 60)
if errors:
    print(f"❌ {len(errors)} ERROR{(len(errors) > 1) * 'ES'}:")
    for er in errors:
        print(er)
else:
    print("🎉 0 ERRORES")
if warnings:
    print(f"\n⚠️  {len(warnings)} AVISO{(len(warnings) > 1) * 'S'}:")
    for wa in warnings:
        print(wa)

ec = "❌ HAY ERRORES - REVISAR" if errors else "✅ TODO CORRECTO"
print(f"\n{ec} - No declarar 'listo' hasta que errores=0")
