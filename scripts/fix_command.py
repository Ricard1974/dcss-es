#!/usr/bin/env python3
"""Aplica soporte de traducción a command.cc - carga archivos de ayuda localizados"""

import sys


def main():
    filepath = sys.argv[1] if len(sys.argv) > 1 else "command.cc"

    with open(filepath, "r") as f:
        content = f.read()

    # Modificar _get_help_section() para cargar archivos traducidos primero
    old = """            string fname = canonicalise_file_separator(help_files[i].name);
            FILE* fp = fopen_u(datafile_path(fname, false).c_str(), "r");
            ASSERTM(fp, "Failed to open '%s'!", fname.c_str());"""

    new = """            string fname = canonicalise_file_separator(help_files[i].name);
            string help_path;
            if (Options.lang_name && Options.lang_name[0])
            {
                string localized = "ui/" + string(Options.lang_name) + "/" + fname;
                help_path = datafile_path(localized, false);
            }
            if (help_path.empty())
                help_path = datafile_path(fname, false);
            FILE* fp = fopen_u(help_path.c_str(), "r");
            ASSERTM(fp, "Failed to open '%s'!", fname.c_str());"""

    if old in content:
        content = content.replace(old, new)
        with open(filepath, "w") as f:
            f.write(content)
        print("OK: command.cc - soporte para ayuda localizada")
    else:
        print("ERROR: No se encontró el patrón original en command.cc")
        # Debug
        lines = content.split("\n")
        found = False
        for i, line in enumerate(lines):
            if "canonicalise_file_separator(help_files" in line:
                # Print context
                for j in range(max(0, i - 1), min(len(lines), i + 5)):
                    print(f"  Line {j + 1}: {lines[j]}")
                found = True
                break
        if not found:
            print("  (patrón no encontrado en ninguna línea)")


if __name__ == "__main__":
    main()
