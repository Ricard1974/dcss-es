#!/usr/bin/env python3
"""
Limpieza de archivos de traducción UI de DCSS.
Elimina código C++ que se coló en los archivos .txt.

Uso: python3 scripts/cleanup_ui.py [--dry-run]
"""

import os
import re
import sys

BASE = os.path.expanduser("~/proyectos/dcss-es/translations/ui/es")


def is_cpp_en_string(s):
    """
    Determina si una cadena en inglés (lado izquierdo del pipe) es realmente
    código C++ y no una cadena de interfaz.
    """
    if not s:
        return False

    s_stripped = s.strip()

    # ── Patrones exactos de código C++ ──

    # Directivas de preprocesador
    if re.match(
        r"^#\s*(if|ifdef|ifndef|else|elif|endif|define|include|undef)", s_stripped
    ):
        return True

    # Palabras clave de C++ (solas, no dentro de texto inglés)
    cpp_keywords = [
        r"^if\s*\(",
        r"^else\b",
        r"^for\s*\(",
        r"^while\s*\(",
        r"^switch\s*\(",
        r"^case\s+\d+",
        r"^default:",
        r"^break;",
        r"^continue;",
        r"^return\b",
        r"^\}\s*",
        r"^\{\s*$",
        r"^const\s+\w+",
        r"^static\s+\w+",
        r"^auto\s+\w+",
        r"^void\s+\w+",
        r"^bool\s+\w+",
        r"^int\s+\w+",
    ]
    for pat in cpp_keywords:
        if re.match(pat, s_stripped):
            return True

    # Concatenación de cadenas C++ (ej: " + colour + ")
    if re.match(r"^\+\s+\w+\s+\+", s_stripped):
        return True

    # Operadores de asignación C++ (ej: "desc += |")
    if re.search(r"\w+\s+\+=", s_stripped):
        return True

    # Llamadas a funciones específicas de C++ del juego
    cpp_calls = [
        r"mprf\s*\(",
        r"simple_god_message\s*\(",
        r"getMiscString\s*\(",
        r"god_name\s*\(",
        r"ard\s*\(",
        r"you\.\w+",
        r"clua\.\w+",
        r"mark_milestone\s*\(",
        r"take_note\s*\(",
        r"_add_to_old_gifts\s*\(",
        r"_article_it\s*\(",
        r"_origin_monster_name\s*\(",
        r"_milestone_collectible\s*\(",
        r"_origin_is_original_equip\s*\(",
        r"item_is_orb\s*\(",
        r"talisman_type_name\s*\(",
        r"cols\.add",
        r"add_formatted",
        r"_add_insert",
        r"keycode_to_name",
        r"command_to_string",
        r"Version::",
        r"getRandMonNameString\s*\(",
        r"is_evil_god\s*\(",
        r"get_mutation_level\s*\(",
        r"_god_rejects_loveless\s*\(",
        r"spell_title\s*\(",
        r"milestone_check\s*\(",
        r"item\.\w+",
        r"talisman_type_name\s*\(",
        r"mprf_nocap\s*\(",
    ]
    for pat in cpp_calls:
        if re.search(pat, s_stripped):
            return True

    # Estructuras de datos C++ (constantes enum)
    cpp_constants = [
        r"\{ STAFF_\w+",
        r"\{ ARM_\w+",
        r"\{ WPN_\w+",
        r"\{ MI_\w+",
        r"\{ GEM_\w+",
        r"SLOT_\w+",
        r"SIZE_LITTLE|SIZE_MEDIUM|SIZE_LARGE|NUM_SIZE_LEVELS",
        r"DAMV_\w+",
        r"ARMF_\w+",
        r"MONS_\w+",
        r"BEAM_\w+",
        r"BRANCH_\w+",
        r"OBJ_\w+",
        r"AQ_\w+",
        r"MUT_\w+",
        r"TAG_MAJOR_VERSION",
        r"DESC_A",
        r"DRAGON_ARMOUR\s*\(",
        r"\.c_str\s*\(\)",
        r"\.base_type",
        r"\.orig_monnum",
        r"\.quantity",
    ]
    for pat in cpp_constants:
        if re.search(pat, s_stripped):
            return True

    # Traducciones literales de C++ que evidencian código mal traducido
    translated_cpp = [
        r"^[A-Z_]+\s*\([A-Z_]",  # LIKE_THIS(ARG
        r"^prefijo de cadena\b",
        r"^nombre de la cadena\b",
        r"^(tal vez|regreso|default|interruptor|ruptura|más)\s",
    ]
    for pat in translated_cpp:
        if re.search(pat, s_stripped):
            return True

    # Líneas que son claramente fragmentos de C++ traducidos
    cpp_residue_en = [
        "milestone_check",
        "milestone_collectible",
        "getMiscString",
        "getRandMonNameString",
        "is_evil_god",
        "get_mutation_level",
        "god_rejects_loveless",
        "spell_title",
        "article_it",
        "origin_monster_name",
        "origin_is_original_equip",
        "item_is_orb",
        "talisman_type_name",
        "keycode_to_name",
        "command_to_string",
        "end(offers)",
        "next == offers",
        "offers.end",
        "_add_to_old_gifts",
        "take_note",
        "NOTE_OFFERED_SPELL",
        "monnum",
        "base_type",
        "orig_monnum",
        "dancing_weapon",
        "MONS_DANCING",
        "clua.callmaybefn",
        "autopickup_item_name",
        "_autopickup_item_name",
        "_autopickup",
        "colour =",
        "old_slot",
        "maybe_bool",
        "callmaybefn",
    ]
    s_lower = s_stripped.lower()
    for residue in cpp_residue_en:
        if residue.lower() in s_lower:
            return True

    return False


