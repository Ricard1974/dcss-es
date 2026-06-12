#!/usr/bin/env python3
"""
Actualiza los archivos de referencia upstream/ desde el repositorio oficial.
Mantiene una copia snapshot de los archivos EN para comparar.

Uso: python3 scripts/update_upstream.py [--repo PATH]
"""

import argparse
import shutil
from pathlib import Path

PROJECT = Path(__file__).parent.parent
UPSTREAM_DESCRIPT = PROJECT / "upstream" / "descript"
UPSTREAM_DATABASE = PROJECT / "upstream" / "database"


def update_from_repo(repo_path: str):
    """Copia los archivos EN desde el repo oficial a upstream/."""
    repo = Path(repo_path)

    # descript/
    src_descript = repo / "crawl-ref" / "source" / "dat" / "descript"
    if src_descript.exists():
        UPSTREAM_DESCRIPT.mkdir(parents=True, exist_ok=True)
        for f in src_descript.glob("*.txt"):
            shutil.copy2(f, UPSTREAM_DESCRIPT / f.name)
        print(
            f"✅ Copiados {len(list(src_descript.glob('*.txt')))} archivos de descript/"
        )
    else:
        print(f"⚠️  No encontrado: {src_descript}")

    # database/
    src_database = repo / "crawl-ref" / "source" / "dat" / "database"
    if src_database.exists():
        UPSTREAM_DATABASE.mkdir(parents=True, exist_ok=True)
        for f in src_database.glob("*.txt"):
            shutil.copy2(f, UPSTREAM_DATABASE / f.name)
        print(
            f"✅ Copiados {len(list(src_database.glob('*.txt')))} archivos de database/"
        )
    else:
        print(f"⚠️  No encontrado: {src_database}")


def main():
    parser = argparse.ArgumentParser(
        description="Actualiza archivos de referencia upstream"
    )
    parser.add_argument(
        "--repo",
        default=str(PROJECT),
        help="Ruta al repositorio de crawl (por defecto: el proyecto mismo)",
    )
    args = parser.parse_args()

    update_from_repo(args.repo)
    print(
        "\nEjecuta 'python3 scripts/stats.py' para ver las estadísticas actualizadas."
    )


if __name__ == "__main__":
    main()
