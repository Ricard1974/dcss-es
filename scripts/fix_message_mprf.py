#!/usr/bin/env python3
"""
Modifica do_message_print() en message.cc para traducir el format string
ANTES de vsnprintf, permitiendo que las claves con %s en combat.txt funcionen.

Sin este cambio, el hook en _mpr() recibe el texto ya formateado
("You hit el goblin.") y no puede matchear contra la clave ("You hit %s.").

Uso: python3 scripts/fix_message_mprf.py <ruta_a_message.cc>
"""

import sys


def main():
    if len(sys.argv) < 2:
        print("Uso: fix_message_mprf.py <message.cc>")
        sys.exit(1)

    path = sys.argv[1]

    with open(path, "r") as f:
        content = f.read()

    # Patrón a buscar: el cuerpo de do_message_print
    old = (
        "    va_list ap;\n"
        "    va_copy(ap, argp);\n"
        "    char buff[200];\n"
        "    size_t len = vsnprintf(buff, sizeof(buff), format, argp);\n"
        "    if (len < sizeof(buff))\n"
        "        _mpr(buff, channel, param, nojoin, cap);\n"
        "    else\n"
        "    {\n"
        "        char *heapbuf = (char*)malloc(len + 1);\n"
        "        vsnprintf(heapbuf, len + 1, format, ap);"
    )

    new = (
        "    string fmt = tr(format);\n"
        "    va_list ap;\n"
        "    va_copy(ap, argp);\n"
        "    char buff[200];\n"
        "    size_t len = vsnprintf(buff, sizeof(buff), fmt.c_str(), argp);\n"
        "    if (len < sizeof(buff))\n"
        "        _mpr(buff, channel, param, nojoin, cap);\n"
        "    else\n"
        "    {\n"
        "        char *heapbuf = (char*)malloc(len + 1);\n"
        "        vsnprintf(heapbuf, len + 1, fmt.c_str(), ap);"
    )

    if old in content:
        content = content.replace(old, new)
        with open(path, "w") as f:
            f.write(content)
        print("  ✓ do_message_print modificado (tr() en format antes de vsnprintf)")
    else:
        print("  ⚠️  No se encontró el patrón en do_message_print")
        print("     (quizás ya está modificado)")


if __name__ == "__main__":
    main()
