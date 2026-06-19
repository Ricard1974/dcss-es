#!/usr/bin/env python3
"""Aplica tr() a cprintf() en libunix.cc - traduce menús y textos de UI"""

import sys


def main():
    filepath = sys.argv[1] if len(sys.argv) > 1 else "libunix.cc"

    with open(filepath, "r") as f:
        content = f.read()

    old = """    va_start(argp, format);
    vsnprintf(buffer, sizeof(buffer), format, argp);
    va_end(argp);

    char32_t c;"""

    new = """    va_start(argp, format);
    vsnprintf(buffer, sizeof(buffer), format, argp);
    va_end(argp);

    // Translate the formatted text
    {
        string trans = tr(string(buffer));
        strncpy(buffer, trans.c_str(), sizeof(buffer) - 1);
        buffer[sizeof(buffer) - 1] = '\0';
    }

    char32_t c;"""

    if old in content:
        content = content.replace(old, new)
        with open(filepath, "w") as f:
            f.write(content)
        print("OK: libunix.cc - cprintf con tr()")
    else:
        print("ERROR: patrón no encontrado en libunix.cc")


if __name__ == "__main__":
    main()