def is_orphan_cpp_line(line):
    """
    Línea SIN pipe que es claramente código C++ suelto
    (no parte de un comentario ni cadena de traducción).
    """
    s = line.strip()
    if not s:
        return False
    if s.startswith("#"):
        return False

    # Semicolons, llaves solitarias, comas C++
    if s in (";", "};", "{", "}", "{}", ");", "},", ","):
        return True
    if re.match(r"^\s*,\s+\d+", s):  # ",                     9,  -110,  500,"
        return True
    if re.match(r"^\s*\{\s*\w+", s):  # "{bastón nigromancia," or "{ WPN_FLAIL,"
        return True

    # C++ traducido con dinero (you.gold, fee, etc)
    if re.match(r"^(tú|sus)\s*,\s*(oro|fee|tarifa)", s, re.IGNORECASE):
        return True

    # Directivas de preprocesador
    if re.match(r"^#\s*(if|ifdef|ifndef|else|elif|endif|define|include)", s):
        return True

    # Palabras clave de C++
    if re.match(
        r"^(if|else|for|while|switch|case|default|break|continue|return|const|static|auto|void|bool|int)\b",
        s,
    ):
        return True

    # Llamadas a funciones C++
    if re.search(r"mprf\s*\(", s):
        return True
    if re.search(r"mark_milestone\s*\(", s):
        return True
    if re.search(r"god_name\s*\(", s):
        return True
    if re.search(r"you\.\w+", s):
        return True
    if re.search(r"item\.\w+", s):
        return True
    if re.search(r"clua\.\w+", s):
        return True
    if re.search(r"simple_god_message\s*\(", s):
        return True
    if re.search(r"getMiscString\s*\(", s):
        return True
    if re.search(r"_autopickup", s):
        return True
    if re.search(r"ard\s*\(", s):
        return True

    # Constantes C++ (enums, defines)
    cpp_consts = [
        r"SLOT_",
        r"\bSIZE_(LITTLE|MEDIUM|LARGE)\b",
        r"\bNUM_SIZE_LEVELS\b",
        r"\bDAMV_",
        r"\bARMF_",
        r"\bSK_",
        r"\bBRANCH_",
        r"\bBEAM_",
        r"\bMONS_",
        r"ac_type::",
        r"TAG_MAJOR_VERSION",
        r"DESC_A",
        r"\bDRAGON_ARMOUR\b",
        # Variantes SIN guión bajo (traducciones automáticas que perdieron _)
        r"\bSLOT\s+\w+\b",
        r"\bSIZE\s+(LITTLE|MEDIUM|LARGE)\b",
        r"\bNUM\s+SIZE\b",
        r"\bDAMV\s+\w+\b",
        r"\bARMF\s+\w+\b",
        r"\bBEAM\s+\w+\b",
        r"\bBRANCH_\w+\b",
        r"\bCA\s+type:\w+\b",
    ]
    for pat in cpp_consts:
        if re.search(pat, s, re.IGNORECASE):
            return True

    # Traducciones literales en español de código C++
    # (case-insensitive porque las traducciones automáticas varían en mayúsculas)
    spanish_cpp_keywords = [
        r"^regreso\b",
        r"^retorno\b",
        r"^caso\s+\w+",
        r"^ruptura\b",
        r"^más\b",
        r"^interruptor\b",
        r"^prefijo\b",
        r"^nombre\s+de\s+la\s+cadena\b",
        r"^tal\s+vez\b",
        r"^golpe\b",
        r"^slouch\b",
        r"^Mons_",
        r"^DAÑO_",
        r"^AUTO\b",
        r"^gema\s+(araña|tumba|guarida|elfo|limo|orco|depths)\s*,",
        r"^caso\b",
        r"^WPN\s+",
        r"^ARM\s+",
        r"^MI\s+",
        r"^gema\s+",
        r"^bastón\s+\w",
        r"^armadura\s+de\s+dragón\s*\(",
    ]
    for pat in spanish_cpp_keywords:
        if re.match(pat, s, re.IGNORECASE):
            return True

    # Líneas con asignaciones C++ (desc =, prompt +=, name +=)
    if re.match(r"^(desc|prompt|name|colour)\s*[\+=]\s*", s, re.IGNORECASE):
        return True

    # C++ suelto con paréntesis y punto y coma al final
    if re.search(r"\(.*\)\s*;", s):
        return True

    # Llamadas a función C++ con espacios (traducción automática sin paréntesis pegados)
    if re.search(r"mprf\s+nocap", s, re.IGNORECASE):
        return True
    if re.search(r"talisman\s+type\s+name\s*\(", s, re.IGNORECASE):
        return True
    if re.search(r"simple\s+god\s+message", s, re.IGNORECASE):
        return True
    if re.search(r"Tú\.hands", s):
        return True
    if re.search(r"slouch_damage", s):
        return True
    if re.search(r",\s+(false|fee|which_god)\s*", s):
        return True
    if re.search(r"next\+\+", s):
        return True

    # Comentarios de código que empiezan con "is " (sin pipe)
    if re.match(r"^is\s+always\s+", s, re.IGNORECASE):
        return True

    # Líneas que parecen C++ traducido por su estructura
    # (tienen paréntesis con contenido técnico que no es español real)
    if re.match(r"^.\s+\([A-ZÁÉÍÓÚÑa-záéíóúñ]+\s+\w+\)", s):
        return True
    if re.match(r"^si\s*\(", s, re.IGNORECASE):
        return True
    if "old gifts" in s.lower() or "god name" in s.lower() or "title(" in s.lower():
        return True
    if "bevel" in s.lower() or "milestone" in s.lower():
        return True
    if re.search(r"#if\s+TAG", s, re.IGNORECASE):
        return True

    return False


