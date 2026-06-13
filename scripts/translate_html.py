#!/usr/bin/env python3
"""
Pipeline de traducción que preserva etiquetas HTML.
Usa el mismo sistema de placeholders que translate_batch.py
para proteger NO_TRANSLATE y FORCED_TERMS.

Uso:
  python3 translate_html.py --translate "Press <w>?</w> for help"
  python3 translate_html.py --file commands.txt
"""

import re
import json
import sys
import os
import subprocess
from typing import List, Tuple, Optional

sys.path.insert(0, os.path.expanduser("~/proyectos/dcss-es/scripts"))
try:
    from terms import FORCED_TERMS, NO_TRANSLATE, POST_PROCESS

    FORCED = FORCED_TERMS
    NO_TRANS = NO_TRANSLATE
    POST_FIXES = POST_PROCESS
except ImportError:
    print("⚠️  No se pudo cargar terms.py, usando modo simple", file=sys.stderr)
    FORCED = {}
    NO_TRANS = set()
    POST_FIXES = []


def split_html(text: str) -> List[Tuple[str, str]]:
    """
    Divide texto en segmentos HTML/texto.

    Los segmentos de texto adyacentes a HTML preservan su padding:
    - Si tienen espacio al inicio/final, se guarda aparte
    """
    segments = []
    pos = 0
    for m in re.finditer(r"(<[^>]+>[^<]*</[^>]+>|<[^>]+>)", text):
        if m.start() > pos:
            segments.append(("text", text[pos : m.start()]))
        segments.append(("html", m.group()))
        pos = m.end()
    if pos < len(text):
        segments.append(("text", text[pos:]))
    return segments


def translate_via_libretranslate(text: str) -> Optional[str]:
    """Traduce con LibreTranslate."""
    try:
        cmd = [
            "curl",
            "-s",
            "http://localhost:5000/translate",
            "-d",
            f"q={text}&source=en&target=es&format=text",
        ]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        d = json.loads(r.stdout)
        return d.get("translatedText")
    except Exception:
        return None


def protect_game_terms(text: str):
    """
    Reemplaza NO_TRANSLATE y FORCED_TERMS (2+ palabras) con placeholders.
    Devuelve (texto_con_placeholders, {placeholder: traduccion_es})
    """
    translations = {}
    counter = 0

    # NO_TRANSLATE
    for term in sorted(NO_TRANS, key=lambda x: -len(x), reverse=True):
        key = f"§NT{counter}§"
        pattern = r"\b" + re.escape(term) + r"\b"
        if re.search(pattern, text, flags=re.IGNORECASE):
            translations[key] = term  # self-translate (keep as-is)
            text = re.sub(pattern, key, text, flags=re.IGNORECASE)
            counter += 1

    # FORCED_TERMS compuestos
    forced_items = [
        (en, es)
        for en, es in sorted(FORCED.items(), key=lambda x: -len(x[0]), reverse=True)
        if len(en.split()) >= 2 and len(en) > 4
    ]
    for en_term, es_term in forced_items:
        key = f"§GT{counter}§"
        pattern = r"\b" + re.escape(en_term) + r"\b"
        if re.search(pattern, text):
            translations[key] = es_term
            text = re.sub(pattern, key, text)
            counter += 1

    return text, translations


def restore_game_terms(text: str, translations: dict) -> str:
    """Restaura placeholders con sus traducciones."""
    for key, es_value in sorted(translations.items(), reverse=True):
        ph_id = re.search(r"§([GN]T\d+)§", key)
        if ph_id:
            for pat in [
                rf"§?\s*{re.escape(ph_id.group(1))}\s*§?",
                rf"§\s*{re.escape(ph_id.group(1))}",
                rf"{re.escape(ph_id.group(1))}\s*§",
            ]:
                text = re.sub(pat, es_value, text)
    return text


def post_process(text: str) -> str:
    """Aplica POST_PROCESS."""
    for pattern, replacement in POST_FIXES:
        if callable(replacement):
            text = re.sub(pattern, replacement, text)
        else:
            text = re.sub(pattern, replacement, text)
    return text


def translate_segment(text: str) -> str:
    """Traduce un segmento de texto plano con protección de términos."""
    if not text.strip():
        return text

    # 1. Proteger términos con placeholders
    protected, translations = protect_game_terms(text)

    # 2. Traducir
    translated = translate_via_libretranslate(protected)
    if translated is None:
        return text

    # 3. Restaurar términos protegidos
    restored = restore_game_terms(translated, translations)

    # 4. Post-procesar
    result = post_process(restored)

    return result


def translate_preserving_html(text: str) -> str:
    """
    Traduce texto preservando etiquetas HTML y espacios entre segmentos.
    """
    if "<" not in text:
        return translate_segment(text)

    segments = split_html(text)
    result = []

    for i, (seg_type, seg_content) in enumerate(segments):
        if seg_type == "html":
            result.append(seg_content)
        else:
            # Preservar espacios alrededor del texto que LT pueda eliminar
            prefix = suffix = ""
            if seg_content and seg_content[0] == " ":
                prefix = " "
                seg_content = seg_content[1:]
            if seg_content and seg_content[-1] == " ":
                suffix = " "
                seg_content = seg_content[:-1]

            translated = translate_segment(seg_content)

            result.append(prefix + translated + suffix)

    return "".join(result)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Traduce texto preservando etiquetas HTML"
    )
    parser.add_argument("--translate", "-t", help="Texto a traducir")
    parser.add_argument("--file", "-f", help="Archivo .txt (formato EN|ES) a procesar")
    parser.add_argument(
        "--update", "-u", action="store_true", help="Actualizar archivo"
    )

    args = parser.parse_args()

    if args.translate:
        print(translate_preserving_html(args.translate))
        return

    if args.file:
        with open(args.file) as f:
            lines = f.readlines()

        updated = []
        total = translated = 0

        for line in lines:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                updated.append(line)
                continue
            if "|" not in stripped:
                updated.append(line)
                continue

            en, es = stripped.split("|", 1)
            en = en.strip()
            es = es.strip()
            total += 1

            if en != es and not args.update:
                translated += 1
                updated.append(line)
                continue

            new_es = translate_preserving_html(en)
            if new_es != es:
                translated += 1
                updated.append(f"{en}|{new_es}\n")
            else:
                updated.append(line)

            if total % 20 == 0:
                print(f"  {total} procesadas...", file=sys.stderr)

        with open(args.file, "w") as f:
            f.writelines(updated)
        print(
            f"✅ {args.file}: {total} total, {translated} traducidas/actualizadas",
            file=sys.stderr,
        )
        return

    # stdin
    for line in sys.stdin:
        stripped = line.strip()
        if not stripped:
            continue
        if "|" in stripped:
            en, _ = stripped.split("|", 1)
            print(f"{en}|{translate_preserving_html(en.strip())}")
        else:
            print(translate_preserving_html(stripped))


if __name__ == "__main__":
    main()