def clean_file(filepath, dry_run=False):
    """Limpia un archivo de traducción, eliminando código C++ tanto en
    líneas con pipe como líneas sueltas."""
    with open(filepath) as f:
        lines = f.readlines()

    cleaned = []
    removed_lines = []

    # Guardamos comentarios acumulados para no perderlos si hay C++ intercalado
    saved_comments = []

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Comentarios y líneas vacías: preservar siempre
        if stripped.startswith("#") or not stripped:
            saved_comments.append(line)
            continue

        if "|" in stripped:
            en_part = stripped.split("|", 1)[0].strip()

            if is_cpp_en_string(en_part):
                # Código C++ con pipe (traducción mal generada)
                removed_lines.append((i + 1, "C++|pipe", stripped[:80]))
                saved_comments = []  # Descartar comentarios acumulados
                continue
            else:
                # Contenido real de UI
                if saved_comments:
                    cleaned.extend(saved_comments)
                    saved_comments = []
                cleaned.append(line)
        else:
            # Línea sin pipe
            if is_orphan_cpp_line(stripped):
                removed_lines.append((i + 1, "C++|orphan", stripped[:80]))
                saved_comments = []
                continue
            else:
                # Línea sin pipe que podría ser contenido real (texto suelto, etc.)
                if saved_comments:
                    cleaned.extend(saved_comments)
                    saved_comments = []
                cleaned.append(line)

    # Escribir archivo limpio
    result = "".join(cleaned)

    if dry_run:
        fname = os.path.basename(filepath)
        print(f"\n📊 {fname}:")
        print(f"   Original: {len(lines)} líneas → Limpio: {len(cleaned)} líneas")
        print(f"   Eliminadas: {len(removed_lines)} líneas de código C++")
        if removed_lines:
            print(f"   Primeras 10 eliminadas:")
            for lineno, tipo, text in removed_lines[:10]:
                print(f"     L{lineno:3d} [{tipo:10s}] {text}")
            if len(removed_lines) > 10:
                print(f"     ... y {len(removed_lines) - 10} más")
    else:
        bak_path = filepath + ".bak"
        os.rename(filepath, bak_path)
        with open(filepath, "w") as f:
            f.write(result)
        fname = os.path.basename(filepath)
        print(
            f"✅ {fname}: {len(lines)} → {len(cleaned)} líneas ({len(removed_lines)} C++ eliminadas)"
        )

    return len(lines), len(cleaned), len(removed_lines)


def main():
    dry_run = "--dry-run" in sys.argv

    files = [
        "ability.txt",
        "inventory.txt",
        "religion.txt",
        "menu.txt",
        "combat.txt",
        "skills.txt",
        "status.txt",
        "misc.txt",
    ]

    total_orig = 0
    total_clean = 0
    total_removed = 0

    print(f"{'🔍 DRY RUN (simulación)' if dry_run else '🧹 LIMPIEZA UI'}")
    print("=" * 60)

    for fname in files:
        fpath = os.path.join(BASE, fname)
        if not os.path.exists(fpath):
            print(f"\n⚠️  {fname} no existe")
            continue

        orig, clean, removed = clean_file(fpath, dry_run)
        total_orig += orig
        total_clean += clean
        total_removed += removed

    print("\n" + "=" * 60)
    print(
        f"Total: {total_orig} → {total_clean} líneas ({total_removed} C++ eliminadas)"
    )

    if dry_run:
        print(
            "\n🔍 Modo simulación. Para aplicar cambios: python3 scripts/cleanup_ui.py"
        )
    else:
        print("✅ Backups creados (.bak). Para restaurar: mv <archivo>.bak <archivo>")


if __name__ == "__main__":
    main()
